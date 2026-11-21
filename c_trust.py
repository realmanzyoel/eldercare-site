from ec import *

def promises(M):
    p, live, cg = M["p"], M["live"], M["cg"]
    result = ("First monthly result published after our first full month of care." if live
              else "Not yet measured: we are not providing care in Australia yet.")
    items = [
        ("Care starts within 72 hours of signing", "Operations lead",
         "Hours from the signed care agreement to the GPS check-in of the first visit, for every new client.",
         "If we miss it, the first week's visits are credited at 10% off and the director calls you to explain why."),
        (f"A replacement {cg} within 48 hours, already introduced", "Scheduling coordinator",
         f"Hours from a {cg} becoming unavailable to a familiar backup checked in. We also count how often the replacement had met your family before.",
         "If we miss it, the hours of the missed shift are free and the director calls you."),
        ("Call back within 15 minutes in business hours", "Care advisor team lead",
         "Minutes from a missed call, text or web request to a human call back, from our phone system logs.",
         "If we miss it, the care manager calls you the same day to apologise and to fix the cause."),
        (f"The same small team of 2 to 3 {M['cgs']}", "Care manager",
         f"Share of visits each month delivered by a {cg} on your named team.",
         "If your team changes without your agreement, we meet you to agree a new team, at no cost."),
        ("A weekly update and a monthly call", "Care manager",
         "Weekly summaries sent on time, and monthly calls held, out of those due.",
         "If an update is late, the care manager calls you that week instead."),
        ("A human answers the phone 24/7" if live else "Advisors available 8am to 8pm, every day", "Operations lead",
         "Share of calls answered by a person, and the average wait, from our phone system.",
         "If a call goes unanswered, we call back and log it in the monthly report."),
    ]
    blocks = "".join(
        f'<section class="card reveal" id="p{i}" style="margin:18px 0;padding:26px"><p class="ey">Promise {i + 1}</p><h2 style="margin-top:4px">{t}</h2>'
        + KV([("Owner", o), ("How we measure it", m), ("Current result", result), ("If we miss it", x)]) + "</section>"
        for i, (t, o, m, x) in enumerate(items))
    months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"]
    tbl = T(["Promise", "Target"] + months,
            [[t, tg] + ["&mdash;"] * 6 for (t, *_), tg in zip(items, ["95% of starts", "95% of gaps", "90% of calls", "85% of visits", "100% of weeks", "95% of calls"])])
    body = (
        SUMMARY("We make six promises we can measure. Each has a named owner, a monthly result and a stated remedy when we miss it. "
                + ("The first results appear after our first full month of care." if live else "In Australia we are not providing care yet, so there are no results to show."))
        + SECTION("The promises", "Six promises, measured every month.")
        + PROMISES(M)
        + SECTION("Our targets", "What good looks like to us.", "These dials show targets, not results. Real monthly results replace them once we have them.")
        + DIALS([(95, "Starts within 72 hours", "Target"), (95, "Replacements within 48 hours", "Target"),
                 (90, "Call backs within 15 minutes", "Target"), (85, "Visits by your named team", "Target")])
        + blocks
        + SECTION("Monthly report", "The report we will publish.", "Empty until real data exists. We will not fill it with estimates.")
        + tbl
        + SPLIT("couple-docs", H2("Why publish this at all?") + P(
            "Families tell us the worst part of home care is not knowing. A promise without a number is a slogan. "
            "Publishing results, including bad months, is how we hold ourselves to it, and how you can check us.")
            + TICKS(["Results come straight from our phone and scheduling systems", "Bad months stay on the page", "Each promise has one owner, not a committee"]))
        + CTA(M, "Ask us how we are doing.", f"Call {M['phone']} and ask for this month's numbers. The person who answers can tell you."))
    page(M, f"{p}/promises", "Our promises", "Six measurable promises, with an owner, a monthly result and a remedy when we miss.",
         body, img="hands-care", eyebrow="Trust", chips=[("72 h", "start"), ("48 h", "replacement"), ("15 min", "call back")])

