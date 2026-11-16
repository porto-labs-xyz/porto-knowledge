---
id: doc_porto_landing_src_pages_products_rack_jsx
type: document
---

# Rack

import React from 'react' import MonumentPage from '../../components/MonumentPage' import Seo from '../../components/Seo' import content from '../../content/rack.json' export default function Page() { return <MonumentPage content={content} / } export const Head = () = <Seo title={content.title} description={content.description} path={content.path} hero={false} /

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'
import MonumentPage from '../../components/MonumentPage'
import Seo from '../../components/Seo'
import content from '../../content/rack.json'
export default function Page() { return <MonumentPage content={content} /> }
export const Head = () => <Seo title={content.title} description={content.description} path={content.path} hero={false} />
