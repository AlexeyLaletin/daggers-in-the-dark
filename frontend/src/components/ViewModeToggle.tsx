import { useViewMode } from "../contexts/ViewModeContext";

export function ViewModeToggle(): JSX.Element {
  const { viewMode, setViewMode } = useViewMode();

  return (
    <div
      style={{
        padding: "0.5rem 1rem",
        borderBottom: "1px solid #ccc",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        backgroundColor: viewMode === "gm" ? "#e3f2fd" : "#fff3e0",
      }}
    >
      <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
        {viewMode === "gm" ? "🎭 GM Mode" : "👥 Player Mode"}
      </span>
      <button
        onClick={() => setViewMode(viewMode === "gm" ? "player" : "gm")}
        style={{
          padding: "0.25rem 0.75rem",
          border: "1px solid #ccc",
          borderRadius: "4px",
          background: "white",
          cursor: "pointer",
          fontSize: "0.85rem",
        }}
      >
        Switch to {viewMode === "gm" ? "Player" : "GM"}
      </button>
    </div>
  );
}
