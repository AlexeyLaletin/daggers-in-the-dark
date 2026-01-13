import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import userEvent from "@testing-library/user-event";
import { AddPlaceForm } from "./AddPlaceForm";
import { ViewModeProvider } from "../contexts/ViewModeContext";
import { apiClient } from "../api/client";

vi.mock("../api/client", () => ({
  apiClient: {
    createPlace: vi.fn(),
  },
}));

describe("AddPlaceForm component", () => {
  const mockPosition = { x: 100, y: 200 };
  const mockOnSuccess = vi.fn();
  const mockOnCancel = vi.fn();

  const renderWithProvider = (ui: React.ReactElement) => {
    return render(<ViewModeProvider>{ui}</ViewModeProvider>);
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders form with all fields", () => {
    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Public Notes/i)).toBeInTheDocument();
  });

  it("displays position coordinates", () => {
    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText(/Position: \(100, 200\)/i)).toBeInTheDocument();
  });

  it("shows GM-only fields in GM mode", () => {
    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByLabelText(/GM Notes/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Public/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/GM Only/i)).toBeInTheDocument();
  });

  it("validates required name field", async () => {
    const user = userEvent.setup();
    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    await user.click(screen.getByText("Create Place"));

    expect(await screen.findByText("Name is required")).toBeInTheDocument();
    expect(mockOnSuccess).not.toHaveBeenCalled();
  });

  it("submits form with valid data", async () => {
    const user = userEvent.setup();
    vi.mocked(apiClient.createPlace).mockResolvedValue({
      id: "1",
      name: "Test Place",
      type: "building",
      position: mockPosition,
      notes_public: null,
      notes_gm: null,
      scope: "public",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });

    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    await user.type(screen.getByLabelText(/Name/i), "Test Place");
    await user.click(screen.getByText("Create Place"));

    await waitFor(() => {
      expect(apiClient.createPlace).toHaveBeenCalledWith({
        name: "Test Place",
        type: "building",
        position: mockPosition,
        scope: "public",
      });
      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  it("calls onCancel when cancel button is clicked", async () => {
    const user = userEvent.setup();
    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    await user.click(screen.getByText("Cancel"));
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it("handles API errors", async () => {
    const user = userEvent.setup();
    vi.mocked(apiClient.createPlace).mockRejectedValue(new Error("API Error"));

    renderWithProvider(
      <AddPlaceForm
        position={mockPosition}
        onSuccess={mockOnSuccess}
        onCancel={mockOnCancel}
      />
    );

    await user.type(screen.getByLabelText(/Name/i), "Test Place");
    await user.click(screen.getByText("Create Place"));

    expect(await screen.findByText("API Error")).toBeInTheDocument();
    expect(mockOnSuccess).not.toHaveBeenCalled();
  });
});
