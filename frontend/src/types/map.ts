/**
 * Map-related types and interfaces
 */

export interface MapPosition {
  x: number;
  y: number;
}

export interface MapViewport {
  offsetX: number;
  offsetY: number;
  scale: number;
}

export interface Place {
  id: string;
  name: string;
  type: "building" | "district" | "landmark" | "other";
  position: MapPosition;
  owner_faction_id?: string;
  notes_public: string | null;
  notes_gm: string | null;
  scope: "public" | "gm" | "player";
  created_at: string;
  updated_at: string;
}

export interface PlaceCreate {
  name: string;
  type: "building" | "district" | "landmark" | "other";
  position: MapPosition;
  owner_faction_id?: string;
  notes_public?: string;
  notes_gm?: string;
  scope?: "public" | "gm";
}

export interface LayerState {
  id: string;
  name: string;
  visible: boolean;
  opacity: number;
  type: "base" | "territory" | "marker";
}

export type MapMode = "pan" | "add-poi" | "brush" | "eraser";

export interface MapState {
  viewport: MapViewport;
  mode: MapMode;
  selectedPlaceId: string | null;
  selectedFactionId: string | null; // For territory painting
  brushSize: number;
  layers: LayerState[];
}
