from ec import *

def rate(M, k, unit="hour"):
    return f'{money(M, M["rates"][k])}/{unit}'

def book_lbl(M): return "Book a free assessment" if M["live"] else "Join the waitlist"

def BTNS(M):
    p = M["p"]
    return (f'<p class="cta-b"><a class="btn big" href="/{p}/book.html">{book_lbl(M)}</a> <a class="btn o big" href="tel:{M["tel"]}">Call {M["phone"]}</a> {PRINT()}</p>')

def PRICE(M, k, text, unit="hour"):
    p = M["p"]
    return (f'<section class="band2 reveal"><p class="ey">Price</p><h2>From {rate(M, k, unit)}</h2><p>{text}</p>'
            f'<p>Your exact price is confirmed in writing after the free assessment. No sign-up fee, no long contract.'
            f'{" GST-free where it applies to aged care services." if p == "au" else ""}</p>'
            f'<p><a class="btn" href="/{p}/pricing.html">Estimate your monthly cost</a> <a class="btn o" href="{M["pay"][0]}">{M["pay"][1]} explained</a></p></section>')

def WAIT(M):
    return "" if M["live"] else CALL("<b>Australia:</b> we are not yet providing care or registered as a Support at Home provider. This page describes the service we plan to offer. "
                                     f"<a href='/au/book.html'>Join the waitlist</a> and we will tell you honestly when we can start.")

def DIFF(M, extra=None):
    cg = M["cg"]
    rows = [("Dementia-trained, every one", f"Every {cg} finishes our dementia training before their first visit, not 'when they get to it'."),
            ("The same small team", f"Two or three {M['cgs']} who know them, and a backup you meet before day one."),
            ("You can see it happen", "The family app shows check-ins, care notes and a weekly summary."),
            ("Promises with numbers", "Start times, replacement times and call-back times we measure and publish.")]
    return GRID([(a, b, None, None) for a, b in (extra or []) + rows][:6], 3)

# ---------------------------------------------------------------- hub
def hub(M):
    p, cg = M["p"], M["cg"]
    r = M["rates"]
    help_ = [("Memory is the main worry", "dementia-care"), ("They need hands-on help washing or dressing", "personal-care"),
             ("They are lonely or not eating well", "companion-care"), ("I am exhausted and need a break", "respite-care"),
             ("They are coming home from hospital", "after-hospital"), ("They should not be alone at night", "24-7-care"),
             ("I live far away", "care-from-afar")]
    chooser = ('<div class="pill-row reveal">' + "".join(f'<a href="/{p}/services/{s}.html">{t} &rsaquo;</a>' for t, s in help_) + "</div>")
    table = T(["Service", "What is included", "Typical hours", "From"], [
        ["<a href='/%s/services/dementia-care.html'>Dementia care</a>" % p, "Life Story profile, routines, sundowning and safety plans, family coaching", "15 to 50 a week", rate(M, "dementia")],
        ["<a href='/%s/services/personal-care.html'>Personal care</a>" % p, "Bathing, dressing, toileting, transfers, grooming", "10 to 30 a week", rate(M, "personal")],
        ["<a href='/%s/services/companion-care.html'>Companion care</a>" % p, "Company, outings, meals, light housework, reminders", "6 to 20 a week", rate(M, "companion")],
        ["<a href='/%s/services/respite-care.html'>Respite care</a>" % p, "Hours to overnight breaks for the family carer", "4 hours to a weekend", rate(M, "companion")],
        ["<a href='/%s/services/after-hospital.html'>Care after hospital</a>" % p, "Discharge coordination, first-week plan, personal care", "Short term, 2 to 6 weeks", rate(M, "personal")],
        ["<a href='/%s/services/24-7-care.html'>24/7 and live-in</a>" % p, "Awake day shifts, awake or sleep-over nights, a team rota", "Around the clock", rate(M, "overnight", "night") + " for nights"],
        ["<a href='/%s/services/care-from-afar.html'>Care from afar</a>" % p, "Named Care Director, app, monthly video call, errands", "Added to any plan", rate(M, "dementia")]])
    body = (WAIT(M) +
            SECTION("Help me choose", "Start with what is worrying you most.", "Tap the closest match, or take the 2-minute care quiz for a suggested plan.") + chooser +
            f'<p style="text-align:center"><a class="btn" href="/{p}/care-quiz.html">Take the care needs quiz</a></p>' +
            SECTION("All services", "Seven services, one small team.", f"Mix them as needs change. The same {M['cgs']} stay with you as the plan grows.") +
            SERVICE_GRID(M) +
            SECTION("Compare", "What each service includes.") + table +
            BAND("couple-dance", "Care that matches the day they are having.", "Some days it is a walk and a chat. Some days it is a bath, a calm afternoon and a careful eye. The plan bends; the team stays the same.",
                 f'<a class="btn" href="/{p}/book.html">{book_lbl(M)}</a>') +
            SECTION("How we are different", f"What you get with every service.") + DIFF(M) +
            GALLERY(["two-women", "bake-three", "flowers", "man-photos", "puzzle", "couple-path"],
                    ["A good afternoon is the goal", "Cooking together, the way they always did", "Garden time", "Old photos, new conversations", "Puzzles at their own pace", "Daily walks"]) +
            P("<small>Photos are illustrative stock images, not our clients.</small>") +
            NOTCOVER(["Nursing or medical care such as injections, wound care or medication administration (we work alongside nurses and doctors)", "Cleaning a whole house top to bottom; we do light housework linked to their care",
                      "Driving in a client's own car without the right insurance in place"]) +
            CTA(M))
    page(M, f"{p}/services/index", "Home care services that grow with them",
         f"Dementia, personal, companion, respite, after-hospital, 24/7 and long-distance care in {M['metro']}, from one small team of trained {M['cgs']}.",
         body, img="couple-color", eyebrow="Services", chips=[(rate(M, "companion"), "Companion care from"), ("7", "services, one team"), ("3 hours", "minimum visit")])

