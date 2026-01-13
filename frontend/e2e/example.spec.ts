import { test, expect } from "@playwright/test";

test("has title", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Blades Faction Map/);
});

test("displays app heading", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Blades Faction Map/i })).toBeVisible();
});
