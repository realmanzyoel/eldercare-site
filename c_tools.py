from ec import *

def _mo(rate, hrs): return rate * hrs * 52 / 12

# ---------------- family app ----------------
def app(M):
    p, cg, cgs, m = M["p"], M["cg"], M["cgs"], M["mom"]
    au = p == "au"
    body = (
        CALL("<b>Demo family.</b> The Rivera family, Dad and Maria on this page are fictional. Screens show sample data so you can see exactly how the app works. "
             + ("The app goes live for each family on their first visit." if M["live"] else "The app will launch in Australia when we start providing care.")) +
        f'<div class="two" style="align-items:center;margin-top:30px"><div>' + SECTION("Why an app", "The feature most agencies cannot match.") +
        P(f"Most families find out how a visit went by phoning their {m} and hoping she remembers. Our app shows it as it happens: who arrived, when, what they ate, how they seemed and anything that worried the {cg}.",
          "It works on a phone first, in large type, and is built to be used by a 75-year-old sibling as easily as a 40-year-old.") +
        f'</div><div>{CARECARD(M)}</div></div>' +
        SECTION("Scroll the tour", "See care happen, from anywhere.") + PHONE(M, APPSCREENS(M)) +
        SPLIT("woman-phone", H2("Live visit tracking") + TICKS(["GPS check-in and check-out with times", f"A status line: 'Maria is with Dad now'", f"An alert if a {cg} is late or a visit is missed, with the backup {cg}'s name",
              "A calendar of every visit, past and future"])) +
        SPLIT("tea-book", H2("Daily care notes") + TICKS(["Quick structured entries each visit: mood, meals, fluids, sleep, activities, bathroom and any concern",
              "Optional photos when your family and the client have agreed", "A weekly digest by email", "A downloadable PDF to take to the doctor"]), flip=True) +
        SECTION("Trends and insight", "See change early, not after a crisis.", "Charts over weeks for mood, meals, hydration and sleep. A gentle flag when a pattern changes prompts a call from the care manager. It is never a diagnosis.") +
        LINE("Demo: mood and hydration scores over 8 weeks (sample data)", [f"W{i}" for i in range(1, 9)],
             [("Mood (out of 10)", [6, 6.5, 7, 6.8, 7.4, 7.2, 7.8, 8]), ("Glasses of water a day", [4, 4.5, 5, 5.5, 5, 6, 6.2, 6.5], "#0e4a4f")],
             note="Fictional demo data. Real charts use your family's care notes.") +
        SECTION("Family circle", "Everyone in the loop, each with the right access.") +
        T(["Role", "Can see visits and notes", "Can message the team", "Can approve plan changes", "Sees billing"],
          [["Primary contact", "Yes", "Yes", "Yes", "Yes"], ["Family member", "Yes", "Yes", "No", "No"], ["View only (for example a grandchild)", "Yes", "No", "No", "No"],
           [f"{M['Cg']}", "Their own visits", "Yes, with the care manager", "No", "No"], ["Care manager", "Yes", "Yes", "Proposes changes", "Yes"]]) +
        P("A shared message thread with the care team and the care manager, with response targets, and a one-tap video call link.") +
        GALLERY(["video-call", "video-call2", "grandpa-selfie"], ["One-tap video calls with the family circle", "Siblings in different cities see the same notes", "Grandchildren can have view-only access"]) +
        SPLIT("couple-docs", H2("Care plan and schedule") + TICKS(["The care plan, visible and editable with approval", "The weekly schedule with change requests",
              "Medication reminders and confirmations, where our licence and scope allow", "Change hours with a few days' notice"])) +
        SPLIT("switch", H2("Safety") + TICKS(["Optional partner integrations for door sensors, fall detection and wearables", "An emergency button that alerts the care manager and the family circle",
              "Incident reports within a stated time: what happened and what changed"]), flip=True) +
        SPLIT("phone1", H2("Billing and ratings") + TICKS(["Live hours and invoices", "Pay by card or bank transfer",
              "A one-tap rating after each visit that feeds our public promises dashboard"] + (["Long-term care insurance claim support: invoices formatted for your insurer"] if not au else []))) +
        ((SECTION("Australia additions", "Your Support at Home budget, in plain view.") +
          DONUT("Demo: quarterly Support at Home budget (sample data)", [("Personal care used", 38, "#bf4128"), ("Everyday living used", 22, "#0e4a4f"), ("Remaining", 40, "#e3efed")], ("40%", "remaining"),
                note="Fictional demo figures. Your real budget, statements and contributions come from your service agreement.") +
          TICKS(["Funds used and remaining, updated after each visit", "Copies of your service agreement", "Monthly statements", "Contribution tracking against the lifetime cap"])) if au else "") +
        SECTION("Privacy", "Who can see what, and what we never do.") +
        T(["Information", "Who can see it"], [["Visit times and GPS check-in", "Family circle, care team"], ["Care notes", "Family circle members with note access, care team"],
                                             ["Photos", "Only people the client and primary contact have approved"], ["Billing", "Primary contact and anyone they add"],
                                             ["Health details", "Never sent to advertising or analytics tools"]]) +
        TICKS(["We do not sell your data, ever", "Data is encrypted in transit and at rest", "Role-based access with audit logs of who viewed what",
               "You can download or delete your family's data when care ends"]) +
        CALL("A formal privacy review in " + ("the United States" if not au else "Australia") + " will be completed before launch. Until then this section describes how the app is designed, not a certified standard.") +
        CTA(M, "See the app with your own family.", f"Book a free assessment and we will set up the family circle on day one. Questions? Call {M['phone']}.", "video-call2"))
    page(M, f"{p}/app", "See care happen, from anywhere.", f"The {BRAND} family app shows every visit, note and mood as it happens, so relatives near and far always know how {M['mom']} or {M['dad']} is doing.",
         body, img="woman-phone", eyebrow="Family app", chips=[("Live", "visit status"), ("Weekly", "family digest"), ("0", "data sold, ever")])

