export type DrawerTab = "people" | "places" | "factions" | "pages" | "graph" | "snapshots" | "events" | "project";

interface DrawerProps {
  isOpen: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}

export function Drawer({ isOpen, onToggle, children }: DrawerProps): JSX.Element {
  return (
    <>
      {/* Toggle button */}
      <button
        onClick={onToggle}
        aria-label={isOpen ? "Close drawer" : "Open drawer"}
        style={{
          position: "absolute",
          left: isOpen ? "320px" : "0",
          top: "50%",
          transform: "translateY(-50%)",
          zIndex: 1001,
          padding: "0.5rem",
          backgroundColor: "#fff",
          border: "1px solid #ccc",
          borderLeft: isOpen ? "none" : "1px solid #ccc",
          borderRadius: isOpen ? "0 4px 4px 0" : "4px",
          cursor: "pointer",
          transition: "left 0.3s ease",
        }}
      >
        {isOpen ? "◀" : "▶"}
      </button>

      {/* Drawer panel */}
      <aside
        style={{
          position: "absolute",
          left: isOpen ? "0" : "-320px",
          top: 0,
          bottom: 0,
          width: "320px",
          backgroundColor: "#fff",
          borderRight: "1px solid #ccc",
          overflowY: "auto",
          transition: "left 0.3s ease",
          zIndex: 1000,
        }}
      >
        {children}
      </aside>
    </>
  );
}

interface DrawerTabsProps {
  activeTab: DrawerTab;
  onTabChange: (tab: DrawerTab) => void;
}

export function DrawerTabs({ activeTab, onTabChange }: DrawerTabsProps): JSX.Element {
  const tabs: { id: DrawerTab; label: string }[] = [
    { id: "people", label: "Люди" },
    { id: "places", label: "Места" },
    { id: "factions", label: "Фракции" },
    { id: "pages", label: "Заметки" },
    { id: "graph", label: "Граф" },
    { id: "snapshots", label: "Снимки" },
    { id: "events", label: "События" },
    { id: "project", label: "Проект" },
  ];

  return (
    <div
      role="tablist"
      style={{
        display: "flex",
        borderBottom: "1px solid #ccc",
        backgroundColor: "#f5f5f5",
      }}
    >
      {tabs.map((tab) => (
        <button
          key={tab.id}
          role="tab"
          aria-selected={activeTab === tab.id}
          aria-controls={`${tab.id}-panel`}
          onClick={() => onTabChange(tab.id)}
          style={{
            flex: 1,
            padding: "0.75rem 0.5rem",
            border: "none",
            backgroundColor: activeTab === tab.id ? "#fff" : "transparent",
            borderBottom: activeTab === tab.id ? "2px solid #1976d2" : "2px solid transparent",
            cursor: "pointer",
            fontWeight: activeTab === tab.id ? "bold" : "normal",
            fontSize: "0.9rem",
          }}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

interface DrawerContentProps {
  activeTab: DrawerTab;
  children: React.ReactNode;
}

export function DrawerContent({ activeTab, children }: DrawerContentProps): JSX.Element {
  return (
    <div
      id={`${activeTab}-panel`}
      role="tabpanel"
      aria-labelledby={`${activeTab}-tab`}
      style={{ padding: "1rem" }}
    >
      {children}
    </div>
  );
}
