from ec import *

# ---------- root: market selector ----------
page(None, "index", f"{BRAND} | Dementia care at home in the United States and Australia", "",
     f'<main class="root-sel" id="main"><a class="logo" href="/index.html"><i>e</i><b>{BRAND}</b><small>{TAG}</small></a>'
     f'<h1 style="text-align:center;margin-top:26px;max-width:18ch">Where does your family need care?</h1>'
     f'<p class="lede" style="text-align:center">Prices, funding and rules are different in each country, so each has its own site.</p><p class="sugnote" aria-live="polite" style="font-weight:700;color:#1d1d1f"></p>'
     f'<div class="mcards"><a class="mcard" data-m="us" href="/us/index.html" hreflang="en-US" style="--bg:url(/img/skyway.jpg)"><div><span class="sg">Suggested for you</span><h2>United States</h2><p>Florida, starting in Tampa Bay. Private pay, long-term care insurance and veterans\' benefits explained.</p><span class="btn">Go to the US site</span></div></a>'
     f'<a class="mcard" data-m="au" href="/au/index.html" hreflang="en-AU" style="--bg:url(/img/sydney.jpg)"><div><span class="sg">Suggested for you</span><h2>Australia</h2><p>Waitlist and information. Support at Home funding explained step by step.</p><span class="btn">Go to the Australian site</span></div></a></div>'
     f'<p class="cn" style="margin-top:26px;text-align:center">Photos are illustrative stock images. &copy; 2026 {BRAND}.</p></main>',
     desc=f"{BRAND} dementia and in-home care. Choose the United States (Florida) or Australia.",
     jsonld=[{"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": DOMAIN}])

