"""Evenhome elder care site: markets, layout and interactive components.
Built on the Investor Labs design system (lib.py helpers + il.css/il.js), re-themed by assets/ec.css + ec.js.
Content modules do:  from site import *   and call page(M, path, ...).
Write internal links root-absolute ("/us/book.html"); render() rewrites them relative so the site also works from file://.
"""
import os, re, html, json
from lib import *   # P, H2, H3, UL, T, KV, GRID, FLOW, IMG, SPLIT, GALLERY, STRIP, BAND, MOSAIC, QUOTE, KPI, BARS, COLS, LINE, DONUT, RING, FUNNEL, TIMELINE, VS, PILLS, SECTION, CALL, BTN, alt, ALT

BRAND = "Evenhome"
TAG = "Dementia care at home"
MAIL = "contact@eliteleadgrow.com"  # booking/referral forms open the visitor's mail app addressed here

# ---------- markets ----------
# Phone numbers are fictional placeholders (555-01xx in the US, 02 5550 xxxx in Australia). Replace before launch.
US = dict(
    p="us", lang="en-US", country="United States", region="Florida", metro="Tampa Bay", flag="US", cur="USD", sym="$",
    phone="(813) 555-0142", tel="+18135550142", text="(813) 555-0143", sms="+18135550143",
    hours="A real person answers 24 hours a day, 7 days a week",
    lic="Florida AHCA license number: application in progress. We will not provide care until the license is issued.",
    lic_short="FL AHCA license: pending",
    regulator=("Florida Agency for Health Care Administration", "https://quality.healthfinder.fl.gov/"),
    addr="[Office address, Tampa, FL]",
    mom="mom", Mom="Mom", dad="dad", cg="caregiver", cgs="caregivers", Cg="Caregiver", Cgs="Caregivers",
    color="color", center="center", organize="organize", program="program",
    rates=dict(companion=30, personal=34, dementia=38, overnight=32, live=420),
    pay=("/us/paying-for-care.html", "Paying for care"),
    cities=[("Tampa", 1.0), ("St. Petersburg", 1.0), ("Clearwater", 0.98), ("Brandon", 0.97), ("Wesley Chapel", 0.98), ("Sarasota", 1.04)],
    live=True,
)
AU = dict(
    p="au", lang="en-AU", country="Australia", region="Australia", metro="Sydney", flag="AU", cur="AUD", sym="$",
    phone="(02) 5550 0142", tel="+61255500142", text="(02) 5550 0143", sms="+61255500143",
    hours="Care advisors answer 8am to 8pm AEST, 7 days. Waitlist families get a call back the next business day",
    lic="Not yet registered with the Aged Care Quality and Safety Commission. This site is a waitlist and information site until registration questions are settled.",
    lic_short="AU registration: not yet held",
    regulator=("Aged Care Quality and Safety Commission", "https://www.agedcarequality.gov.au/"),
    addr="[Office address, Sydney NSW]",
    mom="mum", Mom="Mum", dad="dad", cg="support worker", cgs="support workers", Cg="Support worker", Cgs="Support workers",
    color="colour", center="centre", organize="organise", program="programme",
    rates=dict(companion=85, personal=102, dementia=120, overnight=95, live=1100),
    pay=("/au/funding.html", "Funding"),
    cities=[("Sydney metro", 1.0), ("Northern Beaches", 1.04), ("Parramatta", 0.98), ("Sutherland Shire", 1.0), ("Central Coast", 0.97)],
    live=False,
)
MARKETS = {"us": US, "au": AU}

def money(M, v):
    return f"{M['cur']} {M['sym']}{v:,.0f}" if isinstance(v, (int, float)) else v

def ph(M):  # phone link
    return f'<a class="tel" href="tel:{M["tel"]}">{M["phone"]}</a>'

# ---------- registry ----------
PAGES = {}  # path (no .html) -> dict

def page(M, path, title, lede, body, img=None, chips=None, eyebrow=None, landing=False, nohero=False, desc=None, jsonld=None):
    """path like 'us/services/dementia-care' (M may be None for root pages)."""
    PAGES[path] = dict(M=M, title=title, lede=lede, body=body, img=img, chips=chips or [], eyebrow=eyebrow,
                       landing=landing, nohero=nohero, desc=desc, jsonld=jsonld or [])

# ---------- navigation ----------
SERVICES = [  # slug, name, one-line promise, from-rate key, image
    ("dementia-care", "Dementia care", "Care that knows who they are, not only what they need.", "dementia", "elder-care"),
    ("personal-care", "Personal care", "Help with bathing and dressing that protects their dignity.", "personal", "bathroom"),
    ("companion-care", "Companion care", "Someone to talk to, walk with and cook alongside.", "companion", "two-women"),
    ("respite-care", "Respite care", "Take a break without worrying.", "companion", "tea-woman"),
    ("after-hospital", "Care after hospital", "Home from hospital. Care starting in 72 hours.", "personal", "hospital"),
    ("24-7-care", "24/7 and live-in care", "Around-the-clock care with a team, not one tired person.", "overnight", "moon-house"),
    ("care-from-afar", "Care from afar", "Live far away? Be there anyway.", "dementia", "video-call"),
]

def nav_links(M):
    p = M["p"]
    return [("Services", f"/{p}/services/index.html"), ("Family app", f"/{p}/app.html"), ("Pricing", f"/{p}/pricing.html"),
            (M["pay"][1], M["pay"][0]), ("Our promises", f"/{p}/promises.html"), ("About", f"/{p}/about.html"),
            ("Resources", f"/{p}/resources/index.html"), ("Careers", f"/{p}/careers.html")]

def other_market_path(path):
    if not path.startswith(("us/", "au/")): return None
    o = ("au/" if path.startswith("us/") else "us/") + path[3:]
    swap = {"us/paying-for-care": "au/funding", "au/funding": "us/paying-for-care"}
    o = swap.get(path, o)
    return o if o in PAGES else ("au/index" if path.startswith("us/") else "us/index")

