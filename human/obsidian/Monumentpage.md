---
id: doc_porto_landing_src_components_monumentpage_jsx
type: document
---

# Monumentpage

import React, { useEffect, useRef } from 'react' import { teamSection } from '../content/co-founders' import { withFinishViewer } from '../content/finish-viewer.mjs' import { mountMonument } from '../lib/monument.mjs' // Trusted, versioned editorial markup. Never insert visitor-supplied HTML here. export default function MonumentPage({ content }) { const root = useRef(null) useEffect(() =.

## Connected knowledge

No outgoing links.

## Source content

import React, { useEffect, useRef } from 'react'
import { teamSection } from '../content/co-founders'
import { withFinishViewer } from '../content/finish-viewer.mjs'
import { mountMonument } from '../lib/monument.mjs'

// Trusted, versioned editorial markup. Never insert visitor-supplied HTML here.
export default function MonumentPage({ content }) {
  const root = useRef(null)
  useEffect(() => mountMonument(root.current), [content])
  const html = withFinishViewer(content.body, content.path).replace('<!-- team section -->', teamSection)
  return <div ref={root} dangerouslySetInnerHTML={{ __html: html }} />
}
