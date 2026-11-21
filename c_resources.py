from ec import *

# ---------- helpers ----------
def EMERG(M): return "911" if M["p"] == "us" else "000"
def HELPLINE(M):
    return ("the Alzheimer's Association 24/7 Helpline on 1-800-272-3900" if M["p"] == "us"
            else "the National Dementia Helpline on 1800 100 500")

ARTS = {}  # (p, slug) -> (cat, title, img, summary)

def art(M, slug, cat, title, img, summary, body, related=(), img2=None):
    p = M["p"]
    rel = "".join(f'<a href="/{p}/resources/{s}.html">{ARTS[(p, s)][1] if (p, s) in ARTS else s}</a>' for s in related if (p, s) in ARTS)
    html_ = (f'<div class="art">{SUMMARY(summary)}{ARTICLE_META()}{body}'
             + (IMG(img2) if img2 else "")
             + (f'<h2>Related guides</h2><div class="pill-row">{rel}</div>' if rel else "")
             + f'<p class="cn">General information, not medical, legal or financial advice. If someone is in danger, call {EMERG(M)}.</p>{PRINT()}</div>' + CTA(M))
    ARTS[(p, slug)] = (cat, title, img, summary)
    page(M, f"{p}/resources/{slug}", title, summary, html_, img=img, eyebrow="Resources &middot; " + cat,
         jsonld=[{"@context": "https://schema.org", "@type": "Article", "headline": title, "description": summary,
                  "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND},
                  "dateModified": "2026-11-21", "inLanguage": M["lang"], "mainEntityOfPage": f"{DOMAIN}/{p}/resources/{slug}.html"}])