def header(M, path):
    p = M["p"]
    links = "".join(f'<a href="{h}"{" class=on" if h.endswith(path.split("/",1)[1] + ".html") or (path.split("/")[1:2] == [h.split("/")[2]] and h.split("/")[2] in ("services", "resources")) else ""}>{t}</a>' for t, h in nav_links(M))
    sv = "".join(f'<a href="/{p}/services/{s}.html"><b>{n}</b><span>{d}</span></a>' for s, n, d, _, _ in SERVICES)
    om = other_market_path(path)
    mk = (f'<div class="mkt" role="group" aria-label="Country"><a href="/{path}.html" class="on" aria-current="true">{M["flag"]}</a>'
          f'<a href="/{om}.html" hreflang="{"en-AU" if p == "us" else "en-US"}">{"AU" if p == "us" else "US"}</a></div>')
    return (f'<a class="skip" href="#main">Skip to content</a>'
            f'<div class="util"><div class="w"><span>{M["lic_short"]} &middot; <button class="lic-tip" type="button" aria-describedby="lictip">Do I need a license number to trust you?</button>'
            f'<span role="tooltip" id="lictip">Yes, ask for it. A licensed agency must show it, and you can check it yourself on the <a href="{M["regulator"][1]}" target="_blank" rel="noopener">{M["regulator"][0]}</a> site. Ours is shown in the footer of every page.</span></span>'
            f'<span class="u-r">{M["hours"].split(".")[0]} &middot; {ph(M)}</span></div></div>'
            f'<nav class="top" aria-label="Main"><div class="w"><a class="logo" href="/{p}/index.html" aria-label="{BRAND} home"><i>e</i><b>{BRAND}</b><small>{TAG}</small></a>'
            f'<div class="links"><div class="dd"><a href="/{p}/services/index.html" class="ddt">Services</a><div class="ddm">{sv}<a class="all" href="/{p}/services/index.html">All services &rsaquo;</a></div></div>{links.split("</a>",1)[1]}</div>'
            f'{mk}<a class="ncall" href="tel:{M["tel"]}" aria-label="Call {M["phone"]}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg><span>{M["phone"]}</span></a>'
            f'<a class="cta" href="/{p}/book.html">{"Book a free assessment" if M["live"] else "Join the waitlist"}</a>'
            f'<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><i></i><i></i></button></div><div id="prog"></div>'
            f'<div class="mnav" id="mnav" hidden>{sv}{"".join(f"<a href={chr(34)}{h}{chr(34)}>{t}</a>" for t, h in nav_links(M)[1:])}'
            f'<a class="btn" href="/{p}/book.html">{"Book a free assessment" if M["live"] else "Join the waitlist"}</a> <a class="btn o" href="tel:{M["tel"]}">Call {M["phone"]}</a></div></nav>')

def footer(M):
    p = M["p"]
    cols = [("Care", [(n, f"/{p}/services/{s}.html") for s, n, _, _, _ in SERVICES]),
            ("Plan", [("Pricing and estimator", f"/{p}/pricing.html"), M["pay"][::-1], ("Care needs quiz", f"/{p}/care-quiz.html"),
                      ("Book " + ("a free assessment" if M["live"] else "the waitlist"), f"/{p}/book.html"), ("Hospital and professional referrals", f"/{p}/refer.html")]),
            ("Trust", [("Our promises", f"/{p}/promises.html"), ("Licensing, insurance and safety", f"/{p}/trust.html"), ("Care team", f"/{p}/team.html"),
                       ("Reviews", f"/{p}/reviews.html"), ("About", f"/{p}/about.html")]),
            ("More", [("Family app", f"/{p}/app.html"), ("Resources", f"/{p}/resources/index.html"), ("Careers", f"/{p}/careers.html"),
                      ("Locations", f"/{p}/locations/index.html"), ("Photo gallery", f"/{p}/gallery.html"), ("Client login", f"/{p}/login.html")]),
            ("Legal", [("Privacy policy", f"/{p}/privacy.html"), ("Terms", f"/{p}/terms.html"), ("Accessibility statement", f"/{p}/accessibility.html")]
                      + ([("Complaints", f"/{p}/complaints.html")] if p == "au" else [("Health privacy notice", f"/{p}/privacy.html#health")]))]
    c = "".join(f'<div><h4>{h}</h4>' + "".join(f'<a href="{u}">{t}</a>' for t, u in L) + "</div>" for h, L in cols)
    return (f'<footer><div class="w"><div class="fcall"><div><p class="ey">Talk to a person</p><h2>{ph(M)}</h2><p>{M["hours"]}.</p></div>'
            f'<div><a class="btn" href="/{p}/book.html">{"Book a free care assessment" if M["live"] else "Join the waitlist"}</a> <a class="btn o" href="sms:{M["sms"]}">Text us</a></div></div>'
            f'<div class="cols">{c}</div>'
            f'<div class="lic"><b>{BRAND}</b> &middot; {M["addr"]} &middot; {ph(M)} &middot; {M["lic"]} '
            f'<a href="{M["regulator"][1]}" target="_blank" rel="noopener">Check us with the {M["regulator"][0]}</a>.</div>'
            f'<p class="fine">{BRAND} provides non-medical in-home care. Information on this site is general, is not medical advice and does not replace advice from your doctor. '
            f'Photos are stock images from Unsplash used for illustration; they do not show our clients or staff. Reviews and results are only shown when they are real.</p>'
            f'<p class="fine">&copy; 2026 {BRAND}. <a href="/index.html">Change country</a></p></div></footer>')

def landing_header(M):
    return (f'<nav class="top lp" aria-label="Brand"><div class="w"><span class="logo"><i>e</i><b>{BRAND}</b><small>{TAG}</small></span>'
            f'<a class="ncall big" href="tel:{M["tel"]}"><span>Call {M["phone"]}</span></a></div></nav>')