# ---------------------------------------------------------------- dementia
def dementia(M):
    p, cg, cgs, m = M["p"], M["cg"], M["cgs"], M["mom"]
    life = ('<div class="two reveal"><div class="card" style="padding:26px"><p class="ey">Sample Life Story profile &middot; demo</p>'
            '<h3 style="font-family:var(--serif);font-size:26px">Walter, 82, "Walt"</h3>' +
            KV([("Career", "Shipyard welder for 38 years. Proud of it. Loves talking about boats."), ("Music", "Frank Sinatra, Glenn Miller. Big band calms him in the afternoon."),
                ("Pets", "Had a beagle called Rex. Ask about Rex when he is unsettled."), ("Favourite foods", "Pancakes, tomato soup, root beer floats. Dislikes fish."),
                ("Daily routine", "Up at 6:30. Coffee before anything else. Newspaper on the porch."), ("Things that upset him", "Being rushed. Loud TV. Being told his wife has died; say she is 'out'."),
                ("What calms him", "Holding a warm mug. Sorting nuts and bolts in a tin. Hand on shoulder.")]) +
            '</div><div>' + IMG("man-photos", "The profile is filled in by the family before the first visit and read on every visit.") +
            P(f"Your {cg} reads it before every visit in the app. When Walt asks for Rex, they do not correct him: they ask him to tell them about Rex. "
              "That is what knowing who someone is looks like in practice.") + "</div></div>")
    safety = FLOW([("Home safety walk", "Trip hazards, lighting, the bathroom, stove and medicine storage, with a written list."),
                   ("Wandering plan", "Door sensors through partner products if you want them, a recent photo on file, a list of places they used to go."),
                   ("Emergency ladder", "Who we call first, second and third, and what each person is asked to do."),
                   ("Review monthly", "The care manager updates the plan as things change.")])
    arc = DAYARC([("7:00", "Coffee and the paper, the way it has always been"), ("10:00", "Walk while energy is highest"), ("12:30", "Lunch, finger foods if needed"),
                  ("15:00", "Lights up, TV off, big band on"), ("16:30", "A familiar task: folding, sorting, watering"), ("18:00", "Early supper, calm voices"), ("20:00", "Wind-down, same order every night")])
    faq = [("What stage of dementia do you care for?", f"<p>All stages, from early memory loss to late stage. The plan and hours change as needs change, and the same team stays with you.</p>"),
           ("How are your " + cgs + " trained in dementia?", f"<p>Every {cg} completes our dementia training before their first visit: calming communication, sundowning, wandering safety, personal care with dignity, meals and hydration, then monthly refreshers.</p>"),
           ("What if they refuse help?", f"<p>It is common. We start slowly, often as a 'friend' or 'helper' rather than a carer, lead with things they enjoy and build trust over several visits. Read our guide on <a href='/{p}/resources/index.html'>when a parent refuses help</a>.</p>"),
           ("Can you help with sundowning?", "<p>Yes. We build a late-afternoon routine with the family: light, sound, a snack, a familiar task and fewer demands. It is written into the care plan.</p>"),
           ("Do you give medicines?", "<p>We give reminders and record that they were taken" + (", within what our license allows" if p == "us" else "") + ". Administering medicines is done by nurses or as their doctor directs.</p>")]
    body = (WAIT(M) +
        SPLIT("elder-care", f'<p class="ey">Who it is for</p><h2>For families living with dementia at home.</h2>' +
              P(f"Your {m} or {M['dad']} has a diagnosis, or you are seeing the signs: repeated questions, missed meals, confusion in the late afternoon, getting lost on a familiar walk.",
                f"You want them to stay at home, safely, with people who understand dementia and treat them as the person they have always been.") +
              f'<p><a class="btn" href="/{p}/book.html">{book_lbl(M)}</a></p>') +
        SECTION("Life Story profile", "Before the first visit, we learn who they are.", f"Career, music, pets, favourite foods, routines and the things that upset them. Your {cg} sees it on every visit.") + life +
        SECTION("Stage guide", "What care looks like at each stage.", "Drag the slider. Honest guidance on when to add hours.") + STAGES(M) +
        BAND("hands-young", "Matched on temperament, not only on availability.",
             f"A quiet retired engineer and a chatty {cg} who loves gardening may not be the right fit. We match on personality, interests and language, then check in after the first two weeks.") +
        SECTION("Safety plan", "A plan for the worries that keep you up at night.") + safety +
        SPLIT("switch", H3("Partner sensors, if you want them") + P("Door sensors, fall-detection pendants and smart plugs can alert the care team and family. They are optional, from partner companies, and set up with your consent.") +
              TICKS(["Door opened at night: alert to the on-call care manager", "No movement by 9am: a check-in call", "Emergency button: alerts the family circle"]), flip=True) +
        SECTION("Sundowning plan", "A calmer late afternoon, built with the family.", "Many people with dementia become restless or frightened as daylight fades. We plan for it rather than react to it.") + arc +
        SECTION("Family coaching", "A free session for relatives.") +
        SPLIT("video-call2", P("One hour, at home or by video, for anyone in the family. What to say when they ask for someone who has died. How to stop arguing about facts. How to share care between siblings without resentment. How to look after yourself.") +
              TICKS(["Calming phrases that work", "What to stop saying", "Making visits easier", "Planning the next six months"]) + P("<small>Included free with every dementia care plan.</small>")) +
        SECTION("What is included", f"Everything a good dementia {cg} does.") +
        GRID([("Personal care", "Bathing, dressing, toileting and continence care with dignity and patience.", None, None),
              ("Meals and fluids", "Cooking their favourites, finger foods, drinks offered on a schedule and recorded.", None, None),
              ("Routine and activity", "Music, memory boxes, photos, walks, gardening and simple tasks with purpose.", None, None),
              ("Medication reminders", "Reminders and a record in the app, within the scope we are allowed.", None, None),
              ("Appointments", "Getting ready, getting there, and notes for the family afterwards.", None, None),
              ("Light housework", "Laundry, dishes and tidy spaces that are safe to move around.", None, None)], 3) +
        SECTION("How we are different", "Not a general agency with a dementia page.") +
        DIFF(M, [("Life Story on every visit", "Not a form in a drawer: it is in the app, read before each visit."), ("Family coaching included", "Because the family lives with dementia too.")]) +
        STRIP(["man-photos", "piano3", "puzzle", "flowers", "couple-path", "tea-book", "man-dog", "bake-three"]) +
        PRICE(M, "dementia", f"Dementia care is our specialist rate because every {cg} is trained for it and works in a small, stable team. Twenty hours a week is about {money(M, M['rates']['dementia'] * 20 * 52 / 12)} a month.") +
        SECTION("Questions", "Five questions families ask about dementia care.") + ACC(faq, id="faq-dem") +
        NOTCOVER(["Diagnosis, treatment or medical advice; that is for their doctor or specialist", "Locked-door or restraint-based care; we never restrain anyone",
                  "Clinical nursing tasks such as injections or wound dressings", "A guarantee of any health outcome; good care supports wellbeing but cannot stop dementia progressing"]) +
        BTNS(M) + CTA(M, img="elder-hands"))
    page(M, f"{p}/services/dementia-care", "Dementia care that knows who they are, not only what they need",
         f"Trained {cgs}, a Life Story profile read on every visit, a stage-by-stage plan and a family app, so your {m} stays at home with people who understand.",
         body, img="elder-care", eyebrow="Dementia care",
         chips=[(rate(M, "dementia"), "From"), ("Before day one", "dementia training complete"), ("2 to 3", f"the same {cgs}")])

