import { useState } from "react";
import { ProjectInitRequest } from "../api/client";

interface ProjectInitModalProps {
  onSubmit: (request: ProjectInitRequest) => Promise<void>;
  isSubmitting: boolean;
  error: string | null;
}

export function ProjectInitModal({
  onSubmit,
  isSubmitting,
  error,
}: ProjectInitModalProps): JSX.Element {
  const [worldName, setWorldName] = useState("Doskvol");
  const [description, setDescription] = useState("");
  const [timezone, setTimezone] = useState("UTC");
  const [snapshotLabel, setSnapshotLabel] = useState("Initial");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit({
      world_name: worldName,
      description: description || undefined,
      timezone,
      initial_snapshot_label: snapshotLabel,
    });
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 10000,
      }}
    >
      <div
        style={{
          backgroundColor: "#fff",
          borderRadius: "8px",
          padding: "2rem",
          maxWidth: "500px",
          width: "90%",
          boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
        }}
      >
        <h2 style={{ marginTop: 0, marginBottom: "1rem" }}>Initialize Project</h2>
        <p style={{ marginBottom: "1.5rem", color: "#666", fontSize: "0.9rem" }}>
          Create a new Blades in the Dark campaign project
        </p>

        {error && (
          <div
            style={{
              padding: "0.75rem",
              marginBottom: "1rem",
              backgroundColor: "#ffebee",
              color: "#d32f2f",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="world-name"
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontSize: "0.9rem",
                fontWeight: "500",
              }}
            >
              World Name *
            </label>
            <input
              id="world-name"
              type="text"
              value={worldName}
              onChange={(e) => setWorldName(e.target.value)}
              required
              autoFocus
              disabled={isSubmitting}
              style={{
                width: "100%",
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
              }}
            />
          </div>

          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="description"
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontSize: "0.9rem",
                fontWeight: "500",
              }}
            >
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isSubmitting}
              rows={3}
              placeholder="Optional description of your campaign setting"
              style={{
                width: "100%",
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
                resize: "vertical",
              }}
            />
          </div>

          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="timezone"
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontSize: "0.9rem",
                fontWeight: "500",
              }}
            >
              Timezone
            </label>
            <input
              id="timezone"
              type="text"
              value={timezone}
              onChange={(e) => setTimezone(e.target.value)}
              disabled={isSubmitting}
              style={{
                width: "100%",
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
              }}
            />
            <small style={{ color: "#666", fontSize: "0.8rem" }}>
              e.g., UTC, America/New_York, Europe/London
            </small>
          </div>

          <div style={{ marginBottom: "1.5rem" }}>
            <label
              htmlFor="snapshot-label"
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontSize: "0.9rem",
                fontWeight: "500",
              }}
            >
              Initial Snapshot Label
            </label>
            <input
              id="snapshot-label"
              type="text"
              value={snapshotLabel}
              onChange={(e) => setSnapshotLabel(e.target.value)}
              disabled={isSubmitting}
              style={{
                width: "100%",
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
              }}
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting || !worldName.trim()}
            style={{
              width: "100%",
              padding: "0.75rem",
              border: "none",
              borderRadius: "4px",
              backgroundColor: isSubmitting || !worldName.trim() ? "#ccc" : "#1976d2",
              color: "#fff",
              fontSize: "1rem",
              fontWeight: "bold",
              cursor: isSubmitting || !worldName.trim() ? "not-allowed" : "pointer",
            }}
          >
            {isSubmitting ? "Initializing..." : "Initialize Project"}
          </button>
        </form>
      </div>
    </div>
  );
}
