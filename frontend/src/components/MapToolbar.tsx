import { useMap } from "../contexts/MapContext";
import { MapMode } from "../types/map";
import { useState, useEffect } from "react";
import { apiClient, Faction } from "../api/client";

export function MapToolbar(): JSX.Element {
  const { mapState, setMode, selectFaction, setBrushSize } = useMap();
  const [factions, setFactions] = useState<Faction[]>([]);

  useEffect(() => {
    apiClient
      .getFactions()
      .then(setFactions)
      .catch(() => setFactions([]));
  }, []);

  const handleModeChange = (mode: MapMode) => {
    setMode(mode);
  };

  const modes: Array<{ mode: MapMode; label: string; icon: string }> = [
    { mode: "pan", label: "Pan", icon: "🖐️" },
    { mode: "add-poi", label: "Add POI", icon: "📍" },
    { mode: "brush", label: "Brush", icon: "🖌️" },
    { mode: "eraser", label: "Eraser", icon: "🧹" },
  ];

  return (
    <div
      style={{
        position: "absolute",
        top: "10px",
        left: "50%",
        transform: "translateX(-50%)",
        backgroundColor: "#fff",
        border: "1px solid #ccc",
        borderRadius: "4px",
        padding: "0.5rem",
        display: "flex",
        gap: "0.5rem",
        alignItems: "center",
        zIndex: 100,
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
      }}
    >
      {modes.map(({ mode, label, icon }) => (
        <button
          key={mode}
          onClick={() => handleModeChange(mode)}
          aria-label={`${label} mode`}
          aria-pressed={mapState.mode === mode}
          style={{
            padding: "0.5rem 1rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            backgroundColor: mapState.mode === mode ? "#1976d2" : "#fff",
            color: mapState.mode === mode ? "#fff" : "#000",
            cursor: "pointer",
            fontSize: "0.9rem",
            fontWeight: mapState.mode === mode ? "bold" : "normal",
          }}
        >
          {icon} {label}
        </button>
      ))}

      {/* Faction selector for painting */}
      {(mapState.mode === "brush" || mapState.mode === "eraser") && (
        <>
          <div style={{ width: "1px", height: "30px", backgroundColor: "#ccc" }} />
          {mapState.mode === "brush" && (
            <select
              value={mapState.selectedFactionId || ""}
              onChange={(e) => selectFaction(e.target.value || null)}
              style={{
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
              }}
            >
              <option value="">Select Faction</option>
              {factions.map((faction) => (
                <option key={faction.id} value={faction.id}>
                  {faction.name}
                </option>
              ))}
            </select>
          )}
          <input
            type="range"
            min="5"
            max="50"
            value={mapState.brushSize}
            onChange={(e) => setBrushSize(Number(e.target.value))}
            style={{ width: "100px" }}
            title={`Brush size: ${mapState.brushSize}px`}
          />
          <span style={{ fontSize: "0.85rem", color: "#666" }}>{mapState.brushSize}px</span>
        </>
      )}
    </div>
  );
}