# ---------------------------------------------------------------- personal care
def personal(M):
    p, cg, cgs = M["p"], M["cg"], M["cgs"]
    tasks = T(["Task", "What we do", "How we train for it"], [
        ["Bathing and showering", "Shower, bath or bed bath, at their pace, with towels kept over them", "Practical session on privacy, skin checks and water safety"],
        ["Dressing", "Choosing clothes with them, helping with buttons, shoes and compression stockings", "Offering choices, adaptive clothing, dressing someone in pain"],
        ["Toileting and continence", "Prompting, help in the bathroom, continence products, changing and skin care", "Dignity and infection control, recognising urinary infections"],
        ["Transfers", "Bed to chair, chair to toilet, using hoists or frames that are in the home", "Safe moving and handling, equipment checks"],
        ["Grooming", "Hair, shaving, nails (not medical foot care), teeth and dentures, make-up if they like it", "Looking how they want to look, not how we would"],
        ["Eating", "Setting up meals, cutting food, gentle help to eat, recording meals and drinks", "Swallowing warning signs, when to call for help"]])
    faq = [(f"Can I ask for a male or female {cg}?", "<p>Yes. Same-gender care is a standard option, not a special request, and we plan rotas around it.</p>"),
           ("What if they are embarrassed?", "<p>That is normal. We start with the least personal tasks, explain each step, keep them covered and let them do every part they can.</p>"),
           ("How long is a visit?", "<p>Visits are at least 3 hours, so nothing is rushed. Shorter morning routines can be combined with other help.</p>"),
           ("Can you help if they use a hoist?", "<p>Yes, if the equipment is in the home, has been assessed, and our " + cgs + " have been shown how to use it safely.</p>"),
           ("Is personal care a medical service?", "<p>No. It is hands-on help with daily living. Nursing tasks are done by nurses.</p>")]
    body = (WAIT(M) +
        SPLIT("bathroom", '<p class="ey">Who it is for</p><h2>For people who need hands-on help, and want to keep their dignity.</h2>' +
              P(f"Maybe a fall has made the shower frightening. Maybe arthritis makes buttons impossible. Maybe your {M['mom']} has started wearing the same clothes for a week.",
                "Personal care means help with the most private parts of the day, done with patience, privacy and as much independence as they want.")) +
        SECTION("What is included", "A clear list of what we help with.") +
        '<div class="two">' + TICKS(["Bathing, showering and bed baths", "Dressing and undressing", "Toileting and continence care", "Transfers and moving safely"]) +
        TICKS(["Grooming: hair, shaving, teeth, nails", "Help to eat and drink", "Skin checks and reporting changes", "Getting ready for appointments"]) + "</div>" +
        SECTION("Tasks and training", "How we train for each task.") + tasks +
        BAND("hands-care", "Our privacy promise.", f"Doors closed. Towels over them. Every step explained before it happens. They decide the order. Nothing about their body goes in a photo or a message without their agreement, ever.") +
        SPLIT("woman-glasses", H3(f"Choose a male or female {cg}") +
              P(f"Same-gender care is a standard option. Tell us at the assessment and we build the team around it. If a backup is needed, they are the same gender too.") +
              TICKS(["Same-gender team on request", "Language and culture taken into account", "You can ask to change a " + cg + ", no reason needed"]), flip=True) +
        SECTION("How we are different", "Personal care without the rush.") + DIFF(M, [("Three-hour minimum", "Long enough to do it properly, not a 15-minute dash.")]) +
        PRICE(M, "personal", "Personal care includes everything on this page and the companionship in between.") +
        SECTION("Questions", "Five questions about personal care.") + ACC(faq, id="faq-pc") +
        NOTCOVER(["Wound care, catheter changes, injections or other nursing tasks", "Medical foot care such as cutting thick or diseased toenails (a podiatrist does this)", "Lifting someone without the right equipment when an assessment says it is needed"]) +
        BTNS(M) + CTA(M, img="woman-glass"))
    page(M, f"{p}/services/personal-care", "Help with bathing and dressing that protects their dignity",
         f"Hands-on help with washing, dressing, toileting and moving safely, from trained {cgs} who never rush and always ask first.",
         body, img="woman-glass", eyebrow="Personal care", chips=[(rate(M, "personal"), "From"), ("Same-gender", "option, as standard"), ("3 hours", "minimum visit")])

