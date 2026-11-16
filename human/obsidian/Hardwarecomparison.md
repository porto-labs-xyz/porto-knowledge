---
id: doc_porto_landing_src_components_hardwarecomparison_jsx
type: document
---

# Hardwarecomparison

import React from 'react' export default function HardwareComparison() { return ( <dialog id="specs-dialog" className="comparison-sheet" aria-labelledby="specs-title" <div className="comparison-toolbar"<spanHardware / Compare</span<button className="dialog-close" aria-label="Close specifications"×</button</div <div className="comparison-scroll" <header className="comparison-intro"<h2 id="specs-title"Find your.

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'

export default function HardwareComparison() {
  return (
<dialog id="specs-dialog" className="comparison-sheet" aria-labelledby="specs-title">
<div className="comparison-toolbar"><span>Hardware / Compare</span><button className="dialog-close" aria-label="Close specifications">×</button></div>
<div className="comparison-scroll">
<header className="comparison-intro"><h2 id="specs-title">Find your fit.</h2><p>Proposed configurations. In development.</p></header>
<table className="comparison-table" role="table" aria-label="Kiln One and Kiln Atelier proposed configurations">
<thead role="rowgroup"><tr role="row"><th className="comparison-label" scope="col" role="columnheader">At a glance</th><th id="compare-one" scope="col" role="columnheader" className="compare-product compare-one"><span className="compare-name">Kiln One</span><span className="compare-purpose">Your studio’s starting point</span><strong>£17,000</strong><span className="compare-price-note">Target hardware price</span></th><th id="compare-atelier" scope="col" role="columnheader" className="compare-product compare-atelier"><span className="compare-name">Kiln Atelier</span><span className="compare-purpose">Room for heavier workloads</span><strong>Let’s talk</strong><span className="compare-price-note">Pricing to be confirmed</span></th></tr></thead>
<tbody role="rowgroup">
<tr className="compare-renders" role="row"><th id="spec-inside" scope="row" role="rowheader">Inside the hardware</th><td headers="compare-one spec-inside" role="cell"><figure><div className="compare-render compare-render-one"><img src="/assets/kiln/one-interior-led.webp" alt="Kiln One uncovered, showing two graphics cards, CPU cooling and power supply" width="1254" height="1254" loading="lazy" decoding="async" /></div><figcaption>Two-GPU concept shown</figcaption></figure></td><td headers="compare-atelier spec-inside" role="cell"><figure><div className="compare-render compare-render-atelier"><img src="/assets/kiln/atelier-interior-led.webp" alt="Kiln Atelier uncovered, showing four graphics cards, motherboard, cooling and power supply" width="1536" height="1024" loading="lazy" decoding="async" /></div><figcaption>Four-GPU concept shown</figcaption></figure></td></tr>
<tr role="row"><th id="spec-gpu" scope="row" role="rowheader">Graphics</th><td headers="compare-one spec-gpu" role="cell"><strong>RTX PRO 5000</strong></td><td headers="compare-atelier spec-gpu" role="cell"><strong>RTX PRO 6000</strong><span className="compare-note">Max-Q</span></td></tr>
<tr role="row"><th id="spec-vram" scope="row" role="rowheader">Memory per GPU</th><td headers="compare-one spec-vram" role="cell"><strong className="compare-number">72 <small>GB</small></strong></td><td headers="compare-atelier spec-vram" role="cell"><strong className="compare-number">96 <small>GB</small></strong></td></tr>
<tr role="row"><th id="spec-count" scope="row" role="rowheader">GPU capacity</th><td headers="compare-one spec-count" role="cell"><strong>1 GPU</strong><span className="compare-note">Up to 2 GPUs</span></td><td headers="compare-atelier spec-count" role="cell"><strong>2 GPUs</strong><span className="compare-note">Up to 4 GPUs</span></td></tr>
<tr role="row"><th id="spec-ram" scope="row" role="rowheader">System memory</th><td headers="compare-one spec-ram" role="cell"><strong className="compare-number">128 <small>GB</small></strong></td><td headers="compare-atelier spec-ram" role="cell"><strong className="compare-number">512 <small>GB</small></strong><span className="compare-note">ECC memory</span></td></tr>
<tr role="row"><th id="spec-storage" scope="row" role="rowheader">Storage</th><td headers="compare-one spec-storage" role="cell"><strong className="compare-number">4 <small>TB</small></strong></td><td headers="compare-atelier spec-storage" role="cell"><strong className="compare-number">8 <small>TB</small></strong></td></tr>
<tr role="row"><th id="spec-size" scope="row" role="rowheader">Dimensions <span className="compare-note">Width × height × depth</span></th><td headers="compare-one spec-size" role="cell"><strong>250 × 450 × 460</strong><span className="compare-note">mm</span></td><td headers="compare-atelier spec-size" role="cell"><strong>520 × 220 × 600</strong><span className="compare-note">mm</span></td></tr>
</tbody></table>
<section className="comparison-shared" aria-labelledby="shared-title"><span className="eyebrow">Built into both</span><h3 id="shared-title">Same foundations.</h3><dl><div><dt>Enclosure</dt><dd>Satin aluminium, coloured front grille and one tilted-square light.</dd></div><div><dt>Studio connection</dt><dd>Ethernet. Kiln app for Mac and Windows, with an authenticated browser fallback.</dd></div></dl></section>
<details className="comparison-notes"><summary>Development notes <span aria-hidden="true">+</span></summary><p>These are current targets, subject to engineering validation. Performance, thermals and enclosure fit are still being qualified. Renders illustrate component layout, not a final build.</p><p>GPU memory is per card; multiple GPUs do not automatically form one memory pool. Dimensions are preliminary exterior targets. The proposed four-unit Atelier rack is 560 × 1100 × 680 mm.</p><p>£17,000 is a target hardware price, not an order price or binding quote. Final configuration, software, support, taxes and delivery terms are still to be confirmed.</p></details>
<details className="comparison-notes"><summary>For managed studios <span aria-hidden="true">+</span></summary><p>Company sign-in, security-key policies, project permissions, approved models and controlled external connections are development requirements. Provider compatibility and enforcement will be qualified during pilots.</p></details>
<div className="comparison-end"><button className="button button-ink dialog-done">Back to the hardware <span className="action-square" aria-hidden="true"></span></button></div>
</div></dialog>
  )
}
