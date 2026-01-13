import { useState, useEffect } from "react";
import { apiClient, Snapshot } from "../api/client";
import { useProject } from "../contexts/ProjectContext";
import { MapUploadPanel } from "./MapUploadPanel";

export function SnapshotsPanel(): JSX.Element {
  const { activeSnapshot, setActiveSnapshot } = useProject();
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newLabel, setNewLabel] = useState("");
  const [newDate, setNewDate] = useState("");

  const loadSnapshots = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getSnapshots();
      setSnapshots(data.snapshots);
      if (data.active_snapshot_id) {
        const active = data.snapshots.find((s) => s.id === data.active_snapshot_id);
        if (active) {
          setActiveSnapshot(active);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load snapshots");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSnapshots();
  }, []);

  const handleCreateSnapshot = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newLabel.trim() || !newDate) return;

    setIsCreating(true);
    try {
      await apiClient.createSnapshot({
        at_date: newDate,
        label: newLabel.trim(),
      });
      setNewLabel("");
      setNewDate("");
      await loadSnapshots();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create snapshot");
    } finally {
      setIsCreating(false);
    }
  };

  const handleSetActive = async (snapshot: Snapshot) => {
    try {
      await apiClient.setActiveSnapshot(snapshot.id);
      setActiveSnapshot(snapshot);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to set active snapshot");
    }
  };

  const handleDelete = async (snapshotId: string) => {
    if (!confirm("Are you sure you want to delete this snapshot?")) return;

    try {
      await apiClient.deleteSnapshot(snapshotId);
      await loadSnapshots();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete snapshot");
    }
  };

  if (loading) return <div style={{ padding: "1rem" }}>Loading snapshots...</div>;

  return (
    <div style={{ padding: "1rem" }}>
      <h2 style={{ marginTop: 0 }}>Snapshots</h2>

      {/* Map upload section */}
      {activeSnapshot && (
        <div
          style={{
            marginBottom: "1.5rem",
            padding: "1rem",
            backgroundColor: "#f5f5f5",
            borderRadius: "4px",
          }}
        >
          <MapUploadPanel onMapUploaded={loadSnapshots} />
        </div>
      )}

      {error && (
        <div
          style={{
            padding: "0.5rem",
            marginBottom: "1rem",
            backgroundColor: "#ffebee",
            color: "#d32f2f",
            borderRadius: "4px",
            fontSize: "0.85rem",
          }}
        >
          {error}
        </div>
      )}

      {/* Active snapshot indicator */}
      {activeSnapshot && (
        <div
          style={{
            padding: "0.75rem",
            marginBottom: "1rem",
            backgroundColor: "#e3f2fd",
            borderRadius: "4px",
            fontSize: "0.9rem",
          }}
        >
          <strong>Active:</strong> {activeSnapshot.label}
          <br />
          <small style={{ color: "#666" }}>
            {new Date(activeSnapshot.at_date).toLocaleString()}
          </small>
        </div>
      )}

      {/* Create snapshot form */}
      <form onSubmit={handleCreateSnapshot} style={{ marginBottom: "1.5rem" }}>
        <h3 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>Create New Snapshot</h3>
        <div style={{ marginBottom: "0.5rem" }}>
          <input
            type="text"
            value={newLabel}
            onChange={(e) => setNewLabel(e.target.value)}
            placeholder="Label (e.g., Session 3)"
            disabled={isCreating}
            style={{
              width: "100%",
              padding: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "0.9rem",
              marginBottom: "0.5rem",
            }}
          />
          <input
            type="datetime-local"
            value={newDate}
            onChange={(e) => setNewDate(e.target.value)}
            disabled={isCreating}
            style={{
              width: "100%",
              padding: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "0.9rem",
              marginBottom: "0.5rem",
            }}
          />
        </div>
        <button
          type="submit"
          disabled={isCreating || !newLabel.trim() || !newDate}
          style={{
            width: "100%",
            padding: "0.5rem",
            border: "none",
            borderRadius: "4px",
            backgroundColor: isCreating || !newLabel.trim() || !newDate ? "#ccc" : "#1976d2",
            color: "#fff",
            cursor: isCreating || !newLabel.trim() || !newDate ? "not-allowed" : "pointer",
            fontSize: "0.9rem",
          }}
        >
          {isCreating ? "Creating..." : "Create Snapshot"}
        </button>
      </form>

      {/* Snapshots list */}
      <h3 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>All Snapshots</h3>
      {snapshots.length === 0 ? (
        <p style={{ color: "#666", fontSize: "0.9rem" }}>No snapshots yet.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {snapshots
            .sort((a, b) => new Date(b.at_date).getTime() - new Date(a.at_date).getTime())
            .map((snapshot) => (
              <li
                key={snapshot.id}
                style={{
                  padding: "0.75rem",
                  marginBottom: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  backgroundColor: activeSnapshot?.id === snapshot.id ? "#e3f2fd" : "#fff",
                }}
              >
                <div
                  style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}
                >
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: "bold", marginBottom: "0.25rem" }}>
                      {snapshot.label}
                    </div>
                    <div style={{ fontSize: "0.85rem", color: "#666" }}>
                      {new Date(snapshot.at_date).toLocaleString()}
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: "0.5rem" }}>
                    {activeSnapshot?.id !== snapshot.id && (
                      <button
                        onClick={() => handleSetActive(snapshot)}
                        style={{
                          padding: "0.25rem 0.5rem",
                          border: "1px solid #1976d2",
                          borderRadius: "4px",
                          backgroundColor: "#fff",
                          color: "#1976d2",
                          cursor: "pointer",
                          fontSize: "0.85rem",
                        }}
                      >
                        Activate
                      </button>
                    )}
                    <button
                      onClick={() => handleDelete(snapshot.id)}
                      style={{
                        padding: "0.25rem 0.5rem",
                        border: "1px solid #d32f2f",
                        borderRadius: "4px",
                        backgroundColor: "#fff",
                        color: "#d32f2f",
                        cursor: "pointer",
                        fontSize: "0.85rem",
                      }}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </li>
            ))}
        </ul>
      )}
    </div>
  );
}
