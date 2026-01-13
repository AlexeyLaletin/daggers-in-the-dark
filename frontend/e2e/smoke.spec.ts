import { test, expect } from "@playwright/test";

test.describe("Smoke tests", () => {
  test("app loads successfully", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/Blades Faction Map/);
    await expect(page.getByRole("heading", { name: /Blades Faction Map/i })).toBeVisible();
  });

  test("will test faction creation workflow when implemented", async ({ page }) => {
    // TODO: implement after factions CRUD is working
    // await page.goto("/");
    // await page.click("button:has-text('New Faction')");
    // await page.fill('input[name="name"]', "Test Faction");
    // await page.fill('input[name="color"]', "#FF0000");
    // await page.click("button:has-text('Save')");
    // await expect(page.getByText("Test Faction")).toBeVisible();
  });

  test("will test territory painting when implemented", async ({ page }) => {
    // TODO: implement after Canvas and tiles API are working
  });

  test("will test GM/Player mode switch when implemented", async ({ page }) => {
    // TODO: implement after mode toggle is working
  });

  test("will test snapshot creation when implemented", async ({ page }) => {
    // TODO: implement after snapshots API is working
  });
});
