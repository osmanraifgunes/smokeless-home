#!/usr/bin/env python3
"""Smokeless tanıtım sitesini üretir.

Girdi:  i18n/<dil>.json  +  tools/site/page.html
Çıktı:  index.html (en), <dil>/index.html, media.html, sitemap.xml,
        tools/og/strings.js (OG görsel şablonu için)

Kullanım:  python3 tools/build.py
Yalnızca Python standart kütüphanesi gerekir.
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://osmanraifgunes.github.io/smokeless-home/"
OG_VERSION = "3"  # OG görselleri değişince artırın; sosyal medya önbelleğini kırar.
APP_STORE = "https://apps.apple.com/app/id6798220798"
PLAY_STORE = "https://play.google.com/store/apps/details?id=com.org.smokeless"

# Uygulamanın desteklediği diller (smokeless/src/i18n/index.ts ile aynı sıra).
LANGS = [
    # kod, yerel ad, og:locale, yön, ekran görüntüsü klasörü
    ("en", "English", "en_US", "ltr", "en"),
    ("zh", "中文", "zh_CN", "ltr", "zh"),
    ("hi", "हिन्दी", "hi_IN", "ltr", "hi"),
    ("es", "Español", "es_ES", "ltr", "es"),
    ("fr", "Français", "fr_FR", "ltr", "fr"),
    ("ar", "العربية", "ar_AR", "rtl", "ar"),
    ("bn", "বাংলা", "bn_IN", "ltr", "en"),
    ("pt", "Português", "pt_PT", "ltr", "en"),
    ("ru", "Русский", "ru_RU", "ltr", "en"),
    ("ur", "اردو", "ur_PK", "rtl", "en"),
    ("id", "Bahasa Indonesia", "id_ID", "ltr", "en"),
    ("de", "Deutsch", "de_DE", "ltr", "en"),
    ("ja", "日本語", "ja_JP", "ltr", "en"),
    ("tr", "Türkçe", "tr_TR", "ltr", "tr"),
    ("vi", "Tiếng Việt", "vi_VN", "ltr", "en"),
]
SHOTS = ["01-craving", "02-ride-it-out", "03-recovery", "04-plan", "05-insights"]
TOPICS = ["main", "craving", "plan", "recovery", "insights", "widget"]
FORMATS = [("landscape", "1200×630", "Link preview · X · LinkedIn · Facebook"),
           ("square", "1080×1080", "Instagram · Facebook post"),
           ("story", "1080×1920", "Stories · Reels · TikTok")]


def esc(v):
    return html.escape(v, quote=True)


def url(code):
    return BASE if code == "en" else f"{BASE}{code}/"


def load():
    en = json.load(open(os.path.join(ROOT, "i18n", "en.json"), encoding="utf-8"))
    data = {}
    for code, *_ in LANGS:
        path = os.path.join(ROOT, "i18n", f"{code}.json")
        if not os.path.exists(path):
            raise SystemExit(f"Eksik çeviri: i18n/{code}.json")
        d = json.load(open(path, encoding="utf-8"))
        for part in ("page", "og"):
            missing = set(en[part]) - set(d[part])
            if missing:
                raise SystemExit(f"i18n/{code}.json {part} eksik anahtarlar: {sorted(missing)}")
        data[code] = d
    return data


def head(code, locale, p, root):
    og_img = f"{BASE}assets/og/{code}/main-landscape.jpg?v={OG_VERSION}"
    alts = "\n".join(f'  <link rel="alternate" hreflang="{c}" href="{url(c)}">' for c, *_ in LANGS)
    loc_alt = "\n".join(f'  <meta property="og:locale:alternate" content="{l}">' for c, _, l, *_ in LANGS if c != code)
    app = {
        "@context": "https://schema.org", "@type": "MobileApplication",
        "name": "Smokeless", "description": p["_desc"], "url": url(code), "inLanguage": code,
        "image": BASE + "assets/img/icon-256.png",
        "screenshot": [f"{BASE}assets/img/{dict((c, s) for c, _, _, _, s in LANGS)[code]}/{n}.jpg" for n in SHOTS],
        "applicationCategory": "HealthApplication", "operatingSystem": "iOS, Android",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "downloadUrl": [APP_STORE, PLAY_STORE], "sameAs": [APP_STORE, PLAY_STORE],
    }
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage", "inLanguage": code,
        "mainEntity": [{"@type": "Question", "name": p[f"faq.q{i}"],
                        "acceptedAnswer": {"@type": "Answer", "text": p[f"faq.a{i}"]}} for i in range(1, 6)],
    }
    return f'''  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(p["_title"])}</title>
  <meta name="description" content="{esc(p["_desc"])}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url(code)}">
{alts}
  <link rel="alternate" hreflang="x-default" href="{BASE}">
  <meta name="google-play-app" content="app-id=com.org.smokeless">
  <meta name="apple-itunes-app" content="app-id=6798220798">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Smokeless">
  <meta property="og:url" content="{url(code)}">
  <meta property="og:title" content="{esc(p["_share_title"])}">
  <meta property="og:description" content="{esc(p["_share_desc"])}">
  <meta property="og:locale" content="{locale}">
{loc_alt}
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(p["_share_title"])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(p["_share_title"])}">
  <meta name="twitter:description" content="{esc(p["_share_desc"])}">
  <meta name="twitter:image" content="{og_img}">
  <meta name="theme-color" content="#EF6B4A">
  <link rel="icon" type="image/png" href="{root}assets/img/favicon.png">
  <link rel="apple-touch-icon" href="{root}assets/img/icon-256.png">
  <script type="application/ld+json">{json.dumps(app, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'''


def lang_menu(code, name, label, root):
    links = "".join(
        f'<a href="{root}{"" if c == "en" else c + "/"}" hreflang="{c}" lang="{c}"{" aria-current=\"page\"" if c == code else ""}>{esc(n)}</a>'
        for c, n, *_ in LANGS)
    return f'<details class="langs"><summary aria-label="{esc(label)}">🌐 {esc(name)}</summary><nav>{links}</nav></details>'


SCRIPT_EN = '''  <script>
    // Eski ?lang=xx linklerini dil sayfasına yönlendir.
    (function () {
      var l = new URLSearchParams(location.search).get("lang");
      if (l && %s.indexOf(l) > 0) location.replace(l + "/");
    })();
    document.getElementById("year").textContent = new Date().getFullYear();
  </script>'''
SCRIPT = '''  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>'''


def build_pages(data):
    tpl = open(os.path.join(ROOT, "tools", "site", "page.html"), encoding="utf-8").read()
    codes = [c for c, *_ in LANGS]
    for code, name, locale, direction, shot in LANGS:
        p = data[code]["page"]
        root = "" if code == "en" else "../"
        out = tpl
        out = out.replace("{{HEAD}}", head(code, locale, p, root))
        out = out.replace("{{LANGS}}", lang_menu(code, name, p["lang.label"], root))
        out = out.replace("{{SCRIPT}}", SCRIPT_EN % json.dumps(codes) if code == "en" else SCRIPT)
        out = out.replace("{{lang}}", code).replace("{{dir}}", direction)
        out = out.replace("{{shotdir}}", f"{root}assets/img/{shot}/").replace("{{root}}", root)
        for k, v in p.items():
            out = out.replace("{{%s}}" % k, esc(v))
        if "{{" in out:
            raise SystemExit(f"{code}: doldurulmamış yer tutucu kaldı")
        dest = os.path.join(ROOT, "index.html" if code == "en" else os.path.join(code, "index.html"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(out)


def build_og_strings(data):
    shots = {c: s for c, _, _, _, s in LANGS}
    dirs = {c: d for c, _, _, d, _ in LANGS}
    T = {c: {**data[c]["og"], "_shots": shots[c], "_dir": dirs[c]} for c, *_ in LANGS}
    js = "// tools/build.py tarafından üretilir — elle düzenlemeyin, i18n/*.json'ı düzenleyin.\nwindow.T = " + json.dumps(T, ensure_ascii=False, indent=1) + ";\n"
    open(os.path.join(ROOT, "tools", "og", "strings.js"), "w", encoding="utf-8").write(js)


def build_media(data):
    blocks = []
    for i, (code, name, *_rest) in enumerate(LANGS):
        og = data[code]["og"]
        rows = []
        for t in TOPICS:
            items = "".join(
                f'<a class="item {f}" href="assets/og/{code}/{t}-{f}.jpg" download>'
                f'<img src="assets/og/{code}/{t}-{f}.jpg" loading="lazy" alt="{esc(og[t + "_h"])} — {sz}">'
                f'<span>{sz}<small>{use}</small></span></a>' for f, sz, use in FORMATS)
            rows.append(f'<h3 lang="{code}">{esc(og[t + "_h"])}</h3><div class="row">{items}</div>')
        blocks.append(f'<details id="{code}"{" open" if i == 0 else ""}><summary><b lang="{code}">{esc(name)}</b> <em>{code.upper()}</em></summary>{"".join(rows)}</details>')
    p = data["en"]["page"]
    out = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Smokeless Media Kit</title>
  <meta name="description" content="Download Smokeless social media images in {len(LANGS)} languages: link previews, Instagram posts and stories.">
  <link rel="canonical" href="{BASE}media.html">
  <link rel="icon" type="image/png" href="assets/img/favicon.png">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Smokeless Media Kit">
  <meta property="og:description" content="Ready-to-post Smokeless images in {len(LANGS)} languages.">
  <meta property="og:url" content="{BASE}media.html">
  <meta property="og:image" content="{BASE}assets/og/en/main-landscape.jpg?v={OG_VERSION}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{BASE}assets/og/en/main-landscape.jpg?v={OG_VERSION}">
  <meta name="theme-color" content="#EF6B4A">
  <style>
    :root {{ color-scheme: light; --brand: #EF6B4A; --ink: #2B1D17; --muted: #6E5D55; --bg: #F7E8DA; --card: #FFFFFF; --line: #EED9C7; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: var(--ink); background: var(--bg); line-height: 1.5; }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 20px 64px; }}
    header {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 24px 0 8px; }}
    header a {{ color: var(--ink); text-decoration: none; font-weight: 700; display: flex; align-items: center; gap: 10px; }}
    header img {{ width: 36px; height: 36px; border-radius: 9px; }}
    header .back {{ color: var(--brand); font-weight: 600; }}
    h1 {{ font-size: clamp(2rem, 5vw, 3rem); margin: 24px 0 8px; letter-spacing: -.02em; }}
    .lead {{ color: var(--muted); margin: 0 0 28px; }}
    details {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; margin-bottom: 12px; padding: 0 20px; }}
    summary {{ cursor: pointer; padding: 18px 0; font-size: 1.15rem; list-style: none; display: flex; align-items: center; gap: 10px; }}
    summary::-webkit-details-marker {{ display: none; }}
    summary::after {{ content: "+"; margin-inline-start: auto; color: var(--brand); font-size: 1.4rem; }}
    details[open] summary::after {{ content: "–"; }}
    summary em {{ font-style: normal; font-size: .72rem; font-weight: 700; color: #fff; background: var(--brand); border-radius: 999px; padding: 3px 9px; }}
    h3 {{ font-size: 1rem; margin: 18px 0 10px; }}
    .row {{ display: grid; grid-template-columns: 2.2fr 1.2fr .7fr; gap: 12px; align-items: start; padding-bottom: 8px; }}
    .item {{ display: block; background: var(--bg); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; color: var(--ink); text-decoration: none; transition: transform .15s ease, box-shadow .15s ease; }}
    .item:hover {{ transform: translateY(-2px); box-shadow: 0 10px 24px rgba(120,60,30,.14); }}
    .item img {{ display: block; width: 100%; height: auto; }}
    .item span {{ display: block; padding: 8px 10px; font-weight: 700; font-size: .85rem; background: var(--card); }}
    .item small {{ display: block; font-weight: 400; color: var(--muted); font-size: .75rem; }}
    @media (max-width: 720px) {{ .row {{ grid-template-columns: 1fr 1fr; }} .item.landscape {{ grid-column: 1 / -1; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <header><a href="./"><img src="assets/img/icon-256.png" alt="">Smokeless</a><a class="back" href="./">← smokeless</a></header>
    <h1>Media kit</h1>
    <p class="lead">Ready-to-post images in {len(LANGS)} languages. Open a language, then click any image to download it. Page links for sharing: {" · ".join(f'<a href="{url(c)}">{c}</a>' for c, *_ in LANGS)}</p>
    {"".join(blocks)}
  </div>
</body>
</html>
'''
    open(os.path.join(ROOT, "media.html"), "w", encoding="utf-8").write(out)


def build_sitemap():
    today = date.today().isoformat()
    alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{c}" href="{url(c)}"/>' for c, *_ in LANGS)
    alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    urls = "".join(f'''
  <url>
    <loc>{url(c)}</loc>{alts}
    <lastmod>{today}</lastmod>
  </url>''' for c, *_ in LANGS)
    out = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}
  <url>
    <loc>{BASE}media.html</loc>
    <lastmod>{today}</lastmod>
  </url>
</urlset>
'''
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    d = load()
    build_pages(d)
    build_og_strings(d)
    build_media(d)
    build_sitemap()
    print(f"✓ {len(LANGS)} dil: sayfalar, media.html, sitemap.xml, tools/og/strings.js")
