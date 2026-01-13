import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { Drawer, DrawerTabs, DrawerContent } from "./Drawer";

describe("Drawer component", () => {
  it("renders toggle button", () => {
    render(
      <Drawer isOpen={true} onToggle={vi.fn()}>
        <div>Content</div>
      </Drawer>
    );
    expect(screen.getByLabelText("Close drawer")).toBeInTheDocument();
  });

  it("calls onToggle when button is clicked", async () => {
    const user = userEvent.setup();
    const onToggle = vi.fn();
    render(
      <Drawer isOpen={true} onToggle={onToggle}>
        <div>Content</div>
      </Drawer>
    );

    await user.click(screen.getByLabelText("Close drawer"));
    expect(onToggle).toHaveBeenCalledTimes(1);
  });

  it("shows correct button label when closed", () => {
    render(
      <Drawer isOpen={false} onToggle={vi.fn()}>
        <div>Content</div>
      </Drawer>
    );
    expect(screen.getByLabelText("Open drawer")).toBeInTheDocument();
  });
});

describe("DrawerTabs component", () => {
  it("renders all tabs", () => {
    render(<DrawerTabs activeTab="places" onTabChange={vi.fn()} />);
    expect(screen.getByRole("tab", { name: "Люди" })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Места" })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Фракции" })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "События" })).toBeInTheDocument();
  });

  it("marks active tab as selected", () => {
    render(<DrawerTabs activeTab="places" onTabChange={vi.fn()} />);
    const placesTab = screen.getByRole("tab", { name: "Места" });
    expect(placesTab).toHaveAttribute("aria-selected", "true");
  });

  it("calls onTabChange when tab is clicked", async () => {
    const user = userEvent.setup();
    const onTabChange = vi.fn();
    render(<DrawerTabs activeTab="places" onTabChange={onTabChange} />);

    await user.click(screen.getByRole("tab", { name: "Люди" }));
    expect(onTabChange).toHaveBeenCalledWith("people");
  });
});

describe("DrawerContent component", () => {
  it("renders children", () => {
    render(
      <DrawerContent activeTab="places">
        <div>Test content</div>
      </DrawerContent>
    );
    expect(screen.getByText("Test content")).toBeInTheDocument();
  });

  it("has correct role and attributes", () => {
    render(
      <DrawerContent activeTab="places">
        <div>Test content</div>
      </DrawerContent>
    );
    const panel = screen.getByRole("tabpanel");
    expect(panel).toHaveAttribute("id", "places-panel");
    expect(panel).toHaveAttribute("aria-labelledby", "places-tab");
  });
});