def trust(M):
    p, live, us = M["p"], M["live"], M["p"] == "us"
    reg_name, reg_url = M["regulator"]
    if us:
        lic = (H2("Licensing") + P(M["lic"]) + P(
            "Home care in Florida is licensed by the Agency for Health Care Administration (AHCA). Hands-on personal care needs a home health agency license or a nurse registry license, "
            "and every license number must appear on marketing materials, which is why ours is in the footer of every page.")
            + FLOW([("1. Open the AHCA site", f'<a href="{reg_url}" target="_blank" rel="noopener">quality.healthfinder.fl.gov</a>'),
                    ("2. Search by name", f"Type {BRAND} or our license number"), ("3. Check status", "Active, the license type and the address")]))
        screen = (H2("Background screening") + P(
            f"Every {M['cg']} and every office employee who could reach a client passes Florida Level 2 background screening under Chapter 435, Florida Statutes, "
            "through the AHCA Clearinghouse: fingerprints checked against state and FBI records. We do not schedule anyone before the result is clear.")
                  + TICKS(["Level 2 fingerprint screening (Chapter 435, F.S.)", "Clearinghouse rescreening and arrest alerts", "Two references and a work history check",
                           "Driving record check for anyone who drives clients", "Identity and right-to-work check"]))
        report = "Florida Abuse Hotline: 1-800-96-ABUSE (1-800-962-2873), or 911 in an emergency"
    else:
        lic = (H2("Registration") + P(M["lic"]) + P(
            "Providers that deliver government-funded aged care under Support at Home must be registered with the Aged Care Quality and Safety Commission. "
            "Until we are registered we will not deliver funded services, and we say so on every page.")
            + FLOW([("1. Open the Commission site", f'<a href="{reg_url}" target="_blank" rel="noopener">agedcarequality.gov.au</a>'),
                    ("2. Search the provider register", f"Type {BRAND}"), ("3. Check status", "Registration category and any notices")]))
        screen = (H2("Worker screening") + P(
            f"Every {M['cg']} will hold a current NDIS Worker Screening Check or an aged care police check, as the law requires at the time, and follow the Code of Conduct for Aged Care. "
            "Our work will be measured against the strengthened Aged Care Quality Standards.")
                  + TICKS(["NDIS Worker Screening Check or police check", "Code of Conduct for Aged Care, signed and trained", "Two references and a work history check",
                           "Driver's licence and vehicle check for anyone who drives clients", "Identity and right-to-work check"]))
        report = "Serious incidents reported under the Serious Incident Response Scheme (SIRS); 000 in an emergency"
    safety = TIMELINE([
        ("Falls", "Prevent, respond, review", f"A home safety walk-through before day one. If a fall happens the {M['cg']} does not lift the person alone, calls {'911' if us else '000'} if they are hurt, then the family and care manager. We review every fall within 48 hours."),
        ("Medicines", "Reminders, not guesswork", f"We remind and record; we only assist further where our {'license' if us else 'registration'} and the care plan allow. A missed or wrong dose is reported to the family and the prescriber the same day."),
        ("Abuse and neglect", "Speak up, always", f"Every worker is trained to recognise and report abuse. {report}. Reporting is never optional and never punished."),
        ("Emergencies", "Clear steps", "Call emergency services first, then the care manager, then the family circle through the app. An incident report follows within 24 hours: what happened and what changed."),
    ])
    complaints = FLOW([("1. Your care manager", "Call or message in the app. Answer within 1 business day."),
                       ("2. The director", "If it is not resolved in 5 business days, or you prefer, go straight to the director."),
                       ("3. Outside help", (f'The {reg_name} (<a href="{reg_url}" target="_blank" rel="noopener">site</a>)' if us else
                                            f'The Aged Care Quality and Safety Commission, free on 1800 951 822') + ". You can go here at any stage.")])
    body = (SUMMARY(f"{M['lic']} We will show proof of insurance and screening before care starts, and you can check our {'license' if us else 'registration'} yourself.")
            + SPLIT("couple-docs", lic) + SPLIT("woman-glasses", screen, flip=True)
            + H2("Insurance")
            + KV([("General and professional liability", "[Policy in place before first visit; certificate on request]"),
                  ("Workers' compensation" if us else "Workers' compensation (icare or state scheme)", f"[Covers every employed {M['cg']}; certificate on request]"),
                  ("Employment model", f"{M['Cgs']} are our employees, not contractors, so they are covered and supervised")])
            + CALL("Insurance details are placeholders until policies are bound. We will not start care before they are.")
            + SECTION("Safety", "What we do when something goes wrong.", "Written protocols for the four risks families worry about most.")
            + safety
            + BAND("hands-young", "Say something, and we act on it.", "A named complaints process, with outside help you can reach at any time.")
            + H2("Complaints and escalation") + complaints
            + (P(f'Read the full <a href="/au/complaints.html">complaints process</a>.') if not us else "")
            + CTA(M, "Questions about safety?", f"Ask us anything before you sign. Call {M['phone']}."))
    page(M, f"{p}/trust", "Licensing, insurance and safety", "How to check us, how we screen people, and what we do when something goes wrong.",
         body, img="hands-table", eyebrow="Trust", chips=[("Level 2" if us else "Screened", "background checks"), ("24 h", "incident reports"), ("3", "step complaints ladder")])

