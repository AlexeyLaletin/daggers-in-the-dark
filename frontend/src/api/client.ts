/**
 * API client for backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

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

export type ViewMode = "gm" | "player";

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
}

export const apiClient = new APIClient(API_BASE_URL);