# ---------- shared articles ----------
def shared(M):
    p, m, cg, cgs, Cgs = M["p"], M["mom"], M["cg"], M["cgs"], M["Cgs"]
    us = p == "us"

    art(M, "dementia-stages", "Dementia", "What are the stages of dementia, and what care is needed at each?", "man-photos",
        f"Dementia is usually described in three broad stages: early, middle and late. In the early stage people need reminders and company a few hours a week; in the middle stage they need daily hands-on help and a safety plan; in the late stage they need help with almost everything, often around the clock.",
        H2("Why stages are only a rough guide") +
        P("Doctors use several scales, and no two people move through dementia the same way. Alzheimer's disease, vascular dementia, Lewy body dementia and frontotemporal dementia all progress differently, and good and bad days overlap. "
          "Think of the stages as a way to plan help, not a prediction. Ask their doctor which type of dementia they have, because it changes what to expect.") +
        H2("Early stage: still independent, needs a safety net") +
        P(f"Your {m} may still drive, cook and manage a conversation well, but miss appointments, repeat questions, lose track of bills or medicines and feel anxious about it. This is the time to plan while they can take part in the decisions.") +
        TICKS(["Companion visits 2 to 3 times a week, 8 to 15 hours in total", "Help with appointments, shopping and medication reminders",
               "Write the Life Story profile together: career, music, food, pets, routines and what upsets them",
               "Put legal and money paperwork in order: " + ("power of attorney and a health care surrogate" if us else "enduring power of attorney and an advance care directive"),
               "Learn calming communication before you need it"]) +
        SPLIT("elder-hands2", H3("Middle stage: daily help and a safety plan") +
              P("This is usually the longest stage. Routines get harder, late-afternoon confusion (sundowning) is common, and wandering, missed meals and trouble with bathing start to appear. Most families need daily help now.") +
              TICKS(["Daily visits from the same 2 to 3 " + cgs + ", 20 to 50 hours a week", "Personal care with dignity: bathing, dressing, toileting",
                     "A sundowning routine and a home safety walk-through", "Door sensors and an emergency contact ladder for wandering", "Regular breaks for the main family carer"])) +
        H2("Late stage: comfort, touch and familiar things") +
        P("People in the late stage may speak little, need help to eat, move and use the toilet, and sleep much of the day. Care becomes about comfort: skin care, careful repositioning, mouth care, familiar music and a calm voice. "
          "Many families use long shifts or 24/7 care with a team, and work alongside " + ("hospice" if us else "palliative care") + " services.") +
        T(["Stage", "What you might notice", "Typical help", "Typical hours"],
          [["Early", "Forgetting recent events, repeating questions, losing things", "Companion care, reminders, planning", "8 to 15 a week"],
           ["Middle", "Confusion late in the day, wandering, help needed to wash and dress", "Dementia care, personal care, safety plan", "20 to 50 a week"],
           ["Late", "Little speech, help with eating and moving, more sleep", "Long shifts or 24/7, comfort care", "50 a week to 24/7"]]) +
        H2("When to add hours") +
        UL(["A fall, a near miss with the stove or getting lost", "Weight loss or signs of not drinking enough", "The family carer is exhausted or unwell",
            "They are frightened when alone, especially in the evening", "A hospital stay, which often brings a step down"]) +
        P(f'Try our <a href="/{p}/services/dementia-care.html">interactive stage guide</a>, or talk it through with {HELPLINE(M)}.'),
        related=("sundowning", "wandering", "signs-time-for-home-care"), img2="hands-young")

    art(M, "sundowning", "Dementia", "How to handle sundowning at home", "moon-house",
        "Sundowning is restlessness, confusion or distress that gets worse in the late afternoon and evening. It usually helps to keep the day active, the late afternoon calm and bright, cut down noise and caffeine, and answer the feeling behind the words rather than arguing with the facts.",
        H2("What it looks like") +
        P(f"From around 3 or 4 pm your {m} may pace, ask to 'go home' while already at home, become suspicious, cry, or get angry with the person they love most. It is not deliberate, and it is not a sign you are doing something wrong.") +
        H2("Common triggers") +
        UL(["Tiredness, too little or too much daytime sleep", "Fading light and shadows that look like people", "Hunger, thirst, pain, constipation or needing the toilet",
            "A busy house: TV, visitors, cooking noise", "Changes in routine, a new " + cg + " or a recent hospital stay"]) +
        SPLIT("tea-woman", H3("A calm late-afternoon routine") +
              TICKS(["Get outside or near a window in the morning; daylight helps the body clock", "Keep naps short and early", "A snack and a drink at about 3 pm",
                     "Lights on before it gets dark; close curtains to cut reflections", "One familiar, gentle task: folding towels, sorting buttons, watering plants",
                     "Their music from age 15 to 25, played quietly", "Fewer visitors and no big decisions after 4 pm"])) +
        H2("What to say") +
        P("Answer the feeling, not the fact. If they say 'I need to go home', try 'You miss home. Tell me about it', then offer a cup of tea or a walk around the garden. Correcting them ('you are home') usually makes it worse.") +
        H2("When to call the doctor") +
        P("A sudden change in behaviour can be a sign of an infection, pain or a medicine side effect. Call their doctor if sundowning appears suddenly or gets much worse in a few days. Never change medicines without medical advice.") +
        P(f"Every {BRAND} client with dementia has a written sundowning plan, built with the family and followed by every {cg}."),
        related=("dementia-stages", "wandering", "caregiver-burnout"), img2="tea-sill")

    art(M, "refuses-help", "Dementia", f"What to do when a parent with dementia refuses help", "thoughtful",
        f"Refusing help is common and usually comes from fear of losing independence, not stubbornness. It helps to introduce help slowly, call it something else (a friend, a cleaner, someone 'for you, not them'), offer choices, and let the {cg} start with something they enjoy.",
        H2("Why they say no") +
        UL(["They do not believe they need help, which is part of the illness for many people", "Fear of strangers, of being 'put in a home' or of the cost",
            "Embarrassment about washing and toileting", "Feeling talked about rather than talked to"]) +
        H2("Approaches that work") +
        TICKS(["Start small: a 3-hour visit for an outing, cooking or gardening, not 'care'",
               f"Introduce the {cg} as a friend, a helper for you, or someone the doctor suggested",
               "Offer two choices, both of which are yes: 'Tuesday or Thursday?'", "Keep the same person for the first weeks",
               "Leave personal care until trust is built, unless safety demands it", "Let them give something back: teaching a recipe, showing photos"]) +
        P("Avoid long explanations and arguments. If a visit goes badly, try again another day with a different activity. Most people settle within two to four weeks.") +
        CALL(f"If they are unsafe and still refuse all help, speak to their doctor and {HELPLINE(M)} about options."),
        related=("dementia-stages", "talking-to-siblings", "signs-time-for-home-care"))

    art(M, "wandering", "Dementia", "How to keep a person with dementia safe from wandering", "walk-street",
        "Wandering is common in dementia and can be dangerous. Reduce the reasons to leave (boredom, needing the toilet, looking for 'home'), make exits less obvious, use door alerts, keep a recent photo ready and agree an emergency plan with neighbours and family.",
        H2("Why people wander") +
        P("Walking often has a purpose: going to a job they used to have, looking for a parent, needing the toilet, or simply restlessness. Looking for the reason helps more than locks alone.") +
        H2("A home safety checklist") +
        TICKS(["Door chimes or partner door sensors that alert the family's phones", "A curtain or mural over the main door; a stop sign at eye level can help",
               "Car keys out of sight", "Daily walks with someone, so the need to move is met", "Toilet signs and a night light on the route",
               "ID bracelet or a card in their wallet with your number", "A recent photo and a description of clothes, shared with family"]) +
        SPLIT("porch", H3("If they go missing") +
              P(f"Search the house and garden quickly, then call {EMERG(M)} within 15 minutes. Tell the police they have dementia. Check old routes: a former workplace, church, shops. Do not wait for hours.")) +
        P(f"Our dementia safety plan includes a home walk-through, optional door sensors and an emergency contact ladder that every {cg} knows."),
        related=("dementia-stages", "sundowning"))

    art(M, "signs-time-for-home-care", "Dementia", "Signs it is time for home care for dementia", "kitchen-sink",
        f"It is time to bring in home care when safety, eating, hygiene or the health of the family carer start to slip: falls or near misses, weight loss, missed medicines, an unwashed or unchanged look, getting lost, or a carer who is exhausted. Starting a few hours a week before a crisis is easier than starting after one.",
        H2("Ten signs families tell us they missed") +
        OL(["Unopened mail and unpaid bills", "Spoiled food in the fridge, or very little food", "Weight loss or looking thinner in the face",
            "The same clothes several days running; a change in personal hygiene", "Burnt pans or the stove left on", "Bruises they cannot explain",
            "Missed doses, or doses taken twice", "Getting lost on a familiar route", "Withdrawing from friends, church or clubs",
            "The family carer is not sleeping, is ill or is angry most of the time"]) +
        SPLIT("couple-docs", H3("Why earlier is easier") +
              P(f"Introducing a {cg} while your {m} can still enjoy the company and get to know them is much easier than after a fall or a hospital stay. A few hours a week of companionship now builds the trust you will need later for washing and dressing.")) +
        H2("A quick self-check") +
        P(f'If you said yes to three or more of the signs above, book a free assessment or try our <a href="/{p}/care-quiz.html">2-minute care needs quiz</a>. It suggests starting hours and does not ask for your email first.') +
        H2("What an assessment looks at") +
        UL(["Daily routine and what they still enjoy", "Safety in the home: stairs, bathroom, kitchen, doors", "Meals, drinks, medicines and sleep",
            "Memory and mood, and what helps", "Who helps now, and how they are coping"]),
        related=("dementia-stages", "questions-to-ask-an-agency", "caregiver-burnout"), img2="woman-glass")

    art(M, "eating-and-hydration", "Dementia", "Dementia and eating: how to keep a loved one fed and hydrated", "breakfast",
        "People with dementia often eat and drink less because they forget, cannot recognise food, find cutlery hard or do not feel thirst. Small frequent meals, finger foods, high-contrast plates, drinks offered on a schedule and eating together all help.",
        H2("Why eating gets harder") +
        UL(["Forgetting to eat, or thinking they already have", "Not recognising food on a busy or same-coloured plate", "Trouble with cutlery or chewing; sore teeth or ill-fitting dentures",
            "Losing the feeling of thirst", "Too much choice or noise at the table"]) +
        H2("Practical ideas") +
        TICKS(["Finger foods: sandwiches cut small, cheese cubes, fruit, mini quiches", "A plain plate in a strong " + M["color"] + " that contrasts with the food",
               "One course at a time", "Eat together; people copy what they see", "Favourite foods from their past", "Drinks every hour: water, milk, soup, jelly, juicy fruit",
               "Keep a simple log of meals and drinks"]) +
        SPLIT("woman-glass", H3("Signs of dehydration to watch for") +
              P("Dark urine, dry mouth, headaches, more confusion than usual, dizziness and constipation. Dehydration can make dementia symptoms look much worse. Call the doctor if you are worried.")) +
        P(f"Our {cgs} log every meal and every glass in the family app, so the family can see a pattern before it becomes a problem."),
        related=("dementia-stages", "sundowning"))

    qs = ["Are you licensed, and can I see the number?" if us else "Are you a registered Support at Home provider?",
          "What screening does every " + cg + " pass?" if not us else "What background screening does every caregiver pass? (In Florida, Level 2 screening applies.)",
          "Are " + cgs + " your employees, or contractors?", "What dementia training do they get, and how many hours?",
          "Will we have the same small team, and will we meet the backup?", "How fast can care start, and what is the record?",
          "What happens if a " + cg + " is sick or late?", "Who is our named contact, and how fast do they call back?",
          "How do you write and update the care plan?", "How will the family know what happened at each visit?",
          "What are the exact rates, minimum visit lengths and extra charges?", "What is the notice period to change or stop care?",
          "How do you handle falls, medication errors and complaints?", "Are you insured, including workers' compensation?", "Can we speak to families you currently care for?"]
    art(M, "questions-to-ask-an-agency", "Choosing care", "15 questions to ask a home care agency before you sign", "couple-docs",
        "Before you sign, ask about licensing, screening, training, staffing, reliability, communication, prices and complaints. A good agency answers all 15 questions below plainly, in writing, and is happy to be checked.",
        H2("The 15 questions") + OL(qs) +
        SPLIT("papers", H3("Red flags") + UL(["No license or registration number on the website", "Vague prices or 'we will discuss it at the visit'",
                                              "A different " + cg + " every week", "Long lock-in contracts", "Pressure to sign the same day",
                                              "No written care plan", "Reviews that only praise, with no replies to complaints"])) +
        H2("How we answer them") +
        P(f'We publish our answers: see <a href="/{p}/trust.html">licensing and safety</a>, <a href="/{p}/promises.html">our promises and results</a>, '
          f'<a href="/{p}/team.html">how we hire and train</a> and <a href="/{p}/pricing.html">every price</a>.') + PRINT(),
        related=("agency-vs-private-hire", "check-a-license" if us else "check-a-provider", "signs-time-for-home-care"))

    art(M, "agency-vs-private-hire", "Choosing care", "Agency, registry or private hire: what is the difference?" if us else "Agency or private hire: what is the difference?", "two-women",
        ("An agency employs, screens, trains, insures and supervises its caregivers and replaces them when they are sick. A nurse registry refers independent contractors, so you take on more of the responsibility. Private hire is usually cheaper per hour but you become the employer, with taxes, insurance and backup cover to arrange."
         if us else "A provider employs, screens, trains, insures and supervises its support workers and covers sick days. Hiring privately (directly or through a platform) can cost less per hour, but you take on more responsibility for checks, insurance, backup and, with Support at Home funding, rules about who can be paid."),
        T(["", "Agency" , "Registry" if us else "Platform", "Private hire"],
          [["Who employs the " + cg, "The agency", "Usually the " + cg + " (contractor)", "You"],
           ["Screening and training", "Agency", "Varies", "You arrange"], ["Backup when sick", "Agency", "Varies", "You find it"],
           ["Insurance and " + ("payroll taxes" if us else "super"), "Agency", "Often the " + cg, "You"],
           ["Typical cost per hour", "Highest", "Middle", "Lowest"]]) +
        H2("Which to choose") +
        P(f"If your {m} has dementia, consistency, training and reliable backup usually matter more than the lowest hourly rate. If needs are light and you have time to manage, private hire can work well.") +
        TICKS(["Ask who is liable if a " + cg + " is injured in the home", "Ask what happens on a sick day", "Get everything in writing"]),
        related=("questions-to-ask-an-agency",))

    art(M, "caregiver-burnout", "Family caregivers", "Caregiver burnout: signs and what to do", "tea-woman",
        "Caregiver burnout is physical and emotional exhaustion from caring for someone over a long time. Signs include constant tiredness, irritability, poor sleep, illness and feeling trapped. Regular breaks, shared tasks, practical help and support for yourself make the biggest difference.",
        H2("Signs to take seriously") +
        UL(["You are tired all the time, even after sleep", "You snap at the person you care for, then feel guilty", "You have stopped seeing friends",
            "Your own health appointments are slipping", "You feel hopeless, or that nobody understands", "You drink more or eat badly"]) +
        SPLIT("couple-out", H3("What actually helps") +
              TICKS(["A regular break you can count on, not 'when things settle'", "Split tasks with family: money, appointments, visits",
                     "Respite: a few hours, a day, or an overnight", "A support group or counsellor", "Sleep and your own doctor's appointment"])) +
        P(f'Our <a href="/{p}/services/respite-care.html">respite planner</a> suggests hours based on how worn out you feel. If you feel unsafe or in crisis, call ' +
          ("988 (Suicide and Crisis Lifeline)" if us else "Lifeline on 13 11 14") + " now."),
        related=("talking-to-siblings", "family-meeting-agenda"))

    art(M, "talking-to-siblings", "Family caregivers", "How to talk to siblings about sharing care", "seniors-table",
        "Start with facts, not blame: what your parent needs each week, what it costs and who is doing what now. Then let each person offer what they can (time, money, admin or visits) and write it down. A neutral person or a family meeting agenda helps.",
        H2("Before the conversation") + UL(["List the weekly tasks and hours", "Gather costs and the money available", "Ask the parent what they want"]) +
        H2("During it") + TICKS(["Share the list, not your frustration", "Ask each person what they can realistically do", "Value money, admin and distance help, not only hands-on care",
                                 "Agree a review date"]) +
        P(f'Siblings far away can still help: the family app lets everyone see visits, notes and messages, with roles for view-only, messaging and approving changes. Use our <a href="/{p}/resources/family-meeting-agenda.html">family meeting agenda</a>.'),
        related=("family-meeting-agenda", "caring-from-afar", "caregiver-burnout"))

    art(M, "caring-from-afar", "Family caregivers", "Caring for a parent from another state or country" if us else "Caring for a parent from interstate or overseas", "video-call",
        "You can care well from far away by building a local team, getting legal permissions in place, using technology to see what happens day to day, and visiting with a plan. A named local care manager is the single most useful person you can have.",
        H2("Your long-distance checklist") +
        TICKS(["Legal: " + ("power of attorney, health care surrogate and HIPAA release" if us else "enduring power of attorney and an advance care directive"),
               "A list of doctors, medicines, pharmacy and insurance", "A trusted neighbour with a key", "A local care manager or Care Director",
               "A shared calendar and one family message thread", "A plan for emergencies: who is called first, second, third"]) +
        SPLIT("video-call2", H3("Make visits count") + UL(["Check the fridge, mail and medicines", "Meet the " + cg + " and care manager", "Walk the home for safety", "Spend time just being family"])) +
        P(f'Our <a href="/{p}/services/care-from-afar.html">care from afar</a> service gives you a named Care Director, the live app, monthly video calls and errands.'),
        related=("talking-to-siblings", "family-meeting-agenda"))

    art(M, "leaving-hospital-checklist", "Family caregivers", "Leaving hospital: a first-week checklist", "hospital",
        "The first week home from hospital is when problems are most likely: confusion about medicines, falls, missed follow-ups and not eating. Before discharge, get the medicine list, follow-up appointments, equipment and a named contact; at home, check safety, food and help for the first 72 hours.",
        H2("Before you leave hospital") +
        TICKS(["Written discharge summary and an up-to-date medicine list", "What changed: new medicines, stopped medicines, new doses",
               "Follow-up appointments booked, with transport", "Equipment ordered: walker, shower chair, commode",
               "Who to call with questions, day and night", "Who will be home on the first night"]) +
        SPLIT("porch2", H3("The first 72 hours at home") +
              TICKS(["Clear paths, rugs up, night lights on", "Food and drinks within easy reach", "Medicines in a dosette box, checked by a pharmacist",
                     "Help with washing and dressing", "Someone checking in morning and evening"])) +
        H2("Days 4 to 7") +
        UL(["Watch for new confusion, fever, pain, breathlessness or not eating", "Keep the follow-up appointment", "Decide what ongoing help is needed"]) +
        P(f'Coming home soon? See <a href="/{p}/services/after-hospital.html">care after hospital</a>' + (": we aim to start within 72 hours of signing." if M["live"] else ".")) + PRINT(),
        related=("signs-time-for-home-care",), img2="switch")

    art(M, "family-meeting-agenda", "Family caregivers", "A family meeting agenda for deciding on care", "women-table",
        "A good family meeting has a written agenda, the person needing care involved as much as possible, facts about needs and money, and clear decisions with names and dates. Use the eight-point agenda below and keep it under an hour.",
        H2("The agenda") +
        OL(["What " + m + " or " + M["dad"] + " wants, in their words", "What has changed in the last 3 months", "Safety worries", "Care options and hours",
            "Money: costs and how it will be paid", "Who does what (hands-on, admin, visits, money)", "What happens in an emergency", "When we meet again"]) +
        SPLIT("seniors-table", H3("Tips") + TICKS(["Send the agenda beforehand", "Video-call those far away", "One person takes notes and shares them", "Disagree about the plan, not about each other"])) + PRINT(),
        related=("talking-to-siblings", "caring-from-afar"))

