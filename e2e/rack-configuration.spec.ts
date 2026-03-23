import { test, expect } from "./helpers/base-test";
import type { Page } from "@playwright/test";
import { gotoWithRack, clickNewRack, locators } from "./helpers";

/**
 * Helper to open the New Rack wizard and advance past step 1 (name/type).
 * In multi-rack mode, clicking New Rack opens the wizard directly.
 * Fills name in step 1, clicks Next to reach step 2 (width + height).
 */
async function openWizardStep2(page: Page, name: string) {
  await clickNewRack(page);
  await expect(page.locator('[role="dialog"]')).toBeVisible();
  await page.fill("#rack-name", name);
  // Advance from step 1 (Name/Type) to step 2 (Width/Height)
  await page.click('[data-testid="btn-wizard-next"]');
}

test.describe("Rack Configuration", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRack(page);
  });

  test("can create 10-inch rack with narrower render", async ({ page }) => {
    await openWizardStep2(page, "Narrow Rack");

    // Step 2: Select 10" width using radio button, then height
    await page.click('[data-testid="radio-width-10"]');
    await page.click('[data-testid="btn-height-24"]');

    // Create rack
    await page.click('[data-testid="btn-wizard-next"]');

    // Rack should be visible (dual-view has 2 containers)
    await expect(page.locator(locators.rack.container).first()).toBeVisible();

    // The rack SVG should have a narrower viewBox for 10" rack
    const rackSvg = page.locator(locators.rack.svg).first();
    const viewBox = await rackSvg.getAttribute("viewBox");
    expect(viewBox).toBeDefined();

    if (viewBox) {
      const parts = viewBox.split(" ");
      const width = parseFloat(parts[2] || "0");
      // 10" rack should be narrower (roughly half of 19")
      expect(width).toBeLessThan(200);
    }
  });

  test("can create 19-inch rack with standard render", async ({ page }) => {
    await openWizardStep2(page, "Standard Rack");

    // Step 2: 19" is default, just select height
    await page.click('[data-testid="btn-height-42"]');

    // Create rack
    await page.click('[data-testid="btn-wizard-next"]');

    // Rack should be visible (dual-view has 2 containers)
    await expect(page.locator(locators.rack.container).first()).toBeVisible();

    const rackSvg = page.locator(locators.rack.svg).first();
    const viewBox = await rackSvg.getAttribute("viewBox");
    expect(viewBox).toBeDefined();

    if (viewBox) {
      const parts = viewBox.split(" ");
      const width = parseFloat(parts[2] || "0");
      // 19" rack should be standard width
      expect(width).toBeGreaterThan(200);
    }
  });

  // Descending units, custom starting unit, and form factor tests
  // are tracked by #1402. Stubs removed by #1226 triage.

  test("rack with ascending units shows U1 at bottom (default desc_units=false, starting_unit=1)", async ({
    page,
  }) => {
    await openWizardStep2(page, "Ascending Rack");

    // Step 2: Use custom height of 10U
    await page.click('[data-testid="btn-height-custom"]');
    await page.fill("#custom-height", "10");

    // Create rack
    await page.click('[data-testid="btn-wizard-next"]');

    // Rack should be visible (dual-view has 2 containers)
    await expect(page.locator(locators.rack.container).first()).toBeVisible();

    // In dual-view mode, each view has its own U labels - scope to first view
    const firstRackSvg = page.locator(locators.rack.svg).first();
    const uLabels = firstRackSvg.locator(locators.rack.uLabel);
    const count = await uLabels.count();
    expect(count).toBe(10);

    // First label (top) should be "10", last label (bottom) should be "1"
    const firstLabel = uLabels.first();
    const lastLabel = uLabels.last();
    await expect(firstLabel).toHaveText("10");
    await expect(lastLabel).toHaveText("1");
  });

});
