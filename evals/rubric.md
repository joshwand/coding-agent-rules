# Handoff rubric

Twenty-one assertions about a handoff document. Each is worth one point and is
answered yes or no — if it needs a paragraph of hedging, the answer is no.

Grade against the session the handoff was written from. Nearly every assertion
is a claim about whether the handoff carries something the session contained,
and you cannot check that without both halves.

## Calibrate before you grade

Score `calibration/bad.md` and `calibration/good.md` first, both written from
`cases/01-midstream-implementation/`. A working grader puts good at 18 or above
and bad at 10 or below. If they land closer together than that, the grader is
being generous and its scores on real handoffs mean nothing yet. Fix that before
going further.

## Actionable

1. **First action is executable.** Someone with no other context could carry out
   the first thing in "Your scope" without asking a question.
2. **Everything named is findable.** Every file, module, command, and test named
   in "Your scope" is given a path, or is somewhere the named reading will reach.
3. **Reading is ordered.** "Read first" says what to read *in what order*, not
   just which documents are relevant.
4. **Authority is settled.** "Read first" says which documents outrank the
   handoff, so a conflict between them resolves without asking.

## Grounded

5. **Nothing invented.** Every claim traces to the session or to the repository.
   One fabricated file path fails this outright.
6. **Inference is marked.** Anything concluded rather than established is stated
   as an inference, not asserted flatly.
7. **Points rather than paraphrases.** Where a rules file, design doc, or memory
   file already covers something, the handoff names it instead of restating it.

## Carries the state

8. **Finished is separated from half-finished**, and anything half-finished has a
   location.
9. **Specifics survive.** SHAs, test counts, versions, and error strings that the
   session established appear verbatim rather than as "a few tests" or "recently".
10. **Breakage is declared.** What is broken, and what is unfinished on purpose,
    are both stated. Silence here reads as "everything works".

## Bounded

11. **Says where to stop.** There is an explicit boundary — what not to start,
    what not to commit, what is out of scope for this stretch.
12. **Says what to escalate.** Names at least one thing to bring back rather than
    decide alone, or states plainly that the scope is fully delegated.

## Constrained

13. **Prohibitions carry their mechanism.** Each constraint says what enforces it
    — a hook, a permission, a protected path, a service that will refuse. A bare
    "be careful with X" does not count.
14. **Dead ends are recorded.** Approaches already tried and ruled out are named,
    so the next agent does not spend the session rediscovering them.
15. **Human-only steps are flagged.** Anything the agent cannot do itself is
    named, along with what to do instead of attempting it.

## Honest about what is open

16. **Options are preserved, not re-litigated.** Open decisions are presented as
    they stood at the end of the session, without the handoff quietly picking one.
17. **The human's decisions are marked as theirs**, and separated from the
    judgment calls the next agent is free to make.

## Verifiable

18. **Done is testable.** The exit criteria can be checked by running or reading
    something. "Works correctly" fails; "full suite green, 214 passing" passes.
19. **The report is specified.** It says what the final message back to the human
    needs to contain.

## Written well enough to use

20. **No filler.** No section padded to look complete, no summary of the summary,
    no restating the request back.
21. **Register matches** the session it came from.

## Scoring

Total out of 21.

Four are load-bearing: **1** (first action executable), **8** (state separated),
**11** (says where to stop), and **13** (prohibitions carry their mechanism).
Failing any of those caps the handoff at "not usable" regardless of the total —
they are the difference between a briefing and a nicely written recap.

| Score | Reading |
|---|---|
| 18–21, all four load-bearing passed | Usable as written |
| 14–17 | Usable after the human patches the gaps; note which |
| Below 14, or any load-bearing failure | Regression — the skill is drifting back toward a recap |

Report the failed assertion numbers, not just the total. A score with no failure
list is not actionable, which is the same complaint this rubric exists to make.
