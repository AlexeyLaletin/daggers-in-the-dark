import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import userEvent from "@testing-library/user-event";
import { MapToolbar } from "./MapToolbar";
import { MapProvider } from "../contexts/MapContext";

describe("MapToolbar component", () => {
  const renderWithProvider = (ui: React.ReactElement) => {
    return render(<MapProvider>{ui}</MapProvider>);
  };

  it("renders pan and add POI buttons", () => {
    renderWithProvider(<MapToolbar />);
    expect(screen.getByLabelText("Pan mode")).toBeInTheDocument();
    expect(screen.getByLabelText("Add POI mode")).toBeInTheDocument();
  });

  it("pan mode is active by default", () => {
    renderWithProvider(<MapToolbar />);
    const panButton = screen.getByLabelText("Pan mode");
    expect(panButton).toHaveAttribute("aria-pressed", "true");
  });

  it("switches to add POI mode when clicked", async () => {
    const user = userEvent.setup();
    renderWithProvider(<MapToolbar />);

    const addPoiButton = screen.getByLabelText("Add POI mode");
    await user.click(addPoiButton);

    expect(addPoiButton).toHaveAttribute("aria-pressed", "true");
  });

  it("switches back to pan mode when clicked", async () => {
    const user = userEvent.setup();
    renderWithProvider(<MapToolbar />);

    // Switch to add POI
    await user.click(screen.getByLabelText("Add POI mode"));
    // Switch back to pan
    await user.click(screen.getByLabelText("Pan mode"));

    expect(screen.getByLabelText("Pan mode")).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByLabelText("Add POI mode")).toHaveAttribute("aria-pressed", "false");
  });
});
