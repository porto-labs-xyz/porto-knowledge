---
id: doc_porto_landing_src_pages_book_jsx
type: document
---

# Book

import React, { useEffect, useRef } from 'react' const calendlyUrl = 'https://calendly.com/d/dz7f-tjf-km7/20-min-meeting-porto-meeting?backgroundcolor=101313&textcolor=eee8dc&primarycolor=ee6251' const widgetScriptUrl = 'https://assets.calendly.com/assets/external/widget.js' function CalendlyInlineEmbed() { const widgetRef = useRef(null) useEffect(() = { const container = widgetRef.current if (!container) return.

## Connected knowledge

No outgoing links.

## Source content

import React, { useEffect, useRef } from 'react'

const calendlyUrl = 'https://calendly.com/d/dz7f-tjf-km7/20-min-meeting-porto-meeting?background_color=101313&text_color=eee8dc&primary_color=ee6251'
const widgetScriptUrl = 'https://assets.calendly.com/assets/external/widget.js'

function CalendlyInlineEmbed() {
  const widgetRef = useRef(null)

  useEffect(() => {
    const container = widgetRef.current
    if (!container) return undefined

    let cancelled = false
    let script = document.querySelector(`script[src="${widgetScriptUrl}"]`)
    const initializeWidget = () => {
      if (cancelled || !window.Calendly || container.dataset.initialized === 'true') return
      container.dataset.initialized = 'true'
      window.Calendly.initInlineWidget({
        url: calendlyUrl,
        parentElement: container,
      })
    }

    if (window.Calendly) {
      initializeWidget()
    } else {
      if (!script) {
        script = document.createElement('script')
        script.src = widgetScriptUrl
        script.async = true
        document.body.appendChild(script)
      }
      script.addEventListener('load', initializeWidget)
    }

    return () => {
      cancelled = true
      script?.removeEventListener('load', initializeWidget)
      container.innerHTML = ''
      delete container.dataset.initialized
    }
  }, [])

  return (
    <div className="booking-widget-frame">
      <div
        className="calendly-inline-widget"
        data-url={calendlyUrl}
        ref={widgetRef}
        style={{ minWidth: '320px', height: '880px' }}
        aria-label="Calendly booking calendar"
      />
      <p className="booking-fallback">Calendar not loading? <a href="https://calendly.com/d/dz7f-tjf-km7/20-min-meeting-porto-meeting">Open the booking page directly</a>.</p>
    </div>
  )
}

export default function BookPage() {
  return (
    <div className="booking-page">
      <header className="booking-header">
        <a className="booking-brand" href="/" aria-label="Porto home">
          <span className="booking-brand-mark" aria-hidden="true" />
          <span>PORTO</span>
        </a>
        <a className="booking-join" href="/#join">Join The Network <span aria-hidden="true">↗</span></a>
      </header>
      <main className="booking-main">
        <div className="booking-intro">
          <p className="booking-eyebrow">Porto / Conversation</p>
          <h1>Book A Call</h1>
          <p>Choose a time to meet the Porto co-founders.</p>
        </div>
        <CalendlyInlineEmbed />
      </main>
    </div>
  )
}

export const Head = () => (
  <>
    <html lang="en" />
    <title>Book a call with Porto</title>
    <meta name="description" content="Book a 20 minute call with Porto's co-founders." />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://www.portolabs.xyz/book/" />
    <link rel="icon" href="/images/porto-mark-dark-branded.webp" type="image/webp" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://www.portolabs.xyz/book/" />
    <meta property="og:title" content="Book a call with Porto" />
    <meta property="og:description" content="Book a 20 minute call with Porto's co-founders." />
    <meta property="og:site_name" content="Porto" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="https://www.portolabs.xyz/images/og-book-dark-p-1200x630.png" />
    <meta property="og:image:secure_url" content="https://www.portolabs.xyz/images/og-book-dark-p-1200x630.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Porto's hand-drawn P centered on charcoal" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Book a call with Porto" />
    <meta name="twitter:description" content="Book a 20 minute call with Porto's co-founders." />
    <meta name="twitter:image" content="https://www.portolabs.xyz/images/og-book-dark-p-1200x630.png" />
    <meta name="twitter:image:alt" content="Porto's hand-drawn P centered on charcoal" />
    <link rel="preconnect" href="https://assets.calendly.com" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
  </>
)
