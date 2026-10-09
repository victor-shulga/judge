# Site / multi-page rubric (70 points + 30 core)

Applies to: a whole site or a section (services, industry, cases, skills catalog), a client
site after a copy reframe, a design-system page. The judge walks it as a buyer researching
before a first call: home → the page for their problem → proof → contact.

| # | Category | Pts | 10/10 looks like | 0 looks like |
|---|---|---|---|---|
| S1 | **Ten-second test on home** | 12 | Who you serve, what problem, what result, one action, all readable in ten seconds on the first screen. | "We are a team of passionate…"; a carousel; three audiences at once. |
| S2 | **Page per job, not per service** | 12 | Pages are organised by what the buyer is trying to do (problem, industry, situation), each with its own promise, proof and CTA. A buyer lands on the right page from search and does not need home. | One "Services" page listing everything; industry pages that are the services page with a different header. |
| S3 | **Proof at the moment of doubt** | 12 | Cases with numbers sit next to the claim they support; each key ICP has at least one case; case pages have the 8 elements (situation, problem, why us, what we did, numbers, timeline, quote, next step). | A "Portfolio" grid of logos; cases with no numbers; testimonials with no names or roles. |
| S4 | **Consistency of system** | 10 | One design system across every page (tokens, type, buttons, footer); one voice; nav the same everywhere; the same promise on home and on inner pages. | Pages from three eras; a page in another palette; CTA wording that changes per page. |
| S5 | **Paths converge** | 12 | Every page ends in the same one or two actions; no dead ends; 404s and orphan pages absent; internal links lead somewhere useful. | Pages with no CTA; three booking tools; "coming soon". |
| S6 | **Search and machines** | 12 | Titles and H1s carry the buyer's words; each page has one canonical, hreflang if bilingual, a sitemap; the copy answers the question an AI assistant would be asked about this company. | Titles = company name on every page; duplicate H1s; no sitemap; pages missing from index. |

**Type hard fails:** a banned name on any page; two design systems live at once; a client's
site carrying your own tokens; any download or CTA that resolves to a 404 or an HTML-as-file.

**Mechanical pre-gate is mandatory for this type:** run `scripts/pregate.py` on every page
in scope (a sitemap or a list of URLs). The judge receives the aggregated pre-gate report
(broken links, banned strings, claims) and scores S5/S6 partly from it.

**Judge input:** the list of pages (URLs or files) in the order a buyer would walk them, the
ICP in one line, which design system applies, the pre-gate report, this rubric, core.md.

**JSON:** `{"scores": {"C1":0,"C2":0,"C3":0,"S1":0,"S2":0,"S3":0,"S4":0,"S5":0,"S6":0}, "total": 0, "hard_fails": [], "lowest": "", "one_fix": "", "pages_below_80": []}`
