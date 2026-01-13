import { useState } from "react";
import { apiClient } from "../api/client";
import { useProject } from "../contexts/ProjectContext";

export function ProjectPanel(): JSX.Element {
  const { world, checkInitialization } = useProject();
  const [isExporting, setIsExporting] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleExport = async () => {
    setIsExporting(true);
    setError(null);
    setSuccess(null);
    try {
      const blob = await apiClient.exportProject();

      // Create download link
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `blades-project-${world?.name || "export"}-${new Date().toISOString().split("T")[0]}.db`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setSuccess("Project exported successfully!");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to export project");
    } finally {
      setIsExporting(false);
    }
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!confirm("WARNING: Importing will replace ALL current data. Are you sure you want to continue?")) {
      e.target.value = "";
      return;
    }

    setIsImporting(true);
    setError(null);
    setSuccess(null);
    try {
      await apiClient.importProject(file);
      setSuccess("Project imported successfully! Reloading...");

      // Reload application state
      setTimeout(async () => {
        await checkInitialization();
        window.location.reload();
      }, 1000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to import project");
    } finally {
      setIsImporting(false);
      e.target.value = "";
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2 style={{ marginTop: 0 }}>Project Settings</h2>

      {/* World info */}
      {world && (
        <div style={{ padding: "1rem", marginBottom: "1.5rem", backgroundColor: "#f5f5f5", borderRadius: "4px" }}>
          <h3 style={{ marginTop: 0, fontSize: "1rem" }}>Current Project</h3>
          <div style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>
            <strong>Name:</strong> {world.name}
          </div>
          {world.description && (
            <div style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>
              <strong>Description:</strong> {world.description}
            </div>
          )}
          <div style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>
            <strong>Timezone:</strong> {world.timezone}
          </div>
          <div style={{ fontSize: "0.85rem", color: "#666" }}>
            Created: {new Date(world.created_at).toLocaleString()}
          </div>
        </div>
      )}

      {/* Messages */}
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

      {success && (
        <div
          style={{
            padding: "0.75rem",
            marginBottom: "1rem",
            backgroundColor: "#e8f5e9",
            color: "#2e7d32",
            borderRadius: "4px",
            fontSize: "0.9rem",
          }}
        >
          {success}
        </div>
      )}

      {/* Export section */}
      <div style={{ marginBottom: "2rem" }}>
        <h3 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>Export Project</h3>
        <p style={{ fontSize: "0.9rem", color: "#666", marginBottom: "1rem" }}>
          Download your entire project (including all data, snapshots, and territory tiles) as a single database file.
        </p>
        <button
          onClick={handleExport}
          disabled={isExporting}
          style={{
            padding: "0.75rem 1.5rem",
            border: "none",
            borderRadius: "4px",
            backgroundColor: isExporting ? "#ccc" : "#1976d2",
            color: "#fff",
            cursor: isExporting ? "not-allowed" : "pointer",
            fontSize: "0.9rem",
            fontWeight: "bold",
          }}
        >
          {isExporting ? "Exporting..." : "📥 Export Project"}
        </button>
      </div>

      {/* Import section */}
      <div>
        <h3 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>Import Project</h3>
        <p style={{ fontSize: "0.9rem", color: "#666", marginBottom: "1rem" }}>
          Replace your current project with a previously exported database file.
        </p>
        <div
          style={{
            padding: "1rem",
            marginBottom: "1rem",
            backgroundColor: "#fff3e0",
            border: "1px solid #ff9800",
            borderRadius: "4px",
            fontSize: "0.85rem",
            color: "#e65100",
          }}
        >
          <strong>⚠️ WARNING:</strong> Importing will permanently delete ALL current project data
          (factions, people, places, pages, snapshots, territories).
          Make sure to export your current project first!
        </div>
        <label
          htmlFor="import-file"
          style={{
            display: "inline-block",
            padding: "0.75rem 1.5rem",
            border: "none",
            borderRadius: "4px",
            backgroundColor: isImporting ? "#ccc" : "#d32f2f",
            color: "#fff",
            cursor: isImporting ? "not-allowed" : "pointer",
            fontSize: "0.9rem",
            fontWeight: "bold",
          }}
        >
          {isImporting ? "Importing..." : "📤 Import Project"}
        </label>
        <input
          id="import-file"
          type="file"
          accept=".db,.sqlite,.sqlite3"
          onChange={handleImport}
          disabled={isImporting}
          style={{ display: "none" }}
        />
      </div>

      {/* Help section */}
      <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#e3f2fd", borderRadius: "4px", fontSize: "0.85rem" }}>
        <strong>💡 Tip:</strong> Regularly export your project to create backups.
        The exported .db file contains everything and can be imported on another device.
      </div>
    </div>
  );
}
