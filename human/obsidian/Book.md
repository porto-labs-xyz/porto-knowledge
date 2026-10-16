---
id: doc_porto_landing_src_pages_book_jsx
type: document
---

# Book

import React from 'react' const bookingUrl = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ3mIWxC1ktiq8hY4v2k7n7OLV9-mV5LeNDbw39rutjhWd3O-u4CbNtFsOxOMJ4Vc1W2c5RFv9J?gv=true' function GoogleBookingEmbed() { return ( <section className="booking-widget-frame" aria-label="Choose a time to meet Porto" <div className="booking-calendar-surface" <iframe className="booking-calendar" src={bookingUrl}.

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'

const bookingUrl = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ3mIWxC1ktiq8hY4v2k7n7OLV9-mV5LeNDbw39rutjhWd3O-u4CbNtFsOxOMJ4Vc1W_2c5RFv9J?gv=true'

function GoogleBookingEmbed() {
  return (
    <section className="booking-widget-frame" aria-label="Choose a time to meet Porto">
      <div className="booking-calendar-surface">
        <iframe
          className="booking-calendar"
          src={bookingUrl}
          title="Book a call with Porto on Google Calendar"
          width="100%"
          height="720"
          style={{ border: 0 }}
        />
      </div>
      <p className="booking-fallback">Calendar not loading? <a href={bookingUrl} target="_blank" rel="noopener noreferrer">Open the booking page directly <span aria-hidden="true">↗</span></a></p>
    </section>
  )
}

export default function BookPage() {
  return (
    <div className="booking-page">
      <a className="skip-link" href="#booking-main">Skip to booking</a>
      <header className="booking-header">
        <a className="booking-brand" href="/" aria-label="Porto home">
          <span className="booking-brand-mark" aria-hidden="true" />
          <span>PORTO</span>
        </a>
        <a className="booking-join" href="/#join">Explore Porto <span aria-hidden="true">↗</span></a>
      </header>
      <main className="booking-main" id="booking-main">
        <div className="booking-intro">
          <p className="booking-eyebrow">Porto / Conversation</p>
          <h1>Book a call</h1>
          <p>Choose a time to meet the Porto co-founders.</p>
        </div>
        <GoogleBookingEmbed />
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
    <meta property="og:title" content="20 minutes with Peter &amp; Richard" />
    <meta property="og:description" content="Book a 20 minute call with Porto's co-founders." />
    <meta property="og:site_name" content="Porto" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="https://www.portolabs.xyz/images/og-book-dark-p-thumb-256.png" />
    <meta property="og:image:secure_url" content="https://www.portolabs.xyz/images/og-book-dark-p-thumb-256.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="256" />
    <meta property="og:image:height" content="256" />
    <meta property="og:image:alt" content="Porto's hand-drawn P centered on charcoal" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="20 minutes with Peter &amp; Richard" />
    <meta name="twitter:description" content="Book a 20 minute call with Porto's co-founders." />
    <meta name="twitter:image" content="https://www.portolabs.xyz/images/og-book-dark-p-thumb-256.png" />
    <meta name="twitter:image:alt" content="Porto's hand-drawn P centered on charcoal" />
    <link rel="preconnect" href="https://calendar.google.com" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
  </>
)