# ---------- US-only ----------
def us_only(M):
    r = M["rates"]
    art(M, "home-care-cost-florida", "Paying for care", "How much does home care cost in Florida?", "tampa-river",
        f"Non-medical home care in Florida typically costs around $30 an hour, and our starting rates in Tampa Bay are $30 for companion care, $34 for personal care and $38 for dementia specialist care. Twenty hours a week of dementia care is about ${r['dementia'] * 20 * 52 / 12:,.0f} a month.",
        H2("Our starting prices") +
        T(["Type of care", "From, per hour", "20 hours a week, per month"],
          [[n, f"${v}", f"${v * 20 * 52 / 12:,.0f}"] for n, v in [("Companion care", r["companion"]), ("Personal care", r["personal"]), ("Dementia specialist care", r["dementia"])]]) +
        H2("What changes the price") +
        UL(["Hours per week and visit length", "Weekends, nights and holidays", "Level of care: companion, personal or dementia", "Area: some areas cost more to staff", "Live-in or 24/7 care"]) +
        SPLIT("couple-docs", H3("How families pay") + UL(["Private pay (most common)", "Long-term care insurance", "Veterans' benefits", "Medicaid waiver programs (waitlists apply)"]) +
              P('Medicare generally does not cover ongoing non-medical home care. <a href="/us/resources/medicare-and-home-care.html">Here is why</a>.')) +
        P('Use the <a href="/us/pricing.html">estimator</a> to see a monthly range for your hours.'),
        related=("medicare-and-home-care", "long-term-care-insurance", "veterans-home-care-benefits"))

    art(M, "medicare-and-home-care", "Paying for care", "Does Medicare cover home care, and what does it not cover?", "papers",
        "Medicare covers part-time skilled home health care (nursing or therapy) for people who are homebound and need it under a doctor's plan, usually for a limited time. It does not pay for ongoing non-medical home care such as companionship, help with bathing and dressing, or 24-hour care when that is the only care needed.",
        H2("What Medicare home health covers") +
        UL(["Part-time skilled nursing", "Physical, speech and occupational therapy", "Some part-time home health aide help, only alongside skilled care",
            "Medical social services"]) +
        P("To qualify, a person generally has to be under a doctor's care, need skilled services and be considered homebound, and the agency must be Medicare-certified. Check the current rules on Medicare.gov.") +
        H2("What it does not cover") +
        TICKS(["24-hour care at home", "Meals delivered to the home", "Homemaker services like shopping and cleaning, when not related to the care plan",
               "Personal care (bathing, dressing, toileting) when that is the only care needed", "Companion care and supervision for dementia"], cls="") +
        SPLIT("woman-phone", H3("Medicare Advantage plans") + P("Some Medicare Advantage plans offer limited extra in-home support hours. The benefit varies by plan and year; call your plan and ask exactly how many hours, which providers, and what it costs.")) +
        H2("Other ways to pay") +
        P('Long-term care insurance, veterans\' benefits, Medicaid waiver programs and private pay. See <a href="/us/paying-for-care.html">paying for care</a>.'),
        related=("long-term-care-insurance", "veterans-home-care-benefits", "home-care-cost-florida"))

    art(M, "long-term-care-insurance", "Paying for care", "Long-term care insurance and home care: how to claim", "couple-docs",
        "Most long-term care insurance policies pay for home care once a person needs help with two or more activities of daily living or has a cognitive impairment such as dementia, and after an elimination period. Start the claim early, keep visit records, and ask the agency to send invoices in the insurer's format.",
        H2("Step by step") +
        OL(["Find the policy and read the benefit trigger, daily maximum and elimination period", "Call the insurer to open a claim", "Get the doctor's assessment or plan of care",
            "Choose a provider the policy accepts (licensed agency is often required)", "Keep invoices and care notes", "Submit monthly and track payments"]) +
        SPLIT("papers", H3("How we help") + P("Our app produces itemised invoices and visit records, and our team will help you with the paperwork for your claim.")),
        related=("medicare-and-home-care", "home-care-cost-florida"))

    art(M, "veterans-home-care-benefits", "Paying for care", "Veterans and home care benefits", "man-blue",
        "Veterans and surviving spouses may get help paying for home care through the VA, including the Aid and Attendance or Housebound add-on to a VA pension, and through VA home and community care programs. Eligibility depends on service, need and income, and amounts are set each year.",
        H2("Main routes") +
        UL(["Aid and Attendance or Housebound pension benefits", "VA homemaker and home health aide care", "Veteran-directed care in some areas", "Respite care for family caregivers"]) +
        H2("How to start") +
        TICKS(["Gather the DD214 discharge papers", "Contact the VA or a free accredited Veterans Service Officer", "Get a doctor's statement of care needs", "Never pay anyone to file a VA claim"]) +
        SPLIT("grandpa-selfie", H3("Where we fit") + P("We are a private-pay agency. VA pension benefits paid to the veteran can be used toward our care. We will provide the paperwork you need.")),
        related=("medicare-and-home-care", "long-term-care-insurance"))

    art(M, "check-a-license", "Choosing care", "How to check an agency's license in Florida", "papers",
        "In Florida, home care agencies are licensed by the Agency for Health Care Administration (AHCA). You can check any agency's license on the state's health finder site using its name or license number, and you should see the license number on its website and ads.",
        H2("How to check") +
        OL(['Ask the agency for its license number', 'Search it on <a href="https://quality.healthfinder.fl.gov/" target="_blank" rel="noopener">quality.healthfinder.fl.gov</a>', "Check the license type and that it is current",
            "Read any inspection reports"]) +
        H2("License types you will see") +
        UL(["Home Health Agency: can provide personal care and skilled services", "Nurse Registry: refers independent contractors", "Homemaker and Companion Service: companionship and household help, no hands-on personal care"]) +
        CALL(M["lic"]),
        related=("questions-to-ask-an-agency", "agency-vs-private-hire"))