def landing_footer(M):
    return (f'<footer class="lpf"><div class="w"><p>{BRAND} &middot; {M["addr"]} &middot; {ph(M)}</p><p class="lic">{M["lic"]}</p>'
            f'<p><a href="/{M["p"]}/privacy.html">Privacy</a> &middot; <a href="/{M["p"]}/terms.html">Terms</a></p></div></footer>')

def sticky(M):
    p = M["p"]
    return (f'<div class="sbar" aria-label="Quick contact"><a href="tel:{M["tel"]}" class="pulse">Call now</a><a href="sms:{M["sms"]}">Text</a>'
            f'<a href="/{p}/book.html" class="pri">{"Free assessment" if M["live"] else "Waitlist"}</a></div>' + CHAT(M))

# ---------- interactive components (behaviour in assets/ec.js) ----------
def WORDS(text, tag="h1", cls=""):
    """Word-by-word headline reveal."""
    w = " ".join(f'<span style="--i:{i}">{x}</span>' for i, x in enumerate(text.split()))
    return f'<{tag} class="words {cls}" aria-label="{html.escape(re.sub("<[^>]+>", "", text))}">{w}</{tag}>'

def CARECARD(M, events=None, title="Live care card", who="Dad"):
    ev = events or [("9:02 am", f"Maria arrived &middot; GPS check-in"), ("9:40 am", "Breakfast eaten, all of it"), ("10:15 am", "Fluids: 2 glasses of water"),
                    ("11:05 am", "Walk in the garden, 20 minutes"), ("12:30 pm", "Lunch eaten"), ("1:10 pm", "Mood: calm &middot; listened to Sinatra"),
                    ("2:00 pm", "Photo shared with the family circle"), ("3:58 pm", "Afternoon routine started early, as planned")]
    li = "".join(f'<li><time>{t}</time><span>{e}</span></li>' for t, e in ev)
    return (f'<div class="ccard" aria-live="off"><div class="cc-h"><i class="live"></i><b>Maria is with {who} now</b><small>Demo &middot; sample data</small></div>'
            f'<ol class="cc-l">{li}</ol><div class="cc-f"><span>Weekly update every Sunday</span><span>{title}</span></div></div>')

def SITU(M):
    m = M["mom"]
    cards = [("dementia", f"My {m} or {M['dad']} has dementia", "Specialist training, a routine they recognise and a Life Story profile for every visit.", "elder-care"),
             ("afar", "I live far away", "A named Care Director, a live app and a weekly update, so you are there even when you cannot be.", "video-call"),
             ("hospital", "We are coming home from hospital", "Care starting within 72 hours, coordinated with the discharge team.", "hospital")]
    c = "".join(f'<button class="sit" type="button" data-sit="{k}" aria-pressed="false" style="--bg:url(/img/{im}.jpg)"><span><b>{t}</b><em>{d}</em></span></button>' for k, t, d, im in cards)
    return f'<div class="sits" role="group" aria-label="Choose your situation">{c}</div><p class="sit-note" aria-live="polite"></p>'

def FOR(sit, inner):
    """Content shown/highlighted for a situation (dementia|afar|hospital)."""
    return f'<div class="for" data-for="{sit}">{inner}</div>'

def PROMISES(M, link=True):
    p = M["p"]
    items = [("72", "-hour", "Care starts within 72 hours of signing"), ("48", "-hour", "Replacement caregiver, already introduced"),
             ("15", "-minute", "Call back in business hours"), ("2", " to 3", f"The same small team of {M['cgs']}"),
             ("1", " update", "Every week to the family, plus a monthly call"), ("24", "/7", "A human answers the phone")]
    if not M["live"]:
        items[5] = ("12", " hours", "Advisors available 8am to 8pm, every day")
    t = "".join(f'<a class="prom reveal" style="--i:{i}" href="/{p}/promises.html#p{i}"><b><span class="cnt" data-to="{a}" data-dec="0" data-pre="" data-suf="" data-comma="0">{a}</span><small>{b}</small></b><span>{c}</span><em>See how we measure it &rsaquo;</em></a>'
                for i, (a, b, c) in enumerate(items))
    return f'<div class="proms">{t}</div>'

def PATH(steps):
    """Steps joined by a line that draws as you scroll. steps: (title, text, img)."""
    li = "".join(f'<li class="ps"><i>{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div>' + (f'<img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy">' if im else "") + '</li>' for i, (t, d, im) in enumerate(steps))
    return f'<ol class="path"><i class="pl" aria-hidden="true"></i>{li}</ol>'

def SERVICE_GRID(M, only=None):
    p = M["p"]
    cards = []
    for i, (s, n, d, rk, im) in enumerate(SERVICES):
        if only and s not in only: continue
        tags = {"dementia-care": "dementia", "care-from-afar": "afar", "after-hospital": "hospital"}.get(s, "")
        cards.append(f'<a class="svc tilt reveal" style="--i:{i}" href="/{p}/services/{s}.html" data-tags="{tags}"><img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy">'
                     f'<span class="rec">Suggested for you</span><div><h3>{n}</h3><p>{d}</p><small>From {money(M, M["rates"][rk])}{"/night" if rk == "overnight" else "/hour"}</small><em>See what is included &rsaquo;</em></div></a>')
    return f'<div class="svcs">{"".join(cards)}</div>'

def PHONE(M, screens):
    """Pinned phone scroll. screens: (title, text, screen_html)."""
    sc = "".join(f'<div class="scr{" on" if i == 0 else ""}">{h}</div>' for i, (_, _, h) in enumerate(screens))
    st = "".join(f'<div class="pst" data-i="{i}"><p class="ey">{i + 1} of {len(screens)}</p><h3>{t}</h3><p>{d}</p></div>' for i, (t, d, _) in enumerate(screens))
    return (f'<div class="pin"><div class="pin-ph"><div class="phone"><div class="notch"></div><div class="pbar"><span>9:41</span><span>{BRAND}</span></div>{sc}</div>'
            f'<p class="demo-l">Demo family &middot; sample data</p></div><div class="pin-st">{st}</div></div>')

