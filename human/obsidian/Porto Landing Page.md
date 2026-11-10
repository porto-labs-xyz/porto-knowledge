---
id: doc_porto_landing_src_pages_index_jsx
type: document
---

# Porto Landing Page

import React, { useRef, useState } from 'react' const contact = 'mailto:[redacted-email]' const description = 'Kiln by Porto Labs. Private creative AI. A space for your imagination. Join the waitlist or start a conversation.' const Arrow = () = <span aria-hidden="true"↗</span export default function IndexPage() { const [email, setEmail] = useState('') const [status, setStatus] = useState('idle') const pending =.

## Connected knowledge

No outgoing links.

## Source content

import React, { useRef, useState } from 'react'

const contact = 'mailto:[redacted-email]'
const description = 'Kiln by Porto Labs. Private creative AI. A space for your imagination. Join the waitlist or start a conversation.'
const Arrow = () => <span aria-hidden="true">↗</span>

export default function IndexPage() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState('idle')
  const pending = useRef(false)

  async function handleSubmit(event) {
    event.preventDefault()
    if (pending.current) return
    pending.current = true
    setStatus('sending')
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 15000)
    try {
      const response = await fetch('https://formspree.io/f/xjgepgbg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ email: email.trim() }),
        signal: controller.signal,
      })
      if (!response.ok) throw new Error('Submission failed')
      setEmail('')
      setStatus('success')
    } catch {
      setStatus('error')
    } finally {
      clearTimeout(timeout)
      pending.current = false
    }
  }

  return (
    <div className="kiln-site" id="home">
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="kiln-header kiln-wrap">
        <a className="kiln-brand" href="#home" aria-label="Kiln by Porto Labs home">
          <span className="kiln-wordmark">kiln</span>
          <span className="kiln-byline">by Porto Labs</span>
        </a>
        <nav aria-label="Main navigation">
          <a className="kiln-nav-join" href="#join">Join the waitlist</a>
          <a className="kiln-nav-call" href="/book/">Book a call <Arrow /></a>
        </nav>
      </header>
      <main id="main">
        <section className="kiln-hero" aria-labelledby="hero-heading">
          <div className="kiln-art" aria-hidden="true"><div className="kiln-aperture" /><span className="kiln-fragment kiln-fragment-one" /><span className="kiln-fragment kiln-fragment-two" /><span className="kiln-art-caption">ROOM FOR THE UNEXPECTED</span></div>
          <div className="kiln-hero-inner kiln-wrap">
            <p className="kiln-eyebrow"><span className="kiln-signal" aria-hidden="true" /> In the making</p>
            <h1 id="hero-heading">Your imagination.<br />A space of its own.</h1>
            <p className="kiln-intro">Private creative AI.<br />Something new is taking shape at Kiln.</p>
            <div className="kiln-actions">
              <a className="kiln-button" href="#join">Join the waitlist <Arrow /></a>
              <a className="kiln-text-link" href="/book/">Book a call <Arrow /></a>
            </div>
          </div>
          <div className="kiln-hero-foot kiln-wrap"><span>KILN / BY PORTO LABS</span><a href="#join">Stay close <span aria-hidden="true">↓</span></a></div>
        </section>
        <section className="kiln-join kiln-wrap" id="join" aria-labelledby="join-heading">
          <div>
            <p className="kiln-eyebrow">An open invitation</p>
            <h2 id="join-heading">Be here for <br />what’s next.</h2>
          </div>
          <div className="kiln-signup">
            <p>A little mystery. A lot in the making.<br />Leave your email for the first look.</p>
            <form onSubmit={handleSubmit} action="https://formspree.io/f/xjgepgbg" method="POST" aria-busy={status === 'sending'}>
              <label htmlFor="email">Email address</label>
              <div className="kiln-form-row">
                <input id="email" name="email" type="email" autoComplete="email" placeholder="[redacted-email]" required maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} disabled={status === 'sending'} aria-describedby="signup-note signup-status" />
                <button className="kiln-button" type="submit" disabled={status === 'sending'}>{status === 'sending' ? 'Joining…' : 'Join the waitlist'} <Arrow /></button>
              </div>
              <p className="kiln-small" id="signup-note">By joining, you agree to receive Kiln updates from Porto Labs.</p>
              <p className="kiln-form-status" id="signup-status" role="status" aria-live="polite">
                {status === 'success' && 'You’re on the list. We’ll be in touch.'}
                {status === 'error' && <>We couldn’t add you just now. Please try again or <a href={contact}>email us</a>.</>}
              </p>
            </form>
          </div>
        </section>
      </main>
      <footer className="kiln-footer kiln-wrap">
        <div><span className="kiln-company">Porto Labs</span><span className="kiln-small">© {new Date().getFullYear()} Porto Labs Ltd.</span></div>
        <nav aria-label="Footer navigation"><a href={contact}>Get in touch <Arrow /></a><a href="https://x.com/porto_labs" target="_blank" rel="noopener noreferrer">Follow on X <Arrow /></a></nav>
      </footer>
    </div>
  )
}

export const Head = () => (
  <>
    <html lang="en" />
    <title>Kiln by Porto Labs | A space for your imagination</title>
    <meta name="description" content={description} />
    <meta name="robots" content="index, follow" />
    <meta name="theme-color" content="#f1f0ec" />
    <link rel="canonical" href="https://www.portolabs.xyz/" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://www.portolabs.xyz/" />
    <meta property="og:title" content="Kiln by Porto Labs | A space for your imagination" />
    <meta property="og:description" content={description} />
    <meta property="og:site_name" content="Kiln by Porto Labs" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="https://www.portolabs.xyz/images/kiln-social.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Kiln. Your imagination. A space of its own." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Kiln by Porto Labs | A space for your imagination" />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content="https://www.portolabs.xyz/images/kiln-social.png" />
    <meta name="twitter:image:alt" content="Kiln. Your imagination. A space of its own." />
  </>
)
