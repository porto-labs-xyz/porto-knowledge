---
id: doc_porto_landing_src_pages_index_jsx
type: document
---

# Porto Landing Page

import React, { useRef, useState } from 'react' const contact = 'mailto:[redacted-email]' const description = 'FREQ by Porto Labs. A new kind of creative system, where AI, imagination and personal computing meet. Join the waitlist or start a conversation.' const Arrow = () = <span aria-hidden="true"↗</span export default function IndexPage() { const [email, setEmail] = useState('') const [status, setStatus] =.

## Connected knowledge

No outgoing links.

## Source content

import React, { useRef, useState } from 'react'

const contact = 'mailto:[redacted-email]'
const description = 'FREQ by Porto Labs. A new kind of creative system, where AI, imagination and personal computing meet. Join the waitlist or start a conversation.'
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
    <div className="freq-site" id="home">
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="freq-header freq-wrap">
        <a className="freq-brand" href="#home" aria-label="FREQ by Porto Labs home">
          <span className="freq-wordmark">FREQ</span>
          <span className="freq-byline">by Porto Labs</span>
        </a>
        <nav aria-label="Main navigation">
          <a className="freq-nav-join" href="#join">Join the waitlist</a>
          <a className="freq-nav-call" href="/book/">Book a call <Arrow /></a>
        </nav>
      </header>
      <main id="main">
        <section className="freq-hero" aria-labelledby="hero-heading">
          <img className="freq-art" src="/images/freq/afterimage-orbits.png" width="1672" height="941" alt="" fetchpriority="high" />
          <div className="freq-hero-shade" aria-hidden="true" />
          <div className="freq-hero-inner freq-wrap">
            <img className="freq-fluid-wordmark" src="/images/freq/wordmark.png" width="2172" height="724" alt="" />
            <p className="freq-eyebrow"><span className="freq-signal" aria-hidden="true" /> In the making</p>
            <h1 id="hero-heading">A new frequency <br />for <span>imagination.</span></h1>
            <p className="freq-intro">We’re building a new kind of creative system.<br className="freq-desktop-break" /> Where AI, imagination and personal computing meet.</p>
            <div className="freq-actions">
              <a className="freq-button" href="#join">Join the waitlist <Arrow /></a>
              <a className="freq-text-link" href="/book/">Book a call <Arrow /></a>
            </div>
          </div>
          <div className="freq-hero-foot freq-wrap"><span>FREQ / BY PORTO LABS</span><a href="#join">Stay close <span aria-hidden="true">↓</span></a></div>
        </section>
        <section className="freq-join freq-wrap" id="join" aria-labelledby="join-heading">
          <div>
            <p className="freq-eyebrow">An open invitation</p>
            <h2 id="join-heading">Be here for <br />what’s next.</h2>
          </div>
          <div className="freq-signup">
            <p>We’re keeping a few things under wraps.<br />Leave your email. You’ll hear when there’s more.</p>
            <form onSubmit={handleSubmit} action="https://formspree.io/f/xjgepgbg" method="POST" aria-busy={status === 'sending'}>
              <label htmlFor="email">Email address</label>
              <div className="freq-form-row">
                <input id="email" name="email" type="email" autoComplete="email" placeholder="[redacted-email]" required maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} disabled={status === 'sending'} aria-describedby="signup-note signup-status" />
                <button className="freq-button" type="submit" disabled={status === 'sending'}>{status === 'sending' ? 'Joining…' : 'Join the waitlist'} <Arrow /></button>
              </div>
              <p className="freq-small" id="signup-note">By joining, you agree to receive FREQ updates from Porto Labs.</p>
              <p className="freq-form-status" id="signup-status" role="status" aria-live="polite">
                {status === 'success' && 'You’re on the list. We’ll be in touch.'}
                {status === 'error' && <>We couldn’t add you just now. Please try again or <a href={contact}>email us</a>.</>}
              </p>
            </form>
          </div>
        </section>
      </main>
      <footer className="freq-footer freq-wrap">
        <div><span className="freq-company">Porto Labs</span><span className="freq-small">© {new Date().getFullYear()} Porto Labs Ltd.</span></div>
        <nav aria-label="Footer navigation"><a href={contact}>Get in touch <Arrow /></a><a href="https://x.com/porto_labs" target="_blank" rel="noopener noreferrer">Follow on X <Arrow /></a></nav>
      </footer>
    </div>
  )
}

export const Head = () => (
  <>
    <html lang="en" />
    <title>FREQ by Porto Labs | A new frequency for imagination</title>
    <meta name="description" content={description} />
    <meta name="robots" content="index, follow" />
    <meta name="theme-color" content="#251820" />
    <link rel="canonical" href="https://www.portolabs.xyz/" />
    <link rel="preload" href="/images/freq/wordmark.png" as="image" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://www.portolabs.xyz/" />
    <meta property="og:title" content="FREQ by Porto Labs | A new frequency for imagination" />
    <meta property="og:description" content={description} />
    <meta property="og:site_name" content="FREQ by Porto Labs" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="https://www.portolabs.xyz/images/freq/afterimage-orbits.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1672" />
    <meta property="og:image:height" content="941" />
    <meta property="og:image:alt" content="Orbital grain artwork from the FREQ Afterimage identity." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="FREQ by Porto Labs | A new frequency for imagination" />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content="https://www.portolabs.xyz/images/freq/afterimage-orbits.png" />
    <meta name="twitter:image:alt" content="Orbital grain artwork from the FREQ Afterimage identity." />
  </>
)
