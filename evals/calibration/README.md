# Calibration pair

Two handoffs written from `../cases/01-midstream-implementation/`. They exist to
test the grader, not the skill.

Score these before scoring anything real. A grader that cannot separate them is
not measuring anything, and its verdict on a fresh handoff is noise.

| File | Expected rubric score | Expected linter result |
|---|---|---|
| `good.md` | 18 or above, all four load-bearing assertions passed | PASS, no warnings |
| `bad.md` | 10 or below, load-bearing assertions failed | FAIL — 9 failures (seven missing sections, a preamble, nothing concrete anywhere) and 3 warnings |

If `good.md` scores below 18, the grader is too harsh, or the rubric has an
assertion the skill never promised. If `bad.md` scores above 10, the grader is
rewarding fluent prose — which is the exact failure this whole eval exists to
catch, since `bad.md` is fluent, well organised, and nearly useless.

## What bad.md gets wrong

It is not a strawman. It is the shape the skill produced before the rewrite, and
it reads fine until you try to act on it.

Every specific has been sanded off: no SHA, no test count, no file paths, no test
node id, `rapidfuzz` never named, the design doc referred to as "the design doc"
rather than by path. The half-built tie breaker — the thing that blocks all the
work — appears as "some unfinished work in the candidate selection code", so the
next agent starts on the engine and discovers the stub the hard way.

Two errors are worse than vagueness. The deliberate xfail is described as "one of
the fuzzy name tests is currently failing", which invites the next agent to fix
it and thereby destroy the signal. And "pick up the next step of the plan" omits
that step 4 and only step 4 was authorized, so step 5 is a live risk.

Everything in the constraints category is simply gone: the protected file and its
hook, the container build failure behind the dropped dependency, the human-only
credential rotation, the instruction not to commit. None of it is contradicted —
it is just absent, which reads exactly like there being none.