# ---------- AU-only ----------
def au_only(M):
    art(M, "support-at-home-explained", "Paying for care", "Support at Home explained step by step", "couple-docs",
        "Support at Home is the Australian Government's in-home aged care program, which replaced Home Care Packages and Short-Term Restorative Care from 1 November 2025. You get an assessment through My Aged Care, are assigned one of eight funding classifications, choose a registered provider, and pay a contribution based on your pension status and the type of service.",
        H2("The steps") +
        OL(["Contact My Aged Care online or on 1800 200 422", "Have an aged care assessment at home", "Receive your notice of decision with your classification",
            "Wait to be assigned funding (there can be a wait)", "Choose a registered provider and sign a service agreement", "Plan services within your quarterly budget"]) +
        H2("Classifications and budgets") +
        P("There are eight ongoing classifications. As published for July 2026, yearly budgets run from about $11,010 at level 1 to about $80,137 at level 8. Budgets are indexed each July and managed quarterly.") +
        H2("Contributions") +
        T(["Service type", "Full pensioner", "Part pensioner / CSHC", "Self-funded"],
          [["Clinical care (e.g. nursing)", "0%", "0%", "0%"], ["Independence (e.g. personal care)", "5%", "5% to 50%", "50%"],
           ["Everyday living (e.g. cleaning, meals)", "17.5%", "17.5% to 80%", "80%"]]) +
        P("These are the standard rates for people who entered from 1 November 2025. People who had a Home Care Package before then may have different rates under the no worse off principle. A lifetime cap applies.") +
        SPLIT("papers", H3("Try the explainer") + P('Our <a href="/au/funding.html">funding page</a> has a contribution explainer. It is general information; check your own figures with My Aged Care and Services Australia.')) +
        CALL(M["lic"]),
        related=("my-aged-care-assessment", "check-a-provider"))

    art(M, "my-aged-care-assessment", "Paying for care", "How to get a My Aged Care assessment", "kitchen-sink",
        "Call My Aged Care on 1800 200 422 or apply online. They ask questions by phone and, if eligible, arrange an assessor to visit at home. Have Medicare details, your doctor's contact and a family member present if possible.",
        H2("Before the call") + TICKS(["Medicare card", "Doctor's details and medicine list", "A list of what is hard day to day", "Consent for a family member to speak for them"]) +
        H2("At the assessment") + UL(["Be honest about bad days, not just good ones", "Mention memory problems and falls", "Mention the family carer's health"]) +
        SPLIT("seniors-table", H3("After") + P("You get a notice of decision. Keep it: it states the services and classification you are approved for.")),
        related=("support-at-home-explained", "check-a-provider"))

    art(M, "check-a-provider", "Choosing care", "How to check an aged care provider's registration", "papers",
        "Registered aged care providers are listed by the Aged Care Quality and Safety Commission. Ask for the provider's registration, check it on the Commission's website and My Aged Care's Find a provider tool, and read any compliance notices.",
        H2("How to check") + OL(["Ask the provider for its registration details", 'Search on <a href="https://www.agedcarequality.gov.au/" target="_blank" rel="noopener">agedcarequality.gov.au</a>',
                                 "Use Find a provider on My Aged Care", "Check star ratings and any notices"]) +
        CALL(M["lic"]),
        related=("support-at-home-explained", "questions-to-ask-an-agency"))