def team(M):
    p, us, cg, Cg = M["p"], M["p"] == "us", M["cg"], M["Cg"]
    scr = "Level 2 screened" if us else "Worker screening"
    flips = FLIP([
        ("elder-nurse", f"Dementia {cg}", "Illustrative photo", f"<b>Before day one</b><span>40 hours of dementia training, shadow shifts with a senior {cg}.</span><div class=badges><i>Dementia trained</i><i>{scr}</i><i>First aid</i></div>"),
        ("elder-care", f"Senior {cg}", "Illustrative photo", "<b>What they do</b><span>Leads a small team, covers sick days and coaches newer team members on shift.</span><div class=badges><i>2+ years</i><i>Mentor</i></div>"),
        ("woman-glasses", "Care manager", "Illustrative photo", "<b>What they do</b><span>Runs your assessment, writes the plan, calls monthly and owns our promises for your family.</span><div class=badges><i>Care planning</i><i>Family coaching</i></div>"),
        ("elder-activity", "Activities lead", "Illustrative photo", "<b>What they do</b><span>Music, memory and outing ideas that turn a visit into a good afternoon.</span><div class=badges><i>Music and memory</i><i>Life Story</i></div>"),
        ("two-women", "Care advisor", "Illustrative photo", "<b>What they do</b><span>Answers the phone, books assessments and calls back within 15 minutes.</span><div class=badges><i>First contact</i></div>"),
        ("man-table", "Director", "Illustrative photo", "<b>What they do</b><span>Accountable for every promise. The person you escalate to.</span><div class=badges><i>Escalation</i></div>"),
    ])
    curriculum = T(["Module", "Hours", "What it covers"], [
        ["Understanding dementia", "6", "Types, stages and what changes in the brain, in plain words"],
        ["Calming communication", "8", "One question at a time, validating feelings, never arguing"],
        ["Sundowning and distress", "6", "Triggers, routines and calm responses in the late afternoon"],
        ["Wandering and home safety", "4", "Door sensors, safety walk-throughs, the emergency ladder"],
        ["Personal care with dignity", "8", "Bathing, dressing, toileting, transfers, privacy"],
        ["Meals and hydration", "4", "Finger foods, prompts, recording every glass"],
        ["Life Story and activities", "4", "Music, photos, purposeful tasks"],
    ])
    body = (SUMMARY(f"Every {cg} is screened, dementia trained and introduced to your family before their first visit. Real names and photos appear here as each person joins; until then the photos are illustrative.")
            + SECTION("The team", "The people who will be in their home.", "Tap or hover a card to turn it over.")
            + flips
            + SPLIT("hands-care", H2("Meet your " + cg + " before day one") + P(
                f"You meet the main {cg} and the backup {cg} before care starts, at home or on a video call. If it does not feel right, we change the match, no questions asked.")
                + TICKS(["Matched on temperament and interests, not only availability", "A 30-second intro video for each " + cg + " (being filmed as we hire)", "A backup who already knows your family"]))
            + H2("What every " + cg + " passes")
            + T(["Check", "United States (Florida)" if us else "Australia"],
                ([["Background", "Level 2 fingerprint screening, Chapter 435 F.S."], ["References", "Two, checked by phone"], ["Training", "40 hours dementia program plus shadow shifts"],
                  ["Health", "TB screening where required"], ["Driving", "Licence and record check if they drive clients"]] if us else
                 [["Background", "NDIS Worker Screening Check or police check"], ["Conduct", "Code of Conduct for Aged Care"], ["References", "Two, checked by phone"],
                  ["Training", "40 hours dementia program plus shadow shifts"], ["Driving", "Licence and vehicle check if they drive clients"]]))
            + H2("Dementia training curriculum") + curriculum
            + GALLERY(["elder-activity", "piano3", "puzzle"], ["Activities that fit the person", "Music they still know by heart", "Small tasks with a purpose"])
            + CTA(M, "Want to meet the team?", f"Book a free assessment and meet your care manager first.", img="elder-couple"))
    page(M, f"{p}/team", "Our care team", f"Screened, dementia trained and introduced to you before day one.",
         body, img="elder-nurse", eyebrow="Trust", chips=[("40 h", "dementia training"), ("2 to 3", "named team"), ("Day 0", "meet before care")])

