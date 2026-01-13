import { useEffect, useState } from "react";
import { useMap } from "../contexts/MapContext";
import { apiClient, Place, Faction, Person, NotePage } from "../api/client";
import { useViewMode } from "../contexts/ViewModeContext";

type DetailEntity = Place | Faction | Person | NotePage;
type EntityType = "place" | "faction" | "person" | "page";

export function DetailPanel(): JSX.Element {
  const { mapState, selectPlace, selectFaction } = useMap();
  const { viewMode } = useViewMode();
  const [entity, setEntity] = useState<DetailEntity | null>(null);
  const [entityType, setEntityType] = useState<EntityType | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (mapState.selectedPlaceId) {
      setLoading(true);
      apiClient
        .getPlaces()
        .then((places) => {
          const found = places.find((p) => p.id === mapState.selectedPlaceId);
          if (found) {
            setEntity(found);
            setEntityType("place");
          } else {
            setEntity(null);
            setEntityType(null);
          }
        })
        .catch(() => {
          setEntity(null);
          setEntityType(null);
        })
        .finally(() => setLoading(false));
    } else if (mapState.selectedFactionId) {
      setLoading(true);
      apiClient
        .getFactions()
        .then((factions) => {
          const found = factions.find((f) => f.id === mapState.selectedFactionId);
          if (found) {
            setEntity(found);
            setEntityType("faction");
          } else {
            setEntity(null);
            setEntityType(null);
          }
        })
        .catch(() => {
          setEntity(null);
          setEntityType(null);
        })
        .finally(() => setLoading(false));
    } else {
      setEntity(null);
      setEntityType(null);
    }
  }, [mapState.selectedPlaceId, mapState.selectedFactionId]);

  if (!mapState.selectedPlaceId && !mapState.selectedFactionId) {
    return (
      <div style={{ padding: "1rem", color: "#666", fontSize: "0.9rem" }}>
        <p>Select an entity on the map or in the sidebar to view details.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: "1rem" }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (!entity || !entityType) {
    return (
      <div style={{ padding: "1rem", color: "#666" }}>
        <p>Entity not found.</p>
      </div>
    );
  }

  const handleClose = () => {
    if (entityType === "place") selectPlace(null);
    if (entityType === "faction") selectFaction(null);
  };

  // Render based on entity type
  if (entityType === "place") {
    const place = entity as Place;
    return (
      <div style={{ padding: "1rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
          <h3 style={{ margin: "0 0 0.5rem 0" }}>📍 {place.name}</h3>
          <button
            onClick={handleClose}
            aria-label="Close details"
            style={{
              border: "none",
              background: "none",
              fontSize: "1.2rem",
              cursor: "pointer",
              padding: "0",
            }}
          >
            ✕
          </button>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <div style={{ fontSize: "0.85rem", color: "#666", marginBottom: "0.25rem" }}>
            Type: <strong>{place.type}</strong>
          </div>
          {place.position && (
            <div style={{ fontSize: "0.85rem", color: "#666", marginBottom: "0.25rem" }}>
              Position: ({place.position.x.toFixed(0)}, {place.position.y.toFixed(0)})
            </div>
          )}
          {place.scope === "gm" && (
            <div style={{ fontSize: "0.85rem", color: "#d32f2f" }}>🔒 GM Only</div>
          )}
        </div>

        {place.notes_public && (
          <div style={{ marginBottom: "1rem" }}>
            <h4 style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>Public Notes</h4>
            <div
              style={{
                padding: "0.5rem",
                backgroundColor: "#f5f5f5",
                borderRadius: "4px",
                fontSize: "0.85rem",
                whiteSpace: "pre-wrap",
              }}
            >
              {place.notes_public}
            </div>
          </div>
        )}

        {viewMode === "gm" && place.notes_gm && (
          <div style={{ marginBottom: "1rem" }}>
            <h4 style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>GM Notes</h4>
            <div
              style={{
                padding: "0.5rem",
                backgroundColor: "#fff3e0",
                borderRadius: "4px",
                fontSize: "0.85rem",
                whiteSpace: "pre-wrap",
              }}
            >
              {place.notes_gm}
            </div>
          </div>
        )}
      </div>
    );
  }

  if (entityType === "faction") {
    const faction = entity as Faction;
    return (
      <div style={{ padding: "1rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <div
              style={{
                width: "24px",
                height: "24px",
                backgroundColor: faction.color,
                opacity: faction.opacity,
                border: "1px solid #ccc",
                borderRadius: "2px",
              }}
            />
            <h3 style={{ margin: 0 }}>{faction.name}</h3>
          </div>
          <button
            onClick={handleClose}
            aria-label="Close details"
            style={{
              border: "none",
              background: "none",
              fontSize: "1.2rem",
              cursor: "pointer",
              padding: "0",
            }}
          >
            ✕
          </button>
        </div>

        <div style={{ marginTop: "1rem", fontSize: "0.85rem", color: "#666" }}>
          <div>Color: {faction.color}</div>
          <div>Opacity: {Math.round(faction.opacity * 100)}%</div>
        </div>

        {faction.notes_public && (
          <div style={{ marginTop: "1rem" }}>
            <h4 style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>Public Notes</h4>
            <div
              style={{
                padding: "0.5rem",
                backgroundColor: "#f5f5f5",
                borderRadius: "4px",
                fontSize: "0.85rem",
                whiteSpace: "pre-wrap",
              }}
            >
              {faction.notes_public}
            </div>
          </div>
        )}

        {viewMode === "gm" && faction.notes_gm && (
          <div style={{ marginTop: "1rem" }}>
            <h4 style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>GM Notes</h4>
            <div
              style={{
                padding: "0.5rem",
                backgroundColor: "#fff3e0",
                borderRadius: "4px",
                fontSize: "0.85rem",
                whiteSpace: "pre-wrap",
              }}
            >
              {faction.notes_gm}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={{ padding: "1rem", color: "#666" }}>
      <p>Unknown entity type.</p>
    </div>
  );
}
