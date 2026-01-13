import { useState } from "react";

function App(): JSX.Element {
  const [count, setCount] = useState(0);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Blades Faction Map</h1>
      <p>Frontend initialization complete.</p>
      <button onClick={() => setCount((count) => count + 1)}>count is {count}</button>
    </div>
  );
}

export default App;
