/**
 * Map component placeholder
 * TODO: Implement Canvas rendering, pan/zoom, territory painting
 */

export function Map(): JSX.Element {
  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#f0f0f0",
        border: "2px dashed #ccc",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h2>Map Canvas</h2>
        <p>Territory painting will be implemented here</p>
        <p style={{ fontSize: "0.9rem", color: "#666" }}>
          Features:
          <br />- Base map loading
          <br />- Pan/zoom controls
          <br />- Brush/eraser tools
          <br />- Semi-transparent faction overlays
        </p>
      </div>
    </div>
  );
}