# ---------------------------------------------------------------- companion
def companion(M):
    p, cg, cgs = M["p"], M["cg"], M["cgs"]
    outings = ["Coffee at the same caf&eacute; every Tuesday", "The library or a bookshop", "A garden " + M["center"] + " in spring", "A walk by the water",
               "Church, temple or mosque", "The hairdresser or barber", "A matinee", "Visiting an old friend"]
    library = GRID([("Breakfast club", "Pancakes, eggs the way they like them and the morning paper read aloud.", None, None),
                    ("Soup and bake", "Cooking an old family recipe together, then sharing it with a neighbour.", None, None),
                    ("Music hour", "Their favourite decade on the speaker, singing optional.", None, None),
                    ("Memory box", "Old photos, postcards and objects that start a conversation.", None, None),
                    ("Garden jobs", "Watering, deadheading, potting herbs for the kitchen.", None, None),
                    ("Puzzles and cards", "Jigsaws, crosswords, gin rummy, dominoes.", None, None)], 3)
    faq = [("What is companion care?", "<p>Company and practical help at home: conversation, meals, outings, light housework and reminders, without hands-on personal care.</p>"),
           ("Can you drive them places?", "<p>Yes, in our insured arrangements or by accompanying them on taxis or rideshare. Mileage is listed on the pricing page.</p>"),
           ("What if they say they do not need company?", f"<p>Many people say that. We start with something practical, like shopping or a lift to the hairdresser, and the friendship follows.</p>"),
           ("How do you match " + cgs + "?", "<p>On interests, temperament and language. A retired teacher and a " + cg + " who loves books often get on very well.</p>"),
           ("Can companion care grow into more?", "<p>Yes. If needs change, the same " + cgs + " can add personal or dementia care.</p>")]
    body = (WAIT(M) +
        SPLIT("two-women", '<p class="ey">Who it is for</p><h2>For people who are lonely, or managing but slipping.</h2>' +
              P("Long days alone. Meals skipped because cooking for one feels pointless. Fewer phone calls, fewer outings, more television.",
                f"Companion care brings back the ordinary good things: conversation, a cooked lunch, a walk, a reason to get dressed. It also means someone notices early when things change.")) +
        SECTION("Daily life", "What a companion visit looks like.") +
        TIMELINE([("10:00", "Arrive and catch up", "Coffee, the news, what is on their mind."), ("10:30", "Something practical", "Shopping, a prescription, laundry, the garden."),
                  ("12:00", "Lunch together", "Cooked together where possible, and drinks recorded."), ("13:00", "Out or in", "A walk, an outing or a project at home."),
                  ("14:30", "Wind down", "A note in the app for the family and a plan for next time.")]) +
        SECTION("Outing ideas", "Getting out, at their pace.") + PILLS(outings) +
        SECTION("Meal and activity library", "Ideas our " + cgs + " bring with them.") + library +
        BAND("couple-path", "Matched on what they love.", f"Gardener with gardener. Card player with card player. We ask about hobbies at the assessment and match {cgs} to them.") +
        SECTION("A good day", "The good-day photo wall.", "When clients and families agree, we share moments like these. These are illustrative stock photos until our own clients share theirs.") +
        GALLERY(["flowers", "bake-three", "puzzle", "piano3", "tea-book", "man-dog", "couple-out", "grandpa-selfie", "breakfast"],
                ["Watering the roses", "Three generations, one recipe", "The corner pieces first", "Playing again after years", "Tea and a good book",
                 "A walk with an old friend", "Sitting in the sun", "A selfie for the grandchildren", "Breakfast with company"]) +
        SECTION("How we are different", "Company that is planned, not just time filled.") + DIFF(M) +
        PRICE(M, "companion", "Companion care is our most flexible service and the easiest way to start.") +
        SECTION("Questions", "Five questions about companion care.") + ACC(faq, id="faq-cc") +
        NOTCOVER(["Hands-on personal care such as bathing or toileting (that is personal care)", "Heavy cleaning, gardening with machinery or home repairs", "Managing their money or signing documents for them"]) +
        BTNS(M) + CTA(M, img="couple-out"))
    page(M, f"{p}/services/companion-care", "Someone to talk to, walk with and cook alongside",
         "Company, meals, outings and a watchful eye, from a matched companion who comes back week after week.",
         body, img="two-women", eyebrow="Companion care", chips=[(rate(M, "companion"), "From"), ("Matched", "on hobbies and temperament"), ("Weekly", "family update")])

