import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { ViewModeProvider } from "./contexts/ViewModeContext.tsx";
import { MapProvider } from "./contexts/MapContext.tsx";
import { ProjectProvider } from "./contexts/ProjectContext.tsx";
import "./index.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ProjectProvider>
      <ViewModeProvider>
        <MapProvider>
          <App />
        </MapProvider>
      </ViewModeProvider>
    </ProjectProvider>
  </React.StrictMode>
);