# ---------- hub ----------
CATS = ["Dementia", "Paying for care", "Choosing care", "Family caregivers"]
def hub(M):
    p = M["p"]
    def cards(cat):
        return "".join(f'<a class="rcard reveal" style="--i:{i}" href="/{p}/resources/{s}.html"><img src="/img/{im}.jpg" alt="{alt(im)}" loading="lazy"><span><b>{t}</b>{sm.split(". ")[0]}.</span></a>'
                       for i, ((pp, s), (c, t, im, sm)) in enumerate([x for x in ARTS.items() if x[0][0] == p and x[1][0] == cat]))
    secs = "".join(f'<section class="rsec" id="{c.lower().replace(" ", "-")}"><h2>{c if c != "Family caregivers" or p == "us" else "Family carers"}</h2><div class="rgrid">{cards(c)}</div></section>' for c in CATS)
    tools = MOSAIC([("hands-young", "Dementia stage guide", "Drag through early, middle and late stage", f"/{p}/services/dementia-care.html"),
                    ("papers", "Is it time for help?", "A printable checklist", f"/{p}/resources/signs-time-for-home-care.html"),
                    ("hospital", "Hospital discharge checklist", "Printable, first week home", f"/{p}/resources/leaving-hospital-checklist.html"),
                    ("tampa-river" if p == "us" else "sydney2", "Cost guide", "See monthly costs in seconds", f"/{p}/pricing.html"),
                    ("women-table", "Family meeting agenda", "Eight points, under an hour", f"/{p}/resources/family-meeting-agenda.html")])
    body = (f'<label class="fsearch"><span>Search the guides</span><input type="search" placeholder="Try: sundowning, cost, hospital" data-rfilter></label><p class="rnone" hidden>No guide matches. Call us and ask a person: {ph(M)}</p>'
            f'<div class="pill-row">' + "".join(f'<a href="#{c.lower().replace(" ", "-")}">{c}</a>' for c in CATS) + f'<a href="#tools">Free tools</a></div>'
            + secs + f'<section id="tools">{SECTION("Free tools and downloads", "Tools families use most.")}{tools}'
            + f'<p style="text-align:center"><a class="btn" href="/{p}/care-quiz.html">Take the 2-minute care quiz</a> <a class="btn o" href="/{p}/pricing.html">Estimate the cost</a></p></section>'
            + CALL("Every guide is written answer-first, with the author and last-updated date shown. Clinical review is pending: until a qualified reviewer signs a guide off, it is general information only.")
            + CTA(M))
    page(M, f"{p}/resources/index", "Guides for families caring for someone with dementia", "Plain answers on dementia, paying for care, choosing a provider and looking after yourself, written for " + ("Florida" if p == "us" else "Australia") + ".",
         body, img="tea-book", eyebrow="Resources", chips=[(str(sum(1 for k in ARTS if k[0] == p)), "guides"), ("5", "free tools"), ("0", "emails required")])