# ---------------- pricing ----------------
def pricing(M):
    p, r, s, cur = M["p"], M["rates"], M["sym"], M["cur"]
    au = p == "au"
    rows = [["Companion care", f"{s}{r['companion']}/hour", "Company, meals, outings, light housework, reminders"],
            ["Personal care", f"{s}{r['personal']}/hour", "Bathing, dressing, toileting, transfers, grooming"],
            ["Dementia specialist care", f"{s}{r['dementia']}/hour", f"Dementia-trained {M['cgs']}, Life Story profile, sundowning plan"],
            ["Sleep-over night", f"{s}{r['overnight']}/night", f"A {M['cg']} sleeps at the home and helps if needed"],
            ["Live-in care", f"{s}{r['live']}/day", "A team rotating through the week, with rest breaks"]]
    packs = [("Steady", 10, "companion", "Two or three visits a week for company and help around the house.", "two-women"),
             ("Daily", 25, "dementia", "A visit every day with the same small team and a set routine.", "elder-care"),
             ("Full support", 50, "dementia", "Long daily shifts, a safety plan and family coaching.", "hands-young")]
    pk = "".join(f'<div class="card tilt reveal" style="--i:{i}"><img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy" style="width:100%;height:170px;object-fit:cover;border-radius:16px;margin-bottom:12px">'
                 f'<h3>{n}</h3><p><b style="font-size:28px;font-family:var(--serif);color:var(--teal)">about {s}{_mo(r[k], h):,.0f}</b> a month</p>'
                 f'<p>{h} hours a week of {k} care at {s}{r[k]}/hour. {d}</p></div>' for i, (n, h, k, d, im) in enumerate(packs))
    body = (
        SUMMARY(f"Our care starts from {cur} {s}{r['companion']} an hour for companion care, {s}{r['personal']} for personal care and {s}{r['dementia']} for dementia specialist care. "
                f"Twenty hours a week of dementia care costs about {cur} {s}{_mo(r['dementia'], 20):,.0f} a month. There is no sign-up fee." +
                (" If you have a Support at Home budget, most of the cost comes from your budget." if au else "")) +
        (CALL("<b>Australia:</b> we are not yet providing care. These are planned private-pay prices. For Support at Home clients, prices will align with the published price caps and be set out in your service agreement.") if au else "") +
        SECTION("Price list", "Every price, in writing.", f"All prices in {cur}" + (", including GST where it applies." if au else ".")) +
        T(["Service", "From", "What it covers"], rows) +
        SECTION("Packages", "Three common starting points.", "Most families start here and adjust after the first month.") +
        f'<div class="grid g3">{pk}</div>' +
        SECTION("Estimator", "Work out your own monthly cost.") + EST(M) +
        COLS("Illustrative: monthly cost of 20 hours a week, by type of care", ["Companion", "Personal", "Dementia"],
             [("Monthly cost", [round(_mo(r[k], 20)) for k in ("companion", "personal", "dementia")], "#bf4128")], note="Illustrative figures from our starting rates, before any insurance, benefit or funding.",
             fmt=lambda v: f"{s}{v:,.0f}") +
        SPLIT("couple-docs", H2("Fees and policies") + TICKS(["No sign-up or assessment fee", "Minimum visit of 3 hours", "Change or stop care with 7 days' notice, no long contracts",
              "Weekend and public holiday hours cost about 15% more", "Your price is confirmed in writing before care starts"])) +
        NOTCOVER(["Nursing or medical care (we work alongside nurses and doctors)", "Medical equipment and supplies", "Mileage over 20 " + ("miles" if not au else "kilometres") + " a week for errands",
                  "Meals out, tickets and other costs during outings"]) +
        SECTION("Questions", "Pricing questions families ask.") +
        ACC([("Why do you charge more for dementia care?", f"<p>Dementia specialist {M['cgs']} complete extra training and stay with a small team per client. That costs more, and it is what keeps the same faces in the home.</p>"),
             ("Do you charge for the assessment?", "<p>No. The assessment is free and there is no obligation.</p>"),
             ("How do I pay?", "<p>By card or bank transfer, invoiced " + ("every two weeks" if not au else "monthly") + " in the family app.</p>"),
             ("Can insurance or benefits pay?", f"<p>Often, partly. See <a href='{M['pay'][0]}'>{M['pay'][1].lower()}</a>.</p>"),
             ("Will prices change?", "<p>Prices are reviewed once a year, with at least 30 days' written notice.</p>")], id="pfaq") +
        f'<p>{PRINT()}</p>' + CTA(M, "Get an exact price for your family.", None, "couple-color"))
    page(M, f"{p}/pricing", "Know the cost before you call.", "Every rate, three common packages and an estimator that updates as you move the sliders.",
         body, img="couple-docs", eyebrow="Pricing", chips=[(f"{s}{r['companion']}", "from, per hour"), ("$0", "sign-up fee"), ("7 days", "notice to stop")])

