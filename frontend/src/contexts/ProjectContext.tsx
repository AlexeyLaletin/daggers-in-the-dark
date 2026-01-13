import { createContext, useContext, useState, ReactNode, useEffect, useCallback } from "react";
import { apiClient, World, ProjectInitRequest, Snapshot } from "../api/client";

interface ProjectContextType {
  world: World | null;
  activeSnapshot: Snapshot | null;
  isInitialized: boolean;
  isLoading: boolean;
  error: string | null;
  initProject: (request: ProjectInitRequest) => Promise<void>;
  checkInitialization: () => Promise<void>;
  setActiveSnapshot: (snapshot: Snapshot | null) => void;
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

export function ProjectProvider({ children }: { children: ReactNode }): JSX.Element {
  const [world, setWorld] = useState<World | null>(null);
  const [activeSnapshot, setActiveSnapshotState] = useState<Snapshot | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkInitialization = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Try to fetch factions - if it returns 409, project is not initialized
      await apiClient.getFactions();
      // If successful, fetch snapshots to get world info
      const snapshotsData = await apiClient.getSnapshots();
      if (snapshotsData.active_snapshot_id) {
        const activeSnap = snapshotsData.snapshots.find(
          (s) => s.id === snapshotsData.active_snapshot_id
        );
        if (activeSnap) {
          setActiveSnapshotState(activeSnap);
        }
      }
      setIsInitialized(true);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Unknown error";
      if (errorMsg.includes("not initialized") || errorMsg.includes("409")) {
        setIsInitialized(false);
      } else {
        setError(errorMsg);
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const initProject = useCallback(async (request: ProjectInitRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.initProject(request);
      setWorld(response.world);
      setActiveSnapshotState(response.initial_snapshot);
      setIsInitialized(true);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Failed to initialize project";
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const setActiveSnapshot = useCallback((snapshot: Snapshot | null) => {
    setActiveSnapshotState(snapshot);
  }, []);

  useEffect(() => {
    checkInitialization();
  }, [checkInitialization]);

  return (
    <ProjectContext.Provider
      value={{
        world,
        activeSnapshot,
        isInitialized,
        isLoading,
        error,
        initProject,
        checkInitialization,
        setActiveSnapshot,
      }}
    >
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject(): ProjectContextType {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error("useProject must be used within ProjectProvider");
  }
  return context;
}
