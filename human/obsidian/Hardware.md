---
id: doc_porto_landing_src_pages_hardware_jsx
type: document
---

# Hardware

import React from 'react' import MonumentPage from '../components/MonumentPage' import Seo from '../components/Seo' import content from '../content/hardware.json' export default function Page() { return <MonumentPage content={content} / } export const Head = () = <Seo title={content.title} description={content.description} path={content.path} hero={false} /

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'
import MonumentPage from '../components/MonumentPage'
import Seo from '../components/Seo'
import content from '../content/hardware.json'
export default function Page() { return <MonumentPage content={content} /> }
export const Head = () => <Seo title={content.title} description={content.description} path={content.path} hero={false} />
