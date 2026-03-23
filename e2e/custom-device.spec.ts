import { test, expect } from "./helpers/base-test";
import { gotoWithRack, dragDeviceToRack, locators } from "./helpers";

/**
 * E2E Tests for Custom Device Creation and Placement (Issue #166)
 * Tests that custom multi-U devices preserve their height after placement
 */

test.describe("Custom Device Height (Issue #166)", () => {
  test.beforeEach(async ({ page }) => {
    await gotoWithRack(page);
  });

  // TODO: Playwright fill() on number input doesn't trigger Svelte bind:value — needs dispatchEvent workaround
  test.skip("custom 4U device renders with correct height after placement", async ({
    page,
  }) => {
    // 1. Open Add Device form
    const addDeviceButton = page.locator('[data-testid="btn-create-custom-device"]');
    await addDeviceButton.click();

    // 2. Fill in custom device details — click height input first to ensure focus
    await page.fill("#device-name", "RACKOWL 4U Server");
    const heightInput = page.locator("#device-height");
    await heightInput.click();
    await heightInput.fill("4");
    await page.selectOption("#device-category", "server");

    // 3. Submit the form
    await page.click('[data-testid="btn-add-device"]');

    // 4. Verify custom device appears in palette
    const customDevice = page.locator(
      '.device-palette-item:has-text("RACKOWL 4U Server")',
    );
    await expect(customDevice).toBeVisible();

    // 5. Drag device to rack using shared helper (new device is last in list)
    const deviceCount = await page.locator(locators.device.paletteItem).count();
    await dragDeviceToRack(page, { deviceIndex: deviceCount - 1 });

    // 6. Verify device appears in rack
    const rackDevice = page.locator(locators.rack.device).first();
    await expect(rackDevice).toBeVisible({ timeout: 5000 });

    // 7. CRITICAL: Verify device has correct height (4U = 4 * 22px = 88px)
    const deviceRect = page.locator(locators.rack.deviceRect).first();
    const height = await deviceRect.getAttribute("height");

    // Verify multi-U device has proportionally larger height than 1U
    const heightVal = parseFloat(height || "0");
    // A 4U device should be roughly 4x the U_HEIGHT (22px each = 88px)
    // Use a range check since rendering may vary slightly
    expect(heightVal).toBeGreaterThan(60);
  });

  // TODO: Same fill() issue as above
  test.skip("custom 2U device blocks correct number of rack positions", async ({
    page,
  }) => {
    // 1. Open Add Device form
    const addDeviceButton = page.locator('[data-testid="btn-create-custom-device"]');
    await addDeviceButton.click();

    // 2. Create a custom 2U device — clear then type to ensure Svelte binding updates
    await page.fill("#device-name", "Test 2U Storage");
    const heightInput = page.locator("#device-height");
    await heightInput.click();
    await heightInput.fill("2");
    await page.selectOption("#device-category", "storage");

    // 3. Submit the form
    await page.click('[data-testid="btn-add-device"]');

    // 4. Drag device to rack (new device is last in list)
    const deviceCount = await page.locator(locators.device.paletteItem).count();
    await dragDeviceToRack(page, { deviceIndex: deviceCount - 1 });

    // 5. Verify device renders with 2U height
    const deviceRect = page.locator(locators.rack.deviceRect).first();
    const height = await deviceRect.getAttribute("height");

    // A 2U device should be roughly 2x the U_HEIGHT (22px each = 44px)
    const heightVal = parseFloat(height || "0");
    expect(heightVal).toBeGreaterThan(30);
  });
});
