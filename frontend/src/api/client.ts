/**
 * API client for backend communication
 */

// Get backend URL from Electron API if available, otherwise use env var
const getBackendURL = (): string => {
  if (typeof window !== "undefined" && window.electronAPI?.getBackendURL) {
    return window.electronAPI.getBackendURL();
  }
  return (import.meta as any).env?.VITE_API_URL || "http://localhost:8000/api";
};

const API_BASE_URL = getBackendURL();

export type ViewMode = "gm" | "player";

// Project/World interfaces
export interface ProjectInitRequest {
  world_name?: string;
  description?: string;
  timezone?: string;
  initial_snapshot_date?: string;
  initial_snapshot_label?: string;
}

export interface World {
  id: string;
  name: string;
  description: string | null;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectInitResponse {
  world: World;
  initial_snapshot: Snapshot;
}

// Faction interfaces
export interface Faction {
  id: string;
  name: string;
  color: string;
  opacity: number;
  notes_public: string | null;
  notes_gm: string | null;
  created_at: string;
  updated_at: string;
}

export interface FactionCreate {
  name: string;
  color: string;
  opacity?: number;
  notes_public?: string;
  notes_gm?: string;
}

// Place interfaces
export interface Place {
  id: string;
  name: string;
  type: "building" | "district" | "landmark" | "other";
  position: { x: number; y: number } | null;
  owner_faction_id?: string;
  notes_public: string | null;
  notes_gm: string | null;
  scope: "public" | "gm" | "player";
  created_at: string;
  updated_at: string;
}

export interface PlaceCreate {
  name: string;
  type: "building" | "district" | "landmark" | "other";
  position: { x: number; y: number };
  owner_faction_id?: string;
  notes_public?: string;
  notes_gm?: string;
  scope?: "public" | "gm";
}

// Person interfaces
export interface Person {
  id: string;
  name: string;
  aliases: string[];
  status: string;
  workplace_place_id?: string;
  home_place_id?: string;
  tags: string[];
  notes_public: string | null;
  notes_gm: string | null;
  created_at: string;
  updated_at: string;
}

export interface PersonCreate {
  name: string;
  aliases?: string[];
  status?: string;
  workplace_place_id?: string;
  home_place_id?: string;
  tags?: string[];
  notes_public?: string;
  notes_gm?: string;
}

// Page interfaces
export interface NotePage {
  id: string;
  title: string;
  body_markdown: string;
  visibility: "public" | "gm" | "player";
  entity_type?: "faction" | "person" | "place";
  entity_id?: string;
  created_at: string;
  updated_at: string;
}

export interface NotePageCreate {
  title: string;
  body_markdown: string;
  visibility?: "public" | "gm";
  entity_type?: "faction" | "person" | "place";
  entity_id?: string;
}

// Snapshot interfaces
export interface Snapshot {
  id: string;
  at_date: string;
  label: string;
  created_at: string;
}

export interface SnapshotCreate {
  at_date: string;
  label: string;
  clone_from?: string;
}

export interface SnapshotsListResponse {
  snapshots: Snapshot[];
  active_snapshot_id: string | null;
}

// Graph interfaces
export interface GraphNode {
  id: string;
  type: "page";
  title: string;
  visibility: string;
}

export interface GraphEdge {
  from_id: string;
  to_id: string;
  link_type: string;
  visibility: string;
}

export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// Tile interfaces
export interface TileBatchItem {
  z: number;
  x: number;
  y: number;
  data: string; // base64-encoded PNG
}

export interface TileBatchUpload {
  faction_id: string;
  tiles: TileBatchItem[];
}

class APIClient {
  private baseURL: string;
  private viewMode: ViewMode = "gm";

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setViewMode(mode: ViewMode): void {
    this.viewMode = mode;
  }

  private getHeaders(): HeadersInit {
    return {
      "Content-Type": "application/json",
      "X-View-Mode": this.viewMode,
    };
  }

  // Project/Init endpoints
  async initProject(data: ProjectInitRequest = {}): Promise<ProjectInitResponse> {
    const response = await fetch(`${this.baseURL}/project/init`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Failed to initialize project" }));
      throw new Error(error.detail || "Failed to initialize project");
    }
    return response.json();
  }

