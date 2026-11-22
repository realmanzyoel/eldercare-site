#!/usr/bin/env python3
"""Builds the Evenhome elder care site into ./public.  Run: python3 build.py"""
import os, sys, glob, hashlib, shutil, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ec as S
MODS = ["c_home", "c_services", "c_trust", "c_tools", "c_resources", "c_more", "c_gallery"]

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")

def main():
    for m in MODS:
        if os.path.exists(os.path.join(ROOT, m + ".py")): importlib.import_module(m)
        else: print("skip (missing):", m)
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    css = "".join(open(os.path.join(ROOT, "assets", f)).read() for f in ("il.css", "ec.css")) + "".join(open(f).read() for f in sorted(glob.glob(os.path.join(ROOT, "assets", "m_*.css"))))
    js = open(os.path.join(ROOT, "assets", "il.js")).read() + "\n" + open(os.path.join(ROOT, "assets", "ec.js")).read() + "".join("\n" + open(f).read() for f in sorted(glob.glob(os.path.join(ROOT, "assets", "m_*.js"))))
    v = hashlib.md5((css + js).encode()).hexdigest()[:8]
    open(os.path.join(OUT, "assets", "site.css"), "w").write(css)
    open(os.path.join(OUT, "assets", "site.js"), "w").write(js)
    shutil.copytree(os.path.join(ROOT, "img"), os.path.join(OUT, "img"))
    # every root-absolute link must point at a generated page or file
    import re
    targets = {p + ".html" for p in S.PAGES} | {"img/" + f for f in os.listdir(os.path.join(ROOT, "img"))} | {"assets/site.css", "assets/site.js"}
    missing = set()
    for path, d in S.PAGES.items():
        h = S.render(path, d, v)
        fn = os.path.join(OUT, path + ".html")
        os.makedirs(os.path.dirname(fn), exist_ok=True)
        open(fn, "w").write(h)
        depth = path.count("/")
        for u in re.findall(r'(?:href|src)="([^"#?:]+)', h):
            if u.startswith(("http", "mailto", "tel", "sms", "data")): continue
            parts = path.split("/")[:-1]
            for seg in u.split("/"):
                if seg == "..": parts = parts[:-1]
                elif seg not in ("", "."): parts.append(seg)
            t = "/".join(parts)
            if t not in targets: missing.add((path, u))
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<url><loc>{S.DOMAIN}/{'' if p == 'index' else p + '.html'}</loc></url>" for p, d in S.PAGES.items() if not d["landing"]) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /us/lp/\nSitemap: {S.DOMAIN}/sitemap.xml\n")
    print(len(S.PAGES), "pages ->", OUT)
    if missing:
        print("BROKEN LINKS:", len(missing))
        for m in sorted(missing)[:60]: print("  ", m)

if __name__ == "__main__":
    main()
