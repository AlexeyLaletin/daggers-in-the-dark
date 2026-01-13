import { useEffect, useState } from "react";
import { apiClient, Faction } from "../api/client";

export function FactionList(): JSX.Element {
  const [factions, setFactions] = useState<Faction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFactions().catch((err: Error) => {
      setError(err.message);
      setLoading(false);
    });
  }, []);

  const loadFactions = async (): Promise<void> => {
    try {
      setLoading(true);
      const data = await apiClient.getFactions();
      setFactions(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading factions...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Factions</h2>
      {factions.length === 0 ? (
        <p>No factions yet. Create one to get started.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {factions.map((faction) => (
            <li key={faction.id} style={{ marginBottom: "0.5rem" }}>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.5rem",
                }}
              >
                <div
                  style={{
                    width: "20px",
                    height: "20px",
                    backgroundColor: faction.color,
                    opacity: faction.opacity,
                    border: "1px solid #ccc",
                  }}
                />
                <span>{faction.name}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