# ---------------- US paying for care ----------------
def paying(M):
    body = (
        SUMMARY("Most families pay for non-medical home care privately. Long-term care insurance and veterans' benefits often cover part of it. Medicare generally does not pay for ongoing custodial care at home, "
                "and Florida Medicaid's long-term care program has a waitlist.") +
        SECTION("Step by step", "Five questions that find the money.", "Scroll down: each step lights up as you go.") +
        PATH([("Check for long-term care insurance", "Find the policy. Look for the daily benefit, the elimination period and whether home care is covered.", "papers"),
              ("Check veterans' benefits", "A veteran or surviving spouse may qualify for a pension with Aid and Attendance or Housebound benefits.", "man-table"),
              ("Understand what Medicare covers", "Short-term skilled home health after a hospital stay, yes. Ongoing help with bathing and meals, generally no.", "hospital"),
              ("Look at Florida Medicaid", "The Statewide Medicaid Managed Care long-term care program can help people who qualify financially, but there is usually a waitlist.", "couple-docs"),
              ("Plan private pay", "Savings, income, family cost-sharing and sometimes home equity. We give you a written monthly figure to plan with.", "couple-color")]) +
        SPLIT("couple-docs", H2("Private pay") + P("Most of our families pay privately, at least at first. We invoice every two weeks, by card or bank transfer, and you can change hours with a few days' notice.",
              "Families often share the cost between siblings. The app lets each sibling see the invoices if the primary contact allows it.") +
              f'<p><a href="/us/pricing.html">See our prices and estimator &rsaquo;</a></p>') +
        SPLIT("papers", H2("Long-term care insurance") + P("Many policies pay for home care once the insured person needs help with two or more activities of daily living, or has a cognitive impairment such as dementia.") +
              TICKS(["Elimination period: most policies pay only after a waiting period, often 30 to 90 days of care", "You usually pay us first and the insurer reimburses you",
                     "We provide care plans, visit logs and invoices formatted for your insurer", "Call the insurer early: claims take weeks to approve"]), flip=True) +
        SPLIT("man-photos", H2("Veterans' benefits") + P("The VA pension can include an extra monthly amount for Aid and Attendance, for veterans or surviving spouses who need help with daily activities, or Housebound benefits. "
              "Amounts are set by the VA each year and depend on income and assets.",
              f'Start at <a href="https://www.va.gov/pension/aid-attendance-housebound/" target="_blank" rel="noopener">va.gov: Aid and Attendance and Housebound</a>. Accredited representatives help for free; be wary of anyone charging to file.')) +
        SECTION("Medicare", "What Medicare does and does not pay for.") +
        VS("Medicare usually covers", [("Skilled home health", "Part-time, prescribed"), ("Nursing and therapy", "After an illness or hospital stay"), ("Who must be", "Homebound, doctor certified")],
           "Medicare usually does not cover", [("Ongoing personal care", "Bathing, dressing"), ("Companion care", "Company, meals, errands"), ("24-hour care", "At home")]) +
        P(f'Details are at <a href="https://www.medicare.gov/coverage/home-health-services" target="_blank" rel="noopener">medicare.gov: home health services</a>. Some Medicare Advantage plans include limited in-home support; check your plan.') +
        SPLIT("hospital", H2("Florida Medicaid") + P("The Statewide Medicaid Managed Care (SMMC) long-term care program can pay for home and community-based care for people who meet medical and financial rules. There is usually a waitlist, managed through the local Aging and Disability Resource Center.",
              "At launch we are a private-pay agency and do not bill Medicaid. We will help you understand the program and apply while private care fills the gap.",
              f'Read more at <a href="https://ahca.myflorida.com/medicaid/statewide-medicaid-managed-care" target="_blank" rel="noopener">ahca.myflorida.com</a>.')) +
        SPLIT("porch", H2("Other ways families pay") + TICKS(["Family cost-sharing agreements: written down, so siblings know who pays what", "A reverse mortgage or home equity line, after independent financial advice",
              "Life insurance with a long-term care rider or accelerated benefit", "Respite grants from local Alzheimer's organisations, when available"]), flip=True) +
        CALL("General information, not financial or legal advice. Benefit rules change; check with the program or an elder law attorney before making decisions.") +
        ACC([("Does Medicare pay for home care for dementia?", "<p>Not for ongoing non-medical care. It may pay for short-term skilled home health if a doctor orders it and the person is homebound.</p>"),
             ("Can you help with my insurance claim?", "<p>Yes. We provide the care plan, visit logs and invoices your insurer asks for, at no charge.</p>"),
             ("Do you take Medicaid?", "<p>Not at launch. We are private-pay, and we will tell you plainly if that changes.</p>")], id="payfaq") +
        CTA(M, "Talk it through with a care advisor.", f"Call {M['phone']}. We will help you see which of these apply before you spend a dollar.", "couple-docs"))
    page(M, "us/paying-for-care", "Paying for home care, made clear.", "Private pay, long-term care insurance, veterans' benefits, Medicare and Florida Medicaid, explained in plain words.",
         body, img="couple-docs", eyebrow="Paying for care", chips=[("Private pay", "most families"), ("LTC insurance", "claim help"), ("VA", "benefits explained")])