# ---------------------------------------------------------------- respite
def respite(M):
    p, cg, cgs = M["p"], M["cg"], M["cgs"]
    faq = [("What is respite care?", "<p>Care that gives the usual family carer a break, from a few hours to an overnight or a weekend.</p>"),
           ("Will they be OK with someone new?", f"<p>We introduce the {cg} before the first break, use the Life Story profile and keep the same {cg} for future breaks.</p>"),
           ("Can I book respite at short notice?", "<p>Yes when we have " + cgs + " free; booking a regular break is the most reliable way to get one.</p>"),
           ("Is there funding for respite?", ("<p>Some long-term care insurance policies and veterans' programs cover respite. <a href='/us/paying-for-care.html'>Paying for care</a>.</p>" if p == "us"
              else "<p>Respite can be part of a Support at Home plan. <a href='/au/funding.html'>Funding explained</a>.</p>")),
           ("Do I have to leave the house?", "<p>No. Many carers stay home and sleep, or work in another room. The break is yours to use.</p>")]
    burnout = ACC([("You are tired even after sleeping", "<p>Exhaustion that does not lift is one of the earliest signs. It is a signal to get help, not to try harder.</p>"),
                   ("You feel resentful, then guilty", "<p>Very common and not a sign you love them less. It is a sign you are carrying too much alone.</p>"),
                   ("You have stopped seeing friends", "<p>Isolation creeps up on carers. A regular break gives you one fixed afternoon that is yours.</p>"),
                   ("Your own health is slipping", "<p>Missed check-ups, back pain, poor sleep. See your own doctor and tell them you are a carer.</p>"),
                   ("You snap at the person you care for", "<p>It happens to good people under too much strain. Take a break before it gets worse, and talk to someone.</p>")], id="burn")
    body = (WAIT(M) +
        SPLIT("tea-woman", '<p class="ey">Who it is for</p><h2>For family carers who need time back.</h2>' +
              P(f"You are looking after your {M['mom']}, your {M['dad']} or your partner, and you have not had a day off in months. You love them. You are also worn out.",
                f"Respite care means a trained {cg} steps in for a few hours, a day or a night, so you can sleep, work, see friends or simply sit down.")) +
        SECTION("Take a break planner", "Build your breaks for the month.", "Tell us how worn out you feel, pick the length of break, then tap the days. We will suggest a plan.") + CAL(M) +
        P("<small>The total is an estimate at the companion rate. Personal or dementia care rates apply when that help is needed.</small>") +
        SECTION("Options", "From a few hours to a weekend.") +
        GRID([("4-hour break", "A morning to yourself. Great for appointments, a haircut or a nap.", None, None),
              ("Full day", "Eight hours: go to work, visit friends, or do nothing at all.", None, None),
              ("Overnight", "Sleep through. A " + cg + " stays awake or sleeps over, as the plan needs.", None, None),
              ("Weekend or holiday", "A team covers a few days so you can travel or attend a family event.", None, None)], 2) +
        BAND("tea-sill", "Caring for the carer is part of the care.", "A rested carer is a kinder, safer carer. Breaks are not a luxury.") +
        SECTION("Caregiver burnout", "Signs it is time for a break.") + burnout +
        P(f"Read more in our guide to <a href='/{p}/resources/index.html'>caregiver burnout and what to do</a>.") +
        SECTION("How we are different", "A break you do not spend worrying.") + DIFF(M, [("Same face each time", f"Regular breaks use the same {cg}, so they become a familiar friend.")]) +
        PRICE(M, "companion", "Respite is charged at the rate for the help needed, from companion care upwards. Overnights are priced per night.") +
        SECTION("Questions", "Five questions about respite care.") + ACC(faq, id="faq-rs") +
        NOTCOVER(["Respite in a residential facility; we provide care at home", "Emergency medical cover; call " + ("911" if p == "us" else "000") + " in an emergency", "Care for other people in the home who have not been assessed"]) +
        BTNS(M) + CTA(M, img="tea-book"))
    page(M, f"{p}/services/respite-care", "Take a break without worrying",
         f"Hourly, full-day and overnight breaks for family carers, from a trained {cg} who already knows them.",
         body, img="tea-woman", eyebrow="Respite care", chips=[(rate(M, "companion"), "From"), ("4 hours", "to a weekend"), ("Same", f"{cg} each break")])

