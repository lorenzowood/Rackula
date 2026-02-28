<p align="center">
  <a href="https://count.racku.la">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/Rackula-lockup-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="assets/Rackula-lockup-light.svg">
      <img src="assets/Rackula-lockup-dark.svg" alt="Rackula" width="420">
    </picture>
  </a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-bd93f9?style=for-the-badge&labelColor=44475a" alt="License: MIT"></a>
  <img src="https://img.shields.io/github/v/release/RackulaLives/Rackula?style=for-the-badge&labelColor=44475a&color=ff79c6" alt="GitHub Release">
  <a href="https://github.com/RackulaLives/Rackula/pkgs/container/Rackula"><img src="https://img.shields.io/github/v/release/RackulaLives/Rackula?style=for-the-badge&labelColor=44475a&color=50fa7b&label=docker&logo=docker&logoColor=white" alt="Docker"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FRackulaLives%2FRackula%2Freport%2Fbadges%2Fdocs%2Fbadges%2Fcoverage.json&style=for-the-badge&labelColor=44475a" alt="Coverage">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FRackulaLives%2FRackula%2Freport%2Fbadges%2Fdocs%2Fbadges%2Fratio.json&style=for-the-badge&labelColor=44475a" alt="Code to Test Ratio">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FRackulaLives%2FRackula%2Freport%2Fbadges%2Fdocs%2Fbadges%2Ftime.json&style=for-the-badge&labelColor=44475a" alt="Test Time">
</p>

<p align="center">
  <strong>Open-source drag-and-drop rack layout designer.</strong><br>
  <em>Plan your racks before you wreck your back.</em>
</p>

<p align="center">
  <img src="assets/Rackula-hero-drac.gif" alt="Rackula demo" width="500">
</p>

<p align="center">
  <a href="https://count.racku.la"><strong>count.racku.la</strong></a> — no signup, runs in your browser. Self-host it if you want, we're not your dad.
</p>

---

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

## Who It's For

- **Homelabbers:** plan before you buy, rearrange without lifting anything
- **Sysadmins & IT teams:** document what's in the rack so the next person doesn't have to guess
- **AV techs & touring crews:** map out bayed racks for studios and road cases
- **IT students:** learn rack planning without a rack (or a budget)
- **Anyone with a rack:** honestly, if you put things in a rack, this is for you

## Quick Start

**Use it now:** [count.racku.la](https://count.racku.la)

**Self-host it:** See the [Self-Hosting Guide](docs/guides/SELF-HOSTING.md) for Docker, Compose, persistent storage, and auth setup.

**Build from source:**

```bash
git clone https://github.com/RackulaLives/Rackula.git
cd Rackula && npm install && npm run build
```

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Technical Specification](docs/reference/SPEC.md)
- [Self-Hosting Guide](docs/guides/SELF-HOSTING.md)

## Contributing

Rackula is open source and contributions are welcome. Check out the [Contributing Guide](CONTRIBUTING.md) to get started.

Not sure where to start? Look for issues labelled [`good first issue`](https://github.com/RackulaLives/Rackula/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

## Built With Claude

This project was built using AI-assisted development with Claude. I told it what to build and then said "no, not like that" a lot. The AI did a lot of typing. Commits with substantial AI contributions are marked with `Co-authored-by` tags because we're not going to pretend otherwise.

## Acknowledgements

Built on [Dracula Theme](https://draculatheme.com/) colours, [NetBox devicetype-library](https://github.com/netbox-community/devicetype-library) device data, and a lot of open source. See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for full credits.

## Star History

<a href="https://star-history.com/#RackulaLives/Rackula&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=RackulaLives/Rackula&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=RackulaLives/Rackula&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=RackulaLives/Rackula&type=Date" />
  </picture>
</a>

## Licence

[MIT](LICENSE) - Copyright (c) 2025 Gareth Evans
