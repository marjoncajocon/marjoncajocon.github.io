#!/usr/bin/env python3
"""Generates every page of marjoncajocon.github.io.

The SITE IS STATIC: this script is run by hand and the HTML it writes is
committed. GitHub Pages serves those files directly - there is no build step at
deploy time. The generator exists only so that ~14 pages sharing a header,
footer, About overlay and lightbox stay consistent.

    python tools/build_pages.py

Never writes to checker/, chess/ or app-ads.txt - those are live URLs the store
listings point at.

Every engine claim here was verified against the C sources. In particular
Turkish ships a ZERO NNUE net (nnue_weights.h: "Every weight is zero, so
bb_nnue_score16 returns 0 and the engine plays on its hand-crafted evaluation
alone"), so it is deliberately excluded from the NNUE claims.
"""

import html
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://marjoncajocon.github.io"
AUTHOR = "Marjon Cajocon"
PUBLISHER = "MMC Solo Dev"
EMAIL = "marjoncajocon08@gmail.com"
GITHUB = "https://github.com/marjoncajocon"

PLAY = "https://play.google.com/store/apps/details?id="

# ── Projects ────────────────────────────────────────────────────────────────
# nnue: (hidden, features, extra) or None when the shipped net is a zero net.
PROJECTS = [
    dict(
        slug="chess-ta", name="Chess Ta!", kind="Chess",
        tagline="Offline chess with an NNUE engine, a real 3D board, and analysis tools.",
        title="Chess Ta! — offline chess app with an NNUE neural-network engine and 3D board",
        desc="Chess Ta! plays offline chess with a hand-written NNUE neural-network engine in C, "
             "a real 3D board, an analysis board, game review and eleven difficulty tiers.",
        keyword="offline chess app NNUE engine 3D board",
        nnue=("256", "768", "quantised int16, QA 255 / QB 64"),
        play=None, package="com.marjoncajocon.chessta",
        privacy="/chess/privacy.html",
        rules="Standard chess, plus Chess960 (Fischer Random). Eleven opponent tiers run from "
              "a deliberately gentle beginner up to a full-strength engine, so the same app "
              "works for someone learning the moves and someone studying an opening.",
        features=[
            "Play offline against eleven difficulty tiers, from beginner to full strength",
            "A real 3D board rendered with three.js, alongside the classic 2D board",
            "Analysis board with an evaluation bar and Best Move hints",
            "Game review: step through a finished game move by move",
            "PGN library — import, browse and review your own games",
            "Custom position setup, pass & play on one device, and AI vs AI",
            "Board and piece themes, and full offline operation",
        ],
        images=[
            ("phone_03_both_views.png", "Both board modes side by side", "Chess Ta! showing the 3D board and the 2D board together"),
            ("phone_01_3d_board.png", "The 3D board", "Chess Ta! 3D chess board rendered with three.js"),
            ("phone_02_2d_board.png", "The classic 2D board", "Chess Ta! classic 2D chess board"),
            ("board3d_wide.png", "3D board, wide layout", "Chess Ta! 3D chess board on a wide screen"),
        ],
    ),
    dict(
        slug="dama-ta", name="Dama Ta!", kind="Filipino draughts",
        tagline="Filipino dama with the strongest net in the family — a 512-wide NNUE.",
        title="Dama Ta! — Filipino dama app with an NNUE neural-network engine",
        desc="Dama Ta! plays Filipino dama offline against a hand-written NNUE neural-network "
             "engine in C, with a 3D board, analysis tools and custom positions.",
        keyword="Filipino dama NNUE engine",
        nnue=("512", "128", "4 phase buckets on piece count"),
        play="com.marjoncajocon.damata", package="com.marjoncajocon.damata",
        privacy=None,
        rules="Filipino dama on an 8×8 board. Men move diagonally forward; kings fly any "
              "distance along a diagonal. Capturing is mandatory and you must take the line "
              "that captures the most pieces.",
        features=None,
        images=[
            ("board3d.png", "The 3D board", "Dama Ta! 3D Filipino dama board"),
            ("phone_02_vs_ai.png", "Playing the engine", "Dama Ta! game against the AI"),
            ("phone_03_analysis.png", "Analysis board", "Dama Ta! analysis board"),
            ("phone_04_setup.png", "Custom position setup", "Dama Ta! custom board setup"),
            ("phone_01_home.png", "Home screen", "Dama Ta! home screen"),
            ("board3d_wide.png", "3D board, wide layout", "Dama Ta! 3D board on a wide screen"),
        ],
    ),
    dict(
        slug="brazilian", name="Brazilian Checkers", kind="Brazilian draughts",
        tagline="8×8 Brazilian rules with international capture logic, on a 256-wide NNUE.",
        title="Brazilian Checkers — NNUE neural-network engine, offline Android app",
        desc="Brazilian checkers played offline against a hand-written NNUE neural-network "
             "engine in C, with a 3D board, analysis tools and custom positions.",
        keyword="Brazilian checkers NNUE neural network app",
        nnue=("256", "128", "4 phase buckets on piece count"),
        play="com.marjoncajocon.brazilianchecker", package="com.marjoncajocon.brazilianchecker",
        privacy="/checker/brazilian/privacy.html",
        rules="Brazilian draughts is played on an 8×8 board with international rules: men "
              "capture both forwards and backwards, kings fly along a diagonal, and you must "
              "always play the capture that takes the most pieces.",
        features=None,
        images=[
            ("board3d.png", "The 3D board", "Brazilian checkers 3D board"),
            ("phone_02_vs_ai.png", "Playing the engine", "Brazilian checkers game against the AI"),
            ("phone_03_analysis.png", "Analysis board", "Brazilian checkers analysis board"),
            ("phone_04_setup.png", "Custom position setup", "Brazilian checkers custom board setup"),
            ("phone_01_home.png", "Home screen", "Brazilian checkers home screen"),
            ("board3d_wide.png", "3D board, wide layout", "Brazilian checkers 3D board on a wide screen"),
        ],
    ),
    dict(
        slug="international", name="International Draughts", kind="International draughts",
        tagline="The 10×10 game, 20 pieces a side, on a compact 32-wide net.",
        title="International Draughts 10×10 — neural-network engine, offline Android app",
        desc="International draughts on a 10×10 board, played offline against a hand-written "
             "NNUE neural-network engine in C, with a 3D board and analysis tools.",
        keyword="International draughts 10x10 neural network engine",
        nnue=("32", "200", "50 dark squares × 4 piece planes"),
        play="com.marjoncajocon.intcheckers", package="com.marjoncajocon.intcheckers",
        privacy="/checker/international-checker/privacy.html",
        rules="International draughts uses a 10×10 board and twenty pieces a side. Men capture "
              "in every direction, kings fly, and the maximum-capture rule is strict — you must "
              "take the longest available line.",
        features=None,
        images=[
            ("board3d.png", "The 10×10 board in 3D", "International draughts 10x10 3D board"),
            ("phone_02_vs_ai.png", "Playing the engine", "International draughts game against the AI"),
            ("phone_03_analysis.png", "Analysis board", "International draughts analysis board"),
            ("phone_04_setup.png", "Custom position setup", "International draughts custom board setup"),
            ("phone_01_home.png", "Home screen", "International draughts home screen"),
            ("board3d_wide.png", "3D board, wide layout", "International draughts 3D board on a wide screen"),
        ],
    ),
    dict(
        slug="russian", name="Russian Checkers", kind="Russian draughts",
        tagline="Russian rules, including promotion mid-capture, on a 128-wide NNUE.",
        title="Russian Checkers — NNUE neural-network engine, offline Android app",
        desc="Russian checkers played offline against a hand-written NNUE neural-network engine "
             "in C, with a 3D board, analysis tools and custom positions.",
        keyword="Russian checkers AI neural network",
        nnue=("128", "128", None),
        play="com.marjoncajocon.russiandama", package="com.marjoncajocon.russiandama",
        privacy="/checker/russian-checker/privacy.html",
        rules="Russian draughts is played on 8×8 with flying kings and captures in all "
              "directions. Its distinctive rule: a man that reaches the back row during a "
              "capture promotes immediately and continues the same capture as a king.",
        features=None,
        images=[
            ("board3d.png", "The 3D board", "Russian checkers 3D board"),
            ("phone_02_vs_ai.png", "Playing the engine", "Russian checkers game against the AI"),
            ("phone_03_analysis.png", "Analysis board", "Russian checkers analysis board"),
            ("phone_04_setup.png", "Custom position setup", "Russian checkers custom board setup"),
            ("phone_01_home.png", "Home screen", "Russian checkers home screen"),
            ("board3d_wide.png", "3D board, wide layout", "Russian checkers 3D board on a wide screen"),
        ],
    ),
    dict(
        slug="english", name="English Draughts", kind="English / American checkers",
        tagline="The classic American game — men capture forward only — on a 128-wide NNUE.",
        title="English / American Checkers — NNUE neural-network engine, offline app",
        desc="English draughts (American checkers) played offline against a hand-written NNUE "
             "neural-network engine in C, with a 3D board and analysis tools.",
        keyword="English American checkers NNUE engine",
        nnue=("128", "128", None),
        play="com.marjoncajocon.englishdama", package="com.marjoncajocon.englishdama",
        privacy="/checker/english-checker/privacy.html",
        rules="English draughts — American checkers — is the most restrictive of the family. "
              "Men move and capture forwards only, and kings step one square at a time rather "
              "than flying. Capturing is mandatory, but you may choose which capture to play.",
        features=None,
        images=[
            ("board3d.png", "The 3D board", "English draughts 3D board"),
            ("phone_02_vs_ai.png", "Playing the engine", "English draughts game against the AI"),
            ("phone_03_analysis.png", "Analysis board", "English draughts analysis board"),
            ("phone_04_setup.png", "Custom position setup", "English draughts custom board setup"),
            ("phone_01_home.png", "Home screen", "English draughts home screen"),
            ("board3d_wide.png", "3D board, wide layout", "English draughts 3D board on a wide screen"),
        ],
    ),
    dict(
        slug="turkish", name="Turkish Draughts", kind="Turkish draughts",
        tagline="Orthogonal movement on all 64 squares — a different game entirely.",
        title="Turkish Draughts — orthogonal 8×8 draughts engine in C",
        desc="Turkish draughts on all 64 squares with orthogonal movement, played offline "
             "against a hand-written engine in C with a 3D board and analysis tools.",
        keyword="Turkish draughts engine app",
        nnue=None,
        play=None, package="com.marjoncajocon.turkishdama",
        privacy=None,
        rules="Turkish draughts is the outlier. Every one of the 64 squares is playable, men "
              "move and capture sideways and forwards rather than diagonally, and kings slide "
              "orthogonally any distance. None of the diagonal-board work transfers.",
        features=None,
        images=[
            ("board3d.png", "The 3D board", "Turkish draughts 3D board with orthogonal movement"),
            ("board3d_wide.png", "3D board, wide layout", "Turkish draughts 3D board on a wide screen"),
        ],
    ),
]

