import { useState, useRef, useCallback, useEffect } from "react";
import { apiClient, Faction } from "../api/client";
import { useProject } from "../contexts/ProjectContext";
import { getTileKey, TILE_SIZE, canvasToPngDataUrl } from "../utils/tileUtils";

interface TileCanvasData {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  isDirty: boolean;
}

export function useTerritoryPainting(factions: Faction[]) {
  const { activeSnapshot } = useProject();
  const [tilesCache, setTilesCache] = useState<Map<string, TileCanvasData>>(new Map());
  const [dirtyTiles, setDirtyTiles] = useState<Set<string>>(new Set());
  const uploadTimeoutRef = useRef<number | null>(null);

  // Get or create a tile canvas
  const getTileCanvas = useCallback(
    (factionId: string, z: number, x: number, y: number): TileCanvasData => {
      const key = getTileKey(factionId, z, x, y);
      const existing = tilesCache.get(key);
      if (existing) return existing;

      // Create new tile canvas
      const canvas = document.createElement("canvas");
      canvas.width = TILE_SIZE;
      canvas.height = TILE_SIZE;
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) throw new Error("Failed to get 2D context");

      const data: TileCanvasData = { canvas, ctx, isDirty: false };
      setTilesCache((prev) => new Map(prev).set(key, data));
      return data;
    },
    [tilesCache]
  );

  // Mark tile as dirty
  const markTileDirty = useCallback((factionId: string, z: number, x: number, y: number) => {
    const key = getTileKey(factionId, z, x, y);
    setDirtyTiles((prev) => new Set(prev).add(key));
    setTilesCache((prev) => {
      const newMap = new Map(prev);
      const tile = newMap.get(key);
      if (tile) {
        tile.isDirty = true;
      }
      return newMap;
    });
  }, []);

  // Load tile from backend
  const loadTile = useCallback(
    async (factionId: string, z: number, x: number, y: number): Promise<void> => {
      if (!activeSnapshot) return;

      try {
        const blob = await apiClient.getTile(activeSnapshot.id, factionId, z, x, y);
        if (blob) {
          const tileData = getTileCanvas(factionId, z, x, y);
          const img = new Image();
          img.onload = () => {
            tileData.ctx.clearRect(0, 0, TILE_SIZE, TILE_SIZE);
            tileData.ctx.drawImage(img, 0, 0);
          };
          img.src = URL.createObjectURL(blob);
        }
      } catch (err) {
        console.warn(`Failed to load tile ${factionId} ${z},${x},${y}:`, err);
      }
    },
    [activeSnapshot, getTileCanvas]
  );

  // Paint on tile
  const paintOnTile = useCallback(
    (factionId: string, mapX: number, mapY: number, brushSize: number, isEraser: boolean): void => {
      const tileX = Math.floor(mapX / TILE_SIZE);
      const tileY = Math.floor(mapY / TILE_SIZE);
      const localX = mapX - tileX * TILE_SIZE;
      const localY = mapY - tileY * TILE_SIZE;

      const tileData = getTileCanvas(factionId, 0, tileX, tileY);
      const ctx = tileData.ctx;

      ctx.globalCompositeOperation = isEraser ? "destination-out" : "source-over";

      if (isEraser) {
        ctx.fillStyle = "rgba(0,0,0,1)"; // Full alpha for erasing
      } else {
        const faction = factions.find((f) => f.id === factionId);
        if (faction) {
          ctx.fillStyle = faction.color;
          ctx.globalAlpha = faction.opacity;
        }
      }

      ctx.beginPath();
      ctx.arc(localX, localY, brushSize / 2, 0, Math.PI * 2);
      ctx.fill();

      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = "source-over";

      markTileDirty(factionId, 0, tileX, tileY);
    },
    [factions, getTileCanvas, markTileDirty]
  );

  // Upload dirty tiles with debounce
  const uploadDirtyTiles = useCallback(async () => {
    if (!activeSnapshot || dirtyTiles.size === 0) return;

    // Group by faction
    const tilesByFaction = new Map<
      string,
      Array<{ z: number; x: number; y: number; data: string }>
    >();

    for (const key of dirtyTiles) {
      const parts = key.split("_");
      if (parts.length !== 4) continue;
      const [factionId, zStr, xStr, yStr] = parts;
      if (!factionId || !zStr || !xStr || !yStr) continue;
      const tileData = tilesCache.get(key);
      if (!tileData) continue;

      try {
        const base64Data = await canvasToPngDataUrl(tileData.canvas);
        if (!base64Data) continue;
        if (!tilesByFaction.has(factionId)) {
          tilesByFaction.set(factionId, []);
        }
        tilesByFaction.get(factionId)!.push({
          z: Number(zStr),
          x: Number(xStr),
          y: Number(yStr),
          data: base64Data,
        });
      } catch (err) {
        console.error("Failed to convert tile to PNG:", err);
      }
    }

    // Upload each faction's tiles
    for (const [factionId, tiles] of tilesByFaction) {
      try {
        await apiClient.uploadTilesBatch(activeSnapshot.id, { faction_id: factionId, tiles });
        console.log(`Uploaded ${tiles.length} tiles for faction ${factionId}`);
      } catch (err) {
        console.error(`Failed to upload tiles for faction ${factionId}:`, err);
      }
    }

    // Clear dirty tiles
    setDirtyTiles(new Set());
    setTilesCache((prev) => {
      const newMap = new Map(prev);
      for (const key of dirtyTiles) {
        const tile = newMap.get(key);
        if (tile) {
          tile.isDirty = false;
        }
      }
      return newMap;
    });
  }, [activeSnapshot, dirtyTiles, tilesCache]);

  // Debounced upload
  const scheduleUpload = useCallback(() => {
    if (uploadTimeoutRef.current !== null) {
      window.clearTimeout(uploadTimeoutRef.current);
    }
    uploadTimeoutRef.current = window.setTimeout(() => {
      uploadDirtyTiles();
    }, 2000); // Upload after 2 seconds of inactivity
  }, [uploadDirtyTiles]);

  // Trigger upload when dirty tiles change
  useEffect(() => {
    if (dirtyTiles.size > 0) {
      scheduleUpload();
    }
  }, [dirtyTiles, scheduleUpload]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (uploadTimeoutRef.current !== null) {
        window.clearTimeout(uploadTimeoutRef.current);
        // Force upload remaining dirty tiles
        uploadDirtyTiles();
      }
    };
  }, [uploadDirtyTiles]);

  return {
    tilesCache,
    loadTile,
    paintOnTile,
    uploadDirtyTiles,
    hasDirtyTiles: dirtyTiles.size > 0,
  };
}