def home(M):
    p, m, cg, cgs = M["p"], M["mom"], M["cg"], M["cgs"]
    live = M["live"]
    slides = "".join(f'<div class="sl" style="background-image:url(/img/{n}.jpg);animation-delay:{i * 8}s"></div>' for i, n in enumerate(["elder-care", "two-women", "couple-dance", "elder-nurse"]))
    book = "Book a free care assessment" if live else "Join the waitlist"
    trust = (f'<span>{M["lic_short"]}</span><span>No Google rating shown until real families review us</span><span>{"Care starts within 72 hours" if live else "Support at Home explained honestly"}</span>')
    hero = (f'<header class="hero2">{slides}<canvas id="net"></canvas><div class="au"></div><div class="sp"></div><button class="hpause" type="button" aria-pressed="false">Pause</button><div class="w"><div>'
            f'<p class="ey">{"Dementia care at home in " + M["metro"] if live else "Coming to Australia: join the waitlist"}</p>'
            f'<h1>Dementia care your whole family can <span class="shim">see.</span></h1>'
            f'<p class="lede">Trained {cgs} at home, {"a start within 72 hours" if live else "a small team who knows them"}, and a live app so you always know how they are.</p>'
            f'<div class="hb"><a class="btn big" href="/{p}/book.html">{book}</a> <a class="btn o big" href="tel:{M["tel"]}">{"Call us now, any hour" if live else "Call a care advisor"}</a></div>'
            f'<div class="trust">{trust}</div></div>{CARECARD(M)}</div></header>')

    au_note = "" if live else CALL(f"<b>Where we are in Australia:</b> we are not yet a registered Support at Home provider and are not providing care yet. "
                                    f"This site explains how funding works and lets you join the waitlist. We will tell you plainly when we can start, and what it depends on.")

    body = (au_note +
        # 2. who is this for
        SECTION("Who is this for", "Tell us what is happening and we will show you the way.", "Choose the one closest to you. The page below changes to match, and we remember your choice.") +
        SITU(M) +
        FOR("dementia", SPLIT("elder-care", H3(f"When your {m} has dementia") + P(f"You want someone who does not rush them, who knows their story and who notices the small changes. "
              f"Every {cg} completes our dementia training before their first visit, and works in a team of two or three so your {m} sees familiar faces.") +
              TICKS(["A Life Story profile read before every visit", "A sundowning plan for the late afternoon", "A home safety walk-through", "Free family coaching on communication"]) +
              f'<p><a class="btn" href="/{p}/services/dementia-care.html">See dementia care</a></p>')) +
        FOR("afar", SPLIT("video-call", H3("When you live far away") + P("You get a named Care Director, a live app that shows each visit as it happens, a weekly update and a monthly video call. "
              "If something goes wrong, you hear within minutes, not days.") +
              TICKS(["GPS check-in and check-out for every visit", "Care notes, mood and meals in the app", "Emergency escalation to the family circle", "Errands: groceries, prescriptions, appointment rides"]) +
              f'<p><a class="btn" href="/{p}/services/care-from-afar.html">See care from afar</a></p>', flip=True)) +
        FOR("hospital", SPLIT("hospital", H3("When they are coming home from hospital") + P(f"The first week home is when things go wrong. We speak to the discharge team, check the home, and {'start care within 72 hours of signing' if live else 'explain what transition care and Support at Home can cover'}.") +
              TICKS(["A discharge checklist", "Medicines and follow-up appointments tracked", "Help with washing, dressing and meals", "A first-week plan the whole family can see"]) +
              f'<p><a class="btn" href="/{p}/services/after-hospital.html">See care after hospital</a></p>')) +
        # 3. promises
        f'<section class="band2"><p class="ey">Our promises</p><h2>Six promises we measure and publish.</h2>'
        f'<p>Anyone can say they care. We put numbers on it, name who owns each promise, and publish the results every month{" from our first full month of care" if live else " once we start"}.</p>{PROMISES(M)}</section>' +
        # 4. how it works
        SECTION("How it works", "From first call to first visit in four steps.") +
        PATH([("Free care assessment", f"A care manager visits at home or in hospital, meets your {m} and listens to the family. No cost and no obligation.", "couple-docs"),
              ("A personal care plan", "Written with you: routines, likes and dislikes, safety, the Life Story profile and the hours that make sense.", "man-photos"),
              ("Meet your team", f"You meet the main {cg} and a backup {cg} before day one, so a sick day never means a stranger.", "two-women"),
              ("Live updates", "Every visit is checked in on the family app, with notes, photos (with consent) and a weekly summary.", "woman-phone")]) +
        # 5. services
        SECTION("Services", "Care that matches the day they are having.", "Seven services, one team. Prices are starting rates; your exact price is in writing after the assessment.") +
        SERVICE_GRID(M) +
        STRIP(["two-women", "bake-three", "couple-path", "flowers", "puzzle", "grandpa-selfie", "tea-book", "couple-dance", "piano3", "man-dog"]) +
        # 6. app
        SECTION("The family app", "See care happen, from anywhere.", "Built for phones first, in large type, and simple enough for a 75-year-old sibling. Scroll to walk through it.") +
        PHONE(M, APPSCREENS(M)) +
        f'<p style="text-align:center"><a class="btn" href="/{p}/app.html">Take the full app tour</a></p>' +
        # 7. dementia difference
        f'<div class="split"><div class="sp-img reveal"><img class="px" data-px="0.06" src="/img/hands-young.jpg" alt="{alt("hands-young")}" loading="lazy"><span>Training is practised, not just watched.</span></div><div class="sp-tx reveal" style="--i:1">'
        f'<p class="ey">The dementia difference</p><h2 style="margin-top:0">Training that goes beyond the basics.</h2>' +
        ACC([("Calming communication", "<p>Short sentences, one question at a time, and never arguing with their reality. Our " + cgs + " learn to answer the feeling behind the words, so a question like 'when is Mum coming?' gets comfort, not a correction.</p><p class='cn'>Technique videos will be filmed with our own team and added here.</p>"),
             ("Sundowning", "<p>Late afternoon can bring restlessness and fear. We build a calm routine for that time with the family: light, sound, a snack, a familiar task and fewer visitors.</p>"),
             ("Wandering safety", "<p>A home walk-through, door sensors through partner products if the family wants them, an up-to-date photo on file and an emergency contact ladder that everyone knows.</p>"),
             ("Meals and hydration", "<p>Finger foods, coloured plates, offering drinks on a schedule and noting every glass in the app, because dehydration often shows up as more confusion.</p>"),
             ("Family coaching", "<p>A free session for relatives on what to say, what to stop saying and how to look after yourself. Families tell us this is the hour that changed the most.</p>")], id="dd") +
        '</div></div>' +
        # 8. reviews
        SECTION("Real families", "What families say.") +
        f'<div class="empty reveal"><h3>No reviews yet, and we will not invent any.</h3><p style="margin:8px auto">{"We are a new agency in " + M["metro"] + "." if live else "We are not providing care in Australia yet."} '
        f'When real families review us on Google, their words appear here, live, with the total count and our replies to every review, including the low ones.</p>'
        f'<p><a href="/{p}/reviews.html">Read our review policy &rsaquo;</a></p></div>' +
        # 9. cost
        SECTION("Cost made clear", "Know the cost before you call.", "Move the sliders. The estimate updates as you go.") +
        EST(M, mini=True) +
        f'<p style="text-align:center"><a href="/{p}/pricing.html">Full price list and detailed estimator &rsaquo;</a> &nbsp; <a href="{M["pay"][0]}">{M["pay"][1]} explained &rsaquo;</a></p>' +
        # 10. team
        SECTION("Meet the team", "The people who will be in their home.", f"We are hiring now. Real photos, first names and badges go here as each {cg} joins. Until then, here is what every one of them will have done. Photos are illustrative.") +
        FLIP([("elder-nurse", f"Dementia {cg}", "The core of every team", f"<b>What they have done</b><span>40 hours of dementia training before day one, then monthly refreshers.</span><div class=badges><i>Dementia trained</i><i>{'Level 2 screened' if live else 'Police check'}</i><i>First aid</i></div><span>Favourite part of the job, in their words, will go here.</span>"),
              ("elder-care", f"Senior {cg}", "Leads a small team", "<b>What they do</b><span>Trains newer team members on shift, covers when someone is sick and knows every client on their team.</span><div class=badges><i>2+ years' experience</i><i>Mentor</i></div>"),
              ("woman-glasses", "Care manager", "Your named contact", "<b>What they do</b><span>Runs the assessment, writes the care plan, calls the family every month and owns the promises for your family.</span><div class=badges><i>Care planning</i><i>Family coaching</i></div>"),
              ("elder-activity", "Activities lead", "Good days, on purpose", "<b>What they do</b><span>Builds the music, memory and outing ideas that turn a visit into a good afternoon.</span><div class=badges><i>Music and memory</i><i>Life Story</i></div>")]) +
        f'<p style="text-align:center"><a href="/{p}/team.html">How we hire, screen and train &rsaquo;</a></p>' +
        # 11. questions
        SECTION("Questions", "The questions every family asks.", "Answers first, details after.") +
        ACC(FAQ_HOME(M), search=True, id="hfaq") +
        # 12. final CTA
        CTA(M))
    page(M, f"{p}/index", f"Dementia care your whole family can see", "", hero + f'<div class="w">{body}</div>', nohero="bare", landing=False,
         desc=f"In-home dementia care in {M['metro']} with trained {cgs}, {'a 72-hour start ' if live else ''}and a live family app. Call {M['phone']}.",
         jsonld=[{"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness" if False else "LocalBusiness", "name": BRAND, "url": f"{DOMAIN}/{p}/",
                  "telephone": M["tel"], "areaServed": M["metro"], "description": f"Non-medical in-home dementia care in {M['metro']}."}])