# ---------------------------------------------------------------- after hospital
def hospital(M):
    p, cg, live = M["p"], M["cg"], M["live"]
    week = T(["Day", "What happens"], [["Day 1", "Home safely. Bed, bathroom and kitchen checked. Medicines collected and matched against the discharge list."],
                                       ["Days 2 to 3", "Personal care, meals and fluids. Watching for warning signs the hospital told us about."],
                                       ["Day 4", "Follow-up appointment booked or attended, with notes for the family."],
                                       ["Days 5 to 7", "Gentle activity as advised, review with the care manager, hours adjusted."]])
    faq = [("How fast can you start?", "<p>Within 72 hours of signing, and often sooner. Call before discharge and we can plan with the hospital team.</p>" if live else
                                       "<p>We are not providing care in Australia yet. Ask the hospital about transition care and short-term restorative care, and join our waitlist.</p>"),
           ("Can the hospital refer directly?", f"<p>Yes. Discharge planners, social workers and doctors can use our <a href='/{p}/refer.html'>referral form</a>, which takes under two minutes.</p>"),
           ("Is this short-term?", "<p>Usually 2 to 6 weeks, then we step down or stop. Some families continue with fewer hours.</p>"),
           ("What about nursing and physio?", ("<p>Home health nursing and therapy ordered by a doctor may be covered by Medicare; we coordinate with those visits and do the non-medical care in between.</p>" if p == "us"
              else "<p>Nursing and allied health may come through transition care or Support at Home; we would work alongside those providers.</p>")),
           ("What if they go back into hospital?", "<p>We pause care, keep the team ready and restart when they come home.</p>")]
    checklist = TICKS(["A written list of medicines, with what changed", "Follow-up appointments and who booked them", "Warning signs to watch for, and who to call",
                       "Equipment needed: frame, shower chair, raised toilet seat", "Food in the fridge and someone to cook it", "Who will be there the first night"])
    body = (WAIT(M) +
        SPLIT("hospital", '<p class="ey">Who it is for</p><h2>For the first weeks home after a hospital or rehab stay.</h2>' +
              P("Coming home is a relief and a risk. Medicines change, energy is low, the bathroom is suddenly dangerous and families are juggling work and visits.",
                f"We coordinate with the discharge team, make the home safe and {'start care within 72 hours of signing' if live else 'plan to provide short-term care'}, with a first-week plan everyone can see.")) +
        SECTION("The 72-hour start", "From the first call to the first visit.", "Tick each step to see how the clock fills." if live else "This is how it will work once we are providing care in Australia.") + COUNT72(M) +
        SECTION("Discharge checklist", "Before they leave the ward, ask for these.") +
        '<div class="two"><div>' + checklist + f'<p>{PRINT()}</p></div>' + IMG("hallway", "Ask the discharge planner for everything in writing.") + '</div>' +
        BAND("porch", "Home is where recovery happens.", "With help in the right places, most people do better in their own bed, their own kitchen and their own routine.") +
        SECTION("First-week plan", "What the first seven days look like.") + week +
        f'<section class="band2"><p class="ey">For discharge planners and clinicians</p><h2>Refer in under two minutes.</h2><p>Name, contact, discharge date and needs. '
        f'{"We call back within the hour." if live else "Australian referrals join our waitlist and get a call the next business day."}</p>'
        f'<p><a class="btn" href="/{p}/refer.html">Make a referral</a></p></section>' +
        SECTION("How we are different", "Coordination, not just a visit.") + DIFF(M, [("We talk to the hospital", "We speak to the discharge team about medicines, mobility and follow-up before day one.")]) +
        PRICE(M, "personal", "After-hospital care is usually personal care rates for a few weeks, stepping down as they recover.") +
        SECTION("Questions", "Five questions about care after hospital.") + ACC(faq, id="faq-ah") +
        NOTCOVER(["Skilled nursing, wound care, IV medicines or physiotherapy (we coordinate with those teams)", "Medical decisions about discharge; those are made by the hospital",
                  "Transport by ambulance"]) +
        BTNS(M) + CTA(M, img="porch2"))
    page(M, f"{p}/services/after-hospital", "Home from hospital. Care starting in 72 hours." if live else "Home from hospital, with a plan for the first week",
         "Discharge coordination, a safe home, personal care and a first-week plan the whole family can see.",
         body, img="hospital", eyebrow="Care after hospital",
         chips=[("72 hours" if live else "Planned", "to the first visit" if live else "for Australia"), (rate(M, "personal"), "From"), ("2 to 6 weeks", "typical length")])

