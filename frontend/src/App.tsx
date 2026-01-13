import { useState } from "react";
import { FactionList } from "./components/FactionList";
import { PlaceList } from "./components/PlaceList";
import { Map } from "./components/Map";
import { ViewModeToggle } from "./components/ViewModeToggle";
import { Drawer, DrawerTabs, DrawerContent, DrawerTab } from "./components/Drawer";
import { DetailPanel } from "./components/DetailPanel";
import { ProjectInitModal } from "./components/ProjectInitModal";
import { SnapshotsPanel } from "./components/SnapshotsPanel";
import { PeoplePanel } from "./components/PeoplePanel";
import { PagesPanel } from "./components/PagesPanel";
import { GraphPanel } from "./components/GraphPanel";
import { ProjectPanel } from "./components/ProjectPanel";
import { useProject } from "./contexts/ProjectContext";

function App(): JSX.Element {
  const [drawerOpen, setDrawerOpen] = useState(true);
  const [activeTab, setActiveTab] = useState<DrawerTab>("places");
  const { isInitialized, isLoading, error, initProject } = useProject();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInitProject = async (request: Parameters<typeof initProject>[0]) => {
    setIsSubmitting(true);
    try {
      await initProject(request);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Show loading state
  if (isLoading) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ textAlign: "center" }}>
          <h2>Loading...</h2>
          <p style={{ color: "#666" }}>Checking project status</p>
        </div>
      </div>
    );
  }

  // Show initialization modal if project is not initialized
  if (!isInitialized) {
    return (
      <ProjectInitModal onSubmit={handleInitProject} isSubmitting={isSubmitting} error={error} />
    );
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        fontFamily: "sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Top bar with mode toggle */}
      <ViewModeToggle />

      {/* Main content */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden", position: "relative" }}>
        {/* Left slide-out drawer */}
        <Drawer isOpen={drawerOpen} onToggle={() => setDrawerOpen(!drawerOpen)}>
          <div style={{ padding: "1rem 1rem 0 1rem" }}>
            <h1 style={{ margin: 0, fontSize: "1.5rem" }}>Blades</h1>
            <p style={{ fontSize: "0.9rem", color: "#666", marginBottom: "1rem" }}>Faction Map</p>
          </div>
          <DrawerTabs activeTab={activeTab} onTabChange={setActiveTab} />
          <DrawerContent activeTab={activeTab}>
            {activeTab === "people" && <PeoplePanel />}
            {activeTab === "places" && <PlaceList />}
            {activeTab === "factions" && <FactionList />}
            {activeTab === "pages" && <PagesPanel />}
            {activeTab === "graph" && <GraphPanel />}
            {activeTab === "snapshots" && <SnapshotsPanel />}
            {activeTab === "events" && (
              <div>
                <h2 style={{ marginTop: 0 }}>Events</h2>
                <p style={{ color: "#666", fontSize: "0.9rem" }}>Coming soon: Event timeline</p>
              </div>
            )}
            {activeTab === "project" && <ProjectPanel />}
          </DrawerContent>
        </Drawer>

        {/* Main map area */}
        <main
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            marginLeft: drawerOpen ? "320px" : "0",
            transition: "margin-left 0.3s ease",
          }}
        >
          <Map />
        </main>

        {/* Right sidebar (entity details) */}
        <aside
          style={{
            width: "300px",
            borderLeft: "1px solid #ccc",
            overflowY: "auto",
            backgroundColor: "#fff",
          }}
        >
          <DetailPanel />
        </aside>
      </div>
    </div>
  );
}

export default App;
