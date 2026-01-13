import { useEffect, useState } from "react";
import { apiClient, Place } from "../api/client";
import { useMap } from "../contexts/MapContext";

export function PlaceList(): JSX.Element {
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { mapState, selectPlace } = useMap();

  useEffect(() => {
    loadPlaces().catch((err: Error) => {
      setError(err.message);
      setLoading(false);
    });
  }, []);

  const loadPlaces = async (): Promise<void> => {
    try {
      setLoading(true);
      const data = await apiClient.getPlaces();
      setPlaces(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading places...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Places</h2>
      {places.length === 0 ? (
        <p style={{ color: "#666", fontSize: "0.9rem" }}>
          No places yet. Click on the map in "Add POI" mode to create one.
        </p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {places.map((place) => (
            <li key={place.id} style={{ marginBottom: "0.5rem" }}>
              <button
                onClick={() => selectPlace(place.id)}
                style={{
                  width: "100%",
                  textAlign: "left",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  backgroundColor:
                    mapState.selectedPlaceId === place.id ? "#e3f2fd" : "#fff",
                  cursor: "pointer",
                }}
              >
                <div style={{ fontWeight: "bold" }}>{place.name}</div>
                <div style={{ fontSize: "0.85rem", color: "#666" }}>
                  {place.type}
                  {place.scope === "gm" && " 🔒"}
                </div>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
