---
id: doc_porto_design_system_specifications_components_md
type: document
---

# Components

Components Implement each line as a Figma main component, using semantic variants, Auto Layout and properties named exactly as shown. Family Component and variants Properties / behaviour --- --- --- Typography Type/Heading, Type/Eyebrow, Type/Body, Type/Citation Mode, level, emphasis; text property; body grows vertically. Navigation Web/Nav, Web/Nav-link, Web/Button Desktop/mobile, active, hover, focus, pressed,.

## Connected knowledge

No outgoing links.

## Source content

# Components

Implement each line as a Figma main component, using semantic variants, Auto Layout and properties named exactly as shown.

| Family | Component and variants | Properties / behaviour |
| --- | --- | --- |
| Typography | `Type/Heading`, `Type/Eyebrow`, `Type/Body`, `Type/Citation` | Mode, level, emphasis; text property; body grows vertically. |
| Navigation | `Web/Nav`, `Web/Nav-link`, `Web/Button` | Desktop/mobile, active, hover, focus, pressed, disabled; icon boolean; button label text. |
| Content | `Content/Stat`, `Content/Quote`, `Content/Callout`, `Content/Evidence`, `Content/List`, `Content/Citation` | Tone: open/glass; source and footnote text properties; citation always visible in export. |
| Shell | `Surface/Card`, `Surface/Glass`, `Layout/Section-divider`, `Layout/Header`, `Layout/Footer`, `Layout/Folio` | Mode and density variants; min-height only, no fixed text height. |
| People | `Content/Biography`, `Content/Contact`, `Content/Partner-strip` | Portrait instance swap; bio and role text; restricted/private badge optional. |
| Forms | `Web/Field`, `Web/Waitlist-form`, `Web/Accordion` | Empty/focus/error/success/disabled; error copy must be text, not colour only. |
| Calls to action | `Content/CTA`, `Web/Text-link` | Primary/secondary; hover and focus defined; external-link icon boolean. |

Website patterns reproduce existing landing patterns only: sticky navigation, hero, button, waitlist form, feature section, statistic, accordion, biographies, partner row and footer. Anything not observed in the website is marked `System specified` in its component description.

## Text rules

Never outline body text. Minimum 11 pt deck captions, 12 px web labels, 8 pt print footnotes. Long names and headline stress tests must use a realistic 90-character heading and a three-line label before release. Citation and footnote components pin to the bottom of their parent using Auto Layout spacer, not absolute positioning.


