# Cold sequence rubric (70 points + 30 core)

Applies to: a cold email or LinkedIn sequence, every step at once (first touch + follow-ups + breakup),
written for one hypothesis (ICP × signal or data-point × offer).

Score the WHOLE sequence, then name the weakest step. One weak step drags the reply rate of the run.

| # | Category | Pts | 10/10 looks like | 0 looks like |
|---|---|---|---|---|
| S1 | **Hook: subject + first line** | 14 | The subject reads like an internal note (3–5 words, no marketing words); the first line names the signal or a situation the reader recognises in under 20 words. Every step opens differently. | "Quick question", "Partnership opportunity", "I hope this finds you well", a compliment, "I came across your profile"; follow-ups that open with "just following up". |
| S2 | **Human voice** | 14 | Reads like one person wrote it to one person: contractions, uneven sentence length, no template smell, no fake personalisation ("Loved your recent post"). Matches how the persona writes. | Passive voice, "we help companies like yours", stacked adjectives, a merge field where a thought should be, the same rhythm in every step. |
| S3 | **Signal → problem → offer, carried** | 14 | The anchor (signal / data-point / segment insight) is named in step 1 and every later step builds on it: consequence, proof, new stakeholder, breakup. A reader can say why THIS company got THIS email now. | Generic pain with no anchor; steps that could be sent to anyone; the offer appears before the problem; follow-ups that only repeat step 1. |
| S4 | **Scannable: one idea per step** | 14 | Each step ≤ 90 words (LinkedIn ≤ 60), one idea, no jargon, readable in 15 seconds on a phone. The whole sequence has a visible arc, not five versions of one email. | Walls of text, two asks in one step, a paragraph of credentials, bullet lists of features, a step over 120 words. |
| S5 | **Their specific problem, not a category** | 14 | The pain is the one this role at this kind of company has this quarter, said in their words, with a denominator where a number appears ("3 of 10 RFPs lost on speed"). | "Growing revenue is hard", "efficiency", "digital transformation"; a metric with no source; a case study the sender cannot show. |

**Type hard fails:** any step asks for a call, meeting, demo or time slot (the CTA asks about interest, never for
time; `cta-interest-based` in outbound-engine-skills has the patterns); spintax anywhere; a fabricated metric, client name or case; no anchor at all in
step 1 (a base without a signal, data-point or segment insight is not a sequence, it is spam); a step over
120 words; a breakup that guilt-trips ("hope I didn't do something wrong").

**Judge input:** every step of the sequence in order with channel and delay, the ICP in one line, the
hypothesis (ICP × anchor × offer) in one line, this rubric, core.md.

**Verdict extra:** `weakest_step` (the step number that would lose the most replies) and `one_fix` written
so the writer changes ONE thing, not the whole sequence. Re-score after the fix; loop max 3, new judge each time.

**JSON:** `{"scores": {"C1":0,"C2":0,"C3":0,"S1":0,"S2":0,"S3":0,"S4":0,"S5":0}, "total": 0, "hard_fails": [], "weakest_step": 0, "lowest": "", "one_fix": ""}`
