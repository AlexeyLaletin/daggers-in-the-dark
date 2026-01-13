import { createContext, useContext, useState, ReactNode } from "react";
import { apiClient, ViewMode } from "../api/client";

interface ViewModeContextType {
  viewMode: ViewMode;
  setViewMode: (mode: ViewMode) => void;
}

const ViewModeContext = createContext<ViewModeContextType | undefined>(undefined);

export function ViewModeProvider({ children }: { children: ReactNode }): JSX.Element {
  const [viewMode, setViewModeState] = useState<ViewMode>("gm");

  const setViewMode = (mode: ViewMode): void => {
    setViewModeState(mode);
    apiClient.setViewMode(mode);
  };

  return (
    <ViewModeContext.Provider value={{ viewMode, setViewMode }}>
      {children}
    </ViewModeContext.Provider>
  );
}

export function useViewMode(): ViewModeContextType {
  const context = useContext(ViewModeContext);
  if (!context) {
    throw new Error("useViewMode must be used within ViewModeProvider");
  }
  return context;
}
