---
id: doc_porto_landing_src_components_kilnpage_jsx
type: document
---

# Kilnpage

import React, { useEffect, useRef } from 'react' import { mountKiln } from '../lib/kiln-interactions' export default function KilnPage({ page, children }) { const root = useRef(null) useEffect(() = mountKiln(root.current), [page]) return <div ref={root} data-page={page}{children}</div }

## Connected knowledge

No outgoing links.

## Source content

import React, { useEffect, useRef } from 'react'
import { mountKiln } from '../lib/kiln-interactions'

export default function KilnPage({ page, children }) {
  const root = useRef(null)
  useEffect(() => mountKiln(root.current), [page])
  return <div ref={root} data-page={page}>{children}</div>
}
