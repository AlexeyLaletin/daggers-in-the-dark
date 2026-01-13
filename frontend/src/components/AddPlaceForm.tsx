import { useState } from "react";
import { apiClient, PlaceCreate } from "../api/client";
import { useViewMode } from "../contexts/ViewModeContext";

interface AddPlaceFormProps {
  position: { x: number; y: number };
  onSuccess: () => void;
  onCancel: () => void;
}

export function AddPlaceForm({ position, onSuccess, onCancel }: AddPlaceFormProps): JSX.Element {
  const { viewMode } = useViewMode();
  const [name, setName] = useState("");
  const [type, setType] = useState<"building" | "district" | "landmark" | "other">("building");
  const [notesPublic, setNotesPublic] = useState("");
  const [notesGm, setNotesGm] = useState("");
  const [scope, setScope] = useState<"public" | "gm">("public");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Name is required");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const placeData: PlaceCreate = {
        name: name.trim(),
        type,
        position,
        notes_public: notesPublic || undefined,
        notes_gm: notesGm || undefined,
        scope: viewMode === "gm" ? scope : "public", // Players can only create public (backend will enforce)
      };

      await apiClient.createPlace(placeData);
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create place");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        padding: "1rem",
        backgroundColor: "#fff",
        border: "1px solid #ccc",
        borderRadius: "4px",
      }}
    >
      <h3 style={{ marginTop: 0 }}>Add New Place</h3>

      <div style={{ marginBottom: "1rem", fontSize: "0.85rem", color: "#666" }}>
        Position: ({position.x.toFixed(0)}, {position.y.toFixed(0)})
      </div>

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

      <div style={{ marginBottom: "1rem" }}>
        <label
          htmlFor="place-name"
          style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}
        >
          Name *
        </label>
        <input
          id="place-name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          autoFocus
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
          htmlFor="place-type"
          style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}
        >
          Type
        </label>
        <select
          id="place-type"
          value={type}
          onChange={(e) => setType(e.target.value as typeof type)}
          style={{
            width: "100%",
            padding: "0.5rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            fontSize: "0.9rem",
          }}
        >
          <option value="building">Building</option>
          <option value="district">District</option>
          <option value="landmark">Landmark</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label
          htmlFor="notes-public"
          style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}
        >
          Public Notes
        </label>
        <textarea
          id="notes-public"
          value={notesPublic}
          onChange={(e) => setNotesPublic(e.target.value)}
          rows={3}
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

      {viewMode === "gm" && (
        <>
          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="notes-gm"
              style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}
            >
              GM Notes
            </label>
            <textarea
              id="notes-gm"
              value={notesGm}
              onChange={(e) => setNotesGm(e.target.value)}
              rows={3}
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
            <label style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>
              Visibility
            </label>
            <div style={{ display: "flex", gap: "1rem" }}>
              <label style={{ fontSize: "0.9rem" }}>
                <input
                  type="radio"
                  value="public"
                  checked={scope === "public"}
                  onChange={(e) => setScope(e.target.value as typeof scope)}
                  style={{ marginRight: "0.25rem" }}
                />
                Public
              </label>
              <label style={{ fontSize: "0.9rem" }}>
                <input
                  type="radio"
                  value="gm"
                  checked={scope === "gm"}
                  onChange={(e) => setScope(e.target.value as typeof scope)}
                  style={{ marginRight: "0.25rem" }}
                />
                GM Only
              </label>
            </div>
          </div>
        </>
      )}

      {viewMode === "player" && (
        <div
          style={{
            padding: "0.5rem",
            backgroundColor: "#e3f2fd",
            borderRadius: "4px",
            fontSize: "0.85rem",
            marginBottom: "1rem",
          }}
        >
          ℹ️ Places created by players are public by default
        </div>
      )}

      <div style={{ display: "flex", gap: "0.5rem", justifyContent: "flex-end" }}>
        <button
          type="button"
          onClick={onCancel}
          disabled={submitting}
          style={{
            padding: "0.5rem 1rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            backgroundColor: "#fff",
            cursor: submitting ? "not-allowed" : "pointer",
            fontSize: "0.9rem",
          }}
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={submitting}
          style={{
            padding: "0.5rem 1rem",
            border: "none",
            borderRadius: "4px",
            backgroundColor: submitting ? "#ccc" : "#1976d2",
            color: "#fff",
            cursor: submitting ? "not-allowed" : "pointer",
            fontSize: "0.9rem",
            fontWeight: "bold",
          }}
        >
          {submitting ? "Creating..." : "Create Place"}
        </button>
      </div>
    </form>
  );
}