# ---------- locations ----------
US_CITIES = {
    "tampa": dict(name="Tampa", f=1.0, img="tampa-night", status="Launch area",
        hoods="South Tampa, Hyde Park, Seminole Heights, Westchase, Carrollwood, New Tampa, Town 'n' Country and Temple Terrace",
        hosp=["Tampa General Hospital", "St. Joseph's Hospital", "AdventHealth Tampa", "James A. Haley Veterans' Hospital"],
        res=["Senior Connection Center (the Area Agency on Aging for Hillsborough County)", "Alzheimer's Association Florida Gulf Coast Chapter", "Hillsborough County Aging Services"],
        intro="Tampa is where we start. Our first care team is recruited and trained here, so families in Tampa get the shortest travel times and the most flexible schedules.",
        note="Tampa traffic on I-275 and the Selmon matters for care: we build each team around a small area, so your caregiver is not driving across the bay twice a day."),
    "st-petersburg": dict(name="St. Petersburg", f=1.0, img="skyway", status="Planned",
        hoods="Downtown, Old Northeast, Kenwood, Snell Isle, Shore Acres, Gulfport and Pinellas Park",
        hosp=["Orlando Health Bayfront Hospital (St. Petersburg)", "St. Anthony's Hospital", "Bay Pines VA Healthcare System"],
        res=["Area Agency on Aging of Pasco-Pinellas", "Alzheimer's Association Florida Gulf Coast Chapter", "Pinellas County senior services"],
        intro="St. Petersburg has one of the oldest populations in Tampa Bay, and many adult children who moved away. Care from afar is the most common request we expect here.",
        note="Many St. Pete families split time between Florida and the North. Our app and monthly video calls are built for exactly that."),
    "clearwater": dict(name="Clearwater", f=0.98, img="tampa-day", status="Planned",
        hoods="Downtown Clearwater, Countryside, Dunedin, Safety Harbor, Largo, Belleair and Clearwater Beach",
        hosp=["Morton Plant Hospital", "Mease Countryside Hospital", "HCA Florida Largo Hospital"],
        res=["Area Agency on Aging of Pasco-Pinellas", "Alzheimer's Association Florida Gulf Coast Chapter"],
        intro="Clearwater and North Pinellas have many people living alone in condos and 55+ communities, where a fall or a missed meal can go unnoticed for days.",
        note="We work with condo and community managers on access, parking and emergency contacts so visits are smooth."),
    "sarasota": dict(name="Sarasota", f=1.04, img="couple-path", status="Planned",
        hoods="Downtown Sarasota, Lakewood Ranch, Siesta Key, Venice, Palmer Ranch and Bradenton",
        hosp=["Sarasota Memorial Hospital", "Lakewood Ranch Medical Center", "Sarasota Memorial Hospital, Venice"],
        res=["Senior Friendship Centers", "Area Agency on Aging for Southwest Florida", "Alzheimer's Association Florida Gulf Coast Chapter"],
        intro="Sarasota and Manatee have some of the highest shares of older residents in the country, and demand for dementia care far exceeds the number of trained caregivers.",
        note="Prices here are slightly higher because travel distances in Lakewood Ranch and Venice are longer and caregivers are harder to recruit."),
}

