from ec import *

REVIEW = CALL("<b>Draft for legal review.</b> This page is a plain-language draft written before launch. It must be reviewed by a lawyer in each country before the site takes real enquiries.")

def legal(M):
    p, us = M["p"], M["p"] == "us"
    law = ("the Florida Information Protection Act, HIPAA where it applies to us, the TCPA for calls and texts, and the CAN-SPAM Act" if us else
           "the Privacy Act 1988 and the Australian Privacy Principles, the Spam Act 2003, the Do Not Call Register Act 2006 and the Aged Care Act 2024")
    page(M, f"{p}/privacy", "Privacy policy", "What we collect, why, who sees it and how to get it deleted. Written to be read.",
        REVIEW + SUMMARY(f"We collect only what we need to arrange and provide care. We never sell your information, and we never send health details to advertising or analytics tools.") +
        H2("What we collect") + T(["Information", "Why", "Kept for"],
            [["Your name, phone and email", "To answer your enquiry and arrange the assessment", "2 years after last contact if you do not become a client"],
             ["The person's care needs, routines and Life Story profile", "To plan and provide safe, personal care", "As long as care continues, then as the law requires"],
             ["Visit records, care notes and photos (photos only with consent)", "To show the family what happened and keep care consistent", "As required by " + ("Florida health records rules" if us else "aged care record-keeping rules")],
             ["Location at check-in and check-out", f"To confirm a {M['cg']} arrived and left", "Visit times only; we do not track staff outside visits"],
             ["Payment details", "To bill for care", "Handled by our payment processor; we do not store full card numbers"],
             ["Website use (pages, device type)", "To improve the site", "Aggregated; no health details are ever attached"]]) +
        H2("What we never do") + TICKS(["Sell or rent your information", "Send health details to ad platforms through tracking tags", "Share care notes with anyone outside the family circle you approve, except where the law requires (for example, abuse reporting)",
                                       "Use photos of your family on our website or ads without separate written consent"]) +
        H2("Who can see what") + T(["Person", "Can see"], [["The client", "Everything about their own care"], ["Family circle members", "What their role allows: view only, can message, or can approve changes"],
                                                          [M["Cgs"], "The care plan and Life Story for clients on their team"], ["Care manager and operations lead", "Everything needed to manage care and keep it safe"],
                                                          ["Service providers (hosting, scheduling, payments)", "Only what they need, under contract"]]) +
        f'<h2 id="health">Health information</h2>' + P(("If we become subject to HIPAA as a covered entity or business associate, we will provide a separate Notice of Privacy Practices before care starts. "
                                                       "Either way, we treat care notes as confidential health information.") if us else
                                                      "Care information is sensitive information under the Privacy Act. We collect it only with consent and use it only to provide and improve your care.") +
        H2("Calls, texts and email") + P(f"We contact you only about the request you made, and only by the channels you agreed to. Reply STOP to any text to opt out. Consent is never a condition of buying care. This is governed by {law}.") +
        H2("Your rights") + UL(["See the information we hold about you", "Ask us to correct it", "Ask us to delete it, where the law allows", "Withdraw consent for photos or marketing at any time",
                                "Complain to us, and then to " + ("the Florida Attorney General or the US Department of Health and Human Services Office for Civil Rights" if us else "the Office of the Australian Information Commissioner (OAIC)")]) +
        H2("Contact our privacy officer") + P(f"Email {MAIL} or call {ph(M)}. We reply within 30 days, usually much sooner.") +
        P("Last updated 21 November 2026."), nohero=True, eyebrow="Legal")

    page(M, f"{p}/terms", "Terms of use and service", "The plain rules for using this website and, once you are a client, for our care.",
        REVIEW + H2("This website") + UL(["Information here is general. It is not medical, legal or financial advice.", "Prices on the site are estimates. Your price is confirmed in writing after the free assessment.",
                                          "Calculators, the care quiz and the app demo are illustrations. The app demo uses a fictional family.",
                                          "Photos are stock images used for illustration and do not show our clients or staff."]) +
        H2("Care services (summary of the care agreement)") + T(["Topic", "What applies"],
            [["Who we are", f"A non-medical in-home care {'agency' if us else 'provider'}. {M['lic']}"],
             ["Minimum visit", "3 hours"], ["Changes", "Change hours in the app with 48 hours' notice"], ["Cancelling a visit", "Free with 24 hours' notice; within 24 hours, up to 50% of the visit may be charged"],
             ["Ending care", "7 days' notice, by either side, no exit fees"], ["Billing", "Weekly or fortnightly invoices for hours delivered, visible live in the app"],
             ["Missed promises", "If we miss a published promise, the remedy shown on the promises page applies"],
             ["Hiring our " + M["cgs"] + " directly", "Not allowed during care and for 6 months after, unless agreed in writing"],
             ["Complaints", f"See the {'trust' if us else 'complaints'} page for the full process and who to escalate to"]]) +
        P(("Your rights under Florida and federal consumer law are not limited by these terms." if us else
           "Nothing in these terms limits your rights under the Australian Consumer Law or the Aged Care Act 2024, including the Statement of Rights.")) +
        P("Last updated 21 November 2026."), nohero=True, eyebrow="Legal")

    page(M, f"{p}/accessibility", "Accessibility statement", "Many of our visitors are over 60, tired, worried and on a phone. The site is built for them first.",
        SUMMARY("We aim to meet WCAG 2.2 at level AA across the whole site, and we test with keyboards, screen readers and large text before every release.") +
        H2("What we have done") + TICKS(["Body text at 18 pixels or larger, with high contrast", "Buttons and links at least 44 pixels tall, and the phone number one tap away on every page",
                                         "Every animation respects your device's reduced-motion setting, and nothing flashes", "Carousels and the hero slideshow have a visible pause button, and no audio plays automatically",
                                         "Forms have visible labels and clear error messages", "Every interactive tool works with a keyboard alone", "Photos have text descriptions"]) +
        H2("Known gaps") + UL(["The scroll-driven demonstrations (the phone tour, the zoom on the care-from-afar page) are easier with a mouse or touch; the same information is written beside them.",
                               "Videos of caregiving techniques are not yet filmed; when they are, they will have captions and transcripts."]) +
        H2("Tell us what is hard to use") + P(f"Call {ph(M)} or email {MAIL}. We aim to reply within 2 business days and fix problems within 30 days.") +
        P("Statement prepared 21 November 2026. Formal audit planned before launch."), nohero=True, eyebrow="Legal")

