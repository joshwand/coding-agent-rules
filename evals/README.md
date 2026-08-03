# Evals

A small suite for the `handoff` skill. Prompts regress silently — a skill can get
edited into something that still produces a plausible document while quietly
dropping the parts that made it useful. This catches that.

Two layers, because the failures come in two kinds. Format regressions are cheap
and mechanical, so a script decides them. Substance regressions need judgment, so
a rubric and a model decide those. No dependencies either way: stdlib Python and
markdown.

```
lint_handoff.py    deterministic structural checks
rubric.md          21 substance assertions, model-graded
cases/             synthetic sessions to generate handoffs from
calibration/       a known-good and known-bad pair, to test the grader
local/             gitignored; your real handoffs
```

## The linter

```
python3 evals/lint_handoff.py handoff.md
```

Checks the seven sections are present and in order, the plain-prose rule holds,
nothing precedes the first section, "Standing constraints" is not empty, and
something paste-able (a path, a command, a SHA) actually appears — including
inside "Read first" specifically.

FAIL exits non-zero. WARN never fails the run; warnings flag recap phrasing,
missing second-person address, and documents thin enough to be worth re-reading.

Verify it works on the pair:

```
python3 evals/lint_handoff.py evals/calibration/good.md   # PASS, 0 failed, 0 warned
python3 evals/lint_handoff.py evals/calibration/bad.md    # FAIL, 9 failed, 3 warned
```

## The full eval

The linter cannot tell a specific handoff from a vague one, which is the failure
that matters. For that:

1. **Calibrate the grader.** Score `calibration/good.md` and `calibration/bad.md`
   against `rubric.md`. Good must land at 18+, bad at 10 or below. If they land
   close together, stop — see `calibration/README.md`.
2. **Generate.** In a fresh chat with the skill available, paste a case's
   `session.md` as context and ask for a handoff (`.cn`). A fresh chat matters:
   grading a handoff in the session that wrote it tests nothing, because the
   grader can see everything the handoff left out.
3. **Lint** the result.
4. **Grade** it against `rubric.md` plus the case's `expected.md`. Report failed
   assertion numbers, not just a total.

Three or four handoffs per case is more informative than one — the interesting
question is which assertions fail *repeatedly*, since a single miss is sampling
noise and a pattern is a gap in the skill.

## The cases

| Case | Shape | Stresses |
|---|---|---|
| `01-midstream-implementation` | Real state, a blocked carryover, protected paths, a human-only step, an open decision | Everything; this is the hard one |
| `02-planning-only` | Nothing built, no constraints, no blockers | Graceful degradation — does the format pad or stay honest |
| `03-blocked-on-human` | Stopped on a human action, two live options | Whether open decisions survive unchosen |

Each case has a `session.md` (the input) and an `expected.md` (the facts that must
survive, and how the case is usually failed).

## Adding a case

New cases should come from a session that produced a *bad* handoff. That is the
one reliable source of eval material: a fixture invented to be tricky tests what
you imagined, while one derived from a real failure tests what actually goes
wrong. Synthesize the shape, drop the project specifics, and write the
`expected.md` from what the real handoff lost.

## local/

`evals/local/` is gitignored. Drop real handoffs there and grade them against the
same rubric without publishing project details. Nothing in the suite depends on
it being populated.