# ---------------- AU funding ----------------
def funding(M):
    body = (
        CALL("<b>Where we are:</b> we are not yet a registered Support at Home provider and are not providing care in Australia. This page explains the program honestly so you can plan, whoever you choose.") +
        SUMMARY("Support at Home is the government program for care at home. You contact My Aged Care, get assessed, receive one of 8 funding classifications (about $11,010 to about $80,137 a year from July 2026), "
                "choose a registered provider and pay a contribution based on your pension status. Clinical care such as nursing has no contribution.") +
        SECTION("Step by step", "From first call to first visit.", "Scroll down: each step lights up as you reach it.") +
        PATH([("Contact My Aged Care", "Call 1800 200 422 or apply online at myagedcare.gov.au. A family member can do this with permission.", "woman-phone"),
              ("Have an assessment", "An assessor visits to understand daily needs, memory, safety and the support around the person.", "couple-docs"),
              ("Get a classification", "You receive a notice of decision with one of 8 ongoing classifications, or a short-term pathway. Funding may take time to be assigned.", "papers"),
              ("Choose a provider", "Compare registered providers on price, services, dementia skills and how they communicate with families.", "two-women"),
              ("Sign a service agreement", "It sets out services, prices, your contributions and how to change or complain. Read it before you sign.", "hands-care")]) +
        SECTION("Classifications", "Eight funding levels.", "Budgets are indexed each July. The exact amount for each level is on the department's published schedule.") +
        BARS("Annual Support at Home budget, July 2026 (AUD, approximate)", [("Level 1", 11010, "about $11,010", "#0e4a4f"), ("Level 8", 80137, "about $80,137", "#bf4128")],
             note='Source: Department of Health, Disability and Ageing, Support at Home classifications and budgets, July 2026. Levels 2 to 7 sit between these; check the official schedule.') +
        SECTION("Contributions", "What you pay, and what the government pays.") +
        T(["Pension status", "Clinical care", "Independence (e.g. personal care)", "Everyday living (e.g. cleaning, meals)"],
          [["Full age pensioner", "0%", "5%", "17.5%"], ["Part pensioner or CSHC holder", "0%", "5% to 50%", "17.5% to 80%"], ["Self-funded retiree", "0%", "50%", "80%"]]) +
        P("Rates shown are the standard rates for people who entered Support at Home from 1 November 2025. People who held a Home Care Package before then may have lower 'no worse off' rates. A lifetime cap on contributions applies.") +
        SAH() +
        SPLIT("hospital", H2("Short-term pathways") + TICKS(["Restorative Care Pathway: about 12 weeks of allied health and nursing to regain independence",
              "End-of-Life Pathway: extra support at home in the last months of life", "Assistive Technology and Home Modifications (AT-HM) scheme: equipment and home changes"])) +
        SPLIT("tea-book", H2("Commonwealth Home Support Programme") + P("People who need only a little help, such as a few hours of cleaning or a meal service, may be supported through the Commonwealth Home Support Programme, which is planned to move into Support at Home later. My Aged Care will tell you which applies."), flip=True) +
        SECTION("Choosing a provider", "Questions worth asking any provider.") +
        TICKS(["Are you registered, and for which categories?", "What are your prices, and do they match the price caps?", "Who will actually come, and will it be the same people?",
               "How are your support workers trained in dementia?", "How do you tell the family what happened at each visit?", "How do I complain, and who do I escalate to?"]) +
        P('Official information: <a href="https://www.myagedcare.gov.au/" target="_blank" rel="noopener">myagedcare.gov.au</a> and <a href="https://www.health.gov.au/our-work/support-at-home" target="_blank" rel="noopener">health.gov.au: Support at Home</a>.') +
        CALL("General information only, based on published program rules as of November 2026. Rules and amounts change; confirm your own situation with My Aged Care or Services Australia.") +
        ACC([("Can I use Support at Home with a private provider?", "<p>Funded services must be delivered by a registered provider. You can also pay privately for extra hours.</p>"),
             ("How long does assessment take?", "<p>It varies by region. Start early: contact My Aged Care as soon as you notice help is needed.</p>"),
             ("When will you be a provider?", "<p>When our registration questions are settled. Join the waitlist and we will tell you as soon as we can, honestly.</p>")], id="ffaq") +
        CTA(M, "Want help understanding your letter?", f"Call {M['phone']}. A care advisor will walk you through it, even if we cannot be your provider yet.", "couple-docs"))
    page(M, "au/funding", "Support at Home, explained step by step.", "How the government program for care at home works: assessment, classifications, contributions and choosing a provider.",
         body, img="couple-docs", eyebrow="Funding", chips=[("8", "classifications"), ("0%", "contribution for clinical care"), ("1800 200 422", "My Aged Care")])

