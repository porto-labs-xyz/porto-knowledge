---
id: doc_porto_landing_src_pages_index_jsx
type: document
---

# Porto Landing Page

import React, { useState } from 'react' const prototype = 'https://porto-prototype.vercel.app/' const contact = 'mailto:[redacted-email]' const seoDescription = 'Streaming + music generation. Discover Porto: licensed originals, personal variations, artist control and connected royalties. Explore the listening prototype.' const Arrow = () = <span aria-hidden="true"↗</span function PrototypeLink({ className =.

## Connected knowledge

No outgoing links.

## Source content

import React, { useState } from 'react'

const prototype = 'https://porto-prototype.vercel.app/'
const contact = 'mailto:[redacted-email]'
const seoDescription = 'Streaming + music generation. Discover Porto: licensed originals, personal variations, artist control and connected royalties. Explore the listening prototype.'

const Arrow = () => <span aria-hidden="true">↗</span>

function PrototypeLink({ className = 'p-button' , children = 'Try the prototype' }) {
  return <a className={className} href={prototype} target="_blank" rel="noopener noreferrer">{children} <Arrow /></a>
}

function ProductScreen({ name, alt, caption, eager = false }) {
  return (
    <figure className={`p-screen p-screen-${name}`}>
      <a href={`/images/october/${name}.webp`} target="_blank" rel="noopener noreferrer" aria-label={`Enlarge ${caption.toLowerCase()} (opens in a new tab)`}>
        <img src={`/images/october/${name}.webp`} width="1458" height="913" alt={alt} loading={eager ? 'eager' : 'lazy'} fetchPriority={eager ? 'high' : 'auto'} />
      </a>
      <figcaption><span>{caption}</span><span>Concept screen <Arrow /></span></figcaption>
    </figure>
  )
}

const IndexPage = () => {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState('idle')

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (status === 'sending') return
    setStatus('sending')
    try {
      const response = await fetch('https://formspree.io/f/xjgepgbg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ email }),
      })
      if (!response.ok) throw new Error('Submission failed')
      setEmail('')
      setStatus('success')
    } catch {
      setStatus('error')
    }
  }

  return (
    <div className="porto-site" id="home">
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="p-header">
        <a className="p-brand" href="#home" aria-label="Porto home"><img src="/images/porto-mark-dark-branded.webp" width="56" height="56" alt="" /><span>PORTO</span></a>
        <nav aria-label="Main navigation">
          <a href="#product">Product</a>
          <a href="#artists">For artists</a>
          <a href="#revenue">Revenue</a>
          <a href="#ledger">Ledger</a>
        </nav>
        <PrototypeLink className="p-nav-cta" />
      </header>

      <main id="main">
        <section className="p-hero p-wrap" aria-labelledby="hero-heading">
          <div className="p-hero-copy">
            <p className="p-kicker">Streaming + music generation</p>
            <h1 id="hero-heading">More music,<br />made to be<br /><span>listened to.</span></h1>
            <p className="p-lead">Licensed originals. Personal variations.<br />More income to fund the next original.</p>
            <div className="p-actions"><PrototypeLink /><a className="p-text-link" href="#product">Meet Porto <span aria-hidden="true">↓</span></a></div>
            <p className="p-micro">Explore the interactive listening prototype.</p>
          </div>
          <div className="p-hero-visual">
            <div className="p-visual-label"><span className="p-dot" /> Your library. A new possibility.</div>
            <ProductScreen name="listening" eager caption="01 / Press play" alt="Porto listening concept: Afterlight by fictional artist June Arcade, a music library, playback controls and a Speak or type prompt." />
            <div className="p-prompt"><span className="p-voice-icon" aria-hidden="true"><i /><i /><i /><i /><i /></span><p>“Play June Arcade’s Afterlight.”</p><span>Speak or type</span></div>
          </div>
        </section>

        <div className="p-principles p-wrap" aria-label="The Porto experience"><span>Listen to originals</span><span>Make it personal</span><span>Keep the artist connected</span></div>

        <section className="p-section p-wrap" id="product" aria-labelledby="product-heading">
          <div className="p-section-heading"><p className="p-kicker">01 / Made for listening</p><h2 id="product-heading">Press play.<br />Then talk to Porto.</h2><p className="p-lead">Familiar streaming. Personalised by you.</p></div>
          <div className="p-product-row">
            <div className="p-product-copy"><span className="p-step">01 → 02</span><h3>Same song.<br /><span className="p-violet">Your version.</span></h3><p>Ask with your voice or type a request. Porto’s product direction is to turn licensed originals into personal User Variation Tracks, within the permissions set by the artist and rights holders.</p><blockquote>“Remove the guitar.<br />Slow it down.<br />Make it dreamy.”</blockquote><p className="p-caption">A concept request. Full generation capabilities are in development.</p></div>
            <ProductScreen name="voice" caption="02 / Make it personal" alt="Porto voice request concept with a violet waveform and the request Remove the guitar. Slow it down. Make it dreamy. The resulting variation is attributed to Afterlight by June Arcade." />
          </div>
          <div className="p-product-row p-product-reverse">
            <div className="p-product-copy"><span className="p-step">02 → 03</span><h3>One track.<br />So many possibilities.</h3><p>Find your version. Follow the people who made it. Share a new way to hear a song, with every variation connected to its original artist.</p><p className="p-pullquote">More ways to listen.<br />More ways for a single track<br />to generate royalties.</p><PrototypeLink className="p-text-link" children="Explore the prototype" /></div>
            <ProductScreen name="creators" caption="03 / Listen. Follow. Share." alt="Porto creator feed concept showing three listener variations of Afterlight: Dreamy, No guitars and Slow drift, with creator portraits and the source artist credited." />
          </div>
          <p className="p-disclosure">Product concept screens feature fictional artists and creators. The interactive prototype demonstrates listening, voice/text requests and variations; it does not provide production model generation, licensed catalogue access or live payments.</p>
        </section>

        <section className="p-section p-artists" id="artists" aria-labelledby="artists-heading">
          <div className="p-wrap">
            <div className="p-section-heading p-heading-split"><div><p className="p-kicker">02 / To benefit the artist</p><h2 id="artists-heading">Amplify your catalogue.<br /><span>Keep it yours.</span></h2></div><p className="p-lead">The original stays at the centre. Every new way to listen should create another way to support the artist behind it.</p></div>
            <div className="p-feature-grid">
              <article><span className="p-step">01 / Permission</span><h3>Licensed from the start.</h3><p>Work with artists and labels on catalogue permissions and bespoke artist models. One model, built around one artist’s sound, with their approval.</p></article>
              <article><span className="p-step">02 / Control</span><h3>Your sound. Your say.</h3><p>Artists and rights holders set the creative permissions. Approved variations keep their source connection, with control over rights and release decisions.</p></article>
              <article><span className="p-step">03 / Income</span><h3>Back to the original.</h3><p>Paid listening to originals and permitted variations funds the source rights holders. Creator credit recognises a contribution; it does not automatically grant a royalty share.</p></article>
            </div>
            <div className="p-section-footer"><p>Artist relationships, licensed music, listening and royalties. One whole solution.</p><a className="p-text-link" href="/book/">Talk to Porto <Arrow /></a></div>
          </div>
        </section>

        <section className="p-section p-wrap" id="revenue" aria-labelledby="revenue-heading">
          <div className="p-section-heading"><p className="p-kicker">03 / The proposed revenue model</p><h2 id="revenue-heading">Pay for what<br />you listen to.</h2><p className="p-lead">Listening, without a subscription. A clear share for the music’s rights holders.</p></div>
          <div className="p-revenue-grid">
            <article className="p-rate-card"><p className="p-rate-type">Original track</p><h3><strong>90%</strong><span>to the rights-holder pool</span></h3><div className="p-split-bar" aria-hidden="true"><span style={{ width: '90%' }} /><i /></div><p className="p-fee"><span>Licensed originals</span><strong>10% Porto fee</strong></p></article>
            <article className="p-rate-card p-rate-variation"><p className="p-rate-type">User Variation Track</p><h3><strong>70%</strong><span>to the rights-holder pool</span></h3><div className="p-split-bar" aria-hidden="true"><span style={{ width: '70%' }} /><i /></div><p className="p-fee"><span>Personal variations</span><strong>30% Porto fee</strong></p></article>
          </div>
          <div className="p-budget"><div><span className="p-budget-amount">£10</span><span className="p-kicker">Proposed monthly listening cap</span></div><p>At the cap, originals play on and variations pause. Choose to top up or wait for the monthly reset. No automatic extra charges.</p></div>
          <p className="p-disclosure">Proposed shares apply to allocated track revenue. Individual artist receipts depend on agreed label, publisher and other rights splits. Launch pricing, generation costs and funding for original listening beyond the cap are still being validated.</p>
        </section>

        <section className="p-section p-ledger" id="ledger" aria-labelledby="ledger-heading">
          <div className="p-wrap">
            <div className="p-section-heading p-heading-split"><div><p className="p-kicker">04 / Porto Ledger</p><h2 id="ledger-heading">Every royalty.<br /><span>Connected.</span></h2></div><div><p className="p-lead">See what was paid, how it was calculated and when it arrived.</p><p className="p-target">Product target: daily payouts on Aptos, in USDC.</p></div></div>
            <ol className="p-ledger-flow"><li><span>01</span><div><h3>Stream</h3><p>Originals and permitted variations.</p></div></li><li><span>02</span><div><h3>Share</h3><p>New versions. New listeners.</p></div></li><li><span>03</span><div><h3>Earn</h3><p>Paid listening returns to the source.</p></div></li></ol>
            <div className="p-ledger-grid">
              <figure className="p-ledger-image"><img src="/images/october/ledger.webp" width="1491" height="343" loading="lazy" alt="Illustrative Porto Ledger: an original earns £3 allocated revenue with £2.70 to its rights-holder pool; the Dreamy variation earns £4 with £2.80 to the pool. These are sample amounts." /><figcaption>From the October concept. Illustrative amounts, no money paid.</figcaption></figure>
              <div className="p-record"><p className="p-kicker">The proposed payout record</p><dl><div><dt>What</dt><dd>USDC amount + royalty obligation</dd></div><div><dt>Who</dt><dd>Recipient + agreed rights version</dd></div><div><dt>How</dt><dd>Allocation rules + transaction record</dd></div><div><dt>When</dt><dd>Payment time + confirmation</dd></div></dl></div>
            </div>
            <p className="p-disclosure">Daily settlement is a product target. The prototype Ledger is illustrative. Private listening data and audio stay off chain; payout records are designed to make the money traceable.</p>
          </div>
        </section>

        <section className="p-section p-wrap p-next" aria-labelledby="next-heading">
          <div className="p-section-heading"><p className="p-kicker">05 / What comes next</p><h2 id="next-heading">London first.<br />Expansion follows proof.</h2></div>
          <div className="p-milestones"><article><p className="p-kicker">Now</p><h3>Listening prototype</h3><p>Explore playback, voice and text requests, variations and track connections.</p><PrototypeLink className="p-text-link" children="Open prototype" /></article><article><p className="p-kicker">Next</p><h3>Controlled artist pilot</h3><p>Licensed catalogue. Real paid listening. Traceable settlement.</p></article><article><p className="p-kicker">Then</p><h3>Repeat what works</h3><p>Measure return listening, sharing and artist income before expanding catalogue and reach.</p></article></div>
          <div className="p-team-heading"><h2>The music.<br />And the systems.</h2><p>Built by people who know both.</p></div>
          <div className="p-team-grid">
            <article><img src="/images/richard_headshot.jpg" alt="" width="112" height="136" loading="lazy" /><div><p className="p-kicker">Technical CEO / Co-founder</p><h3>Richard Melkonian</h3><p>Movement, Parity, Dapper and Fuel. Former CTO of Inflow Music. Publishing experience across 300+ artists.</p></div></article>
            <article><img src="/images/peter-xan.jpg" alt="" width="112" height="136" loading="lazy" /><div><p className="p-kicker">CMO / Co-founder</p><h3>Peter Xan</h3><p>MediaCom, M&amp;C Saatchi, TBWA and BBH. Founder of Thinning Room. Recording artist and artist manager.</p></div></article>
          </div>
          <a className="p-cohort" href="https://altalab.ai" target="_blank" rel="noopener noreferrer"><img src="/images/altalab-logo.png" alt="AltaLab" width="80" height="30" loading="lazy" /><span>Founder programme · Autumn 2026 cohort</span><Arrow /></a>
        </section>

        <section className="p-section p-join" id="join" aria-labelledby="join-heading">
          <div className="p-wrap p-join-grid"><div><p className="p-kicker">Be part of what’s next</p><h2 id="join-heading">Made to be<br /><span>listened to.</span></h2><div className="p-actions"><PrototypeLink /><a className="p-text-link" href="/book/">Artists &amp; labels, let’s talk <Arrow /></a></div></div>
            <div className="p-signup"><h3>Stay close to Porto.</h3><p>Leave your email for product and pilot updates.</p><form onSubmit={handleSubmit}><label htmlFor="email">Email address</label><div className="p-form-row"><input id="email" name="email" type="email" autoComplete="email" placeholder="[redacted-email]" value={email} onChange={(event) => setEmail(event.target.value)} required disabled={status === 'sending'} /><button className="p-button p-button-paper" type="submit" disabled={status === 'sending'}>{status === 'sending' ? 'Joining…' : 'Keep me posted'} <Arrow /></button></div><p className="p-form-status" role="status" aria-live="polite">{status === 'success' && 'You’re on the list. We’ll be in touch.'}{status === 'error' && <>Something went wrong. Try again or <a href={contact}>email us</a>.</>}</p></form></div>
          </div>
        </section>
      </main>
      <footer className="p-footer p-wrap"><div className="p-footer-main"><a className="p-brand" href="#home" aria-label="Porto home"><img src="/images/porto-mark-dark-branded.webp" width="56" height="56" alt="" /><span>PORTO</span></a><p>Streaming + music generation.<br />To benefit the artist.</p><nav aria-label="Footer navigation"><PrototypeLink className="p-text-link" children="Prototype" /><a href={contact}>Contact <Arrow /></a><a href="https://x.com/porto_labs" target="_blank" rel="noopener noreferrer">Follow on X <Arrow /></a></nav></div><div className="p-footer-bottom"><span>© {new Date().getFullYear()} Porto Labs Ltd.</span><span>UK registered company</span></div></footer>
    </div>
  )
}

export default IndexPage

export const Head = () => (
  <>
    <html lang="en" />
    <title>Porto | More music, made to be listened to.</title>
    <meta name="description" content={seoDescription} />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://www.portolabs.xyz/" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://www.portolabs.xyz/" />
    <meta property="og:title" content="Porto | More music, made to be listened to." />
    <meta property="og:description" content={seoDescription} />
    <meta property="og:site_name" content="Porto" />
    <meta property="og:locale" content="en_GB" />
    <meta property="og:image" content="https://www.portolabs.xyz/images/october/porto-listening-1200x630.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Porto. More music, made to be listened to. The listening concept with licensed originals and personal variations." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Porto | More music, made to be listened to." />
    <meta name="twitter:description" content={seoDescription} />
    <meta name="twitter:image" content="https://www.portolabs.xyz/images/october/porto-listening-1200x630.png" />
    <meta name="twitter:image:alt" content="Porto. More music, made to be listened to. The listening concept with licensed originals and personal variations." />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
  </>
)
