import { useState, useEffect } from "react";
import { apiClient, Person, PersonCreate } from "../api/client";
import { useViewMode } from "../contexts/ViewModeContext";

export function PeoplePanel(): JSX.Element {
  const { viewMode } = useViewMode();
  const [people, setPeople] = useState<Person[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState<PersonCreate>({
    name: "",
    aliases: [],
    status: "alive",
    tags: [],
    notes_public: "",
    notes_gm: "",
  });

  const loadPeople = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getPeople();
      setPeople(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load people");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPeople();
  }, [viewMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim()) return;

    setError(null);
    try {
      if (editingId) {
        await apiClient.updatePerson(editingId, formData);
      } else {
        await apiClient.createPerson(formData);
      }
      resetForm();
      await loadPeople();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save person");
    }
  };

  const handleEdit = (person: Person) => {
    setEditingId(person.id);
    setFormData({
      name: person.name,
      aliases: person.aliases,
      status: person.status,
      workplace_place_id: person.workplace_place_id,
      home_place_id: person.home_place_id,
      tags: person.tags,
      notes_public: person.notes_public || "",
      notes_gm: person.notes_gm || "",
    });
    setIsCreating(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this person?")) return;
    try {
      await apiClient.deletePerson(id);
      await loadPeople();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete person");
    }
  };

  const resetForm = () => {
    setFormData({
      name: "",
      aliases: [],
      status: "alive",
      tags: [],
      notes_public: "",
      notes_gm: "",
    });
    setEditingId(null);
    setIsCreating(false);
  };

  if (loading) return <div style={{ padding: "1rem" }}>Loading people...</div>;

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
        <h2 style={{ margin: 0 }}>People</h2>
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
            + New Person
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
          <h3 style={{ marginTop: 0, fontSize: "1rem" }}>{editingId ? "Edit" : "Create"} Person</h3>

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

          <select
            value={formData.status}
            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            style={{
              width: "100%",
              padding: "0.5rem",
              marginBottom: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            <option value="alive">Alive</option>
            <option value="dead">Dead</option>
            <option value="unknown">Unknown</option>
          </select>

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

      {/* People list */}
      {people.length === 0 ? (
        <p style={{ color: "#666", fontSize: "0.9rem" }}>No people yet.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {people.map((person) => (
            <li
              key={person.id}
              style={{
                padding: "0.75rem",
                marginBottom: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                backgroundColor: "#fff",
              }}
            >
              <div
                style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: "bold", marginBottom: "0.25rem" }}>
                    {person.name}
                    <span style={{ marginLeft: "0.5rem", fontSize: "0.85rem", color: "#666" }}>
                      ({person.status})
                    </span>
                  </div>
                  {person.notes_public && (
                    <div style={{ fontSize: "0.85rem", color: "#666", marginTop: "0.25rem" }}>
                      {person.notes_public}
                    </div>
                  )}
                  {viewMode === "gm" && person.notes_gm && (
                    <div
                      style={{
                        fontSize: "0.85rem",
                        color: "#d32f2f",
                        marginTop: "0.25rem",
                        fontStyle: "italic",
                      }}
                    >
                      🔒 {person.notes_gm}
                    </div>
                  )}
                </div>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                  <button
                    onClick={() => handleEdit(person)}
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
                    onClick={() => handleDelete(person.id)}
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
