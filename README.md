# judge

A **Claude Code skill** that grades anything you are about to publish or send, blind, before
it goes out: LinkedIn posts, articles, decks, proposals, landing pages, whole sites,
infographics and carousels, cold sequences.

The writer never marks their own work. `judge` first runs a machine check that settles
everything a script can settle, then hands the artifact to a fresh Claude subagent that has
never seen your brief or earlier drafts. It scores the artifact out of 100 against a shared
core rubric (30) plus a rubric for its type (70). It ships at 90+ with zero hard fails. If it
falls short, you fix one thing and a NEW judge scores it again, up to three rounds.

## What you get

→ a pre-gate report: banned names found, links that are dead or serve HTML instead of a file,
every number on the artifact listed for verification, counts that drift ("70 skills" here,
"69" there), AI-sounding constructions
→ a score per category, the weakest category, hard fails, unverified claims
→ one concrete fix, never "improve the hook"

## Install

```bash
npx skills add victor-shulga/judge
```

Then in Claude: "judge this deck", "is this landing ready to ship", "прожени через суддю".

### Recommended

1. **Your banned list.** Create `~/.config/judge/banned.txt` with one name per line: clients,
   their products, vendors you must not name publicly. It stays on your machine and is never
   part of the skill. Any match on a public artifact is a hard fail.
2. **AI-construction detector:** `npx skills add victor-shulga/gtm-skills/anticopywriting-ai`.
   Without it the pre-gate skips that check and says so.
3. **Post rubric:** `npx skills add victor-shulga/content-engine-skills`. Without it posts are
   scored with the article rubric.

## Requirements & integrations

| Integration | Used for | Required? | Auth / setup |
|---|---|---|---|
| Claude Code | running the skill and the blind subagent | yes | claude.com/claude-code |
| python3 | `scripts/pregate.py` (standard library only) | yes | preinstalled on macOS / most Linux |
| `~/.config/judge/banned.txt` | names that must never appear in public artifacts | recommended | plain text, one name per line |
| anticopywriting-ai (gtm-skills) | AI-construction detector in the pre-gate | optional | `npx skills add victor-shulga/gtm-skills/anticopywriting-ai` |
| content-engine-skills | rubric for LinkedIn posts | optional | `npx skills add victor-shulga/content-engine-skills` |

Part of the GTM-system methodology by [Victor Shulga](https://victorshulga.com) (Fractional CRO).
Every skill in the stack: [CATALOG.md](https://github.com/victor-shulga/max/blob/main/CATALOG.md).

## License

MIT © Victor Shulga
