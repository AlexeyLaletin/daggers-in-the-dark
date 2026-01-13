import { useMap } from "../contexts/MapContext";

export function LayerControl(): JSX.Element {
  const { mapState, updateLayer } = useMap();

  return (
    <div
      style={{
        position: "absolute",
        top: "60px",
        right: "10px",
        backgroundColor: "#fff",
        border: "1px solid #ccc",
        borderRadius: "4px",
        padding: "0.75rem",
        minWidth: "200px",
        zIndex: 100,
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
      }}
    >
      <h3 style={{ margin: "0 0 0.75rem 0", fontSize: "0.9rem", fontWeight: "bold" }}>
        Layers
      </h3>
      {mapState.layers.map((layer) => (
        <div key={layer.id} style={{ marginBottom: "0.75rem" }}>
          <div style={{ display: "flex", alignItems: "center", marginBottom: "0.25rem" }}>
            <input
              type="checkbox"
              id={`layer-${layer.id}`}
              checked={layer.visible}
              onChange={(e) => updateLayer(layer.id, { visible: e.target.checked })}
              style={{ marginRight: "0.5rem" }}
            />
            <label
              htmlFor={`layer-${layer.id}`}
              style={{ fontSize: "0.85rem", fontWeight: "500" }}
            >
              {layer.name}
            </label>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <label
              htmlFor={`opacity-${layer.id}`}
              style={{ fontSize: "0.75rem", color: "#666", minWidth: "50px" }}
            >
              Opacity:
            </label>
            <input
              type="range"
              id={`opacity-${layer.id}`}
              min="0"
              max="1"
              step="0.1"
              value={layer.opacity}
              onChange={(e) => updateLayer(layer.id, { opacity: parseFloat(e.target.value) })}
              disabled={!layer.visible}
              style={{ flex: 1 }}
            />
            <span style={{ fontSize: "0.75rem", color: "#666", minWidth: "30px" }}>
              {Math.round(layer.opacity * 100)}%
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
