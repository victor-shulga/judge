#!/usr/bin/env python3
"""Mechanical pre-gate for the judge skill. Settles everything a regex or an HTTP HEAD can
settle BEFORE a blind judge is spawned, so the judge only spends attention on what needs
reading.

    python3 pregate.py <file-or-url> [--type post|article|deck|proposal|landing|site|creative]
                                     [--lang uk|en|auto] [--banned ~/.config/judge/banned.txt]
                                     [--gate-html <file>]   # post-gate content for a gated landing
                                     [--pretty]

Input may be: .md/.txt (prose), .html (rendered page), an http(s) URL (fetched), or a
directory (every .html inside, for --type site).

What it checks
  1. banned strings  — every line of YOUR private banned list (client, product and vendor
                       names; lives OUTSIDE the skill so the skill can be shared)
  2. AI constructions — runs anticopywriting-ai/scripts/detect.py on the visible prose
                       (mode post for posts, email for proposals, generic otherwise)
  3. links           — every href/src that is a download (.zip/.pdf/.csv/...) or points at
                       github.com/raw.githubusercontent.com: HEAD it; a download that comes
                       back as text/html is a dead link served with status 200
  4. claims          — every number next to a noun ("70 скілів", "23 критерії", "437 з 5 000",
                       "10 секцій") is extracted for the judge to verify one by one
  5. count drift     — the same noun with two different numbers inside one artifact

Output: JSON {verdict: pass|fail, hard_fails: [...], warnings: [...], claims: [...], links: {...}}
verdict = fail  →  fix and re-run; the judge is not spawned on a failing artifact.
"""
import argparse
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import urllib.request

# anticopywriting-ai ships in victor-shulga/gtm-skills; look where skill installers put it.
DETECT = [p for p in [os.environ.get("JUDGE_DETECT")] if p] + [
    os.path.join(os.path.expanduser(root), "anticopywriting-ai", "scripts", "detect.py")
    for root in ("~/.claude/skills", "./.claude/skills", "~/.agents/skills", "./.agents/skills")
]
DOWNLOAD_EXT = (".zip", ".pdf", ".csv", ".xlsx", ".docx", ".pptx", ".json", ".md")

# number + noun, uk/en. Keeps the phrase for the judge; the noun stem is used for drift.
CLAIM = re.compile(
    r"(?<![\w/.-])(\d{1,3}(?:[  ]\d{3})*|\d+)(?:[,.]\d+)?\s?(%|скіл\w*|скілів|паків?|пак\w*|критері\w*|секці\w*|"
    r"сигнал\w*|тижн\w*|днів|дні|блок\w*|крок\w*|рядк\w*|акаунт\w*|компані\w*|відповід\w*|зустріч\w*|"
    r"skills?|packs?|criteria|sections?|signals?|weeks?|days?|blocks?|steps?|rows?|accounts?|companies|replies|meetings?)",
    re.I,
)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "judge-pregate/1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def head(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "judge-pregate/1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", "")
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def prose_only(text, min_words=6):
    """Nav items, chips, labels and command lines are not prose: the AI-construction
    detector sees a 'triad' in any three short fragments in a row. Keep only lines a
    reader would read as a sentence."""
    keep = []
    for line in text.splitlines():
        s = line.strip()
        if len(s.split()) < min_words or s.startswith(("npx ", "/", "$")):
            continue
        keep.append(s)
    return "\n".join(keep)


def visible_text(html):
    m = re.search(r"<main[^>]*>(.*?)</main>", html, flags=re.S | re.I)
    if m:
        html = m.group(1)
    html = re.sub(r"<(script|style|noscript|nav|header|footer)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<br\s*/?>|</(p|div|li|h\d|tr|section|article)>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = htmlmod.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n", text).strip()


def load_banned(path):
    words = []
    p = os.path.expanduser(path)
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#"):
                words.append(line)
    return words


