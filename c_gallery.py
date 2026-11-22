from ec import *
import os

THEMES = {"dementia": "Memory, patience and connection", "caregiver": "Caregivers and the people they support", "family": "Family, near and far", "home": "Home, comfort and routine",
          "hospital": "Coming home from hospital", "activity": "Things that make a good day", "outdoors": "Fresh air and the neighbourhood", "food": "Meals, tea and the kitchen table",
          "tech": "Staying in touch", "place-us": "Tampa Bay and Florida", "place-au": "Australia", "health": "Health, medicines and appointments"}

def rows(names, size=8):
    return [names[i:i + size] for i in range(0, len(names), size)]

def gallery(M):
    p = M["p"]
    seen = set()
    groups = {}
    for m in MANIFEST:
        n = m["file"][:-4]
        if n in ALT and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", m["file"])):
            groups.setdefault(m["theme"], []).append(n); seen.add(n)
    rest = [n for n in all_photos() if n not in seen]
    body = P("These are stock photographs from Unsplash, used to show what good care at home can look like. They do not show our clients or staff.")
    first = True
    for t, title in THEMES.items():
        names = groups.get(t, [])
        if not names: continue
        body += H2(title)
        for r in rows(names): body += GALLERY(r)
        if first: body += STRIP(rest[:14]); first = False
    if rest:
        body += H2("More everyday moments")
        for r in rows(rest): body += GALLERY(r)
    body += CTA(M, "Want this for your family?", img="hands-care")
    page(M, f"{p}/gallery", "Life at home, in pictures", "A look at the small moments that good care at home is made of.", body, img="two-women", eyebrow="Gallery",
         chips=[(str(len(seen) + len(rest)), "photos"), (str(sum(1 for t in THEMES if groups.get(t))), "themes")])

for _M in (US, AU):
    gallery(_M)
