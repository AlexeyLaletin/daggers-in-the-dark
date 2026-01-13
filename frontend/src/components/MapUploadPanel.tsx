import { useState } from "react";
import { apiClient } from "../api/client";
import { useProject } from "../contexts/ProjectContext";

interface MapUploadPanelProps {
  onMapUploaded?: () => void;
}

export function MapUploadPanel({ onMapUploaded }: MapUploadPanelProps): JSX.Element {
  const { activeSnapshot } = useProject();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !activeSnapshot) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      setError("Please select an image file (PNG, JPEG, etc.)");
      e.target.value = "";
      return;
    }

    setIsUploading(true);
    setError(null);
    setSuccess(null);

    try {
      await apiClient.uploadMap(activeSnapshot.id, file);
      setSuccess("Map uploaded successfully!");
      onMapUploaded?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to upload map");
    } finally {
      setIsUploading(false);
      e.target.value = "";
    }
  };

  const handleDelete = async () => {
    if (!activeSnapshot) return;
    if (!confirm("Are you sure you want to delete the base map for this snapshot?")) return;

    setError(null);
    setSuccess(null);

    try {
      await apiClient.deleteMap(activeSnapshot.id);
      setSuccess("Map deleted successfully!");
      onMapUploaded?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete map");
    }
  };

  if (!activeSnapshot) {
    return (
      <div style={{ padding: "1rem" }}>
        <p style={{ color: "#666", fontSize: "0.9rem" }}>
          No active snapshot. Please create a snapshot first.
        </p>
      </div>
    );
  }

  return (
    <div style={{ padding: "1rem" }}>
      <h3 style={{ fontSize: "1rem", marginTop: 0, marginBottom: "0.5rem" }}>Base Map</h3>

      {error && (
        <div
          style={{
            padding: "0.5rem",
            marginBottom: "0.5rem",
            backgroundColor: "#ffebee",
            color: "#d32f2f",
            borderRadius: "4px",
            fontSize: "0.85rem",
          }}
        >
          {error}
        </div>
      )}

      {success && (
        <div
          style={{
            padding: "0.5rem",
            marginBottom: "0.5rem",
            backgroundColor: "#e8f5e9",
            color: "#2e7d32",
            borderRadius: "4px",
            fontSize: "0.85rem",
          }}
        >
          {success}
        </div>
      )}

      <p style={{ fontSize: "0.85rem", color: "#666", marginBottom: "0.75rem" }}>
        Upload a base map image for snapshot: <strong>{activeSnapshot.label}</strong>
      </p>

      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <label
          htmlFor="map-upload"
          style={{
            padding: "0.5rem 1rem",
            border: "none",
            borderRadius: "4px",
            backgroundColor: isUploading ? "#ccc" : "#1976d2",
            color: "#fff",
            cursor: isUploading ? "not-allowed" : "pointer",
            fontSize: "0.85rem",
            fontWeight: "bold",
          }}
        >
          {isUploading ? "Uploading..." : "📤 Upload Map"}
        </label>
        <input
          id="map-upload"
          type="file"
          accept="image/*"
          onChange={handleUpload}
          disabled={isUploading}
          style={{ display: "none" }}
        />

        <button
          onClick={handleDelete}
          disabled={isUploading}
          style={{
            padding: "0.5rem 1rem",
            border: "1px solid #d32f2f",
            borderRadius: "4px",
            backgroundColor: "#fff",
            color: "#d32f2f",
            cursor: isUploading ? "not-allowed" : "pointer",
            fontSize: "0.85rem",
          }}
        >
          🗑️ Delete Map
        </button>
      </div>

      <div style={{ marginTop: "0.75rem", fontSize: "0.8rem", color: "#666" }}>
        💡 Tip: Upload PNG or JPEG images. The map will be displayed as the base layer on the canvas.
      </div>
    </div>
  );
}