def APPSCREENS(M):
    cg = M["Cg"]
    s1 = ('<div class="as"><div class="as-st"><i class="live"></i><b>Maria is with Dad now</b><small>Checked in 9:02 am &middot; GPS verified</small></div>'
          '<div class="as-r"><span>Today</span><b>9:00 am to 3:00 pm</b></div><div class="as-r"><span>Backup ' + M["cg"] + '</span><b>James (met Dad on 3 Oct)</b></div>'
          '<div class="as-r"><span>Next visit</span><b>Tomorrow 9:00 am, Maria</b></div><div class="as-btn">Message the care team</div></div>')
    s2 = ('<div class="as"><h5>Care note &middot; 11:20 am</h5>' + "".join(f'<div class="as-r"><span>{a}</span><b>{b}</b></div>' for a, b in
          [("Mood", "Calm, chatty"), ("Meals", "Breakfast, all"), ("Fluids", "3 glasses"), ("Sleep (reported)", "Woke once"), ("Activity", "Garden walk, 20 min"), ("Bathroom", "Normal")]) +
          '<p class="as-n">Talked about his years at the shipyard. Laughed at the old photos. No concerns today.</p></div>')
    bars = "".join(f'<i style="--h:{h}%"></i>' for h in [62, 70, 66, 74, 78, 72, 80, 84, 76, 82, 86, 88, 84, 90])
    s3 = (f'<div class="as"><h5>Mood trend &middot; 2 weeks</h5><div class="as-ch">{bars}</div><div class="as-r"><span>Hydration</span><b>On track</b></div>'
          '<div class="as-r"><span>Meals</span><b>Steady</b></div><div class="as-flag">Pattern change: shorter sleep 3 nights running. Your care manager will call you today.</div></div>')
    s4 = ('<div class="as"><h5>Photos</h5><div class="as-ph"><img src="/img/flowers.jpg" alt="" loading="lazy"><img src="/img/puzzle.jpg" alt="" loading="lazy">'
          '<img src="/img/tea-book.jpg" alt="" loading="lazy"><img src="/img/piano3.jpg" alt="" loading="lazy"></div><p class="as-n">Shared only when Dad and the family have agreed.</p></div>')
    s5 = ('<div class="as"><h5>Family circle</h5><div class="msg in"><b>Maria</b>He asked about the dog today, so we looked at photos of Rex together.</div>'
          '<div class="msg out"><b>You</b>Thank you. He will love that. Can we move Thursday to 10?</div><div class="msg in"><b>Care manager</b>Done. Thursday is 10:00 to 4:00 now.</div>'
          '<div class="as-btn">Start a video call</div></div>')
    return [("Visit status", f"See who is with them, when they arrived and who the backup {M['cg']} is. If a visit is late, you hear about it before you notice.", s1),
            ("Care notes", "A short structured note every visit: mood, meals, fluids, sleep, activity, bathroom and any concern. A weekly digest and a PDF for the doctor.", s2),
            ("Trends", "Charts over weeks so you see change early. A gentle flag prompts a call from the care manager, never a diagnosis.", s3),
            ("Photos", "Moments from a good day, shared only with consent.", s4),
            ("Messages and family circle", "Brothers, sisters and grandchildren in one thread with the care team, each with their own permissions.", s5)]

