---
id: doc_porto_landing_src_components_seo_jsx
type: document
---

# Seo

import React from 'react' import { graphql, useStaticQuery } from 'gatsby' export default function Seo({ title, description, path, hero = false }) { const { site } = useStaticQuery(graphql query KilnSharingMetadata { site { siteMetadata { siteUrl sharingOrigin } } } ) const { siteUrl, sharingOrigin } = site.siteMetadata const url = ${siteUrl}${path} const image = ${sharingOrigin}/images/kiln-keep-the-work-close.png.

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'
import { graphql, useStaticQuery } from 'gatsby'

export default function Seo({ title, description, path, hero = false }) {
  const { site } = useStaticQuery(graphql`
    query KilnSharingMetadata {
      site {
        siteMetadata { siteUrl sharingOrigin }
      }
    }
  `)
  const { siteUrl, sharingOrigin } = site.siteMetadata
  const url = `${siteUrl}${path}`
  const image = `${sharingOrigin}/images/kiln-keep-the-work-close.png`
  const imageAlt = '“Keep the work close.” beside a charcoal Kiln One workstation with a leather handle.'
  return <>
    <html lang="en" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <meta name="robots" content="index, follow" />
    <meta name="theme-color" content="#f6f6f2" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <link rel="canonical" href={url} />
    <link rel="icon" href="/favicon.png" type="image/png" sizes="512x512" />
    <link rel="preload" href="/assets/fonts/ABCMonumentGrotesk-Regular.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
    {hero && <link rel="preload" as="image" href="/assets/kiln/finishes/charcoal-device-6400.webp" />}
    <meta property="og:type" content="website" />
    <meta property="og:url" content={`${sharingOrigin}${path}`} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:site_name" content="Kiln by Porto Labs" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content={image} />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content={imageAlt} />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={image} />
    <meta name="twitter:image:alt" content={imageAlt} />
  </>
}