# ---------------- quiz, book, refer, login ----------------
def quiz(M):
    p = M["p"]
    body = (SUMMARY("Eight plain questions, about two minutes. At the end you see a suggested starting plan and hours. We never ask for your email before showing the result.") +
            QUIZ(M) +
            GALLERY(["thoughtful", "kitchen-sink", "man-walk"], ["Memory and routine", "Daily living", "Safety and getting out"]) +
            SPLIT("couple-docs", H2("What happens next") + TICKS(["The result is a starting point, not an assessment", "A care manager adjusts it after meeting you both",
                  "You get a written plan and price before anything starts"]) + f'<p><a class="btn" href="/{p}/book.html">{"Book a free assessment" if M["live"] else "Join the waitlist"}</a></p>') +
            CTA(M))
    page(M, f"{p}/care-quiz", "Not sure what you need? Start here.", "Answer eight questions and get a suggested plan and hours, in about two minutes.",
         body, img="thoughtful", eyebrow="Care needs quiz", chips=[("8", "questions"), ("2 min", "to finish"), ("No email", "needed")])

def book(M):
    p, live = M["p"], M["live"]
    side = (f'<div><div class="card"><h3>Prefer to talk?</h3><p>{M["hours"]}.</p><p><a class="btn big pulse" href="tel:{M["tel"]}">Call {M["phone"]}</a></p>'
            f'<p><a class="btn o" href="sms:{M["sms"]}">Text {M["text"]}</a></p></div>'
            f'<div class="card" style="margin-top:14px"><img src="/img/woman-glasses.jpg" alt="{alt("woman-glasses")}" style="width:100%;height:220px;object-fit:cover;border-radius:16px" loading="lazy">'
            f'<h3 style="margin-top:12px">Your care advisor</h3><p>A real person who will listen first. Illustrative photo: your advisor\'s name and photo appear here once our team is in place.</p></div></div>')
    body = (
        (CALL("<b>Australia:</b> we are not providing care yet. Join the waitlist and we will call you by the next business day, explain Support at Home and tell you honestly when we expect to start.") if not live else "") +
        f'<div class="two" style="margin-top:24px"><div>{H2("Three fields. One call back.")}{BOOK(M)}</div>{side}</div>' +
        SECTION("What happens next", "From this form to the first visit.") +
        TIMELINE([("Within 15 min" if live else "Next business day", "A care advisor calls", "We listen, answer questions and book the assessment at a time that suits the family."),
                  ("Within 24 hours" if live else "When we launch", "Free care assessment", f"A care manager visits at home or in hospital, meets your {M['mom']} or {M['dad']} and the family."),
                  ("Within 48 hours" if live else "Before care starts", "Care plan and price", "In writing, with the hours, the team and the exact cost."),
                  ("Within 72 hours" if live else "First visit", "Care starts", f"You have met the {M['cg']} and the backup, and the family app is live.")]) +
        SPLIT("couple-color", H2("On the assessment") + TICKS(["About an hour, at home or in hospital", "We meet the person who needs care, not only the family", "A home safety walk-through",
              "We start the Life Story profile", "No cost, no obligation, no pressure"])) +
        PILLS([M["lic_short"], "No sign-up fee", "7 days' notice to stop", "Dementia-trained " + M["cgs"]]) + CTA(M))
    page(M, f"{p}/book", "Book a free care assessment" if live else "Join the waitlist", "Pick a time, leave a number and a care advisor calls you. Or call now: a person answers." if live else
         "Leave your details and a care advisor will call you by the next business day.", body, img="elder-nurse", eyebrow="Free assessment" if live else "Waitlist",
         chips=[("15 min", "call back") if live else ("1 day", "call back"), ("$0", "assessment"), ("3", "fields")])

