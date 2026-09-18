---
id: doc_porto_design_system_figma_import_md
type: document
---

# Import

Native Figma build and import order Destination Create a private project named Porto Design System. Create three files: Porto DS Library, Porto DS Templates, Porto DS Examples. Publish the library only within the confirmed private team. Build order 1. Import tokens/porto.tokens.json into native Figma Variables. Create collections Primitive, Semantic, Mode and Typography. Confirm aliases resolve in Dark, Editorial.

## Connected knowledge

No outgoing links.

## Source content

# Native Figma build and import order

## Destination

Create a private project named `Porto Design System`. Create three files: `Porto DS Library`, `Porto DS Templates`, `Porto DS Examples`. Publish the library only within the confirmed private team.

## Build order

1. Import `tokens/porto.tokens.json` into native Figma Variables. Create collections `Primitive`, `Semantic`, `Mode` and `Typography`. Confirm aliases resolve in Dark, Editorial Light and Legal Plain.
2. Add local styles for text, colour, effect and grid. Do not create competing automatic sync. Figma is authoritative during editing; export changed tokens into the package at release time.
3. Add approved assets from `assets/approved/`, preserving their natural aspect ratios. Record each created asset or component node ID.
4. Build foundations and components from `specifications/`. Use main components, component sets, variants, Boolean properties, instance swaps and text properties defined there.
5. Build every frame inventory in `templates/`, then create complete examples from `examples/`.
6. Test linked instances, variable propagation, long text, resizes, data proportions, image aspect ratios, focus states and exports.
7. Save a named Figma version, export release evidence and complete `release-manifest.json`. A `.fig` backup is optional recovery only.

## Naming

`00 Start Here`, `01 Foundations`, `02 Identity`, `03 Illustration & Imagery`, `04 Core Components`, `05 Data Visualisation`, `06 Website`, `07 Presentations`, `08 Documents`, `09 Marketing`, `10 Voice & Content`, `11 Examples & Quality`, `12 Governance & Archive`.

Use slash namespaces, for example `Data/Allocation-donut`, `Deck/Problem`, `Web/Button`. Add description, source and usage warning to every main component. Tag system-defined website states as `System specified`.