def reviews(M):
    p, live = M["p"], M["live"]
    body = (SUMMARY("We have no reviews yet. When real families review us on Google, their reviews appear here live, with the total count and our reply to each one, including the low ones.")
            + f'<div class="empty reveal"><h3>No reviews yet, and we will not invent any.</h3><p style="margin:8px auto">'
            + (f"We are a new agency in {M['metro']}." if live else "We are not providing care in Australia yet.")
            + " This space fills from our own Google Business Profile only.</p></div>"
            + H2("How a review will look") + P("Layout example only. No review text is shown until it is real.")
            + '<div class="card reveal" style="max-width:640px;padding:22px"><p><b>[Reviewer first name]</b> &middot; [Star rating from Google] &middot; [Date]</p>'
              '<p>[Review text from Google appears here]</p><p style="border-left:3px solid var(--coral);padding-left:12px"><b>Reply from ' + BRAND + ':</b> [Our reply appears here]</p></div>'
            + SPLIT("tea-book", H2("Our review policy") + TICKS([
                "We never pay for, reward or discount in exchange for a review",
                "We never ask only happy families (no review gating)",
                "We never reuse reviews from another business or another country",
                "We show low reviews and reply to every one in public",
                "US and Australian reviews are never mixed"]))
            + H2("How to leave a review")
            + FLOW([("1. Search Google", f"{BRAND} {M['metro']}"), ("2. Tap 'Write a review'", "Sign in with a Google account"), ("3. Say what happened", "Good or bad, in your own words")])
            + H2("Video stories")
            + P("Families who want to tell their story on video will be filmed only with signed consent from the person receiving care, or their legal decision maker. None exist yet.")
            + STRIP(["couple-dance", "grand-girl", "two-women", "bake-three", "couple-path", "man-photos", "flowers"])
            + CTA(M))
    page(M, f"{p}/reviews", "Reviews", "Real reviews only, with every reply. None yet, and none invented.",
         body, img="couple-couch", eyebrow="Trust")