  // Faction endpoints
  async getFactions(): Promise<Faction[]> {
    const response = await fetch(`${this.baseURL}/factions`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch factions");
    return response.json();
  }

  async createFaction(data: FactionCreate): Promise<Faction> {
    const response = await fetch(`${this.baseURL}/factions`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create faction");
    return response.json();
  }

  async updateFaction(id: string, data: Partial<FactionCreate>): Promise<Faction> {
    const response = await fetch(`${this.baseURL}/factions/${id}`, {
      method: "PUT",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update faction");
    return response.json();
  }

  async deleteFaction(id: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/factions/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to delete faction");
  }

  // Place endpoints
  async getPlaces(): Promise<Place[]> {
    const response = await fetch(`${this.baseURL}/places`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch places");
    return response.json();
  }

  async createPlace(data: PlaceCreate): Promise<Place> {
    const response = await fetch(`${this.baseURL}/places`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create place");
    return response.json();
  }

  async updatePlace(id: string, data: Partial<PlaceCreate>): Promise<Place> {
    const response = await fetch(`${this.baseURL}/places/${id}`, {
      method: "PUT",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update place");
    return response.json();
  }

  async deletePlace(id: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/places/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to delete place");
  }

  // Person endpoints
  async getPeople(): Promise<Person[]> {
    const response = await fetch(`${this.baseURL}/people`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch people");
    return response.json();
  }

  async createPerson(data: PersonCreate): Promise<Person> {
    const response = await fetch(`${this.baseURL}/people`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create person");
    return response.json();
  }

  async updatePerson(id: string, data: Partial<PersonCreate>): Promise<Person> {
    const response = await fetch(`${this.baseURL}/people/${id}`, {
      method: "PUT",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update person");
    return response.json();
  }

  async deletePerson(id: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/people/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to delete person");
  }

  // Page endpoints
  async getPages(): Promise<NotePage[]> {
    const response = await fetch(`${this.baseURL}/pages`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch pages");
    return response.json();
  }

  async createPage(data: NotePageCreate): Promise<NotePage> {
    const response = await fetch(`${this.baseURL}/pages`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create page");
    return response.json();
  }

  async updatePage(id: string, data: Partial<NotePageCreate>): Promise<NotePage> {
    const response = await fetch(`${this.baseURL}/pages/${id}`, {
      method: "PUT",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update page");
    return response.json();
  }

  async deletePage(id: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/pages/${id}`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to delete page");
  }

  // Graph endpoints
  async getGraph(): Promise<GraphResponse> {
    const response = await fetch(`${this.baseURL}/graph`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch graph");
    return response.json();
  }

  async getBacklinks(pageId: string): Promise<Array<{ id: string; title: string; visibility: string }>> {
    const response = await fetch(`${this.baseURL}/graph/backlinks/${pageId}`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch backlinks");
    return response.json();
  }

  // Snapshot endpoints
  async getSnapshots(): Promise<SnapshotsListResponse> {
    const response = await fetch(`${this.baseURL}/snapshots`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to fetch snapshots");
    return response.json();
  }

  async createSnapshot(data: SnapshotCreate): Promise<Snapshot> {
    const response = await fetch(`${this.baseURL}/snapshots`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create snapshot");
    return response.json();
  }

  async setActiveSnapshot(snapshotId: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/snapshots/active/${snapshotId}`, {
      method: "PUT",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to set active snapshot");
  }

  async deleteSnapshot(snapshotId: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/snapshots/${snapshotId}`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to delete snapshot");
  }

  // Tile endpoints
  async getTile(snapshotId: string, factionId: string, z: number, x: number, y: number): Promise<Blob | null> {
    const response = await fetch(
      `${this.baseURL}/snapshots/${snapshotId}/territory/tiles?faction_id=${factionId}&z=${z}&x=${x}&y=${y}`,
      { headers: this.getHeaders() }
    );
    if (response.status === 404) return null; // Tile doesn't exist
    if (!response.ok) throw new Error("Failed to fetch tile");
    return response.blob();
  }

  async uploadTilesBatch(snapshotId: string, batch: TileBatchUpload): Promise<void> {
    const response = await fetch(`${this.baseURL}/snapshots/${snapshotId}/territory/tiles/batch`, {
      method: "PUT",
      headers: this.getHeaders(),
      body: JSON.stringify(batch),
    });
    if (!response.ok) throw new Error("Failed to upload tiles");
  }

  async deleteTiles(snapshotId: string, factionId: string): Promise<void> {
    const response = await fetch(
      `${this.baseURL}/snapshots/${snapshotId}/territory/tiles?faction_id=${factionId}`,
      {
        method: "DELETE",
        headers: this.getHeaders(),
      }
    );
    if (!response.ok) throw new Error("Failed to delete tiles");
  }

  // Map assets endpoints
  async uploadMap(snapshotId: string, file: File): Promise<void> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.baseURL}/snapshots/${snapshotId}/map`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to upload map");
  }

  async downloadMap(snapshotId: string): Promise<Blob | null> {
    const response = await fetch(`${this.baseURL}/snapshots/${snapshotId}/map`, {
      headers: this.getHeaders(),
    });
    if (response.status === 404) return null; // Map doesn't exist
    if (!response.ok) throw new Error("Failed to download map");
    return response.blob();
  }

  async deleteMap(snapshotId: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/snapshots/${snapshotId}/map`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to delete map");
  }

  // Export/Import endpoints
  async exportProject(): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/export`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error("Failed to export project");
    return response.blob();
  }

  async importProject(file: File): Promise<void> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.baseURL}/import`, {
      method: "POST",
      body: formData,
      // Don't set Content-Type header - browser will set it with boundary
    });
    if (!response.ok) throw new Error("Failed to import project");
  }
}

export const apiClient = new APIClient(API_BASE_URL);

// Type declaration for Electron API
declare global {
  interface Window {
    electronAPI?: {
      getBackendURL: () => string;
    };
  }
}