def run_detector(text, lang, mode):
    for d in DETECT:
        if os.path.exists(d):
            r = subprocess.run([sys.executable, d, "--stdin", "--lang", lang, "--mode", mode],
                               input=text, capture_output=True, text=True)
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                return {"verdict": "error", "raw": (r.stdout + r.stderr)[-400:]}
    return {"verdict": "skipped", "reason": "anticopywriting-ai not installed: npx skills add victor-shulga/gtm-skills/anticopywriting-ai"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--type", default="landing",
                    choices=["post", "article", "deck", "proposal", "landing", "site", "creative", "sequence"])
    ap.add_argument("--lang", default="auto", choices=["uk", "en", "auto"])
    ap.add_argument("--banned", default="~/.config/judge/banned.txt")
    ap.add_argument("--gate-html", help="post-gate HTML/markdown for a gated landing (checked too)")
    ap.add_argument("--pretty", action="store_true")
    a = ap.parse_args()

    # ---- gather sources ----
    sources = []  # (label, html_or_text, is_html, base_url)
    t = a.target
    if t.startswith("http"):
        sources.append((t, fetch(t), True, t))
    elif os.path.isdir(t):
        for root, _d, files in os.walk(t):
            for f in sorted(files):
                if f.endswith(".html"):
                    p = os.path.join(root, f)
                    sources.append((p, open(p, encoding="utf-8", errors="replace").read(), True, None))
    else:
        body = open(t, encoding="utf-8", errors="replace").read()
        sources.append((t, body, t.endswith((".html", ".htm")), None))
    if a.gate_html:
        body = open(a.gate_html, encoding="utf-8", errors="replace").read()
        # post-gate content lives on the same origin as the gated page → resolve its links there
        sources.append((a.gate_html, body, "<" in body[:200], t if t.startswith("http") else None))

    banned = load_banned(a.banned)
    hard, warn, claims, links = [], [], [], {}
    all_text = []

    for label, body, is_html, base in sources:
        text = visible_text(body) if is_html else body
        all_text.append(text)

        # 1 banned
        for w in banned:
            if re.search(re.escape(w), body, re.I):
                hard.append(f"banned string «{w}» in {label}")

        # 3 links
        if is_html:
            for href in set(re.findall(r'(?:href|src)="([^"#]+)"', body)):
                if href.startswith("mailto:") or href.startswith("tel:"):
                    continue
                is_dl = any(href.split("?")[0].lower().endswith(e) for e in DOWNLOAD_EXT)
                is_gh = "github.com" in href or "githubusercontent.com" in href
                if not (is_dl or is_gh):
                    continue
                full = href
                if not href.startswith("http"):
                    if base:
                        from urllib.parse import urljoin
                        full = urljoin(base, href)
                    else:
                        warn.append(f"relative link not checked (no base url): {href}")
                        continue
                if full in links:
                    continue
                st, ct = head(full)
                links[full] = f"{st} {ct.split(';')[0]}"
                if st != 200:
                    hard.append(f"link {full} → {st}")
                elif is_dl and "text/html" in ct:
                    hard.append(f"download served as HTML (404 behind a 200): {full}")

        # 4 claims (a leading zero is a card number, not a quantity)
        for m in CLAIM.finditer(text):
            if re.match(r"0\d", m.group(1)):
                continue
            claims.append(m.group(0).strip())

    # 2 detector on prose (skip for site/deck where prose is fragmented)
    detector = None
    if a.type in ("post", "article", "proposal", "landing", "creative"):
        mode = {"post": "post", "proposal": "email"}.get(a.type, "generic")
        prose = "\n".join(all_text)
        if any(s[2] for s in sources):          # html in play → drop fragments before the detector
            prose = prose_only(prose)
        if len(prose) > 200:
            detector = run_detector(prose, a.lang, mode)
            if detector.get("verdict") == "fail":
                for hf in detector.get("hard_fails", []):
                    hard.append(f"AI construction: {hf if isinstance(hf, str) else json.dumps(hf, ensure_ascii=False)}")
            for w in detector.get("warnings", []) or []:
                warn.append(f"detector: {w if isinstance(w, str) else json.dumps(w, ensure_ascii=False)}")

    # 5 count drift: same noun stem, different numbers
    by_noun = {}
    for c in claims:
        m = CLAIM.match(c)
        if not m:
            continue
        num, noun = m.group(1).replace(" ", " "), m.group(2).lower()
        stem = re.sub(r"(ів|и|ах|ами|ів|s|es)$", "", noun)[:5]
        if stem in ("%",):
            continue
        by_noun.setdefault(stem, set()).add(num)
    for stem, nums in by_noun.items():
        if len(nums) > 1 and stem in ("скіл", "пак", "pack", "skill", "крите", "секці", "блок", "block"):
            warn.append(f"count drift for «{stem}»: {sorted(nums)} — verify these are different things")

    out = {
        "verdict": "fail" if hard else "pass",
        "type": a.type,
        "sources": [s[0] for s in sources],
        "hard_fails": hard,
        "warnings": warn,
        "claims": sorted(set(claims)),
        "links": links,
        "detector": detector,
        "banned_list": f"{len(banned)} names" if banned else f"none ({a.banned} not found)",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2 if a.pretty else None))
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