DEFAULT_FEATURES = [
    "Play offline against a neural-network engine — no account, no connection",
    "A real 3D board rendered with three.js, alongside the classic 2D board",
    "Analysis board with an evaluation bar and best-move hints",
    "Game review: step back through a finished game move by move",
    "Custom position setup, pass & play on one device, and AI vs AI",
    "Board and piece themes, and a rules panel for the variant",
]

NNUE_SLUGS = [p["slug"] for p in PROJECTS if p["nnue"]]

# ── Shared chrome ───────────────────────────────────────────────────────────

LOGO = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<rect x="1" y="1" width="10" height="10" rx="2" fill="currentColor"/>'
        '<rect x="13" y="13" width="10" height="10" rx="2" fill="currentColor"/>'
        '<rect x="13" y="1" width="10" height="10" rx="2" stroke="currentColor" stroke-width="1.8"/>'
        '<rect x="1" y="13" width="10" height="10" rx="2" stroke="currentColor" stroke-width="1.8"/>'
        '</svg>')


def head(title, desc, canon, og_image="/assets/img/hero_3d.png", jsonld=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{AUTHOR}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{canon}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<meta name="robots" content="index,follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
{jsonld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active=""):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<header class="site-head"><div class="wrap">
<a class="brand" href="/">{LOGO} Marjon Cajocon</a>
<nav class="nav" aria-label="Main">
{a("/#apps", "Apps", "apps")}
{a("/projects/engine/", "Engine", "engine")}
{a("/projects/llm-project/", "LLM", "llm")}
{a("/blog/", "Writing", "blog")}
<button class="btn-ghost" id="aboutBtn" type="button">About me</button>
<button class="btn-ghost" id="themeToggle" type="button" aria-label="Toggle theme" title="Toggle light / dark">&#9681;</button>
</nav></div></header>
"""


ABOUT = f"""<dialog class="about" id="aboutDlg" aria-labelledby="aboutTitle"><div class="about-in">
<div class="about-head">
  <img src="/res/profile.jpg" alt="" width="68" height="68">
  <div><h2 id="aboutTitle" style="margin:0">Marjon Cajocon</h2>
  <p style="margin:.2rem 0 0;color:var(--muted)">Software engineer · Talibon, Bohol, Philippines</p></div>
</div>
<p>I build game engines in C and the apps that ship them. Seven board-game
engines, six of them running NNUE neural networks I trained myself, plus a
from-scratch LLM engine written in dependency-free C.</p>
<dl>
  <dt>Primary</dt><dd>C — engines, evaluation, search, the LLM stack</dd>
  <dt>Then</dt><dd>Go · Flutter (Dart) · Python · TypeScript / JavaScript</dd>
  <dt>Certification</dt><dd>EDP Specialist — Civil Service, rated <strong>94.65%</strong>
      <span style="color:var(--muted)">(80% to pass)</span></dd>
  <dt>Published</dt><dd>Five apps live on Google Play, more in testing</dd>
  <dt>Contact</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
  <dt>Code</dt><dd><a href="{GITHUB}" rel="noopener">github.com/marjoncajocon</a></dd>
</dl>
<p style="margin-top:1.2rem"><button class="btn btn-outline" id="aboutClose" type="button">Close</button></p>
</div></dialog>
"""


def footer():
    links = "\n".join(
        f'<a href="/projects/{p["slug"]}/">{html.escape(p["name"])}</a>' for p in PROJECTS)
    return f"""<footer class="site-foot"><div class="wrap">
<div class="foot-links">
{links}
<a href="/projects/engine/">Engine</a>
<a href="/projects/llm-project/">LLM engine</a>
<a href="/blog/">Writing</a>
</div>
<p>&copy; 2026 {AUTHOR} · published as {PUBLISHER}. Board-game engines in C, apps in Flutter.</p>
</div></footer>
{ABOUT}
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lb-close" id="lbClose" type="button" aria-label="Close">&times;</button>
  <img id="lbImg" src="" alt="">
  <p class="lb-cap" id="lbCap"></p>
</div>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def page(title, desc, canon, body, active="", og=None, jsonld=""):
    og = og or "/assets/img/hero_3d.png"
    return head(title, desc, canon, og, jsonld) + header(active) + body + footer()


def jsonld_block(obj):
    import json
    return '<script type="application/ld+json">' + json.dumps(obj, indent=None) + "</script>\n"


# ── Page bodies ─────────────────────────────────────────────────────────────

def gallery(slug, images):
    out = ['<div class="gallery">']
    for fn, cap, alt in images:
        src = f"/assets/img/{slug}/{fn}"
        out.append(
            f'<figure style="margin:0"><a class="shot" href="{src}" data-cap="{html.escape(cap)}">'
            f'<img src="{src}" alt="{html.escape(alt)}" loading="lazy" width="800" height="600">'
            f'</a><figcaption>{html.escape(cap)}</figcaption></figure>')
    out.append("</div>")
    return "\n".join(out)


def project_page(p):
    slug, name = p["slug"], p["name"]
    feats = p["features"] or DEFAULT_FEATURES

    if p["nnue"]:
        hid, feat, extra = p["nnue"]
        extra = f", {extra}" if extra else ""
        engine = (
            f'<p>The evaluation is an <strong>NNUE neural network</strong> — '
            f'{hid} hidden units over {feat} input features{extra} — written in C '
            f'and compiled straight into the app. It is trained from self-play by a '
            f'Go trainer, quantised to 16-bit integers, and evaluated incrementally '
            f'so the search can afford to call it at every node.</p>')
        tag = '<span class="tag">NNUE neural network</span>'
    else:
        engine = (
            '<p>The engine is written in C with bitboards and an alpha-beta search, and '
            'evaluates positions with a <strong>hand-crafted evaluation function</strong>. '
            'Turkish draughts uses all 64 squares with orthogonal movement, so none of the '
            'diagonal-board network work transfers to it — an NNUE net for this variant is '
            'still in training and is not in the shipped build.</p>')
        tag = '<span class="tag is-muted">Hand-crafted evaluation</span>'

    if p["play"]:
        cta = (f'<a class="btn btn-primary" href="{PLAY}{p["play"]}" rel="noopener">'
               f'Get it on Google Play</a>')
    else:
        cta = '<a class="btn" aria-disabled="true" href="#">Coming to Google Play</a>'

    priv = (f' · <a href="{p["privacy"]}">Privacy policy</a>') if p["privacy"] else ""

    ld = jsonld_block({
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": name, "applicationCategory": "GameApplication",
        "operatingSystem": "Android", "description": p["desc"],
        "author": {"@type": "Person", "name": AUTHOR},
        "publisher": {"@type": "Organization", "name": PUBLISHER},
        "url": f"{SITE}/projects/{slug}/",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    })

    body = f"""<main id="main"><div class="wrap">
<p class="crumb"><a href="/">Home</a> &rsaquo; <a href="/#apps">Apps</a> &rsaquo; {html.escape(name)}</p>
<section class="hero" style="border:0;padding-bottom:1rem">
  <span class="eyebrow">{html.escape(p["kind"])}</span>
  <h1>{html.escape(name)}</h1>
  <p class="lede">{html.escape(p["tagline"])}</p>
  <p>{tag}</p>
  <div class="hero-cta">{cta}<a class="btn btn-outline" href="#screens">See the screens</a></div>
</section>

<div class="prose">
<h2>The engine</h2>
{engine}
<h2>The rules of this variant</h2>
<p>{html.escape(p["rules"])}</p>
<h2>What you get</h2>
<ul>
{"".join(f"<li>{html.escape(f)}</li>" for f in feats)}
</ul>
</div>

<h2 id="screens">Screens</h2>
<p style="color:var(--muted);max-width:44rem">Click any image to view it full size. The 3D
shots are the real board renderer, captured from the same page the app ships.</p>
{gallery(slug, p["images"])}

<div class="prose">
<p style="margin-top:2rem"><a href="/projects/engine/">How the engine and its training pipeline work</a>{priv}</p>
</div>
</div></main>"""

    return page(p["title"], p["desc"], f"/projects/{slug}/", body, "apps",
                og=f"/assets/img/{slug}/{p['images'][0][0]}", jsonld=ld)


def index_page():
    cards = []
    for p in PROJECTS:
        tag = ('<span class="tag">NNUE</span>' if p["nnue"]
               else '<span class="tag is-muted">Hand-crafted eval</span>')
        live = "Live on Google Play" if p["play"] else "In testing"
        cards.append(f"""<a class="card" href="/projects/{p['slug']}/">
<h3>{html.escape(p['name'])}</h3>
<p>{html.escape(p['tagline'])}</p>
<div class="card-foot">{tag} <span style="color:var(--muted);font-size:.83rem">· {live}</span></div>
</a>""")

    ld = jsonld_block({
        "@context": "https://schema.org", "@type": "Person", "name": AUTHOR,
        "url": SITE + "/", "email": EMAIL, "sameAs": [GITHUB],
        "jobTitle": "Software engineer",
        "knowsAbout": ["C", "Go", "Dart", "Flutter", "Python", "TypeScript",
                       "NNUE", "neural networks", "game engines", "draughts", "chess"],
    })

    body = f"""<main id="main"><div class="wrap">
<section class="hero">
  <span class="eyebrow">Board-game engines in C</span>
  <h1>Strong checkers and chess, powered by NNUE neural networks.</h1>
  <p class="lede">I write board-game engines in C and ship them as offline mobile apps.
  Six of them evaluate positions with an <strong>NNUE neural network</strong> — the same
  efficiently-updatable architecture that transformed computer chess — trained from
  self-play and small enough to run on a phone with no connection.</p>
  <div class="hero-cta">
    <a class="btn btn-primary" href="#apps">See the apps</a>
    <a class="btn btn-outline" href="/projects/engine/">How the engine works</a>
  </div>
  <ul class="pills">
    <li class="pill is-primary">C</li><li class="pill">Go</li>
    <li class="pill">Flutter / Dart</li><li class="pill">Python</li>
    <li class="pill">TypeScript / JavaScript</li>
  </ul>
  <div class="stats">
    <div class="stat"><b>7</b><span>engines written in C</span></div>
    <div class="stat"><b>6</b><span>running NNUE nets</span></div>
    <div class="stat"><b>5</b><span>live on Google Play</span></div>
    <div class="stat"><b>100%</b><span>offline play</span></div>
  </div>
  <figure class="hero-shot">
    <img src="/assets/img/hero_3d.png" width="2400" height="1200" fetchpriority="high"
         alt="The Chess Ta! 3D board: chess pieces on a wooden table, rendered in 3D">
    <figcaption>The 3D board in Chess&nbsp;Ta! — the same renderer runs in every app here.</figcaption>
  </figure>
</section>

<h2 id="apps">The apps</h2>
<p style="color:var(--muted);max-width:44rem">Every one plays offline, has a 3D board and a
classic 2D board, and ships its engine compiled in — nothing is evaluated on a server.</p>
<div class="grid">
{"".join(cards)}
</div>

<h2>Why a neural network matters here</h2>
<div class="prose">
<p>Most checkers apps evaluate a position by counting material and adding a few
hand-written bonuses. That is fast, and it is why they play the same predictable way
every game.</p>
<p>An <strong>NNUE</strong> — an efficiently-updatable neural network — replaces those
hand-written rules with a small network trained on millions of self-play positions. It is
built so that moving one piece updates only the part of the network that changed, which
makes it cheap enough to call at every node of the search. That is what lets a phone play
a genuinely strong game rather than a fast shallow one.</p>
<p>Every net here was trained from scratch against its own variant. Rules differ enough
between Brazilian, Russian, English, International, Filipino and Turkish draughts that a
net trained on one is worthless on another — International alone needs a different board
size and a different feature set.</p>
<p><a href="/blog/nnue-for-checkers/">How NNUE works for checkers &rarr;</a></p>
</div>

<h2>Other work</h2>
<div class="grid">
<a class="card" href="/projects/engine/">
<h3>The engine &amp; training pipeline</h3>
<p>The shared C core behind all seven games: bitboards, alpha-beta search, the Go NNUE
trainer, self-play generation and endgame tablebases.</p>
<div class="card-foot"><span class="tag">C · Go</span></div></a>
<a class="card" href="/projects/llm-project/">
<h3>Pure-C LLM engine</h3>
<p>A language-model stack written from scratch in dependency-free C11 — training,
inference, LoRA fine-tuning and a tool-using agent, with no framework underneath.</p>
<div class="card-foot"><span class="tag">C · Python · Go</span></div></a>
</div>
</div></main>"""

    return page(
        "Marjon Cajocon — strong checkers and chess engines powered by NNUE neural networks",
        "Offline checkers and chess apps with hand-written NNUE neural-network engines in C. "
        "Six draughts variants and chess, trained from self-play, playing strong on a phone.",
        "/", body, "", jsonld=ld)


def engine_page():
    rows = "".join(
        f"<tr><td>{html.escape(p['name'])}</td><td>{p['nnue'][1] if p['nnue'] else '—'}</td>"
        f"<td>{p['nnue'][0] if p['nnue'] else '—'}</td>"
        f"<td>{'NNUE' if p['nnue'] else 'Hand-crafted'}</td></tr>"
        for p in PROJECTS)

    body = f"""<main id="main"><div class="wrap">
<p class="crumb"><a href="/">Home</a> &rsaquo; Engine</p>
<section class="hero" style="border:0;padding-bottom:1rem">
  <span class="eyebrow">The shared core</span>
  <h1>One C engine, seven games, six neural networks.</h1>
  <p class="lede">Every app on this site is a thin Flutter shell around the same C engine.
  The search, the move generator and the network evaluator are shared; the rules and the
  trained net are what differ.</p>
</section>

<div class="prose">
<h2>Search</h2>
<p>Bitboard move generation, alpha-beta with iterative deepening, a transposition table,
late-move reductions and futility pruning. Each variant compiles its own move generator
from a shared template, so Turkish draughts — which moves orthogonally across all 64
squares — reuses the same search without special-casing it.</p>

<h2>Evaluation</h2>
<p>Six of the seven engines evaluate with an NNUE network compiled directly into the
binary. The draughts nets use an antisymmetric formulation: the network is evaluated for
the position and for its mirror, and the difference is the score. That guarantees the
engine values a position identically from either side, which a plain network has to learn
approximately and never quite gets right.</p>
<p>Weights are quantised to 16-bit integers, so evaluation is integer-only — no floating
point in the search at all.</p>

<div class="tablewrap">
<table>
<caption style="text-align:left;color:var(--muted);padding-bottom:.5rem">Input features and hidden width per engine.</caption>
<thead><tr><th>Engine</th><th>Input features</th><th>Hidden units</th><th>Evaluation</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>

<div class="callout">
<p><strong>Turkish is honest about what it is.</strong> Its shipped build uses the
hand-crafted evaluation. The diagonal-board nets could not be reused — Turkish draughts
plays on all 64 squares — and the nets trained for it so far have not beaten the
hand-crafted baseline in gated testing, so none has been promoted.</p>
</div>

<h2>Training</h2>
<p>Nets are trained by a Go trainer against positions generated by self-play. The engine
plays itself at a fixed depth, positions and their search scores are written out in
shards, and the trainer fits the network to those labels. New nets are gated: a candidate
only ships if it beats the current one over a match, which is why some trained candidates
were never promoted.</p>

<h2>Endgame tablebases</h2>
<p>Late positions are answered from perfect-play tables rather than searched. The engines
generate their own tablebases for small piece counts and probe them during search, so an
endgame that a search would misjudge is played exactly.</p>

<h2>Portability</h2>
<p>The engine is plain C with no third-party dependencies. It compiles to a shared library
for Android and Windows, and the Flutter apps call into it directly — the same code runs
on a phone and on a desktop.</p>
</div>
</div></main>"""

    return page(
        "The engine — NNUE training pipeline for draughts and chess, written in C",
        "How the shared C engine behind seven board games works: bitboard search, "
        "antisymmetric NNUE evaluation, self-play training in Go, and endgame tablebases.",
        "/projects/engine/", body, "engine")


def llm_page():
    body = f"""<main id="main"><div class="wrap">
<p class="crumb"><a href="/">Home</a> &rsaquo; LLM engine</p>
<section class="hero" style="border:0;padding-bottom:1rem">
  <span class="eyebrow">Machine learning from scratch</span>
  <h1>A language-model stack written in dependency-free C.</h1>
  <p class="lede">No PyTorch, no BLAS, no framework — the C standard library and the maths.
  Training, inference, fine-tuning and a tool-using agent, all hand-written.</p>
</section>

<div class="prose">
<h2>What it does</h2>
<p>It trains and runs transformer language models. Two architectures are implemented and
both train: a classic GPT-2 style network, and a modern LLaMA-family one with RMSNorm,
rotary position embeddings, grouped-query attention and SwiGLU. Every backward pass is
derived by hand and checked numerically against finite differences.</p>
<p>It loads real published weights, runs them with a KV cache and quantised int8 tensors,
fine-tunes them with LoRA adapters, and then uses the result as the brain of a
tool-using coding agent — parse, approve, execute, observe — with no API and no network.</p>

<h2>Why it is interesting</h2>
<ul>
<li>The tokeniser is written in C, matching the reference byte-pair encoders exactly, so
there is no Python anywhere at runtime.</li>
<li>The matrix kernels are plain portable C with no intrinsics, and still reach roughly
seven to nine times the speed of the naive version through cache blocking alone.</li>
<li>It cross-compiles to eight targets including WebAssembly, and runs there.</li>
<li>The agent is fine-tuned by the project's own trainer — the stack trains the model it
then runs.</li>
</ul>

<div class="callout">
<p><strong>Scope, stated plainly.</strong> This is a complete and correct engine, not a
competitive model. Trained from scratch on a CPU, the outputs are toy-scale by design.
The deliverable is the pipeline — every stage implemented and verified — rather than
production quality text.</p>
</div>

<h2>Where it stands</h2>
<p>Working and actively developed. There is a 25-part self-test that gates every change,
including numerical gradient checks and a bit-exactness check on the KV cache, and a
browser UI for driving training and generation.</p>
</div>
</div></main>"""

    return page(
        "Pure-C LLM engine — training, inference and a tool-using agent with no dependencies",
        "A transformer language-model stack written from scratch in dependency-free C11: "
        "hand-derived backpropagation, LoRA fine-tuning, int8 inference and a tool-using agent.",
        "/projects/llm-project/", body, "llm")


# ── Blog ────────────────────────────────────────────────────────────────────

POSTS = [
    dict(
        slug="nnue-for-checkers",
        title="How NNUE works for checkers",
        desc="NNUE transformed computer chess. Here is what it takes to apply the same "
             "efficiently-updatable network architecture to draughts, and why each variant "
             "needs its own net.",
        date="2026-08-28",
        body="""
<p>NNUE — an efficiently-updatable neural network — is the idea that reshaped computer
chess. It is worth explaining what it actually is, because the name suggests something
more exotic than the reality.</p>

<h2>The problem it solves</h2>
<p>A game engine searches millions of positions. For each one it needs a number: how good
is this? Traditionally that number came from hand-written rules — count the material, add
a bonus for a piece on a strong square, subtract for a weak structure. Fast, but it only
knows what its author thought to tell it.</p>
<p>A neural network learns those judgements instead. The catch is cost. A network that
takes a millisecond to evaluate is useless when you need millions of evaluations per
move.</p>

<h2>The trick</h2>
<p>NNUE's insight is that consecutive positions in a search are almost identical. Moving
one piece changes two squares. So instead of recomputing the network from scratch, you
keep a running total — the accumulator — and when a piece moves you subtract the
contribution of the square it left and add the contribution of the square it arrived on.</p>
<p>That is what "efficiently updatable" means. The expensive first layer is never
recomputed, only adjusted. The rest of the network is small enough that evaluating it is
cheap.</p>

<h2>What changes for draughts</h2>
<p>The architecture transfers, but almost nothing else does.</p>
<p><strong>The feature set is smaller.</strong> Chess has six piece types on 64 squares
for each colour — 768 inputs. Draughts has two piece types, men and kings, and on an 8×8
board only 32 squares are ever occupied. That gives 128 inputs: four planes of 32
squares. International draughts, on 10×10, uses 50 squares per plane and 200 inputs.</p>
<p><strong>Symmetry can be enforced rather than learned.</strong> A draughts position seen
from the other side should score exactly the opposite. Rather than hope the network learns
that, you evaluate the network for the position and for its mirror and take the
difference. The result is antisymmetric by construction. A network that has to learn
symmetry approximately will always have small inconsistencies; one built this way cannot.</p>
<p><strong>Each variant needs its own net.</strong> This is the part that surprises people.
Brazilian and English draughts use the same board and the same starting position, but in
one kings fly the length of a diagonal and in the other they step one square. That single
difference changes what a position is worth so thoroughly that a net trained on one plays
badly on the other. Turkish draughts is further still — orthogonal movement across all 64
squares — and shares no feature layout at all.</p>

<h2>Training</h2>
<p>The engine plays itself at a fixed depth and records each position with the score its
search returned. The network is then fit to those scores. It is a distillation: the
network learns to guess in one pass what the search took thousands of nodes to work out.</p>
<p>Every candidate is gated. A new net only ships if it beats the current one over a
match. That gate matters — it is why not every trained net makes it into a release, and
why one variant here still runs on its hand-crafted evaluation.</p>

<h2>Why it is rare in draughts</h2>
<p>Strong neural draughts engines exist, but they are desktop programs. Putting one on a
phone means the whole thing — search, network and weights — has to be small, integer-only
and dependency-free. That is the engineering, more than the architecture.</p>
"""),
    dict(
        slug="how-strong-is-the-engine",
        title="How strong is the engine, and how would you know?",
        desc="Measuring board-game engine strength honestly: what self-play tells you, what "
             "it hides, and why a gated match is the only number worth trusting.",
        date="2026-08-28",
        body="""
<p>Every game app claims a strong AI. Almost none says what that means. Here is how
strength is actually measured, and what the numbers are worth.</p>

<h2>Self-play is a trap</h2>
<p>The obvious test is to have a new version play the old one. Do that and you will find
your engine improving forever, because both sides share the same blind spots. An engine
that misunderstands a certain endgame will keep misunderstanding it, and both versions
will walk into it equally often. The score says nothing.</p>
<p>Self-play is still how training data is generated — you need millions of labelled
positions and there is no other source. But generating data and measuring strength are
different jobs, and conflating them is the classic mistake.</p>

<h2>What a gate actually is</h2>
<p>A gate is a match, played under fixed conditions, that a candidate must win before it
ships. Same time control, same opening set, both colours, enough games that the result
is not noise.</p>
<p>The important part is that <em>it is allowed to fail</em>. A gate that always passes is
decoration. In this project several trained networks were rejected by their gate and never
shipped — one variant still runs its hand-crafted evaluation for exactly that reason. That
is the gate working.</p>

<h2>Why depth is a bad advertisement</h2>
<p>"Searches 20 ply deep" sounds impressive and means very little. Depth depends entirely
on how aggressively the search prunes, and an engine that prunes carelessly reaches great
depths while missing things a shallower, more careful search would find. Two engines
reporting the same depth can be hundreds of Elo apart.</p>

<h2>What difficulty tiers really are</h2>
<p>A difficulty setting is not a weaker engine. It is the same engine, deliberately
constrained — less time, less depth, and at the lower tiers a chance of choosing a move
that is good rather than best.</p>
<p>That last part matters for a game people actually enjoy. An engine made weak purely by
reducing depth plays strangely: excellent for a while, then suddenly blind. Adding
controlled imprecision instead produces an opponent that plays plausibly and makes the
kind of mistakes a human might, which is what a beginner tier is for.</p>

<h2>The honest summary</h2>
<p>The engines here are strong enough that most players will not beat the top tiers, and
the tiers below exist so that is not the only experience on offer. Precise Elo figures
across draughts variants are hard to state meaningfully — there is no common rating pool
to anchor to, the way chess has. Claiming a specific number would be inventing one.</p>
"""),
]


def blog_index():
    items = "".join(f"""<a class="card" href="/blog/{p['slug']}/">
<h3>{html.escape(p['title'])}</h3><p>{html.escape(p['desc'])}</p>
<div class="card-foot"><span style="color:var(--muted);font-size:.83rem">{p['date']}</span></div></a>"""
                    for p in POSTS)
    body = f"""<main id="main"><div class="wrap">
<p class="crumb"><a href="/">Home</a> &rsaquo; Writing</p>
<section class="hero" style="border:0;padding-bottom:1rem">
<h1>Writing</h1>
<p class="lede">Notes on building board-game engines — how the neural networks work, and
how strength is actually measured.</p>
</section>
<div class="grid">{items}</div>
</div></main>"""
    return page("Writing — notes on NNUE, engine strength and board-game AI",
                "Technical write-ups on NNUE neural networks for checkers and chess, and on "
                "measuring board-game engine strength honestly.",
                "/blog/", body, "blog")


def blog_post(p):
    ld = jsonld_block({
        "@context": "https://schema.org", "@type": "TechArticle",
        "headline": p["title"], "description": p["desc"],
        "datePublished": p["date"], "dateModified": p["date"],
        "author": {"@type": "Person", "name": AUTHOR},
        "mainEntityOfPage": f"{SITE}/blog/{p['slug']}/",
    })
    body = f"""<main id="main"><div class="wrap">
<p class="crumb"><a href="/">Home</a> &rsaquo; <a href="/blog/">Writing</a> &rsaquo; {html.escape(p['title'])}</p>
<article class="prose">
<h1 style="margin-top:1.2rem">{html.escape(p['title'])}</h1>
<p style="color:var(--muted)"><time datetime="{p['date']}">{p['date']}</time> · {AUTHOR}</p>
{p['body']}
<p style="margin-top:2.4rem"><a href="/#apps">See the apps these engines ship in &rarr;</a></p>
</article>
</div></main>"""
    return page(f"{p['title']} — {AUTHOR}", p["desc"], f"/blog/{p['slug']}/", body, "blog",
                jsonld=ld)


# ── Static extras ───────────────────────────────────────────────────────────

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
<rect width="24" height="24" rx="4" fill="#14243A"/>
<rect x="3" y="3" width="8" height="8" rx="1.5" fill="#E8B563"/>
<rect x="13" y="13" width="8" height="8" rx="1.5" fill="#E8B563"/>
<rect x="13" y="3" width="8" height="8" rx="1.5" fill="none" stroke="#E8B563" stroke-width="1.6"/>
<rect x="3" y="13" width="8" height="8" rx="1.5" fill="none" stroke="#E8B563" stroke-width="1.6"/>
</svg>
"""

SITE_JS = """/* Progressive enhancement only: every feature here degrades to plain HTML.
   The gallery links go straight to the full image without JS, and the About
   panel is a <dialog> that simply does not open. */
(function () {
  // Theme. Kept compatible with the previous site's localStorage key.
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('theme');
    if (saved) root.setAttribute('data-theme', saved);
    else if (window.matchMedia('(prefers-color-scheme: light)').matches)
      root.setAttribute('data-theme', 'light');
  } catch (e) { /* private mode: fall through to the dark default */ }

  var t = document.getElementById('themeToggle');
  if (t) t.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // About overlay.
  var dlg = document.getElementById('aboutDlg');
  var open = document.getElementById('aboutBtn');
  var close = document.getElementById('aboutClose');
  if (dlg && open && typeof dlg.showModal === 'function') {
    open.addEventListener('click', function () { dlg.showModal(); });
    if (close) close.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  } else if (open) {
    open.hidden = true; // no <dialog> support: do not offer a button that does nothing
  }

  // Lightbox.
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lbImg');
  var lbCap = document.getElementById('lbCap');
  var lbClose = document.getElementById('lbClose');
  if (!lb) return;
  function show(href, cap, alt) {
    lbImg.src = href; lbImg.alt = alt || ''; lbCap.textContent = cap || '';
    lb.classList.add('is-open'); lbClose.focus();
  }
  function hide() { lb.classList.remove('is-open'); lbImg.src = ''; }
  document.querySelectorAll('a.shot').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      show(a.getAttribute('href'), a.dataset.cap, a.querySelector('img').alt);
    });
  });
  lbClose.addEventListener('click', hide);
  lb.addEventListener('click', function (e) { if (e.target === lb) hide(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lb.classList.contains('is-open')) hide();
  });
})();
"""


def not_found():
    body = """<main id="main"><div class="wrap">
