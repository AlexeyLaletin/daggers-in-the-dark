import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import userEvent from "@testing-library/user-event";
import { LayerControl } from "./LayerControl";
import { MapProvider } from "../contexts/MapContext";

describe("LayerControl component", () => {
  const renderWithProvider = (ui: React.ReactElement) => {
    return render(<MapProvider>{ui}</MapProvider>);
  };

  it("renders all layers", () => {
    renderWithProvider(<LayerControl />);
    expect(screen.getByLabelText("Land/Water")).toBeInTheDocument();
    expect(screen.getByLabelText("Territories")).toBeInTheDocument();
    expect(screen.getByLabelText("Markers")).toBeInTheDocument();
  });

  it("all layers are visible by default", () => {
    renderWithProvider(<LayerControl />);
    expect(screen.getByLabelText("Land/Water")).toBeChecked();
    expect(screen.getByLabelText("Territories")).toBeChecked();
    expect(screen.getByLabelText("Markers")).toBeChecked();
  });

  it("can toggle layer visibility", async () => {
    const user = userEvent.setup();
    renderWithProvider(<LayerControl />);

    const landWaterCheckbox = screen.getByLabelText("Land/Water");
    await user.click(landWaterCheckbox);

    expect(landWaterCheckbox).not.toBeChecked();
  });

  it("renders opacity sliders for all layers", () => {
    renderWithProvider(<LayerControl />);
    const sliders = screen.getAllByRole("slider");
    expect(sliders).toHaveLength(3);
  });

  it("can adjust layer opacity", async () => {
    const user = userEvent.setup();
    renderWithProvider(<LayerControl />);

    const slider = screen.getByLabelText(/Opacity/i, { selector: "#opacity-base-land" });
    await user.clear(slider);
    await user.type(slider, "0.5");

    // Verify the slider value changed (implementation detail)
    expect(slider).toHaveValue("0.5");
  });

  it("displays opacity percentage", () => {
    renderWithProvider(<LayerControl />);
    // Default opacity is 1.0 for base-land and markers, 0.6 for territories
    expect(screen.getByText("100%")).toBeInTheDocument();
    expect(screen.getByText("60%")).toBeInTheDocument();
  });
});
