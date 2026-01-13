import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App", () => {
  it("renders the app", () => {
    render(<App />);
    expect(screen.getByText(/Blades Faction Map/i)).toBeInTheDocument();
  });

  it("renders initialization message", () => {
    render(<App />);
    expect(screen.getByText(/Frontend initialization complete/i)).toBeInTheDocument();
  });
});