<section class="hero" style="border:0">
<span class="eyebrow">404</span>
<h1>That page isn't here.</h1>
<p class="lede">The link may be old, or the page may have moved.</p>
<div class="hero-cta"><a class="btn btn-primary" href="/">Go to the home page</a>
<a class="btn btn-outline" href="/#apps">See the apps</a></div>
</section></div></main>"""
    return page("Page not found — Marjon Cajocon", "That page could not be found.",
                "/404.html", body)


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    # Explicit newline="" keeps LF endings on Windows; Path.write_text only
    # grew a newline argument in 3.10 and this runs on 3.9.
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    print(f"  {rel}")


def main():
    print("writing pages:")
    write("index.html", index_page())
    for p in PROJECTS:
        write(f"projects/{p['slug']}/index.html", project_page(p))
    write("projects/engine/index.html", engine_page())
    write("projects/llm-project/index.html", llm_page())
    write("blog/index.html", blog_index())
    for p in POSTS:
        write(f"blog/{p['slug']}/index.html", blog_post(p))
    write("404.html", not_found())
    write("favicon.svg", FAVICON)
    write("assets/site.js", SITE_JS)
    write(".nojekyll", "")

    urls = ["/", "/projects/engine/", "/projects/llm-project/", "/blog/"]
    urls += [f"/projects/{p['slug']}/" for p in PROJECTS]
    urls += [f"/blog/{p['slug']}/" for p in POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == "/" else "0.8"
        sm.append(f"  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq>"
                  f"<priority>{pri}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"\n{len(urls)} pages. checker/, chess/ and app-ads.txt untouched.")


if __name__ == "__main__":
    main()