def refer(M):
    p, live = M["p"], M["live"]
    f = (f'<form class="book" data-mail="{MAIL}" data-kind="referral" data-market="{M["country"]}" novalidate><div class="bk-bar"><i></i></div>'
         f'<label><span>Your name</span><input name="referrer" autocomplete="name" required></label>'
         f'<label><span>Your role</span><select name="role" required><option value="">Choose</option><option>Discharge planner</option><option>Social worker</option><option>Doctor</option><option>Nurse</option><option>Other professional</option></select></label>'
         f'<label><span>Organisation</span><input name="organisation" required></label>'
         f'<label><span>Your phone</span><input name="phone" type="tel" autocomplete="tel" required></label>'
         f'<label><span>Patient initials only</span><input name="initials" maxlength="4" required></label>'
         f'<label><span>Expected discharge date</span><input name="discharge" type="date"></label>'
         f'<label><span>Main needs (no diagnosis details needed)</span><textarea name="needs" rows="3"></textarea></label>'
         f'<label class="chk small"><input type="checkbox" name="consent" required> <span>The patient or their representative has agreed to this referral and to being contacted. <a href="/{p}/privacy.html">Privacy policy</a>.</span></label>'
         f'<button class="btn big" type="submit">Send referral</button><p class="bk-err" role="alert"></p>'
         f'<div class="bk-ok" hidden tabindex="-1"><img src="/img/woman-glasses.jpg" alt="" class="adv"><div><h3>Thank you. Your referral is ready to send.</h3>'
         f'<p>Your email app has opened with the details. Press send and we will {"call you back within the hour during business hours" if live else "reply by the next business day"}. Urgent? Call <a href="tel:{M["tel"]}">{M["phone"]}</a>.</p></div></div></form>')
    body = (
        (CALL("<b>Australia:</b> we cannot accept referrals for care yet. You are welcome to register interest and we will reply by the next business day.") if not live else "") +
        f'<div class="two" style="margin-top:24px"><div>{H2("Refer in under two minutes.")}{f}</div><div>' +
        H3("What referrers get") + TICKS(([ "A call back within the hour during business hours", "Assessment at the bedside or at home within 24 hours", "Care starting within 72 hours of signing"] if live else
                                         ["A reply by the next business day", "Honest information about Support at Home and other options"]) +
                                        ["A named contact for every referral", "A short update to you once care starts, with consent"]) +
        f'<img src="/img/hospital.jpg" alt="{alt("hospital")}" loading="lazy" style="width:100%;height:240px;object-fit:cover;border-radius:22px;margin-top:10px"></div></div>' +
        SECTION("Who refers to us", "Built for busy discharge teams.") +
        GRID([("Discharge planners", "One form, one call back, and a first-week plan the family can see.", None, None),
              ("Social workers", "Help for families who are overwhelmed, including caregiver respite.", None, None),
              (("Doctors and nurses" if not live else "Doctors, neurologists and nurses"), "Dementia-trained " + M["cgs"] + " who follow the care plan and report changes.", None, None)]) +
        CALL("Please send only the minimum details here. Never send diagnoses or medical records by email; we collect what we need by phone.") + CTA(M))
    page(M, f"{p}/refer", "Hospital and professional referrals", "For discharge planners, social workers and doctors." + (" We call back within the hour." if live else ""),
         body, img="hallway", eyebrow="Refer a client", chips=[("< 2 min", "to refer"), ("1 hour", "call back") if live else ("1 day", "reply"), ("72 h", "care start") if live else ("Waitlist", "for now")])

