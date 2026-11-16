---
id: doc_porto_landing_src_pages_index_jsx
type: document
---

# Porto Landing Page

import '../styles/hardware-reveal.css' import React from 'react' import MonumentPage from '../components/MonumentPage' import Seo from '../components/Seo' import content from '../content/index.json' export default function Page() { return <MonumentPage content={content} / } export const Head = () = <Seo title={content.title} description={content.description} path={content.path} hero={true} /

## Connected knowledge

No outgoing links.

## Source content

import '../styles/hardware-reveal.css'
import React from 'react'
import MonumentPage from '../components/MonumentPage'
import Seo from '../components/Seo'
import content from '../content/index.json'
export default function Page() { return <MonumentPage content={content} /> }
export const Head = () => <Seo title={content.title} description={content.description} path={content.path} hero={true} />
