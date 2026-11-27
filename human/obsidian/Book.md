---
id: doc_porto_landing_src_pages_book_jsx
type: document
---

# Book

import React from 'react' import '../styles/booking.css' import Seo from '../components/Seo' const bookingUrl = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ3mIWxC1ktiq8hY4v2k7n7OLV9-mV5LeNDbw39rutjhWd3O-u4CbNtFsOxOMJ4Vc1W2c5RFv9J?gv=true' function GoogleBookingEmbed() { return ( <section className="booking-widget-frame" aria-label="Choose a time to meet Porto" <div.

## Connected knowledge

No outgoing links.

## Source content

import React from 'react'
import '../styles/booking.css'
import Seo from '../components/Seo'

const bookingUrl = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ3mIWxC1ktiq8hY4v2k7n7OLV9-mV5LeNDbw39rutjhWd3O-u4CbNtFsOxOMJ4Vc1W_2c5RFv9J?gv=true'

function GoogleBookingEmbed() {
  return (
    <section className="booking-widget-frame" aria-label="Choose a time to meet Porto">
      <div className="booking-calendar-surface">
        <iframe
          className="booking-calendar"
          src={bookingUrl}
          title="Book a call with Kiln by Porto Labs on Google Calendar"
          width="100%"
          height="720"
        />
      </div>
      <p className="booking-fallback">Calendar not loading? <a href={bookingUrl} target="_blank" rel="noopener noreferrer">open the booking page directly <span className="action-square" aria-hidden="true"></span></a></p>
    </section>
  )
}

export default function BookPage() {
  return (
    <div className="booking-page kiln-site">
      <a className="skip-link" href="#booking-main">skip to booking</a>
      <header className="kiln-header kiln-wrap">
        <a className="kiln-brand" href="/" aria-label="Kiln by Porto Labs home">
          <img src="/assets/kiln/kiln-crucible.svg" width="32" height="35" alt="Kiln" />
        </a>
        <a className="kiln-text-link" href="/#interest">register interest <span className="action-square" aria-hidden="true"></span></a>
      </header>
      <main className="booking-main" id="booking-main">
        <div className="booking-intro">
          <p className="booking-eyebrow">Kiln / a conversation</p>
          <h1>Book a call</h1>
          <p>Choose a time to meet the people building Kiln.</p>
        </div>
        <GoogleBookingEmbed />
      </main>
    </div>
  )
}

export const Head = () => <>
  <Seo title="Book a call with Kiln by Porto Labs" description="Start a conversation with the team behind Kiln by Porto Labs." path="/book/" />
  <link rel="preconnect" href="https://calendar.google.com" />
</>