def locations(M):
    p = M["p"]
    if p == "us":
        pins = [(48, 42, "Tampa", "Launch area", "/us/locations/tampa.html"), (40, 64, "St. Petersburg", "Planned", "/us/locations/st-petersburg.html"),
                (30, 40, "Clearwater", "Planned", "/us/locations/clearwater.html"), (66, 52, "Brandon", "Launch area", "/us/locations/tampa.html"),
                (58, 20, "Wesley Chapel", "Launch area", "/us/locations/tampa.html"), (62, 84, "Sarasota", "Planned", "/us/locations/sarasota.html")]
        cards = "".join(f'<a class="rcard reveal" style="--i:{i}" href="/us/locations/{k}.html"><img src="/img/{c["img"]}.jpg" alt="{alt(c["img"])}" loading="lazy"><span><b>{c["name"]} &middot; {c["status"]}</b>From ${M["rates"]["companion"] * c["f"]:.0f}/hour companion, ${M["rates"]["dementia"] * c["f"]:.0f}/hour dementia care.</span></a>' for i, (k, c) in enumerate(US_CITIES.items()))
        body = (SECTION("Where we care", "Starting in Tampa Bay, one area at a time.", "We start small on purpose. A team that lives near your family arrives on time and stays. Pins show where we start and where we plan to go next.")
                + PINS(pins, "tampa-river") + f'<div class="rgrid">{cards}</div>'
                + CALL("Planned areas open only when we have a trained local team. Join the list and we will tell you when we can start near you.") + CTA(M))
        page(M, "us/locations/index", "Home care locations in Tampa Bay", "Tampa first, then St. Petersburg, Clearwater and Sarasota.", body, img="skyway", eyebrow="Locations",
             chips=[("1", "launch area"), ("3", "planned"), ("72 hours", "start in launch areas")])
        for k, c in US_CITIES.items(): city(M, k, c)
    else:
        pins = [(52, 46, "Sydney CBD", "Waitlist", "/au/locations/sydney.html"), (66, 20, "Northern Beaches", "Waitlist", "/au/locations/sydney.html"),
                (30, 50, "Parramatta", "Waitlist", "/au/locations/sydney.html"), (48, 82, "Sutherland Shire", "Waitlist", "/au/locations/sydney.html")]
        body = (SECTION("Where we plan to care", "Sydney first, once we are registered.", "Australia is a waitlist for now. These are the areas we plan to serve first.")
                + PINS(pins, "sydney2") + SPLIT("melb-homes", H3("Why a waitlist?") + P(M["lic"]) + P('Read <a href="/au/resources/support-at-home-explained.html">Support at Home explained</a> while you wait.'))
                + CTA(M))
        page(M, "au/locations/index", "Planned locations in Australia", "Sydney first. Join the waitlist for your area.", body, img="sydney", eyebrow="Locations",
             chips=[("Sydney", "first city"), ("Waitlist", "status"), ("1800 100 500", "National Dementia Helpline")])
        body = (SUMMARY("We plan to start in Sydney once registration questions are settled. We are not providing care yet. Join the waitlist and we will call you, explain Support at Home and tell you honestly when we can begin.")
                + SPLIT("sydney", H3("Areas we plan to serve first") + UL(["Inner West and Eastern Suburbs", "North Shore and Northern Beaches", "Parramatta and the Hills District", "Sutherland Shire and St George"]))
                + H2("Local hospitals we expect to work with") + UL(["Royal North Shore Hospital", "Westmead Hospital", "Royal Prince Alfred Hospital", "St Vincent's Hospital Sydney", "Sutherland Hospital"])
                + H2("Help you can get now") + TICKS(["My Aged Care: 1800 200 422", "National Dementia Helpline (Dementia Australia): 1800 100 500", "Carer Gateway: 1800 422 737", "Your GP, for a referral and care plan"])
                + SPLIT("au-suburb", H3("Prices") + P(f"Published weekday personal care rates in Sydney are around ${M['rates']['personal']} an hour. Under Support at Home, most of the cost comes from your budget. <a href='/au/funding.html'>See funding</a>."), flip=True)
                + CTA(M))
        page(M, "au/locations/sydney", "Dementia care at home in Sydney", "Waitlist open. Planned areas, local hospitals and help available now.", body, img="sydney2", eyebrow="Locations &middot; Sydney")

