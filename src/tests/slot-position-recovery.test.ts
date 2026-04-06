import { describe, it, expect } from "vitest";
import { parseLayoutYaml } from "$lib/utils/yaml";

/**
 * Regression test for layouts saved without slot_position (broken between
 * dd25f4c and its fix). Two half-width devices at the same position with no
 * slot_position would crash on load with each_key_duplicate. The schema
 * transform should recover by assigning "left"/"right" automatically.
 */
describe("slot_position recovery on load", () => {
  it("assigns left/right to two half-width devices at the same position when slot_position is missing", async () => {
    // Simulate a YAML saved by the broken serializer: two mac minis at
    // position 198, same face, no slot_position AND no slot_width — exactly
    // what the broken serializer produced (both fields were stripped).
    const brokenYaml = `
version: 0.9.1
name: Test Layout
racks:
  - id: rack-1
    name: Test
    height: 42
    width: 19
    desc_units: false
    form_factor: 4-post-cabinet
    starting_unit: 1
    position: 0
    devices:
      - id: device-a
        device_type: apple-mac-mini
        position: 198
        face: front
      - id: device-b
        device_type: apple-mac-mini
        position: 198
        face: front
device_types:
  - slug: apple-mac-mini
    model: Mac Mini
    u_height: 1
    is_full_depth: false
    colour: "#4A7A8A"
    category: server
settings:
  display_mode: label
  show_labels_on_images: false
`;

    const layout = await parseLayoutYaml(brokenYaml);
    const devices = layout.racks[0]?.devices ?? [];

    expect(devices).toHaveLength(2);

    const slots = devices.map((d) => d.slot_position);
    // Both devices must have a slot_position assigned
    expect(slots).not.toContain(undefined);
    // One must be "left" and one must be "right"
    expect(slots).toContain("left");
    expect(slots).toContain("right");

    // slot_width must also be recovered on the device type so it renders correctly
    expect(layout.device_types[0]?.slot_width).toBe(1);
  });

  it("does not assign slot_position to a single half-width device that already has one", async () => {
    const yaml = `
version: 0.9.1
name: Test Layout
racks:
  - id: rack-1
    name: Test
    height: 42
    width: 19
    desc_units: false
    form_factor: 4-post-cabinet
    starting_unit: 1
    position: 0
    devices:
      - id: device-a
        device_type: apple-mac-mini
        position: 198
        face: front
        slot_position: left
device_types:
  - slug: apple-mac-mini
    model: Mac Mini
    u_height: 1
    slot_width: 1
    is_full_depth: false
    colour: "#4A7A8A"
    category: server
settings:
  display_mode: label
  show_labels_on_images: false
`;

    const layout = await parseLayoutYaml(yaml);
    const device = layout.racks[0]?.devices[0];

    // Existing slot_position must be preserved unchanged
    expect(device?.slot_position).toBe("left");
  });
});
