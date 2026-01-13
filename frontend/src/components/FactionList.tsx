import { useEffect, useState } from "react";
import { apiClient, Faction, FactionCreate } from "../api/client";
import { useViewMode } from "../contexts/ViewModeContext";
import { useMap } from "../contexts/MapContext";

export function FactionList(): JSX.Element {
  const { viewMode } = useViewMode();
  const { selectFaction, mapState } = useMap();
  const [factions, setFactions] = useState<Faction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState<FactionCreate>({
    name: "",
    color: "#1976d2",
    opacity: 0.4,
    notes_public: "",
    notes_gm: "",
  });

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

  useEffect(() => {
    loadFactions();
  }, [viewMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim()) return;

    setError(null);
    try {
      if (editingId) {
        await apiClient.updateFaction(editingId, formData);
      } else {
        await apiClient.createFaction(formData);
      }
      resetForm();
      await loadFactions();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save faction");
    }
  };

  const handleEdit = (faction: Faction) => {
    setEditingId(faction.id);
    setFormData({
      name: faction.name,
      color: faction.color,
      opacity: faction.opacity,
      notes_public: faction.notes_public || "",
      notes_gm: faction.notes_gm || "",
    });
    setIsCreating(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this faction?")) return;
    try {
      await apiClient.deleteFaction(id);
      await loadFactions();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete faction");
    }
  };

  const resetForm = () => {
    setFormData({
      name: "",
      color: "#1976d2",
      opacity: 0.4,
      notes_public: "",
      notes_gm: "",
    });
    setEditingId(null);
    setIsCreating(false);
  };

  if (loading) return <div style={{ padding: "1rem" }}>Loading factions...</div>;

  return (
    <div style={{ padding: "1rem" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
        }}
      >
        <h2 style={{ margin: 0 }}>Factions</h2>
        {!isCreating && (
          <button
            onClick={() => setIsCreating(true)}
            style={{
              padding: "0.5rem 1rem",
              border: "none",
              borderRadius: "4px",
              backgroundColor: "#1976d2",
              color: "#fff",
              cursor: "pointer",
              fontSize: "0.9rem",
            }}
          >
            + New Faction
          </button>
        )}
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

      {/* Create/Edit form */}
      {isCreating && (
        <form
          onSubmit={handleSubmit}
          style={{
            marginBottom: "1.5rem",
            padding: "1rem",
            backgroundColor: "#f5f5f5",
            borderRadius: "4px",
          }}
        >
          <h3 style={{ marginTop: 0, fontSize: "1rem" }}>
            {editingId ? "Edit" : "Create"} Faction
          </h3>

          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Name *"
            required
            style={{
              width: "100%",
              padding: "0.5rem",
              marginBottom: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          />

          <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.5rem" }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>
                Color
              </label>
              <input
                type="color"
                value={formData.color}
                onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                style={{
                  width: "100%",
                  height: "40px",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>
                Opacity: {Math.round((formData.opacity || 0.4) * 100)}%
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={formData.opacity}
                onChange={(e) => setFormData({ ...formData, opacity: parseFloat(e.target.value) })}
                style={{ width: "100%", marginTop: "0.5rem" }}
              />
            </div>
          </div>

          <textarea
            value={formData.notes_public || ""}
            onChange={(e) => setFormData({ ...formData, notes_public: e.target.value })}
            placeholder="Public notes"
            rows={3}
            style={{
              width: "100%",
              padding: "0.5rem",
              marginBottom: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "0.9rem",
              resize: "vertical",
            }}
          />

          {viewMode === "gm" && (
            <textarea
              value={formData.notes_gm || ""}
              onChange={(e) => setFormData({ ...formData, notes_gm: e.target.value })}
              placeholder="GM notes"
              rows={3}
              style={{
                width: "100%",
                padding: "0.5rem",
                marginBottom: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
                resize: "vertical",
              }}
            />
          )}

          <div style={{ display: "flex", gap: "0.5rem" }}>
            <button
              type="submit"
              style={{
                flex: 1,
                padding: "0.5rem",
                border: "none",
                borderRadius: "4px",
                backgroundColor: "#1976d2",
                color: "#fff",
                cursor: "pointer",
                fontSize: "0.9rem",
              }}
            >
              {editingId ? "Update" : "Create"}
            </button>
            <button
              type="button"
              onClick={resetForm}
              style={{
                flex: 1,
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                backgroundColor: "#fff",
                cursor: "pointer",
                fontSize: "0.9rem",
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {factions.length === 0 ? (
        <p style={{ color: "#666", fontSize: "0.9rem" }}>
          No factions yet. Create one to get started.
        </p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {factions.map((faction) => (
            <li key={faction.id} style={{ marginBottom: "0.5rem" }}>
              <div
                style={{
                  padding: "0.75rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  backgroundColor: mapState.selectedFactionId === faction.id ? "#e3f2fd" : "#fff",
                  cursor: "pointer",
                }}
                onClick={() => selectFaction(faction.id)}
              >
                <div
                  style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flex: 1 }}>
                    <div
                      style={{
                        width: "24px",
                        height: "24px",
                        backgroundColor: faction.color,
                        opacity: faction.opacity,
                        border: "1px solid #ccc",
                        borderRadius: "2px",
                        flexShrink: 0,
                      }}
                    />
                    <div>
                      <div style={{ fontWeight: "bold" }}>{faction.name}</div>
                      {faction.notes_public && (
                        <div style={{ fontSize: "0.85rem", color: "#666", marginTop: "0.25rem" }}>
                          {faction.notes_public}
                        </div>
                      )}
                    </div>
                  </div>
                  <div
                    style={{ display: "flex", gap: "0.5rem" }}
                    onClick={(e) => e.stopPropagation()}
                  >
                    <button
                      onClick={() => handleEdit(faction)}
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
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(faction.id)}
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
              </div>
            </li>
          ))}
        </ul>
      )}

      <div
        style={{
          marginTop: "1rem",
          padding: "0.75rem",
          backgroundColor: "#e3f2fd",
          borderRadius: "4px",
          fontSize: "0.85rem",
        }}
      >
        💡 <strong>Tip:</strong> Click on a faction to select it for territory painting in Brush
        mode.
      </div>
    </div>
  );
}