def city(M, k, c):
    r = M["rates"]
    prices = T(["Type of care", f"From, per hour in {c['name']}", "20 hours a week"],
               [[n, f"${r[x] * c['f']:.0f}", f"${r[x] * c['f'] * 20 * 52 / 12:,.0f}/month"] for n, x in [("Companion", "companion"), ("Personal care", "personal"), ("Dementia specialist", "dementia")]])
    gal = {"tampa": ["tampa-river", "couple-dance", "two-women"], "st-petersburg": ["skyway", "video-call", "man-dog"],
           "clearwater": ["tampa-day", "walk-street", "woman-glass"], "sarasota": ["couple-path", "flowers", "piano3"]}[k]
    status = ("We are starting here. Book a free assessment and care can begin within 72 hours of signing." if c["status"] == "Launch area"
              else f"{c['name']} is planned, not open yet. Join the list and we will call you when a local team is ready, or ask about care from afar options now.")
    body = (SUMMARY(f"{BRAND} provides non-medical dementia and in-home care in {c['name']}. {status}")
            + SPLIT(gal[0], H3(f"Home care in {c['name']}") + P(c["intro"]) + P(f"Neighborhoods: {c['hoods']}."))
            + H2(f"Local prices in {c['name']}") + prices
            + SPLIT(gal[1], H3("Hospitals we coordinate with") + P(f"For care after hospital, we work with discharge planners at:") + UL(c["hosp"]), flip=True)
            + H2("Local help for families") + TICKS(c["res"] + ["Alzheimer's Association 24/7 Helpline: 1-800-272-3900", "Florida Elder Helpline: 1-800-963-5337"])
            + CALL(c["note"]) + GALLERY(gal) + CTA(M, h=f"Care in {c['name']}, starting with a conversation."))
    page(M, f"us/locations/{k}", f"Dementia and home care in {c['name']}, Florida", f"{c['status']}. Local prices, hospitals and help for families in {c['name']}.", body,
         img=c["img"], eyebrow=f"Locations &middot; {c['name']}", chips=[(c["status"], "status"), (f"${r['dementia'] * c['f']:.0f}/hr", "dementia care from"), ("72 hours", "start, in launch areas")],
         jsonld=[{"@context": "https://schema.org", "@type": "LocalBusiness", "name": f"{BRAND} {c['name']}", "areaServed": f"{c['name']}, FL", "telephone": M["tel"], "url": f"{DOMAIN}/us/locations/{k}.html"}])

# two passes: the second re-registers articles so related links to later articles resolve
for _M in (US, AU):
    shared(_M)
    (us_only if _M["p"] == "us" else au_only)(_M)
for _M in (US, AU):
    shared(_M)
    (us_only if _M["p"] == "us" else au_only)(_M)
for _M in (US, AU):
    hub(_M)
    locations(_M)
