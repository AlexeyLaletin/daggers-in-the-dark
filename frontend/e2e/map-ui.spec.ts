import { test, expect } from "@playwright/test";

test.describe("Map UI E2E Tests", () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses
    await page.route("**/api/factions", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          {
            id: "1",
            name: "The Crows",
            color: "#1976d2",
            opacity: 0.6,
            notes_public: "A criminal gang",
            notes_gm: null,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        ]),
      });
    });

    await page.route("**/api/places", async (route) => {
      if (route.request().method() === "GET") {
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify([
            {
              id: "1",
              name: "The Leaky Bucket",
              type: "building",
              position: { x: 500, y: 400 },
              notes_public: "A tavern",
              notes_gm: "Secret entrance to sewers",
              scope: "public",
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            },
          ]),
        });
      } else if (route.request().method() === "POST") {
        const postData = route.request().postDataJSON();
        await route.fulfill({
          status: 201,
          contentType: "application/json",
          body: JSON.stringify({
            id: "2",
            ...postData,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          }),
        });
      }
    });

    await page.goto("/");
  });

  test("displays main layout elements", async ({ page }) => {
    // Check for main UI elements
    await expect(page.getByText("Blades")).toBeVisible();
    await expect(page.getByRole("tab", { name: "Места" })).toBeVisible();
    await expect(page.getByRole("tab", { name: "Фракции" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Pan mode" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Add POI mode" })).toBeVisible();
  });

  test("can toggle drawer", async ({ page }) => {
    // Drawer should be open by default
    await expect(page.getByRole("button", { name: "Close drawer" })).toBeVisible();

    // Close drawer
    await page.getByRole("button", { name: "Close drawer" }).click();
    await expect(page.getByRole("button", { name: "Open drawer" })).toBeVisible();

    // Open drawer again
    await page.getByRole("button", { name: "Open drawer" }).click();
    await expect(page.getByRole("button", { name: "Close drawer" })).toBeVisible();
  });

  test("can switch between tabs", async ({ page }) => {
    // Start on Places tab
    await expect(page.getByRole("tab", { name: "Места", selected: true })).toBeVisible();

    // Switch to Factions tab
    await page.getByRole("tab", { name: "Фракции" }).click();
    await expect(page.getByRole("tab", { name: "Фракции", selected: true })).toBeVisible();
    await expect(page.getByText("The Crows")).toBeVisible();

    // Switch to People tab
    await page.getByRole("tab", { name: "Люди" }).click();
    await expect(page.getByRole("tab", { name: "Люди", selected: true })).toBeVisible();
    await expect(page.getByText("Coming soon: People management")).toBeVisible();

    // Switch to Events tab
    await page.getByRole("tab", { name: "События" }).click();
    await expect(page.getByRole("tab", { name: "События", selected: true })).toBeVisible();
    await expect(page.getByText("Coming soon: Event timeline")).toBeVisible();
  });

  test("displays places in list", async ({ page }) => {
    await expect(page.getByText("The Leaky Bucket")).toBeVisible();
  });

  test("can select a place and view details", async ({ page }) => {
    // Click on place in list
    await page.getByText("The Leaky Bucket").click();

    // Detail panel should show place information
    await expect(page.getByText("Type:")).toBeVisible();
    await expect(page.getByText("building")).toBeVisible();
    await expect(page.getByText("Public Notes")).toBeVisible();
    await expect(page.getByText("A tavern")).toBeVisible();

    // GM notes should be visible in GM mode
    await expect(page.getByText("GM Notes")).toBeVisible();
    await expect(page.getByText("Secret entrance to sewers")).toBeVisible();
  });

  test("can switch map modes", async ({ page }) => {
    // Pan mode is active by default
    await expect(page.getByRole("button", { name: "Pan mode", pressed: true })).toBeVisible();

    // Switch to Add POI mode
    await page.getByRole("button", { name: "Add POI mode" }).click();
    await expect(page.getByRole("button", { name: "Add POI mode", pressed: true })).toBeVisible();
    await expect(page.getByRole("button", { name: "Pan mode", pressed: false })).toBeVisible();

    // Switch back to Pan mode
    await page.getByRole("button", { name: "Pan mode" }).click();
    await expect(page.getByRole("button", { name: "Pan mode", pressed: true })).toBeVisible();
  });

  test("can adjust layer opacity", async ({ page }) => {
    // Find opacity slider for base layer
    const opacitySlider = page.locator("#opacity-base-land");
    await expect(opacitySlider).toBeVisible();

    // Check initial value (should be 1.0 = 100%)
    await expect(page.getByText("100%")).toBeVisible();

    // Adjust opacity
    await opacitySlider.fill("0.5");
    await expect(page.getByText("50%")).toBeVisible();
  });

  test("can toggle layer visibility", async ({ page }) => {
    // Find layer checkbox
    const landWaterCheckbox = page.getByLabel("Land/Water");
    await expect(landWaterCheckbox).toBeChecked();

    // Toggle off
    await landWaterCheckbox.click();
    await expect(landWaterCheckbox).not.toBeChecked();

    // Toggle back on
    await landWaterCheckbox.click();
    await expect(landWaterCheckbox).toBeChecked();
  });

  test("switches between GM and Player modes", async ({ page }) => {
    // Should start in GM mode
    await expect(page.getByText("🎭 GM Mode")).toBeVisible();

    // Switch to Player mode
    await page.getByRole("button", { name: "Switch to Player" }).click();
    await expect(page.getByText("👥 Player Mode")).toBeVisible();

    // Switch back to GM mode
    await page.getByRole("button", { name: "Switch to GM" }).click();
    await expect(page.getByText("🎭 GM Mode")).toBeVisible();
  });

  test("GM notes are hidden in player mode", async ({ page }) => {
    // Select a place
    await page.getByText("The Leaky Bucket").click();

    // GM notes should be visible in GM mode
    await expect(page.getByText("GM Notes")).toBeVisible();
    await expect(page.getByText("Secret entrance to sewers")).toBeVisible();

    // Switch to Player mode
    await page.getByRole("button", { name: "Switch to Player" }).click();

    // GM notes should be hidden
    await expect(page.getByText("GM Notes")).not.toBeVisible();
    await expect(page.getByText("Secret entrance to sewers")).not.toBeVisible();

    // Public notes should still be visible
    await expect(page.getByText("Public Notes")).toBeVisible();
    await expect(page.getByText("A tavern")).toBeVisible();
  });

  test("displays place markers on map", async ({ page }) => {
    // Check for place marker button
    const marker = page.getByRole("button", { name: "Place: The Leaky Bucket" });
    await expect(marker).toBeVisible();
  });

  test("can click marker to select place", async ({ page }) => {
    // Click on map marker
    await page.getByRole("button", { name: "Place: The Leaky Bucket" }).click();

    // Detail panel should show place details
    await expect(page.getByText("Type:")).toBeVisible();
    await expect(page.getByText("building")).toBeVisible();
  });
});
