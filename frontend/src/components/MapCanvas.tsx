import { useRef, useEffect, useState, useCallback } from "react";
import { useMap } from "../contexts/MapContext";
import { apiClient, Place } from "../api/client";
import { useViewMode } from "../contexts/ViewModeContext";
import { useProject } from "../contexts/ProjectContext";

interface MapCanvasProps {
  onPlaceClick?: (place: Place) => void;
  onMapClick?: (x: number, y: number) => void;
}

export function MapCanvas({ onPlaceClick, onMapClick }: MapCanvasProps): JSX.Element {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const { mapState, setViewport, selectPlace } = useMap();
  const { viewMode } = useViewMode();
  const { activeSnapshot } = useProject();
  const [places, setPlaces] = useState<Place[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [baseMapImage, setBaseMapImage] = useState<HTMLImageElement | null>(null);
  const [mapSize, setMapSize] = useState({ width: 1000, height: 1000 });

  // Load places
  useEffect(() => {
    apiClient
      .getPlaces()
      .then(setPlaces)
      .catch(() => setPlaces([]));
  }, []);

  // Load base map image
  useEffect(() => {
    if (!activeSnapshot) return;

    let isCancelled = false;

    const loadMap = async () => {
      try {
        const blob = await apiClient.downloadMap(activeSnapshot.id);
        if (blob && !isCancelled) {
          const url = URL.createObjectURL(blob);
          const img = new Image();
          img.onload = () => {
            if (!isCancelled) {
              setBaseMapImage(img);
              setMapSize({ width: img.width, height: img.height });
              URL.revokeObjectURL(url);
            }
          };
          img.onerror = () => {
            if (!isCancelled) {
              console.error("Failed to load map image");
              setBaseMapImage(null);
            }
            URL.revokeObjectURL(url);
          };
          img.src = url;
        } else if (!isCancelled) {
          setBaseMapImage(null);
          setMapSize({ width: 1000, height: 1000 });
        }
      } catch (err) {
        if (!isCancelled) {
          console.error("Failed to load map:", err);
          setBaseMapImage(null);
        }
      }
    };

    loadMap();

    return () => {
      isCancelled = true;
    };
  }, [activeSnapshot]);

  // Draw map
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = "#f0f0f0";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.translate(mapState.viewport.offsetX, mapState.viewport.offsetY);
    ctx.scale(mapState.viewport.scale, mapState.viewport.scale);

    // Base layer
    const baseLayer = mapState.layers.find((l) => l.id === "base-land");
    if (baseLayer?.visible) {
      ctx.globalAlpha = baseLayer.opacity;

      if (baseMapImage) {
        // Draw actual map image
        ctx.drawImage(baseMapImage, 0, 0, mapSize.width, mapSize.height);
      } else {
        // Fallback: draw placeholder grid
        ctx.fillStyle = "#e0e0e0";
        ctx.fillRect(0, 0, mapSize.width, mapSize.height);

        // Draw grid lines
        ctx.strokeStyle = "#ccc";
        ctx.lineWidth = 1 / mapState.viewport.scale;
        for (let i = 0; i <= mapSize.width; i += 100) {
          ctx.beginPath();
          ctx.moveTo(i, 0);
          ctx.lineTo(i, mapSize.height);
          ctx.stroke();
        }
        for (let i = 0; i <= mapSize.height; i += 100) {
          ctx.beginPath();
          ctx.moveTo(0, i);
          ctx.lineTo(mapSize.width, i);
          ctx.stroke();
        }
      }

      ctx.globalAlpha = 1;
    }

    ctx.restore();
  }, [mapState.viewport, mapState.layers, baseMapImage, mapSize]);

  // Handle mouse down
  const handleMouseDown = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      if (mapState.mode === "pan") {
        setIsDragging(true);
        setDragStart({
          x: e.clientX - mapState.viewport.offsetX,
          y: e.clientY - mapState.viewport.offsetY,
        });
      }
    },
    [mapState.mode, mapState.viewport]
  );

  // Handle mouse move
  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      if (isDragging && mapState.mode === "pan") {
        setViewport({
          ...mapState.viewport,
          offsetX: e.clientX - dragStart.x,
          offsetY: e.clientY - dragStart.y,
        });
      }
    },
    [isDragging, mapState.mode, mapState.viewport, dragStart, setViewport]
  );

  // Handle mouse up
  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  // Handle click
  const handleClick = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      if (mapState.mode === "add-poi") {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const rect = canvas.getBoundingClientRect();
        const canvasX = e.clientX - rect.left;
        const canvasY = e.clientY - rect.top;

        // Convert to map coordinates
        const mapX = (canvasX - mapState.viewport.offsetX) / mapState.viewport.scale;
        const mapY = (canvasY - mapState.viewport.offsetY) / mapState.viewport.scale;

        onMapClick?.(mapX, mapY);
      }
    },
    [mapState.mode, mapState.viewport, onMapClick]
  );

  // Handle wheel zoom
  const handleWheel = useCallback(
    (e: React.WheelEvent<HTMLCanvasElement>) => {
      e.preventDefault();
      const delta = e.deltaY > 0 ? 0.9 : 1.1;
      const newScale = Math.max(0.1, Math.min(5, mapState.viewport.scale * delta));

      const canvas = canvasRef.current;
      if (!canvas) return;

      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      // Zoom towards mouse position
      const newOffsetX =
        mouseX - ((mouseX - mapState.viewport.offsetX) * newScale) / mapState.viewport.scale;
      const newOffsetY =
        mouseY - ((mouseY - mapState.viewport.offsetY) * newScale) / mapState.viewport.scale;

      setViewport({
        offsetX: newOffsetX,
        offsetY: newOffsetY,
        scale: newScale,
      });
    },
    [mapState.viewport, setViewport]
  );

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        overflow: "hidden",
        cursor: mapState.mode === "pan" ? (isDragging ? "grabbing" : "grab") : "crosshair",
      }}
    >
      <canvas
        ref={canvasRef}
        width={1200}
        height={800}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onClick={handleClick}
        onWheel={handleWheel}
        style={{
          display: "block",
          width: "100%",
          height: "100%",
        }}
      />

      {/* Marker overlay */}
      {mapState.layers.find((l) => l.id === "markers")?.visible && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            pointerEvents: "none",
          }}
        >
          {places
            .filter((place) => {
              // Filter by view mode
              if (viewMode === "player" && place.scope === "gm") return false;
              return true;
            })
            .map((place) => {
              if (!place.position) return null;
              const x = place.position.x * mapState.viewport.scale + mapState.viewport.offsetX;
              const y = place.position.y * mapState.viewport.scale + mapState.viewport.offsetY;

              return (
                <button
                  key={place.id}
                  onClick={() => {
                    selectPlace(place.id);
                    onPlaceClick?.(place);
                  }}
                  aria-label={`Place: ${place.name}`}
                  title={place.name}
                  style={{
                    position: "absolute",
                    left: `${x}px`,
                    top: `${y}px`,
                    transform: "translate(-50%, -100%)",
                    pointerEvents: "auto",
                    border: "none",
                    background: "none",
                    cursor: "pointer",
                    fontSize: "1.5rem",
                    padding: 0,
                    filter:
                      mapState.selectedPlaceId === place.id
                        ? "drop-shadow(0 0 4px #1976d2)"
                        : "none",
                  }}
                >
                  📍
                </button>
              );
            })}
        </div>
      )}
    </div>
  );
}