def about(M):
    p, live, m = M["p"], M["live"], M["mom"]
    body = (SUMMARY(f"{BRAND} is a new in-home care agency built around one group of families: those living with dementia. "
                    + (f"We start in {M['metro']}, Florida." if live else "We start in Florida, and Australia is a waitlist while registration questions are settled."))
            + SPLIT("elder-care", H2("Why we started") + P(
                f"[Founder name] started {BRAND} after seeing how hard it is for families to find dementia care they can trust and see. "
                "Most agencies send whoever is free. Most families hear nothing until something goes wrong.")
                + P(f"We built the opposite: a small named team who knows your {m}'s story, and an app that shows the family every visit as it happens.")
                + CALL("[Founder story to be written by the founder, in their own words. We will not publish invented details.]"))
            + BAND("couple-path", "Care that knows who they are, not only what they need.")
            + SECTION("Mission and values", "What we stand for.")
            + GRID([("Dignity first", "Their home, their routine, their privacy. We are guests.", None, None),
                    ("Seen, not hidden", "Families should see care happen, not hope it did.", None, None),
                    ("Promises with numbers", "If we cannot measure it, we do not promise it.", f"/{p}/promises.html", "Our promises"),
                    ("Good jobs, good care", f"{M['Cgs']} who are paid, trained and respected stay longer.", f"/{p}/careers.html", "Careers"),
                    ("Plain words", "No jargon, no fear, and always what happens next.", None, None),
                    ("Honest limits", "We say what we do not cover, and who can help.", None, None)])
            + SPLIT("hands-table", H2("What we will not do") + UL([
                "Send a stranger without telling you",
                "Publish fake reviews or invented client numbers",
                "Give medical advice or claim to cure, prevent or slow dementia",
                "Lock you into long contracts",
                "Share health details with advertisers",
                "Provide care beyond what our " + ("license" if live else "registration") + " allows"]), flip=True)
            + SECTION("Milestones", "Where we are.", "Only real or clearly planned dates.")
            + TIMELINE([("2026", "Blueprint and service design", "Services, promises and the family app designed with dementia families in mind."),
                        ("Planned", "Florida license", "AHCA license application and approval, before any care is delivered."),
                        ("Planned", f"First families in {US['metro']}", "Assessments, first visits and our first published monthly results."),
                        ("Planned", "Australia", "Registration questions answered, then a move from waitlist to care.")])
            + GALLERY(["two-women", "bake-three", "man-dog", "flowers", "grandpa-selfie", "couple-dance"])
            + CTA(M))
    page(M, f"{p}/about", "About " + BRAND, "A new home care agency built for families living with dementia.",
         body, img="couple-color", eyebrow="About", chips=[("1", "specialty: dementia"), ("2 to 3", "named team"), ("Weekly", "family update")])