def ACC(items, search=False, id="acc"):
    """Accordion; items (q, a). search=True adds a filter box. Emits FAQPage JSON-LD."""
    s = (f'<label class="fsearch"><span>Search the questions</span><input type="search" placeholder="Try: cost, dementia, start" data-filter="{id}"></label>' if search else "")
    d = "".join(f'<details class="acc reveal"><summary>{q}</summary><div>{a}</div></details>' for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": re.sub("<[^>]+>", "", q),
          "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}
    return f'{s}<div class="accs" id="{id}">{d}<p class="nores" hidden>No question matches. Call us and ask a person.</p></div><script type="application/ld+json">{json.dumps(ld)}</script>'

def EST(M, mini=False):
    r = M["rates"]
    tiers = [("companion", "Companion care"), ("personal", "Personal care"), ("dementia", "Dementia specialist")]
    opts = "".join(f'<option value="{r[k]}"{" selected" if k == "dementia" else ""}>{n} (from {M["sym"]}{r[k]}/hour)</option>' for k, n in tiers)
    cities = "".join(f'<option value="{f}">{c}</option>' for c, f in M["cities"])
    extra = "" if mini else ('<label class="chk"><input type="checkbox" data-est="wknd"> <span>Weekend or holiday hours included (about 15% more for those hours)</span></label>'
                             '<label class="chk"><input type="checkbox" data-est="night"> <span>Add sleep-over nights (priced per night)</span></label>'
                             '<label class="rng" data-show="night"><span>Nights per week <output data-o="nights">2</output></span><input type="range" min="1" max="7" value="2" data-est="nights"></label>')
    note = ("Estimates for private-pay care, in US dollars, before any long-term care insurance or veterans' benefit. Not a quote: your price is confirmed in writing after the free assessment. "
            "Not included: nursing, medical equipment, mileage over 20 miles a week."
            if M["p"] == "us" else
            "General information in Australian dollars, GST-aware wording. If you have a Support at Home budget, most of the cost comes from your budget and you pay a contribution; see the funding page. "
            "Private-pay prices are confirmed in writing after the assessment.")
    return (f'<div class="est" data-sym="{M["sym"]}" data-night="{r["overnight"]}"><div class="est-in">'
            f'<label class="rng"><span>Hours per week <output data-o="hours">20</output></span><input type="range" min="4" max="84" step="2" value="20" data-est="hours"></label>'
            f'<label><span>Type of care</span><select data-est="rate">{opts}</select></label>'
            f'<label><span>{"City" if M["p"] == "us" else "Area"}</span><select data-est="city">{cities}</select></label>{extra}</div>'
            f'<div class="est-out"><span class="k">Estimated monthly cost</span><b class="est-v">{M["sym"]}0</b><span class="est-r"></span>'
            f'<div class="est-bar"><i></i></div><p>{note}</p><a class="btn" href="/{M["p"]}/book.html">{"Book a free assessment for an exact price" if M["live"] else "Join the waitlist"}</a></div></div>')

def FLIP(cards):
    """cards: (img, front_title, front_sub, back_html)."""
    c = "".join(f'<button class="flip reveal" style="--i:{i}" type="button" aria-pressed="false"><span class="fr"><img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy"><b>{t}</b><em>{s}</em><small>Tap to turn over</small></span>'
                f'<span class="bk">{b}</span></button>' for i, (im, t, s, b) in enumerate(cards))
    return f'<div class="flips">{c}</div>'

def CTA(M, h="You do not have to work this out alone.", t=None, img="hands-care"):
    p = M["p"]
    t = t or f"Call {M['phone']} and a care advisor will listen first, then tell you plainly what we would do and what it would cost."
    return (f'<section class="cta-f reveal" style="--bg:url(/img/{img}.jpg)"><div><p class="ey">Next step</p><h2>{h}</h2><p>{t}</p>'
            f'<p class="cta-b"><a class="btn big pulse" href="tel:{M["tel"]}">Call {M["phone"]}</a> <a class="btn o big" href="/{p}/book.html">{"Book a free assessment" if M["live"] else "Join the waitlist"}</a> '
            f'<a class="btn ghost big" href="sms:{M["sms"]}">Text us</a></p></div></section>')

def STAGES(M):
    st = [("Early stage", "They are mostly independent but miss appointments, repeat questions and lose track of bills or medicines.",
           ["Companion visits 2 to 3 times a week", "Help with appointments, shopping and medication reminders", "Start the Life Story profile while they can tell it themselves", "Family coaching session"], "8 to 15 hours a week", "man-photos"),
          ("Middle stage", "Daily routines get harder. Confusion in the late afternoon, wandering, missed meals and trouble with bathing are common.",
           ["Daily visits with the same 2 to 3 " + M["cgs"], "Personal care with dignity", "Sundowning plan and a home safety walk-through", "Door sensors and an emergency contact ladder"], "20 to 50 hours a week", "elder-hands2"),
          ("Late stage", "They need help with almost everything, may speak little, and comfort, touch and familiar music matter most.",
           ["Long shifts or 24/7 care with a team", "Transfers, skin care and comfort", "Close work with nurses, hospice or palliative teams", "Respite for the family carer"], "50 hours a week to 24/7", "hands-young")]
    panels = "".join(f'<div class="stg{" on" if i == 0 else ""}" data-i="{i}"><img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy"><div><h3>{t}</h3><p>{d}</p>'
                     f'<ul class="ticks">{"".join(f"<li>{x}</li>" for x in L)}</ul><p class="hrs"><span>Typical starting hours</span><b>{h}</b></p></div></div>' for i, (t, d, L, h, im) in enumerate(st))
    return (f'<div class="stages"><label class="stg-l"><span>Drag to move through the stages</span><input type="range" min="0" max="2" step="1" value="0" aria-valuetext="Early stage" data-stage></label>'
            f'<div class="stg-tl"><span>Early</span><span>Middle</span><span>Late</span><i></i></div>{panels}'
            f'<p class="cn">Every person is different and stages overlap. This is general guidance, not a medical assessment. Talk to their doctor about diagnosis and treatment.</p></div>')

def DAYARC(points):
    """Calm morning-to-evening arc. points: (time, text)."""
    n = len(points)
    dots = "".join(f'<li style="--x:{i / (n - 1) * 100:.1f}%;--i:{i}"><time>{t}</time><span>{x}</span></li>' for i, (t, x) in enumerate(points))
    return (f'<div class="arc reveal"><svg viewBox="0 0 1000 220" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="sky" x1="0" x2="1"><stop offset="0" stop-color="#ffd9a8"/>'
            f'<stop offset=".5" stop-color="#ffe9c9"/><stop offset="1" stop-color="#29495a"/></linearGradient></defs><rect width="1000" height="220" fill="url(#sky)" opacity=".55"/>'
            f'<path d="M0 200 Q500 -60 1000 200" class="arcp" pathLength="1"/><circle class="sun" r="16" cx="0" cy="200"/></svg><ol>{dots}</ol></div>')

def CAL(M):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cells = "".join(f'<button type="button" class="cd" aria-pressed="false" data-d="{w * 7 + d}"><small>{days[d]}</small><b>{w * 7 + d + 1}</b><span></span></button>' for w in range(4) for d in range(7))
    return (f'<div class="resp"><div class="resp-in"><label class="rng"><span>How worn out do you feel? <output data-o="tired">6</output>/10</span>'
            f'<input type="range" min="1" max="10" value="6" data-resp="tired"></label><p class="resp-s" aria-live="polite"></p>'
            f'<div class="resp-blocks" role="group" aria-label="Break length">{"".join(f"<button type=button data-blk={chr(34)}{h}{chr(34)} aria-pressed={chr(34)}{str(i == 1).lower()}{chr(34)}>{t}</button>" for i, (h, t) in enumerate([("4", "4-hour break"), ("8", "Full day"), ("12", "Overnight")]))}</div>'
            f'<p class="resp-t">Tap the days you want off. <b class="resp-sum">0 breaks, 0 hours</b> &middot; about <b class="resp-cost">{M["sym"]}0</b> this month</p></div>'
            f'<div class="cal" data-rate="{M["rates"]["companion"]}" data-sym="{M["sym"]}">{cells}</div></div>')

def COUNT72(M):
    steps = [("Hour 0", "You call or the discharge planner refers. A care advisor answers."), ("Hour 2", "We speak to the discharge team about medicines, mobility and follow-up appointments."),
             ("Hour 12", "A care manager visits the hospital or home for the assessment."), ("Hour 24", "Care plan agreed, home safety check booked, first-week plan written."),
             ("Hour 48", f"You meet your {M['cg']} and the backup {M['cg']}."), ("Hour 72", "First visit. The family app goes live.")]
    li = "".join(f'<li><label><input type="checkbox" data-c72> <b>{a}</b> <span>{b}</span></label></li>' for a, b in steps)
    return (f'<div class="c72"><div class="c72-r"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" class="tr"/><circle cx="60" cy="60" r="50" class="c72-f" pathLength="100"/></svg>'
            f'<div><b class="c72-h">72</b><span>hours to go</span></div></div><ol class="c72-l">{li}</ol></div>'
            '<p class="cn">Tick the steps to see the clock fill. The 72-hour start applies once a care agreement is signed and is subject to the assessment; we publish how often we meet it.</p>')

def DAYNIGHT(M):
    shifts = [("7am to 3pm", "Day shift", "Awake. Breakfast, personal care, outings, lunch, the afternoon routine."),
              ("3pm to 11pm", "Evening shift", "Awake. Sundowning plan, dinner, bath, a calm wind-down."),
              ("11pm to 7am", "Night shift", "Awake or sleep-over. Toileting help, repositioning, reassurance after a bad dream.")]
    return ('<div class="dn24"><div class="sky" aria-hidden="true"><i class="sun"></i><i class="moon"></i><span class="stars"></span><span class="hz"></span></div>'
            '<div class="dn-sh">' + "".join(f'<div class="reveal" style="--i:{i}"><small>{a}</small><h3>{b}</h3><p>{c}</p></div>' for i, (a, b, c) in enumerate(shifts)) + '</div></div>')

def ZOOM(M):
    far = "sydney2" if M["p"] == "au" else "tampa-river"
    layers = [(far, "Wherever you are"), ("melb-homes" if M["p"] == "au" else "au-suburb", f"Their {'suburb' if M['p'] == 'au' else 'neighborhood'}"), ("porch", "Their street"), ("porch2", "Their front door")]
    l = "".join(f'<div class="zl" style="--bg:url(/img/{im}.jpg);--i:{i}"><span>{t}</span></div>' for i, (im, t) in enumerate(layers))
    return f'<div class="zoom"><div class="zoom-st">{l}<div class="zoom-card">{CARECARD(M)}</div></div></div>'

def QUIZ(M):
    qs = [("Who needs care?", ["My parent", "My partner", "Another relative or friend", "Me"]),
          ("How is their memory?", ["No real concerns", "Some forgetting, still managing", "Diagnosed with dementia", "Confused most days"]),
          ("How much help do they need with washing and dressing?", ["None", "Reminders or a little help", "Hands-on help most days", "Help with everything"]),
          ("Have there been safety worries in the last 3 months?", ["None", "A near miss", "A fall or getting lost", "More than one incident"]),
          ("How are meals and drinking?", ["Fine", "Skipping some meals", "Losing weight or not drinking enough", "Needs help to eat"]),
          ("Who helps them now?", ["Nobody regularly", "Family nearby, a few hours a week", "Family most days and getting tired", "One person, around the clock"]),
          ("Where do you live?", ["Same house", "Within 30 minutes", "Hours away", "Another state or country"]),
          ("What is happening right now?", ["Planning ahead", "Things are getting harder", "Coming home from hospital soon", "A crisis this week"])]
    qh = "".join(f'<fieldset class="qq{" on" if i == 0 else ""}" data-q="{i}"><legend>{q}</legend>' + "".join(f'<button type="button" class="qa" data-v="{j}">{a}</button>' for j, a in enumerate(o)) + "</fieldset>" for i, (q, o) in enumerate(qs))
    return (f'<div class="quiz" data-p="{M["p"]}" data-cg="{M["cg"]}" data-live="{1 if M["live"] else 0}"><div class="qz-top"><svg viewBox="0 0 44 44" class="qz-ring"><circle cx="22" cy="22" r="18" class="tr"/><circle cx="22" cy="22" r="18" class="qz-f" pathLength="100"/></svg>'
            f'<span class="qz-c">Question 1 of 8</span><button type="button" class="qz-back" hidden>Back</button></div>{qh}<div class="qz-res" hidden></div></div>'
            '<p class="cn">This quiz suggests a starting plan. It is not a medical or care assessment and does not replace advice from a doctor. Nothing you choose here is sent anywhere unless you ask us to contact you.</p>')

def BOOK(M, compact=False, kind="assessment"):
    p = M["p"]
    title = "Book a free care assessment" if M["live"] else "Join the waitlist"
    slots = "" if (compact or not M["live"]) else ('<fieldset class="slots"><legend>Pick a time in the next 24 hours</legend><div class="slot-g" data-slots></div>'
                                                   '<p class="cn">Times are requests. A care advisor confirms by phone within 15 minutes during business hours.</p></fieldset>')
    who = ("Who needs care?", ["My mother", "My father", "Both parents", "My partner", "Someone else"])
    return (f'<form class="book" data-mail="{MAIL}" data-kind="{kind}" data-market="{M["country"]}" novalidate><div class="bk-bar"><i></i></div>{slots}'
            f'<label><span>Your name</span><input name="name" autocomplete="name" required></label>'
            f'<label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required></label>'
            f'<label><span>{who[0]}</span><select name="who" required><option value="">Choose</option>{"".join(f"<option>{o}</option>" for o in who[1])}</select></label>'
            + ('' if compact else f'<label class="chk"><input type="checkbox" name="call15"> <span>Call me in 15 minutes instead (business hours)</span></label>') +
            f'<label class="chk small"><input type="checkbox" name="consent" required> I agree to be contacted by phone{" and text" if p == "us" else ", SMS"} about this request. Consent is not a condition of any purchase. '
            f'<a href="/{p}/privacy.html">Privacy policy</a>.</label>'
            f'<button class="btn big" type="submit">{title}</button><p class="bk-err" role="alert"></p>'
            f'<div class="bk-ok" hidden tabindex="-1"><img src="/img/woman-glasses.jpg" alt="" class="adv"><div><h3>Thank you. Your request is ready to send.</h3>'
            f'<p>Your email app has opened with the details. Press send and a care advisor will call you{" within 15 minutes during business hours" if M["live"] else " by the next business day"}. '
            f'If it is urgent, call <a href="tel:{M["tel"]}">{M["phone"]}</a> now.</p><p class="cn">Illustrative photo. Your advisor\'s real name and photo will appear here once our team is in place.</p></div></div></form>')

def CHAT(M):
    p = M["p"]
    qa = [("What does it cost?", f"Our care starts from {money(M, M['rates']['companion'])} an hour for companion care. The <a href='/{p}/pricing.html'>estimator</a> shows a monthly range in seconds."),
          ("How fast can you start?", "Within 72 hours of signing, once the free assessment is done." if M["live"] else "We are not yet providing care in Australia. Join the waitlist and we will explain your options, including Support at Home."),
          ("Do you do dementia care?", "Yes. It is what we specialise in. Every " + M["cg"] + " completes our dementia training before their first visit."),
          ("Is it a medical emergency?", "Please call " + ("911" if p == "us" else "000") + " now. This assistant cannot help with emergencies or give medical advice.")]
    b = "".join(f'<button type="button" class="cq" data-a="{html.escape(a)}">{q}</button>' for q, a in qa)
    return (f'<div class="chat"><button class="chat-b" type="button" aria-expanded="false" aria-controls="chatp"><span>Talk to a care advisor</span></button>'
            f'<div class="chat-p" id="chatp" hidden role="dialog" aria-label="Care advisor"><div class="chat-h"><b>Care advisor</b><small>{"A person replies 8am to 8pm. After hours, an assistant answers common questions." if M["live"] else "Waitlist questions, 8am to 8pm AEST"}</small><button type="button" class="chat-x" aria-label="Close">&times;</button></div>'
            f'<div class="chat-l" aria-live="polite"><p class="cm bot">Hello. What would you like to know? I never give medical advice, and you can always talk to a person.</p></div><div class="chat-q">{b}</div>'
            f'<div class="chat-f"><a class="btn" href="tel:{M["tel"]}">Call a person</a> <a class="btn o" href="sms:{M["sms"]}">Text us</a></div></div></div>')

def TICKS(items, cls=""):
    return f'<ul class="ticks tick-in {cls}">' + "".join(f'<li style="--i:{i}">{x}</li>' for i, x in enumerate(items)) + "</ul>"

def NOTCOVER(items):
    return '<div class="notc reveal"><h3>What this does not cover</h3>' + UL(items) + "</div>"

def SUMMARY(text):
    """Quotable answer-first summary box."""
    return f'<div class="sumbox reveal"><p class="ey">The short answer</p><p>{text}</p></div>'

def PRINT():
    return '<button class="btn o printb" type="button" onclick="window.print()">Print a one-page summary</button>'

def CAROUSEL(slides, label="Stories"):
    """slides: (img, title, text). Auto-advances slowly with a visible pause button."""
    s = "".join(f'<figure class="cs{" on" if i == 0 else ""}"><img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy"><figcaption><b>{t}</b>{x}</figcaption></figure>' for i, (im, t, x) in enumerate(slides))
    dots = "".join(f'<button type="button" aria-label="Show {i + 1}"{" aria-current=true" if i == 0 else ""}></button>' for i in range(len(slides)))
    return (f'<div class="car" aria-roledescription="carousel" aria-label="{label}">{s}<div class="car-c"><button type="button" class="car-p" aria-pressed="false">Pause</button>'
            f'<div class="car-d">{dots}</div></div></div>')

def PINS(pins, img):
    """pins: (x%, y%, name, status, link)."""
    p = "".join(f'<a class="pin-m" href="{l}" style="left:{x}%;top:{y}%;--i:{i}"><i></i><span><b>{n}</b>{s}</span></a>' for i, (x, y, n, s, l) in enumerate(pins))
    return f'<div class="pins reveal" style="--bg:url(/img/{img}.jpg)">{p}</div>'

def DIALS(items):
    """items: (pct, label, sub)."""
    return '<div class="dials">' + "".join(
        f'<div class="dial reveal" style="--i:{i}"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="48" class="tr"/><circle cx="60" cy="60" r="48" class="df" pathLength="100" style="--p:{p}"/></svg>'
        f'<b>{p}%</b><span>{l}</span><small>{s}</small></div>' for i, (p, l, s) in enumerate(items)) + "</div>"

def SAH():
    """Australia: Support at Home contribution explainer (general information)."""
    return ('<div class="sah"><div class="est-in">'
            '<label class="rng"><span>Your yearly Support at Home budget <output data-o="bud">$29,000</output></span><input type="range" min="11010" max="80137" step="500" value="29000" data-sah="bud"></label>'
            '<label><span>Pension status</span><select data-sah="pen"><option value="full">Full age pensioner</option><option value="part">Part pensioner or CSHC holder (rates vary by means)</option><option value="self">Self-funded retiree</option></select></label>'
            '<label class="rng"><span>Share of budget on personal care (independence) <output data-o="ind">50%</output></span><input type="range" min="0" max="100" step="5" value="50" data-sah="ind"></label>'
            '<p class="cn">The rest is treated as everyday living (cleaning, meals, shopping). Clinical care such as nursing carries no contribution.</p></div>'
            '<div class="est-out"><span class="k">Estimated yearly contribution</span><b class="sah-v">$0</b><span class="sah-r"></span><div class="est-bar"><i></i></div>'
            '<p>General information only, based on the standard rates for people entering Support at Home from 1 November 2025: full pensioners pay 5% for independence services and 17.5% for everyday living; '
            'self-funded retirees pay 50% and 80%; part pensioners pay in between, set by Services Australia. A lifetime cap applies. Budgets are indexed each July. '
            'Check your own figures with <a href="https://www.myagedcare.gov.au/" target="_blank" rel="noopener">My Aged Care</a>.</p></div></div>')

def ARTICLE_META(author="The " + BRAND + " care team", reviewed="Clinical review pending: no article is published as medical guidance until a qualified reviewer signs it off", date="21 November 2026"):
    return f'<p class="ameta"><span>Written by {author}</span><span>{reviewed}</span><span>Last updated {date}</span></p>'

# ---------- render ----------
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap" rel="stylesheet">'

import random as _random, os as _os2

def all_photos():
    d = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), "img")
    skip = {"skyway", "sydney", "au-suburb"}  # place photos are used deliberately elsewhere
    return sorted(f[:-4] for f in _os2.listdir(d) if f.endswith(".jpg") and f[:-4] in ALT and f[:-4] not in skip)

