---
id: doc_porto_landing_src_components_hardwareredirect_jsx
type: document
---

# Hardwareredirect

import React from 'react' import { graphql, Link, useStaticQuery } from 'gatsby' export default function HardwareRedirect() { return <main<Link to="/hardware/"Explore Kiln hardware</Link</main } export function Head() { const { site } = useStaticQuery(graphql query KilnHardwareRedirectOrigin { site { siteMetadata { siteUrl } } } ) return < <titleKiln hardware</title <meta name="robots" content="noindex, follow" /.

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'
import { graphql, Link, useStaticQuery } from 'gatsby'

export default function HardwareRedirect() {
  return <main><Link to="/hardware/">Explore Kiln hardware</Link></main>
}

export function Head() {
  const { site } = useStaticQuery(graphql`
    query KilnHardwareRedirectOrigin {
      site { siteMetadata { siteUrl } }
    }
  `)
  return <>
    <title>Kiln hardware</title>
    <meta name="robots" content="noindex, follow" />
    <meta httpEquiv="refresh" content="0;url=/hardware/" />
    <link rel="canonical" href={`${site.siteMetadata.siteUrl}/hardware/`} />
  </>
}