def FAQ_HOME(M):
    r, s, p, live = M["rates"], M["sym"], M["p"], M["live"]
    cur = M["cur"]
    qa = [("How much does home care cost?", f"<p>Our care starts from {cur} {s}{r['companion']} an hour for companion care, {s}{r['personal']} for personal care and {s}{r['dementia']} for dementia specialist care. "
                                             f"Twenty hours a week of dementia care is about {cur} {s}{r['dementia'] * 20 * 52 / 12:,.0f} a month. <a href='/{p}/pricing.html'>See every price</a>.</p>"),
          ("How quickly can care start?", "<p>Within 72 hours of signing the care agreement, after a free assessment we can usually book within 24 hours.</p>" if live else
                                          "<p>We are not providing care in Australia yet. Join the waitlist and we will call you, explain Support at Home and tell you honestly when we can start.</p>"),
          ("Are your " + M["cgs"] + " trained in dementia?", "<p>Yes. Every " + M["cg"] + " completes our dementia program before their first visit, including calming communication, sundowning, wandering safety and meals.</p>"),
          ("Will my " + M["mom"] + " see the same " + M["cg"] + "?", "<p>Yes. Each client has a small team of two or three, and you meet the backup before day one.</p>"),
          ("What happens if a " + M["cg"] + " is sick?", "<p>The backup they already know steps in. We promise a replacement within 48 hours at most, and usually the same day.</p>"),
          ("Is there a minimum number of hours?", f"<p>Visits are at least 3 hours, and most families start with 10 to 20 hours a week.</p>"),
          ("Do you provide medical or nursing care?", "<p>No. We provide non-medical care: personal care, companionship, meals, reminders and support. We work alongside doctors, nurses and hospice teams.</p>"),
          ("Does " + ("Medicare" if p == "us" else "Support at Home") + " pay for this?",
           "<p>Medicare generally does not pay for ongoing non-medical home care. Long-term care insurance and veterans' benefits may. <a href='/us/paying-for-care.html'>Paying for care explained</a>.</p>" if p == "us" else
           "<p>If you have a Support at Home classification, the government funds most of the cost and you pay a contribution. <a href='/au/funding.html'>Funding explained step by step</a>.</p>"),
          ("How do I know you are licensed?", f"<p>{M['lic']} You can check any provider on the <a href='{M['regulator'][1]}'>{M['regulator'][0]}</a> site.</p>"),
          ("Can I stop or change care?", "<p>Yes. Change hours in the app with a few days' notice, and stop with 7 days' notice. No long contracts.</p>")]
    return qa

for _M in (US, AU):
    home(_M)
