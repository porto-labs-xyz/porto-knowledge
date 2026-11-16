---
id: doc_porto_landing_src_components_seo_jsx
type: document
---

# Seo

import React from 'react' export default function Seo({ title, description, path, hero = false }) { const url = https://www.portolabs.xyz${path} const image = 'https://www.portolabs.xyz/assets/kiln/one-boot-poster.jpg' return < <html lang="en" / <title{title}</title <meta name="description" content={description} / <meta name="robots" content="index, follow" / <meta name="theme-color" content="F1F0ED" / <meta.

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'

export default function Seo({ title, description, path, hero = false }) {
  const url = `https://www.portolabs.xyz${path}`
  const image = 'https://www.portolabs.xyz/assets/kiln/one-boot-poster.jpg'
  return <>
    <html lang="en" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <meta name="robots" content="index, follow" />
    <meta name="theme-color" content="#F1F0ED" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <link rel="canonical" href={url} />
    <link rel="icon" href="/assets/kiln/kiln-crucible-ink.svg" type="image/svg+xml" />
    <link rel="preload" href="/assets/fonts/ABCMonumentGrotesk-Bold.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
    {hero && <link rel="preload" href="/assets/one-proportions.png" as="image" />}
    <meta property="og:type" content="website" />
    <meta property="og:url" content={url} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:site_name" content="Kiln by Porto Labs" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content={image} />
    <meta property="og:image:alt" content="Kiln One, local AI hardware for creative teams" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={image} />
  </>
}
