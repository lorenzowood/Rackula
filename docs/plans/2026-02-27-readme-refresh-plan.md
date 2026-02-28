# README Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite README.md to match the approved design in `docs/plans/2026-02-27-readme-refresh-design.md`

**Architecture:** Single-file rewrite of README.md plus creation of `assets/screenshots/` directory with placeholder images. No code changes, no tests.

**Tech Stack:** Markdown, GitHub-flavoured HTML for centred elements

---

### Task 1: Add light-mode logo to header

The current README only shows the dark-mode logo. The light-mode variant exists at `assets/Rackula-lockup-light.svg` but isn't used.

**Files:**

- Modify: `README.md:1-5`

**Step 1: Update the logo block to show both variants**

Replace the existing logo `<p>` block with:

```html
<p align="center">
  <a href="https://count.racku.la">
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcset="assets/Rackula-lockup-dark.svg"
      />
      <source
        media="(prefers-color-scheme: light)"
        srcset="assets/Rackula-lockup-light.svg"
      />
      <img src="assets/Rackula-lockup-dark.svg" alt="Rackula" width="420" />
    </picture>
  </a>
</p>
```

Also update the link from `https://app.racku.la` to `https://count.racku.la` (the actual production URL).

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add light-mode logo and fix production URL (#1353)"
```

---

### Task 2: Replace tagline, subtitle, and hero section

**Files:**

- Modify: `README.md:19-27`

**Step 1: Replace the tagline and hero block**

Replace the current `<strong>Drag and drop rack visualizer</strong>` block and everything through the `---` with:

```html
<p align="center">
  <strong>Open-source drag-and-drop rack layout designer.</strong><br />
  <em>Plan your racks before you wreck your back.</em>
</p>

<p align="center">
  <img src="assets/Rackula-hero-drac.gif" alt="Rackula demo" width="500" />
</p>

<p align="center">
  <a href="https://count.racku.la"><strong>count.racku.la</strong></a> — no
  signup, runs in your browser. Self-host it if you want, we're not your dad.
</p>

---
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update tagline and add try-it-now line (#1353)"
```

---

### Task 3: Replace body sections (Features through Licence)

This is the main rewrite. Replace everything from `## What _Is_ This` through the end of the file.

**Files:**

- Modify: `README.md:29-169`

**Step 1: Replace all body content**

Delete lines 29-169 and replace with the following sections in order:

**Features table:**

```markdown
## Features

| Feature                     | Description                                                         |
| --------------------------- | ------------------------------------------------------------------- |
| **Drag & drop**             | Toss devices into your rack. Move them around. Frown at the result. |
| **Real device images**      | Looks like your actual gear, not sad grey boxes                     |
| **Multi-rack layouts**      | Because one rack is never enough                                    |
| **Server & AV racks**       | Standard 19" and bayed racks — homelabs, studios, touring rigs      |
| **Export to PNG, PDF, SVG** | For your documentation, your wall, or your therapist                |
| **QR code sharing**         | Your layout lives in a URL — scan it and it just shows up           |
| **600+ real devices**       | NetBox devicetype-library powered — Dell, HP, Ubiquiti, and more    |
| **Totally offline**         | No cloud, no telemetry, no accounts. It's just files.               |
```

**See It In Action (screenshot placeholders):**

```markdown
## See It In Action

<!-- TODO: Capture and add screenshots for multi-rack, device library, export, QR sharing -->

|                                                         |                                                          |
| ------------------------------------------------------- | -------------------------------------------------------- |
| ![Multi-rack layout](assets/screenshots/multi-rack.png) | ![Device library](assets/screenshots/device-library.png) |
| _Multi-rack layouts_                                    | _600+ real devices_                                      |
| ![Export options](assets/screenshots/export.png)        | ![QR sharing](assets/screenshots/qr-share.png)           |
| _Export to PNG, PDF, SVG_                               | _QR code sharing_                                        |
```

**Who It's For:**

```markdown
## Who It's For

- **Homelabbers:** plan before you buy, rearrange without lifting anything
- **Sysadmins & IT teams:** document what's in the rack so the next person doesn't have to guess
- **AV techs & touring crews:** map out bayed racks for studios and road cases
- **IT students:** learn rack planning without a rack (or a budget)
- **Anyone with a rack:** honestly, if you put things in a rack, this is for you
```

**Quick Start:**

````markdown
## Quick Start

**Use it now:** [count.racku.la](https://count.racku.la)

**Self-host it:** See the [Self-Hosting Guide](docs/guides/SELF-HOSTING.md) for Docker, Compose, persistent storage, and auth setup.

**Build from source:**

```bash
git clone https://github.com/RackulaLives/Rackula.git
cd Rackula && npm install && npm run build
```
````

````

**Documentation:**

```markdown
## Documentation

- [Architecture Overview](docs/reference/ARCHITECTURE.md)
- [Technical Specification](docs/reference/SPEC.md)
- [Self-Hosting Guide](docs/guides/SELF-HOSTING.md)
````

**Contributing:**

```markdown
## Contributing

Rackula is open source and contributions are welcome. Check out the [Contributing Guide](CONTRIBUTING.md) to get started.

Not sure where to start? Look for issues labelled [`good first issue`](https://github.com/RackulaLives/Rackula/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
```

**Built With Claude:**

```markdown
## Built With Claude

This project was built using AI-assisted development with Claude. I told it what to build and then said "no, not like that" a lot. The AI did a lot of typing. Commits with substantial AI contributions are marked with `Co-authored-by` tags because we're not going to pretend otherwise.
```

**Acknowledgements:**

```markdown
## Acknowledgements

Built on [Dracula Theme](https://draculatheme.com/) colours, [NetBox devicetype-library](https://github.com/netbox-community/devicetype-library) device data, and a lot of open source. See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for full credits.
```

**Star History (unchanged):**

```markdown
## Star History

<a href="https://star-history.com/#RackulaLives/Rackula&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=RackulaLives/Rackula&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=RackulaLives/Rackula&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=RackulaLives/Rackula&type=Date" />
  </picture>
</a>
```

**Licence (unchanged):**

```markdown
## Licence

[MIT](LICENSE) - Copyright (c) 2025 Gareth Evans
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README with feature-forward structure (#1353)"
```

---

### Task 4: Create screenshots directory with placeholder files

**Files:**

- Create: `assets/screenshots/.gitkeep`

**Step 1: Create the directory**

```bash
mkdir -p assets/screenshots
touch assets/screenshots/.gitkeep
```

**Step 2: Commit**

```bash
git add assets/screenshots/.gitkeep
git commit -m "docs: add screenshots directory for README gallery (#1353)"
```

---

### Task 5: Capture screenshots and add to gallery

This task is manual — requires running the app and taking screenshots.

**Step 1: Start the dev server**

```bash
npm run dev
```

**Step 2: Capture 4 screenshots**

Using the browser at `localhost:5173`:

1. **Multi-rack layout** (`assets/screenshots/multi-rack.png`): Create a layout with 2+ racks, populate with devices
2. **Device library** (`assets/screenshots/device-library.png`): Show the device browser/search panel
3. **Export options** (`assets/screenshots/export.png`): Show the export dialog with format options
4. **QR sharing** (`assets/screenshots/qr-share.png`): Show a QR code share dialog

Crop to consistent dimensions, dark theme preferred (matches Dracula branding).

**Step 3: Remove .gitkeep, add screenshots**

```bash
rm assets/screenshots/.gitkeep
git add assets/screenshots/
git commit -m "docs: add README gallery screenshots (#1353)"
```

---

### Task 6: Final review and PR

**Step 1: Review the full README**

Read `README.md` top to bottom. Check:

- All links resolve (docs, hosted app, GitHub issues)
- Badge URLs unchanged
- No broken image references
- Tone is consistent throughout

**Step 2: Push and create PR**

```bash
git push -u origin fix/1353-readme-refresh
gh pr create --title "docs: refresh README for FOSS professionalism (#1353)" \
  --body "$(cat <<'EOF'
## Summary

- Rewrites README with feature-forward structure
- Adds feature table, use case section, screenshot gallery
- Moves deployment config to Self-Hosting Guide (link only)
- Adds light-mode logo support
- Moves "Built With Claude" and "Contributing" sections up
- Adds screenshot placeholders (or actual screenshots)

Closes #1353

## Test plan

- [ ] Verify all links resolve on GitHub preview
- [ ] Verify both logo variants render in light/dark mode
- [ ] Verify badges still display correctly
- [ ] Check mobile rendering of feature table

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```
