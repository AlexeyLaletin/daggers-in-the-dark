import { useState, useEffect } from "react";
import { apiClient, NotePage, NotePageCreate } from "../api/client";
import { useViewMode } from "../contexts/ViewModeContext";

export function PagesPanel(): JSX.Element {
  const { viewMode } = useViewMode();
  const [pages, setPages] = useState<NotePage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [selectedPageId, setSelectedPageId] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState<NotePageCreate>({
    title: "",
    body_markdown: "",
    visibility: "public",
  });

  const loadPages = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getPages();
      setPages(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load pages");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPages();
  }, [viewMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title.trim()) return;

    setError(null);
    try {
      if (editingId) {
        await apiClient.updatePage(editingId, formData);
      } else {
        await apiClient.createPage(formData);
      }
      resetForm();
      await loadPages();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save page");
    }
  };

  const handleEdit = (page: NotePage) => {
    setEditingId(page.id);
    setFormData({
      title: page.title,
      body_markdown: page.body_markdown,
      visibility: page.visibility as "public" | "gm",
      entity_type: page.entity_type,
      entity_id: page.entity_id,
    });
    setIsCreating(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this page?")) return;
    try {
      await apiClient.deletePage(id);
      if (selectedPageId === id) {
        setSelectedPageId(null);
      }
      await loadPages();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete page");
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      body_markdown: "",
      visibility: "public",
    });
    setEditingId(null);
    setIsCreating(false);
  };

  const selectedPage = pages.find((p) => p.id === selectedPageId);

  if (loading) return <div style={{ padding: "1rem" }}>Loading pages...</div>;

  return (
    <div style={{ padding: "1rem", display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2 style={{ margin: 0 }}>Pages</h2>
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
            + New Page
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
        <form onSubmit={handleSubmit} style={{ marginBottom: "1.5rem", padding: "1rem", backgroundColor: "#f5f5f5", borderRadius: "4px" }}>
          <h3 style={{ marginTop: 0, fontSize: "1rem" }}>{editingId ? "Edit" : "Create"} Page</h3>

          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            placeholder="Title *"
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

          <textarea
            value={formData.body_markdown}
            onChange={(e) => setFormData({ ...formData, body_markdown: e.target.value })}
            placeholder="Markdown content (use [[Page Title]] for wikilinks)"
            rows={10}
            style={{
              width: "100%",
              padding: "0.5rem",
              marginBottom: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontSize: "0.9rem",
              fontFamily: "monospace",
              resize: "vertical",
            }}
          />

          {viewMode === "gm" && (
            <select
              value={formData.visibility}
              onChange={(e) => setFormData({ ...formData, visibility: e.target.value as "public" | "gm" })}
              style={{
                width: "100%",
                padding: "0.5rem",
                marginBottom: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "0.9rem",
              }}
            >
              <option value="public">Public</option>
              <option value="gm">GM Only</option>
            </select>
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

      {/* Pages list and viewer */}
      <div style={{ display: "flex", gap: "1rem", flex: 1, overflow: "hidden" }}>
        {/* List */}
        <div style={{ flex: "0 0 200px", overflowY: "auto" }}>
          {pages.length === 0 ? (
            <p style={{ color: "#666", fontSize: "0.9rem" }}>No pages yet.</p>
          ) : (
            <ul style={{ listStyle: "none", padding: 0 }}>
              {pages.map((page) => (
                <li key={page.id} style={{ marginBottom: "0.25rem" }}>
                  <button
                    onClick={() => setSelectedPageId(page.id)}
                    style={{
                      width: "100%",
                      textAlign: "left",
                      padding: "0.5rem",
                      border: "1px solid #ccc",
                      borderRadius: "4px",
                      backgroundColor: selectedPageId === page.id ? "#e3f2fd" : "#fff",
                      cursor: "pointer",
                      fontSize: "0.85rem",
                    }}
                  >
                    {page.title}
                    {page.visibility === "gm" && " 🔒"}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Viewer */}
        <div style={{ flex: 1, overflowY: "auto", padding: "1rem", backgroundColor: "#fff", borderRadius: "4px", border: "1px solid #ccc" }}>
          {selectedPage ? (
            <>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "1rem" }}>
                <h3 style={{ margin: 0 }}>{selectedPage.title}</h3>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                  <button
                    onClick={() => handleEdit(selectedPage)}
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
                    onClick={() => handleDelete(selectedPage.id)}
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
              <div style={{ whiteSpace: "pre-wrap", fontSize: "0.9rem", lineHeight: "1.6" }}>
                {selectedPage.body_markdown}
              </div>
              {selectedPage.visibility === "gm" && (
                <div style={{ marginTop: "1rem", padding: "0.5rem", backgroundColor: "#fff3e0", borderRadius: "4px", fontSize: "0.85rem" }}>
                  🔒 This page is only visible to GM
                </div>
              )}
            </>
          ) : (
            <p style={{ color: "#666", fontSize: "0.9rem" }}>Select a page to view</p>
          )}
        </div>
      </div>
    </div>
  );
}