def login(M):
    p = M["p"]
    body = (f'<div class="two" style="margin-top:24px"><form class="book" aria-describedby="lnote" onsubmit="return false"><p id="lnote" class="call" style="margin:0"><b>Sign-in opens when care begins.</b> '
            f'{"Families receive their sign-in link on the first day of care." if M["live"] else "The family app is not yet available in Australia."}</p>'
            f'<label><span>Email</span><input type="email" autocomplete="email" disabled></label><label><span>Password</span><input type="password" autocomplete="current-password" disabled></label>'
            f'<button class="btn big" type="submit" disabled aria-disabled="true">Sign in</button><p class="cn">Secure sign-in with two-step verification will be required.</p></form>'
            f'<div>{H2("Want to see it first?")}{P("Tour the app with our demo family and sample data.")}<p><a class="btn" href="/{p}/app.html">Take the app tour</a></p>'
            f'{H3("Need help?")}{P("Call " + ph(M) + ". " + M["hours"] + ".")}</div></div>' + GALLERY(["woman-phone", "video-call"], ["Large type, phone first", "Video calls with the care team"]))
    page(M, f"{p}/login", "Client login", "Sign in to the family app.", body, nohero=True, eyebrow="Family app")

for _M in (US, AU):
    app(_M); pricing(_M); quiz(_M); book(_M); refer(_M); login(_M)
paying(US)
funding(AU)
