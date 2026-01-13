import { useState, useEffect } from "react";
import { apiClient, GraphNode, GraphEdge } from "../api/client";

export function GraphPanel(): JSX.Element {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [backlinks, setBacklinks] = useState<Array<{ id: string; title: string; visibility: string }>>([]);

  const loadGraph = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getGraph();
      setNodes(data.nodes);
      setEdges(data.edges);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load graph");
    } finally {
      setLoading(false);
    }
  };

  const loadBacklinks = async (pageId: string) => {
    try {
      const data = await apiClient.getBacklinks(pageId);
      setBacklinks(data);
    } catch (err) {
      console.error("Failed to load backlinks:", err);
      setBacklinks([]);
    }
  };

  useEffect(() => {
    loadGraph();
  }, []);

  useEffect(() => {
    if (selectedNodeId) {
      loadBacklinks(selectedNodeId);
    } else {
      setBacklinks([]);
    }
  }, [selectedNodeId]);

  if (loading) return <div style={{ padding: "1rem" }}>Loading graph...</div>;

  const selectedNode = nodes.find((n) => n.id === selectedNodeId);
  const connectedEdges = edges.filter((e) => e.from_id === selectedNodeId || e.to_id === selectedNodeId);

  return (
    <div style={{ padding: "1rem", display: "flex", flexDirection: "column", height: "100%" }}>
      <h2 style={{ marginTop: 0, marginBottom: "1rem" }}>Knowledge Graph</h2>

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

      <div style={{ display: "flex", gap: "1rem", flex: 1, overflow: "hidden" }}>
        {/* Nodes list */}
        <div style={{ flex: "0 0 250px", overflowY: "auto" }}>
          <h3 style={{ fontSize: "1rem", marginTop: 0 }}>Pages ({nodes.length})</h3>
          {nodes.length === 0 ? (
            <p style={{ color: "#666", fontSize: "0.9rem" }}>No pages yet.</p>
          ) : (
            <ul style={{ listStyle: "none", padding: 0 }}>
              {nodes.map((node) => (
                <li key={node.id} style={{ marginBottom: "0.25rem" }}>
                  <button
                    onClick={() => setSelectedNodeId(node.id)}
                    style={{
                      width: "100%",
                      textAlign: "left",
                      padding: "0.5rem",
                      border: "1px solid #ccc",
                      borderRadius: "4px",
                      backgroundColor: selectedNodeId === node.id ? "#e3f2fd" : "#fff",
                      cursor: "pointer",
                      fontSize: "0.85rem",
                    }}
                  >
                    {node.title}
                    {node.visibility === "gm" && " 🔒"}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Details */}
        <div style={{ flex: 1, overflowY: "auto", padding: "1rem", backgroundColor: "#fff", borderRadius: "4px", border: "1px solid #ccc" }}>
          {selectedNode ? (
            <>
              <h3 style={{ marginTop: 0 }}>{selectedNode.title}</h3>

              {/* Connected edges */}
              <div style={{ marginBottom: "1.5rem" }}>
                <h4 style={{ fontSize: "0.95rem", marginBottom: "0.5rem" }}>Links ({connectedEdges.length})</h4>
                {connectedEdges.length === 0 ? (
                  <p style={{ color: "#666", fontSize: "0.85rem" }}>No links</p>
                ) : (
                  <ul style={{ listStyle: "none", padding: 0 }}>
                    {connectedEdges.map((edge, idx) => {
                      const otherNodeId = edge.from_id === selectedNodeId ? edge.to_id : edge.from_id;
                      const otherNode = nodes.find((n) => n.id === otherNodeId);
                      const direction = edge.from_id === selectedNodeId ? "→" : "←";

                      return (
                        <li key={idx} style={{ marginBottom: "0.25rem", fontSize: "0.85rem" }}>
                          <button
                            onClick={() => setSelectedNodeId(otherNodeId)}
                            style={{
                              border: "none",
                              background: "none",
                              color: "#1976d2",
                              cursor: "pointer",
                              textDecoration: "underline",
                              padding: 0,
                            }}
                          >
                            {direction} {otherNode?.title || otherNodeId}
                          </button>
                          <span style={{ marginLeft: "0.5rem", color: "#666" }}>
                            ({edge.link_type})
                          </span>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </div>

              {/* Backlinks */}
              <div>
                <h4 style={{ fontSize: "0.95rem", marginBottom: "0.5rem" }}>Backlinks ({backlinks.length})</h4>
                {backlinks.length === 0 ? (
                  <p style={{ color: "#666", fontSize: "0.85rem" }}>No pages link to this page</p>
                ) : (
                  <ul style={{ listStyle: "none", padding: 0 }}>
                    {backlinks.map((backlink) => (
                      <li key={backlink.id} style={{ marginBottom: "0.25rem", fontSize: "0.85rem" }}>
                        <button
                          onClick={() => setSelectedNodeId(backlink.id)}
                          style={{
                            border: "none",
                            background: "none",
                            color: "#1976d2",
                            cursor: "pointer",
                            textDecoration: "underline",
                            padding: 0,
                          }}
                        >
                          {backlink.title}
                          {backlink.visibility === "gm" && " 🔒"}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </>
          ) : (
            <p style={{ color: "#666", fontSize: "0.9rem" }}>Select a page to view its connections</p>
          )}
        </div>
      </div>

      <div style={{ marginTop: "1rem", padding: "0.75rem", backgroundColor: "#e3f2fd", borderRadius: "4px", fontSize: "0.85rem" }}>
        💡 <strong>Tip:</strong> Use [[Page Title]] in your page content to create wikilinks between pages.
      </div>
    </div>
  );
}
