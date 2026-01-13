import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import App from "../App";

describe("App integration tests", () => {
  beforeEach(() => {
    // Mock fetch for API calls
    globalThis.fetch = vi.fn();
  });

  it("renders without crashing", () => {
    render(<App />);
    expect(screen.getByText(/Blades Faction Map/i)).toBeInTheDocument();
  });

  it("will test API integration when backend is implemented", async () => {
    // TODO: implement after backend API is ready
    // Mock API response
    // (global.fetch as any).mockResolvedValueOnce({
    //   ok: true,
    //   json: async () => ({ factions: [] }),
    // });
    //
    // render(<App />);
    // await waitFor(() => {
    //   expect(global.fetch).toHaveBeenCalledWith(
    //     expect.stringContaining("/api/factions")
    //   );
    // });
  });
});