def careers(M):
    p, us, cg, cgs, Cgs = M["p"], M["p"] == "us", M["cg"], M["cgs"], M["Cgs"]
    pay = ([("USD 15.66", "median Florida home health and personal care aide hourly wage"), ("USD 17 to 19", "our target starting rate per hour, confirmed at offer"), ("40 h", "paid dementia training")]
           if us else [("Award+", "at or above the SCHADS Award"), ("Paid", "dementia training"), ("Choice", "of shifts in the app")])
    form = (f'<form class="book" data-mail="{MAIL}" data-kind="job application" data-market="{M["country"]}" novalidate><div class="bk-bar"><i></i></div>'
            f'<label><span>Your name</span><input name="name" autocomplete="name" required></label>'
            f'<label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required></label>'
            f'<label><span>When can you work?</span><select name="availability" required><option value="">Choose</option><option>Weekdays</option><option>Evenings</option><option>Weekends</option><option>Nights</option><option>Any time</option></select></label>'
            f'<label><span>Experience</span><select name="experience" required><option value="">Choose</option><option>New to care</option><option>Under 2 years</option><option>2 to 5 years</option><option>5+ years</option></select></label>'
            f'<label><span>Anything else (optional)</span><textarea name="note" rows="3" placeholder="Languages, certificates, a car"></textarea></label>'
            f'<label class="chk small"><input type="checkbox" name="consent" required> <span>I agree to be contacted by phone{" and text" if us else ", SMS"} about this application. <a href="/{p}/privacy.html">Privacy policy</a>.</span></label>'
            f'<button class="btn big" type="submit">Send my application</button><p class="bk-err" role="alert"></p>'
            f'<div class="bk-ok" hidden tabindex="-1"><img src="/img/two-women.jpg" alt="" class="adv"><div><h3>Thank you. Your application is ready to send.</h3>'
            f'<p>Your email app has opened with the details. Press send and we will text you within 15 minutes in business hours.</p></div></div></form>')
    body = (KPI(pay)
            + (CALL("The USD 15.66 median is a published figure for Florida aides. Our starting rate is a target until we make our first offers.") if us else
               CALL("Pay is at or above the Social, Community, Home Care and Disability Services (SCHADS) Award. Exact rates are confirmed at offer."))
            + SPLIT("elder-nurse", H2("Why work with us") + TICKS([
                "Pay shown openly, before you apply", "Guaranteed-hours options for people who want stability", "Pick and swap shifts in the app",
                "Paid dementia training, then a specialist track", f"A small client list, so you know the people you care for", "A care manager who answers the phone"]))
            + SECTION("Career path", "From " + cg + " to care manager.")
            + FLOW([(M["Cg"], "Paid training, shadow shifts, a named team"), ("Dementia specialist", "Advanced module and higher rate"),
                    ("Senior " + cg, "Lead a team, mentor new starters"), ("Care manager", "Assessments, care plans and families")])
            + SECTION("A day in the life", "What the work looks like.", "Illustrative scenes. Real stories from our team will replace them, with consent.")
            + CAROUSEL([("tea-woman", "7:45 am", "Check the app: today's client, their Life Story and yesterday's notes."),
                        ("bake-three", "10:00 am", "Baking scones together, because she loved to bake for her grandchildren."),
                        ("couple-path", "1:00 pm", "A slow walk in the garden after lunch."),
                        ("piano3", "3:30 pm", "Familiar music for the late afternoon, part of the sundowning plan."),
                        ("woman-phone", "5:00 pm", "A quick care note, and a thank-you message from the family.")], "A day in the life")
            + SPLIT("phone1", H2(f"The {cg} app") + TICKS([
                "Shift offers with one-tap accept", "Client Life Story profiles", "GPS check-in and check-out", "A quick care-note form",
                "A message line to your care manager", "A feed of thank-you messages from families"]), flip=True)
            + SECTION("Training", "Specialist training is part of the job.")
            + T(["Stage", "What you learn", "Paid"], [["Before day one", "40-hour dementia program, personal care, safety", "Yes"],
                                                      ["First month", "Shadow shifts with a senior " + cg, "Yes"], ["Every month", "Refreshers and case discussions", "Yes"]])
            + SECTION("Apply", "Apply in 3 minutes.", "We text you within 15 minutes in business hours, and you get one contact person and a clear timeline.")
            + f'<div class="two"><div>{form}</div><div>'
            + TIMELINE([("Day 0", "Apply", "This form, about 3 minutes."), ("Day 1", "Phone chat", "15 minutes about you and the work."),
                        ("Days 2 to 7", "Interview and checks", "Meet us, references and " + ("Level 2 screening" if us else "worker screening") + "."),
                        ("Week 2", "Training", "Paid dementia training and shadow shifts.")]) + "</div></div>"
            + BAND("hands-care", "Know someone who would be good at this?", f"Refer a {cg} we hire and you receive a referral bonus once they complete 90 days. [Bonus amount to be confirmed.]")
            + CTA(M, "Questions about the job?", f"Call {M['phone']} and ask for recruitment.", img="two-women"))
    page(M, f"{p}/careers", "Care for people who are not just clients.", f"Open pay, paid dementia training and shifts you pick in the app.",
         body, img="elder-activity", eyebrow="Careers", chips=pay)

for _M in (US, AU):
    promises(_M); trust(_M); team(_M); reviews(_M); about(_M); careers(_M)
