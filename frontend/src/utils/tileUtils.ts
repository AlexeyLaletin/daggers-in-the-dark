/**
 * Utilities for working with territory tiles
 */

export const TILE_SIZE = 256;

/**
 * Get tile coordinates for a given map position and zoom level
 */
export function getTileCoords(mapX: number, mapY: number, _zoom: number = 0): { x: number; y: number } {
  return {
    x: Math.floor(mapX / TILE_SIZE),
    y: Math.floor(mapY / TILE_SIZE),
  };
}

/**
 * Get visible tile range for current viewport
 */
export function getVisibleTiles(
  viewport: { offsetX: number; offsetY: number; scale: number },
  canvasWidth: number,
  canvasHeight: number,
  mapWidth: number,
  mapHeight: number,
  zoom: number = 0
): Array<{ z: number; x: number; y: number }> {
  // Calculate the map coordinates of viewport corners
  const topLeftX = (-viewport.offsetX) / viewport.scale;
  const topLeftY = (-viewport.offsetY) / viewport.scale;
  const bottomRightX = (canvasWidth - viewport.offsetX) / viewport.scale;
  const bottomRightY = (canvasHeight - viewport.offsetY) / viewport.scale;

  // Get tile ranges
  const minTileX = Math.max(0, Math.floor(topLeftX / TILE_SIZE));
  const minTileY = Math.max(0, Math.floor(topLeftY / TILE_SIZE));
  const maxTileX = Math.min(Math.ceil(mapWidth / TILE_SIZE) - 1, Math.floor(bottomRightX / TILE_SIZE));
  const maxTileY = Math.min(Math.ceil(mapHeight / TILE_SIZE) - 1, Math.floor(bottomRightY / TILE_SIZE));

  const tiles: Array<{ z: number; x: number; y: number }> = [];
  for (let x = minTileX; x <= maxTileX; x++) {
    for (let y = minTileY; y <= maxTileY; y++) {
      tiles.push({ z: zoom, x, y });
    }
  }
  return tiles;
}

/**
 * Convert canvas coordinates to map coordinates
 */
export function canvasToMap(
  canvasX: number,
  canvasY: number,
  viewport: { offsetX: number; offsetY: number; scale: number }
): { x: number; y: number } {
  return {
    x: (canvasX - viewport.offsetX) / viewport.scale,
    y: (canvasY - viewport.offsetY) / viewport.scale,
  };
}

/**
 * Convert map coordinates to canvas coordinates
 */
export function mapToCanvas(
  mapX: number,
  mapY: number,
  viewport: { offsetX: number; offsetY: number; scale: number }
): { x: number; y: number } {
  return {
    x: mapX * viewport.scale + viewport.offsetX,
    y: mapY * viewport.scale + viewport.offsetY,
  };
}

/**
 * Create a tile key for caching
 */
export function getTileKey(factionId: string, z: number, x: number, y: number): string {
  return `${factionId}_${z}_${x}_${y}`;
}

/**
 * Convert canvas to PNG data URL
 */
export async function canvasToPngDataUrl(canvas: HTMLCanvasElement): Promise<string> {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (!blob) {
        reject(new Error("Failed to convert canvas to blob"));
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        if (typeof reader.result === "string") {
          // Extract base64 data (remove "data:image/png;base64," prefix)
          const parts = reader.result.split(",");
          const base64 = parts.length > 1 ? parts[1] : parts[0];
          if (base64) {
            resolve(base64);
          } else {
            reject(new Error("Empty base64 data"));
          }
        } else {
          reject(new Error("Failed to read blob"));
        }
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    }, "image/png");
  });
}
