# README Refresh Design

**Date:** 2026-02-27
**Goal:** Update README to be more professional while keeping tongue-in-cheek humour, and elevate Rackula's positioning as a FOSS project.

## Design Decisions

### Audience

Both homelabbers and broader FOSS community equally. Project has expanded beyond homelab to AV techs, IT students, and others.

### Approach

Feature-forward structure (Approach A): professional layout with personality in the copy. Similar to Excalidraw, Hoppscotch, Immich.

### Key Changes from Current README

1. **Deployment details moved out:** All env vars, auth config, CORS settings removed from README. Link to Self-Hosting Guide instead.
2. **Feature showcase added:** Table with descriptions, followed by screenshot gallery.
3. **Use cases section added:** Explicit audience list (homelabbers, sysadmins, AV techs, IT students).
4. **Contributing & community section added.**
5. **"Built With Claude" moved up** after Contributing as a differentiator.
6. **Descriptive subtitle** replaces audience-heavy subtitle. Audiences covered in Who It's For section.

### Tone

Tim Robinson / Mitch Hedberg energy: deadpan, observational, dry. Professional structure, funny copy.

## Final Structure

1. **Logo + badges** (unchanged)
2. **Subtitle:** _Open-source drag-and-drop rack layout designer._
3. **Flavour line:** _Plan your racks before you wreck your back._
4. **Hero GIF** (unchanged)
5. **Try it now:** `count.racku.la` -- no signup, runs in your browser. Self-host it if you want, we're not your dad.
6. **Features** (table format)

| Feature                 | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| Drag & drop             | Toss devices into your rack. Move them around. Frown at the result. |
| Real device images      | Looks like your actual gear, not sad grey boxes                     |
| Multi-rack layouts      | Because one rack is never enough                                    |
| Server & AV racks       | Standard 19" and bayed racks -- homelabs, studios, touring rigs     |
| Export to PNG, PDF, SVG | For your documentation, your wall, or your therapist                |
| QR code sharing         | Your layout lives in a URL -- scan it and it just shows up          |
| 600+ real devices       | NetBox devicetype-library powered -- Dell, HP, Ubiquiti, and more   |
| Totally offline         | No cloud, no telemetry, no accounts. It's just files.               |

1. **See It In Action** (screenshot placeholders, captured during this PR)
   - Multi-rack layout
   - Device library
   - Export options
   - QR sharing

1. **Who It's For**
   - Homelabbers: plan before you buy, rearrange without lifting anything
   - Sysadmins & IT teams: document what's in the rack so the next person doesn't have to guess
   - AV techs & touring crews: map out bayed racks for studios and road cases
   - IT students: learn rack planning without a rack (or a budget)
   - Anyone with a rack: honestly, if you put things in a rack, this is for you

1. **Quick Start**
   - Use it now: count.racku.la
   - Self-host: link to Self-Hosting Guide
   - Build from source: clone + npm install + npm run build

1. **Documentation** (Architecture, Spec, Contributing links)
1. **Contributing** (link to CONTRIBUTING.md, good first issue link)
1. **Built With Claude** (existing paragraph, unchanged)
1. **Acknowledgements** (one-liner linking to ACKNOWLEDGEMENTS.md)
1. **Star History** (unchanged)
1. **Licence** (unchanged)

## Devil's Advocate Review (2 rounds)

### Round 1 Findings

- Tagline rhyme not descriptive for international users -> moved rhyme to flavour line, added descriptive subtitle
- Feature table has no visual weight -> kept table (professional, clean)
- Screenshot placeholders ship incomplete -> will capture during PR
- Documentation buried -> moved up before Contributing
- No plaintext-friendly opening -> descriptive subtitle works without images

### Round 2 Findings

- Subtitle too long with audience list -> shortened, audiences in Who It's For section
- Screenshots too late at position #9 -> moved up after Features table
- Built With Claude is a differentiator -> moved up after Contributing
- No "at a glance" stats -> badges are sufficient, don't over-sell

## Implementation Notes

- GitHub issue: #1353
- Work on branch `fix/1353-readme-refresh`
- Screenshot placeholders added as part of this PR
- All deployment config removed from README (already in Self-Hosting Guide)