# ---------------------------------------------------------------- 24/7
def allday(M):
    p, cg, cgs, r = M["p"], M["cg"], M["cgs"], M["rates"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rota = T(["Shift"] + days, [["Day 7am to 3pm", "Maria", "Maria", "Maria", "James", "James", "Ana", "Ana"],
                                ["Evening 3pm to 11pm", "Ana", "Ana", "James", "Maria", "Maria", "James", "James"],
                                ["Night 11pm to 7am", "Lee", "Lee", "Lee", "Lee", "Sam", "Sam", "Sam"]])
    hourly = r["personal"]
    awake = hourly * 24 * 30
    sleep = (hourly * 16 + r["overnight"]) * 30
    cost = BARS(f"Illustrative monthly cost of round-the-clock options ({M['cur']})", [
        ("24 hours awake care at home, 30 days", awake, money(M, awake)),
        ("16 hours awake plus a sleep-over night, 30 days", sleep, money(M, sleep)),
        ("Two long day shifts only, 12 hours a day", hourly * 12 * 30, money(M, hourly * 12 * 30))],
        "Illustrative estimates from our starting rates, before insurance or funding. Residential care costs vary widely; compare quotes in your area. Your real price is in writing after assessment.")
    faq = [("What is the difference between awake and sleep-over nights?", f"<p>An awake {cg} stays up all night and is paid for every hour. A sleep-over {cg} has a bed and a protected sleep period, and is woken only occasionally. Sleep-over nights cost less.</p>"),
           ("Why a team and not one live-in person?", "<p>Nobody can care well around the clock for weeks. A team of three to five covers shifts, so everyone is rested and someone always knows them.</p>"),
           ("How quickly can 24/7 care start?", "<p>We usually build up over a few days as the team is introduced." + (" Care starts within 72 hours of signing." if M["live"] else "") + "</p>"),
           ("Do " + cgs + " get breaks?", "<p>Yes. Breaks and rest are built into the rota, and the law in each " + ("state" if p == "us" else "jurisdiction") + " sets minimums we follow.</p>"),
           ("Can 24/7 care be temporary?", "<p>Yes, for example after a hospital stay or at end of life, then step down.</p>")]
    body = (WAIT(M) +
        SPLIT("moon-house", '<p class="ey">Who it is for</p><h2>For people who should not be alone, day or night.</h2>' +
              P("Night-time wandering. Falls getting up to the bathroom. A partner who has not slept properly in months. Late-stage dementia, or the last months of life.",
                f"24/7 care puts a trained {cg} in the home around the clock, from a rota of a small team, so there is always someone fresh.")) +
        SECTION("Day and night", "How a 24-hour day is covered.", "Scroll to watch the day pass.") + DAYNIGHT(M) +
        SECTION("Awake or sleep-over nights", "Choose the night that fits the need.") +
        VS("Awake night", [("Who it suits", "Wakes often, wanders, needs turning"), ("The " + cg, "Awake all night"), ("Price", rate(M, "personal") + " for each hour")],
           "Sleep-over night", [("Who it suits", "Wakes once or twice"), ("The " + cg, "Sleeps in a private room"), ("Price", rate(M, "overnight", "night"))]) +
        SECTION("Sample weekly rota", "A team, not one tired person.", "Illustrative names. Every person on the rota has met your family first.") + rota +
        SECTION("Cost comparison", "What round-the-clock care costs.") + cost +
        BAND("moon2", "Rested people give better care.", f"Our rotas cap shift lengths and protect rest breaks. A {cg} on their fifth night without sleep is a risk, so we do not build rotas like that.") +
        SECTION("How we are different", "Planned like a hospital ward, felt like home.") + DIFF(M, [("A team leader", "One senior " + cg + " leads the rota and handovers.")]) +
        PRICE(M, "overnight", "Day hours are charged at the personal or dementia rate. Sleep-over nights are a flat rate per night.", unit="night") +
        SECTION("Questions", "Five questions about 24/7 care.") + ACC(faq, id="faq-247") +
        NOTCOVER(["A single person living in and working around the clock", "Nursing tasks overnight, unless a nurse is part of the plan", "Care for other household members"]) +
        BTNS(M) + CTA(M, img="moon-house"))
    page(M, f"{p}/services/24-7-care", "Around-the-clock care with a team, not one tired person",
         f"Day, evening and night shifts from a small rota of trained {cgs}, with awake or sleep-over nights.",
         body, img="moon-house", eyebrow="24/7 and live-in care", chips=[("3 shifts", "a day"), (rate(M, "overnight", "night"), "Sleep-over nights from"), ("Small", "named team")])

# ---------------------------------------------------------------- afar
def afar(M):
    p, cg, cgs, m = M["p"], M["cg"], M["cgs"], M["mom"]
    emer = 911 if p == "us" else "000"
    faq = [("Who is the Care Director?", "<p>One named senior person who knows your family, takes your calls and makes decisions with you. Not a call centre.</p>"),
           ("How will I know what is happening?", "<p>The family app shows each visit live, care notes and photos with consent. You also get a weekly summary and a monthly video call.</p>"),
           ("What happens in an emergency?", f"<p>The {cg} calls {emer} first, then the Care Director, who calls you within minutes and follows the emergency ladder you agreed.</p>"),
           ("Can you run errands?", "<p>Yes: groceries, prescriptions, rides to appointments, collecting mail and checking the house.</p>"),
           ("Can my siblings see the app too?", "<p>Yes. Invite them to the family circle with their own permissions: view only, can message, or can approve changes.</p>")]
    body = (WAIT(M) +
        SPLIT("video-call", '<p class="ey">Who it is for</p><h2>For families who live hours, states or countries away.</h2>' +
              P(f"You call your {m} every day and still worry. You fly in when there is a crisis. You wonder what you are not being told.",
                "Care from afar puts eyes, hands and a decision-maker in their home, and puts you back in the loop.")) +
        SECTION("Be there anyway", "From wherever you are to their front door.", "Scroll to zoom in.") + ZOOM(M) +
        SECTION("What is included", "Everything a long-distance family needs.") +
        GRID([("A named Care Director", "Your single point of contact, who knows your family and decides with you.", None, None),
              ("The family app", f"Live check-ins, care notes, mood and meals, photos with consent. <a href='/{p}/app.html'>See the app</a>.", None, None),
              ("Monthly video call", "With the Care Director and, if they like, your parent, to review how things are going.", None, None),
              ("Weekly summary", "Every Sunday, in plain words, by email and in the app.", None, None),
              ("Local errands", "Groceries, prescriptions, appointment rides, the mail and a check of the house.", None, None),
              ("Appointment notes", "We go with them and write down what the doctor said.", None, None)], 3) +
        SECTION("Emergency escalation", "What happens when something goes wrong.") +
        TIMELINE([("Minute 0", f"The {cg} acts", f"Calls {emer} if needed, keeps them safe and stays with them."),
                  ("Minute 5", "Care Director alerted", "Through the app and by phone, with what happened."),
                  ("Within minutes", "You are called", "The first person on your emergency ladder, then the next."),
                  ("Same day", "Written incident note", "What happened, what we did and what changes now."),
                  ("Within a week", "Review", "The care plan is updated and you approve it.")]) +
        BAND("grandpa-selfie", "Close, even when you are far.", "Photos, messages and a one-tap video call, so grandchildren and great-grandchildren stay part of the day.") +
        SECTION("How we are different", "You will never have to chase us.") + DIFF(M) +
        PRICE(M, "dementia", "Care from afar is added to any care plan. The Care Director, app and monthly call are included; errands are charged at the hourly rate.") +
        SECTION("Questions", "Five questions from long-distance families.") + ACC(faq, id="faq-af") +
        NOTCOVER(["Legal decisions such as power of attorney or guardianship (we can point you to help)", "Managing their bank accounts", "Medical decisions; those stay with them, you and their doctors"]) +
        BTNS(M) + CTA(M, img="video-call2"))
    page(M, f"{p}/services/care-from-afar", "Live far away? Be there anyway.",
         f"A named Care Director, a live family app, monthly video calls and local errands, so you know your {m} is safe without getting on a plane.",
         body, img="video-call", eyebrow="Care from afar", chips=[("1", "named Care Director"), ("Weekly", "summary"), ("Monthly", "video call")])

# ---------------------------------------------------------------- US landing pages
def lp(path, h, lede, img, points, faq):
    M = US
    body = (f'<section class="two lph reveal" style="margin:30px 0;align-items:center"><div><p class="ey">{M["metro"]} &middot; free care assessment</p>'
            f'<h1 style="max-width:16ch">{h}</h1><p class="lede">{lede}</p>' + TICKS(points) +
            f'<p><a class="btn big pulse" href="tel:{M["tel"]}">Call {M["phone"]}</a></p></div><div>{BOOK(M, compact=True)}</div></section>' +
            f'<img src="/img/{img}.jpg" alt="{alt(img)}" style="width:100%;height:340px;object-fit:cover;border-radius:28px" loading="lazy">' +
            SECTION("Our promises", "Measured and published, every month.") + PROMISES(M, link=False) +
            CALL(M["lic"]) + SECTION("Questions", "Three quick answers.") + ACC(faq, id="lpfaq") + CTA(M))
    page(M, path, h, lede, body, landing=True)

def landings():
    p = "us"
    lp("us/lp/dementia", "Dementia care at home, starting in 72 hours.", f"Trained caregivers, the same small team and a live app for the family. Starting rates from {money(US, US['rates']['dementia'])} an hour.",
       "elder-care", ["Every caregiver dementia-trained before day one", "Life Story profile read on every visit", "48-hour replacement, backup already introduced"],
       [("How much does it cost?", f"<p>Dementia care starts from {money(US, US['rates']['dementia'])} an hour, with a 3-hour minimum visit.</p>"),
        ("How fast can you start?", "<p>Within 72 hours of signing, after a free assessment.</p>"),
        ("Do you help with sundowning?", "<p>Yes. We build a calm late-afternoon routine with the family.</p>")])
    lp("us/lp/after-hospital", "Coming home from hospital? Care in 72 hours.", "We coordinate with the discharge team and start care within 72 hours of signing.",
       "hospital", ["Discharge checklist and first-week plan", "Personal care, meals and medicine reminders", "Updates for the family in the app"],
       [("Can the hospital refer?", "<p>Yes, discharge planners can use our referral form.</p>"),
        ("Is it short term?", "<p>Usually 2 to 6 weeks, then we step down.</p>"),
        ("Does Medicare pay?", "<p>Medicare generally does not cover non-medical home care; we explain your options.</p>")])
    lp("us/lp/care-from-afar", "Live far away? See their care, live.", "A named Care Director, a live family app and a weekly update for families who cannot be there.",
       "video-call", ["GPS check-in for every visit", "Weekly summary and monthly video call", "Emergency escalation within minutes"],
       [("Can my siblings see it?", "<p>Yes, invite them with their own permissions.</p>"),
        ("Can you do errands?", "<p>Yes: groceries, prescriptions and appointment rides.</p>"),
        ("What does it cost?", f"<p>Care from afar is added to any plan; care starts from {money(US, US['rates']['companion'])} an hour.</p>")])
    lp("us/lp/respite", "You need a break. We will take it from here.", "Hourly, full-day and overnight respite from a trained caregiver who already knows them.",
       "tea-woman", ["4-hour, full-day and overnight breaks", "The same caregiver each time", f"From {money(US, US['rates']['companion'])} an hour"],
       [("Can I book at short notice?", "<p>When we have caregivers free; regular breaks are the most reliable.</p>"),
        ("Will they be OK with someone new?", "<p>We introduce the caregiver first and use their Life Story profile.</p>"),
        ("Is respite covered?", "<p>Some long-term care insurance and veterans' programs cover it.</p>")])

for _M in (US, AU):
    hub(_M); dementia(_M); personal(_M); companion(_M); respite(_M); hospital(_M); allday(_M); afar(_M)
landings()