BAND_LINES = [("Care is a hundred small, good things.", "A hand held. A story remembered. A routine that fits them."),
              ("Home is where they know where everything is.", "Familiar rooms, familiar faces, one steady team."),
              ("Good days are made of ordinary moments.", "Tea in the right cup. A walk in the garden. Someone who listens."),
              ("They stay themselves. We keep them safe.", "Specialist care, shaped around the person they have always been.")]

def enrich(path, d):
    """Adds photo-rich sections (marquee strip, parallax band and gallery) to every content page."""
    body = d["body"]
    if d["landing"] or d["nohero"] is True or path.endswith(("/privacy", "/terms", "/accessibility", "/login", "/book", "/care-quiz")): return body
    rnd = _random.Random(path)
    pool = all_photos()
    pick = rnd.sample(pool, min(len(pool), 22))
    strip, band, gal = pick[:12], pick[12], pick[13:19]
    line = BAND_LINES[rnd.randrange(len(BAND_LINES))]
    block = BAND(band, line[0], line[1]) + GALLERY(gal)
    i = body.find("<h2", int(len(body) * .35))
    if i > 0: body = body[:i] + STRIP(strip) + body[i:]
    j = body.rfind('<section class="cta-f')
    return body[:j] + block + body[j:] if j > 0 else body + block

