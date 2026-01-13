import { createContext, useContext, useState, ReactNode, useCallback } from "react";
import { MapState, MapMode, MapViewport, LayerState } from "../types/map";

interface MapContextType {
  mapState: MapState;
  setMode: (mode: MapMode) => void;
  setViewport: (viewport: MapViewport) => void;
  selectPlace: (placeId: string | null) => void;
  selectFaction: (factionId: string | null) => void;
  setBrushSize: (size: number) => void;
  updateLayer: (layerId: string, updates: Partial<LayerState>) => void;
}

const MapContext = createContext<MapContextType | undefined>(undefined);

const DEFAULT_LAYERS: LayerState[] = [
  { id: "base-land", name: "Land/Water", visible: true, opacity: 1, type: "base" },
  { id: "territories", name: "Territories", visible: true, opacity: 0.6, type: "territory" },
  { id: "markers", name: "Markers", visible: true, opacity: 1, type: "marker" },
];

export function MapProvider({ children }: { children: ReactNode }): JSX.Element {
  const [mapState, setMapState] = useState<MapState>({
    viewport: { offsetX: 0, offsetY: 0, scale: 1 },
    mode: "pan",
    selectedPlaceId: null,
    selectedFactionId: null,
    brushSize: 20,
    layers: DEFAULT_LAYERS,
  });

  const setMode = useCallback((mode: MapMode) => {
    setMapState((prev) => ({ ...prev, mode }));
  }, []);

  const setViewport = useCallback((viewport: MapViewport) => {
    setMapState((prev) => ({ ...prev, viewport }));
  }, []);

  const selectPlace = useCallback((placeId: string | null) => {
    setMapState((prev) => ({ ...prev, selectedPlaceId: placeId }));
  }, []);

  const selectFaction = useCallback((factionId: string | null) => {
    setMapState((prev) => ({ ...prev, selectedFactionId: factionId }));
  }, []);

  const setBrushSize = useCallback((size: number) => {
    setMapState((prev) => ({ ...prev, brushSize: size }));
  }, []);

  const updateLayer = useCallback((layerId: string, updates: Partial<LayerState>) => {
    setMapState((prev) => ({
      ...prev,
      layers: prev.layers.map((layer) =>
        layer.id === layerId ? { ...layer, ...updates } : layer
      ),
    }));
  }, []);

  return (
    <MapContext.Provider value={{ mapState, setMode, setViewport, selectPlace, selectFaction, setBrushSize, updateLayer }}>
      {children}
    </MapContext.Provider>
  );
}

export function useMap(): MapContextType {
  const context = useContext(MapContext);
  if (!context) {
    throw new Error("useMap must be used within MapProvider");
  }
  return context;
}
