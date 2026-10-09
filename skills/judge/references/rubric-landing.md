# Landing page / lead magnet rubric (70 points + 30 core)

Applies to: one page with one goal (a download, a booking, a waitlist, a gated map). The
judge arrives from a post or an ad, on a phone, with no terminal and 20 seconds.

| # | Category | Pts | 10/10 looks like | 0 looks like |
|---|---|---|---|---|
| L1 | **First screen answers three questions** | 12 | Who this is for, what they get, what to do next, all above the fold, without scrolling, on a phone. | A slogan; a hero that needs the post to make sense; the form below three screens of text. |
| L2 | **Promise = delivery** | 16 | Everything the source post or the hero promises exists on the page or one click away: the file, the map, the count. Gated page: what is behind the gate is exactly what the gate says. | "All skills" leads to six terminal commands; "download" leads to a page that says "see elsewhere". |
| L3 | **Path without expertise** | 12 | A reader with no terminal, no GitHub account and no prior knowledge can complete the goal. Every step is labelled; jargon has a plain alternative next to it. | Instructions that assume a CLI; a step that says "install X" without saying how. |
| L4 | **Objections met in place** | 10 | The doubts a reader has right before the action are answered right there: is it free, what happens to my email, how long does it take, can I do it without a developer. | FAQ nowhere; "no spam" absent on a form; price hidden. |
| L5 | **One goal, one action** | 10 | One primary button, repeated, same wording. Secondary links do not compete. | Two forms; a booking CTA fighting a download CTA; "learn more" everywhere. |
| L6 | **Mechanics work** | 10 | Every link resolves to real content (a .zip is served as a zip, not an HTML 404 with status 200); the form submits; the page loads under 3 s; counts on the page match the artifact they describe. | Broken download; a form that silently fails; hero says 63, table says 69. |

**Type hard fails:** a client name; a download link that returns HTML; a
promise in the hero that the page cannot fulfil; the primary action needs a terminal and
no alternative is offered.

**Mechanical pre-gate is mandatory for this type:** `scripts/pregate.py <url-or-file>`
checks links by content-type, banned strings and extracts numeric claims. The judge gets the
pre-gate's list of claims and is asked to verify each one on the page.

**Judge input:** the rendered page (URL or HTML; for a gated page ALSO the post-gate content),
the source post or creative's promise in one line (only the promise, not the rationale),
the pre-gate claims list, this rubric, core.md.

**JSON:** `{"scores": {"C1":0,"C2":0,"C3":0,"L1":0,"L2":0,"L3":0,"L4":0,"L5":0,"L6":0}, "total": 0, "hard_fails": [], "lowest": "", "one_fix": "", "unverified_claims": []}`