def relativize(h, depth):
    pre = "../" * depth
    def f(m):
        a, u = m.group(1), m.group(2)
        if u == "" or u.endswith("/"): u += "index.html"
        return f'{a}="{pre}{u}"'
    h = re.sub(r'(href|src|action)="/(?!/)([^"]*)"', f, h)
    h = h.replace("--bg:url(/img/", "--bg:url(../img/")  # custom-property urls resolve against assets/site.css
    return h.replace("url(/img/", f"url({pre}img/")

def render(path, d, v):
    M = d["M"]
    depth = path.count("/")
    d = dict(d, body=enrich(path, d)) if path != "index" else d
    title = d["title"]
    if path.endswith("/careers") and 'id="apply"' not in d["body"]:
        d = dict(d, body=d["body"].replace('<form class="book"', '<form id="apply" class="book"', 1))
    if path == "index":
        body_html = d["body"]; head_extra = ""
    else:
        if d["landing"]:
            top = ""
        elif d["nohero"] == "bare":
            top = ""
        elif d["nohero"]:
            top = f'<header class="phx"><div class="w"><p class="ey">{d["eyebrow"] or BRAND}</p><h1>{title}</h1><p class="lede">{d["lede"]}</p></div></header>'
        else:
            chips = d["chips"]
            hc = '<div class="hc">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in chips[:3]) + "</div>" if chips else ""
            top = (f'<header class="cine ec" style="--bg:url(/img/{d["img"] or "elder-care"}.jpg)"><div class="cb"></div><div class="sp"></div>{hc}'
                   f'<div class="cw"><p class="ey">{d["eyebrow"] or M["region"]}</p>{WORDS(title)}<p class="lede">{d["lede"]}</p>'
                   + (f'<div class="hb"><a class="btn big" href="#apply">Apply in 3 minutes</a> <a class="btn o big" href="#main">Read the job details</a></div></div></header>' if path.endswith("/careers") else
                   f'<div class="hb"><a class="btn big" href="/{M["p"]}/book.html">{"Book a free assessment" if M["live"] else "Join the waitlist"}</a> <a class="btn o big" href="tel:{M["tel"]}">Call {M["phone"]}</a></div></div></header>'))
        if d["landing"]:
            body_html = landing_header(M) + f'<main id="main" class="w lpm">{d["body"]}</main>' + landing_footer(M) + sticky(M)
        else:
            body_html = header(M, path) + top + f'<main id="main"{"" if d["nohero"] == "bare" else " class=w"}>{d["body"]}</main>' + footer(M) + sticky(M)
    desc = html.escape(re.sub(r"<[^>]+>", "", d["desc"] or d["lede"] or title))[:300]
    lang = M["lang"] if M else "en"
    alts = ""
    if M and not d["landing"]:
        o = other_market_path(path)
        same = o and o[3:] == path[3:]
        if same or path.endswith("index"):
            alts = (f'<link rel="alternate" hreflang="{M["lang"]}" href="{DOMAIN}/{path}.html"><link rel="alternate" hreflang="{"en-AU" if M["p"] == "us" else "en-US"}" href="{DOMAIN}/{o}.html">'
                    f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/">')
    lds = "".join(f'<script type="application/ld+json">{json.dumps(j)}</script>' for j in d["jsonld"])
    full = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(re.sub("<[^>]+>", "", title))}{"" if path == "index" else " | " + BRAND}</title><meta name="description" content="{desc}">'
            f'<link rel="canonical" href="{DOMAIN}/{"" if path == "index" else path + ".html"}">{alts}{"<meta name=robots content=noindex>" if d["landing"] else ""}'
            f'<meta name="theme-color" content="#0e4a4f"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%228%22 fill=%22%230e4a4f%22/%3E%3Ctext x=%2216%22 y=%2223%22 font-size=%2220%22 text-anchor=%22middle%22 fill=%22%23ffb199%22 font-family=%22Georgia%22%3Ee%3C/text%3E%3C/svg%3E">'
            f'{FONT}<link rel="stylesheet" href="/assets/site.css?v={v}">{lds}'
            '<script>document.documentElement.classList.add("js")</script></head>'
            f'<body class="g-elder m-{M["p"] if M else "root"}{" lp" if d["landing"] else ""}">{body_html}'
            f'<script src="/assets/site.js?v={v}" defer></script></body></html>')
    return relativize(full, depth)
