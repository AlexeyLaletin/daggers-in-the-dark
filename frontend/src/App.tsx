import { FactionList } from "./components/FactionList";
import { Map } from "./components/Map";

function App(): JSX.Element {
  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        fontFamily: "sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Left sidebar */}
      <aside
        style={{
          width: "300px",
          borderRight: "1px solid #ccc",
          overflowY: "auto",
        }}
      >
        <div style={{ padding: "1rem" }}>
          <h1 style={{ margin: 0, fontSize: "1.5rem" }}>Blades</h1>
          <p style={{ fontSize: "0.9rem", color: "#666" }}>Faction Map</p>
        </div>
        <FactionList />
      </aside>

      {/* Main content */}
      <main style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <Map />
      </main>

      {/* Right sidebar (future: entity details) */}
      <aside
        style={{
          width: "300px",
          borderLeft: "1px solid #ccc",
          overflowY: "auto",
          padding: "1rem",
        }}
      >
        <h3>Details</h3>
        <p style={{ fontSize: "0.9rem", color: "#666" }}>
          Entity details and notes will appear here
        </p>
      </aside>
    </div>
  );
}

export default App;
