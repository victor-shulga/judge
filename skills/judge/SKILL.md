---
name: judge
description: >
  Blind quality gate for every artifact you put in front of a reader, a buyer or a search
  engine: LinkedIn posts, articles and longreads, decks, proposals and offers, landing pages
  and lead magnets, whole sites, creatives (infographics, carousels) and cold sequences.
  Runs a mechanical pre-gate first (your private list of banned names such as clients and
  vendors, AI constructions via the anticopywriting detector, every download and GitHub link
  checked by content-type, numeric claims extracted, count drift), then spawns a FRESH
  subagent that scores the artifact against core.md (30 pts) plus the type rubric (70 pts)
  and returns JSON. Threshold 90 with zero hard fails, max 3 rounds with a new judge each
  time. Use when the user says "judge this", "суддя", "оціни", "прожени через суддю", "gate",
  "is this ready to ship", "чи можна шипити", "перевір перед публікацією", "grade the
  deck/proposal/page", or before anything public goes out. NOT a writer, it never edits the
  artifact; it returns scores and one fix.
---

# Judge — one blind gate for every artifact

A post gets better when the writer never marks their own work. This skill applies the same
rule to everything else you publish or send.

Rule it enforces: **an artifact ships when a stranger, given only the artifact, scores it
≥ 90/100 with zero hard fails, after a machine has already removed everything a machine can
catch.** Nothing below 90 ships silently.

## Step 0 — Identify the type

| Type | What it is | Rubric |
|---|---|---|
| `post` | LinkedIn post ≤ 300 words | optional, if installed: `reference/grader-rubric.md` of content-engine-skills (70) + `references/core.md` (30); without that pack, `references/rubric-article.md` |
| `article` | longread, guide, blog, newsletter | `references/rubric-article.md` |
| `deck` | any presentation, HTML or PDF | `references/rubric-deck.md` |
| `proposal` | send-proposal, call-deck proposal, offer, retainer | `references/rubric-proposal.md` |
| `landing` | one page, one goal; incl. gated lead magnets | `references/rubric-landing.md` |
| `site` | multi-page site or section | `references/rubric-site.md` |
| `creative` | infographic, carousel, cover, banner | `references/rubric-creative.md` |
| `sequence` | cold email / LinkedIn sequence, all steps at once | `references/rubric-sequence.md` |

If the user did not say, infer from the file (length, `<form>`, slide markup, price) and
state the choice in one line. Wrong type = wrong rubric; ask only if two types are equally
likely.

## Step 1 — Mechanical pre-gate (always, before any subagent)

`<skill-dir>` below is the folder this SKILL.md lives in.

```bash
python3 <skill-dir>/scripts/pregate.py <file-or-url> --type <type> --pretty
# gated landing: also pass what the reader sees after the form
python3 <skill-dir>/scripts/pregate.py https://site/page/ --type landing --gate-html post_gate.html --pretty
# site: a directory of built html, or run once per URL and merge
```

It returns `verdict`, `hard_fails`, `warnings`, `claims`, `links`, `detector`.

- **`verdict: fail` → stop.** Report the hard fails, do not spawn the judge. Fix, re-run.
  Hard fails at this stage: a banned string, a download served as `text/html`, a link
  that is not 200, an AI construction in the prose.
- `warnings` do not block but go to the judge as context (count drift, detector warnings).
- `claims` is the list of every number-plus-noun on the artifact. The judge must verify each.

**The banned list is yours and stays private.** Put one name per line (clients, their
products, vendors you must not name in public, an old brand) into
`~/.config/judge/banned.txt`. It lives outside the skill so the skill can be shared without
leaking names. No file = only the AI-construction and link checks run, and the report says
so. Use `--banned <path>` for a per-project list.

**AI-construction detector (optional).** If present, the pre-gate calls `anticopywriting-ai/scripts/detect.py`,
which ships in `victor-shulga/gtm-skills`. It looks in the usual skill folders
(`~/.claude/skills`, `./.claude/skills`, `~/.agents/skills`, `./.agents/skills`) or in
`$JUDGE_DETECT`. Not installed → `detector: skipped`; say that in the report, the judge
still runs. To add it: `npx skills add victor-shulga/gtm-skills/anticopywriting-ai`.

For pages, add the reader walk when the artifact is live: open it at phone width, find the
primary action, complete it without a terminal. If you cannot, that is an `L3` zero and a
hard fail on `L2` if the promise was "download".

## Step 2 — Spawn the blind judge

One `Agent` (general-purpose), clean context. It receives ONLY:

1. The artifact: text, HTML, or images (creatives, decks) — for a gated page, both the
   public page and the post-gate content; for a site, the pages in buyer order.
2. One line of framing: type, intended reader, and (for landing/creative) the promise the
   reader arrives with, quoted from the post or hero. Nothing about why or how it was made.
3. `references/core.md` + the type rubric (or the content-engine grader rubric for posts).
4. The pre-gate `claims` list and `warnings` (never the author's explanation of them).
5. For decks, creatives and sites: which design system applies (yours or your client's), as
   one line with the path or URL of its token file.

Ask for **JSON only**, the shape given at the bottom of the rubric, harsh, no prose. The
judge verifies every claim on the artifact itself and lists the ones it could not verify.

Never give the judge: the brief, previous drafts, the creative that inspired it, the
campaign plan, the detector's reasoning, or praise.

## Step 3 — Gate

`pre-gate pass` **AND** `total ≥ 90` **AND** `hard_fails == []` **AND**
`unverified_claims == []` (where the rubric has that field).

## Step 4 — Loop, with a new judge each time

Not taken → fix `hard_fails` first, then apply `one_fix` to `lowest`, re-run the pre-gate,
spawn a **new** subagent. Never ask the same judge to reconsider. Stop after 3 rounds and
hand it to the user as "gate not taken — X/100, weakest = <category>, one_fix = …"; the
decision to ship is theirs.

## Step 5 — Report (in the user's language)

```
Judge · <type> · <artifact name>
Pre-gate: pass | fail (<n> hard fails) · detector: ran | skipped · banned list: <n> names | none
Score: 87/100 · weakest: L2 "promise = delivery" (9/16)
Hard fails: —
Unverified claims: "156 signals"
One fix: <one edit>
Verdict: gate not taken / gate taken
```

Plus, for pages and sites, the pre-gate link table when anything was red.

## Hard rules

- The judge never edits. Editing is the writer's job; the judge only scores.
- Every rescore = new subagent. "Adjust your previous score" is self-deception.
- A number that cannot be verified on a public surface is a hard fail for `creative` and
  `landing`, a warning for `article` and `deck` (where estimates are allowed if labelled).
- Client names in a public artifact are a hard fail regardless of total; the private banned
  list is the source, and the judge also flags anything that reads like a client.
- For `landing` and `site`, `pregate.py` is part of the gate, not a suggestion.

## Requirements

- Claude Code (subagents) and `python3` (standard library only).
- Optional: `anticopywriting-ai` (`npx skills add victor-shulga/gtm-skills/anticopywriting-ai`) for the AI-construction check.
- Optional: `content-engine-skills` for the post rubric.
- Your own `~/.config/judge/banned.txt`.
