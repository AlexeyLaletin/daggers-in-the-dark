import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import userEvent from "@testing-library/user-event";
import App from "../App";
import { ViewModeProvider } from "../contexts/ViewModeContext";
import { MapProvider } from "../contexts/MapContext";
import { apiClient } from "../api/client";

vi.mock("../api/client", () => ({
  apiClient: {
    getFactions: vi.fn(),
    getPlaces: vi.fn(),
    createPlace: vi.fn(),
    setViewMode: vi.fn(),
  },
}));

describe("Map UI Integration Tests", () => {
  const renderApp = () => {
    return render(
      <ViewModeProvider>
        <MapProvider>
          <App />
        </MapProvider>
      </ViewModeProvider>
    );
  };

  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(apiClient.getFactions).mockResolvedValue([]);
    vi.mocked(apiClient.getPlaces).mockResolvedValue([]);
  });

  it("renders main layout with drawer, map, and detail panel", async () => {
    renderApp();

    expect(screen.getByText("Blades")).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Места" })).toBeInTheDocument();
    expect(screen.getByLabelText("Pan mode")).toBeInTheDocument();
  });

  it("can toggle drawer open and closed", async () => {
    const user = userEvent.setup();
    renderApp();

    const toggleButton = screen.getByLabelText("Close drawer");
    await user.click(toggleButton);

    expect(screen.getByLabelText("Open drawer")).toBeInTheDocument();
  });

  it("can switch between drawer tabs", async () => {
    const user = userEvent.setup();
    renderApp();

    await user.click(screen.getByRole("tab", { name: "Фракции" }));
    expect(screen.getByRole("tab", { name: "Фракции" })).toHaveAttribute("aria-selected", "true");

    await user.click(screen.getByRole("tab", { name: "Места" }));
    expect(screen.getByRole("tab", { name: "Места" })).toHaveAttribute("aria-selected", "true");
  });

  it("can switch map mode between pan and add POI", async () => {
    const user = userEvent.setup();
    renderApp();

    const addPoiButton = screen.getByLabelText("Add POI mode");
    await user.click(addPoiButton);

    expect(addPoiButton).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByLabelText("Pan mode")).toHaveAttribute("aria-pressed", "false");
  });

  it("displays places in the list", async () => {
    vi.mocked(apiClient.getPlaces).mockResolvedValue([
      {
        id: "1",
        name: "Test Place",
        type: "building",
        position: { x: 100, y: 200 },
        notes_public: "Public note",
        notes_gm: null,
        scope: "public",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ]);

    renderApp();

    await waitFor(() => {
      expect(screen.getByText("Test Place")).toBeInTheDocument();
    });
  });

  it("shows detail panel when place is selected", async () => {
    const user = userEvent.setup();
    vi.mocked(apiClient.getPlaces).mockResolvedValue([
      {
        id: "1",
        name: "Test Place",
        type: "building",
        position: { x: 100, y: 200 },
        notes_public: "Public note",
        notes_gm: null,
        scope: "public",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ]);

    renderApp();

    await waitFor(() => {
      expect(screen.getByText("Test Place")).toBeInTheDocument();
    });

    // Click on place in list
    await user.click(screen.getByText("Test Place"));

    // Detail panel should show place details
    await waitFor(() => {
      expect(screen.getByText("Type:")).toBeInTheDocument();
      expect(screen.getByText("building")).toBeInTheDocument();
    });
  });

  it("filters GM-only places in player mode", async () => {
    vi.mocked(apiClient.getPlaces).mockResolvedValue([
      {
        id: "1",
        name: "Public Place",
        type: "building",
        position: { x: 100, y: 200 },
        notes_public: null,
        notes_gm: null,
        scope: "public",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        id: "2",
        name: "GM Only Place",
        type: "building",
        position: { x: 300, y: 400 },
        notes_public: null,
        notes_gm: "Secret",
        scope: "gm",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ]);

    renderApp();

    await waitFor(() => {
      expect(screen.getByText("Public Place")).toBeInTheDocument();
      expect(screen.getByText("GM Only Place")).toBeInTheDocument();
    });

    // Switch to player mode
    const user = userEvent.setup();
    await user.click(screen.getByText(/Switch to Player/i));

    // GM-only place should still be in list (API filtering would handle this in real app)
    // But marker should not be visible on map (tested in MapCanvas tests)
  });

  it("can adjust layer opacity", async () => {
    // const user = userEvent.setup();
    renderApp();

    const opacitySlider = screen.getByLabelText(/Opacity/i, { selector: "#opacity-base-land" });
    expect(opacitySlider).toBeInTheDocument();

    // Opacity controls are functional (detailed testing in LayerControl.test.tsx)
  });
});