for _M in (US, AU):
    legal(_M)

page(AU, "au/complaints", "Complaints and feedback", "Tell us what went wrong. We will listen, fix it, and tell you what changed.",
    REVIEW + SUMMARY("Call or email us first: we acknowledge every complaint within 1 business day. If you are not satisfied, you can go to the Aged Care Quality and Safety Commission at any time, free, and you can do so anonymously.") +
    PATH([("Tell us", f"Call {AU['phone']}, email {MAIL}, tell your support worker or use the app. You can also ask someone to speak for you.", "tea-woman"),
          ("We acknowledge it", "Within 1 business day, with the name of the person handling it.", None),
          ("We look into it", "We talk to you and the people involved, and agree on what a good outcome looks like.", None),
          ("We fix it and tell you", "Within 10 business days for most complaints, with what we changed so it does not happen again.", "hands-care")]) +
    H2("If you are not satisfied") + UL(['<a href="https://www.agedcarequality.gov.au/making-complaint" target="_blank" rel="noopener">Aged Care Quality and Safety Commission</a>, 1800 951 822 (free)',
                                         '<a href="https://opan.org.au/" target="_blank" rel="noopener">Older Persons Advocacy Network (OPAN)</a>, 1800 700 600, for free, independent advocacy',
                                         "The Office of the Australian Information Commissioner, for privacy complaints"]) +
    P("Making a complaint will never affect your care. We record every complaint and report patterns to our leadership every month.") +
    CTA(AU, "Something not right? Talk to a person.", img="hands-young"), nohero=True, eyebrow="Your rights")
