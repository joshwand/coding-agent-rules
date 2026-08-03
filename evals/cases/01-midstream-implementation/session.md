# Case 01 — midstream implementation

A synthetic session record. Paste this into a fresh chat as the context, then ask
for a handoff (`.cn`). The document that comes back is what gets graded.

This is the hard case: real state, real constraints, a blocked carryover, a human
only step, and an open decision. A handoff that carries all of it is doing the job.

---

Project `tessera`, a Python CLI that reconciles invoices against a ledger. We are
working through a six step rewrite plan.

**What happened this session.**

Finished steps 1 through 3 of the plan in
`_memory/knowledgeBase/designs/ReconcilerRewrite.md`. That document is
authoritative over anything I summarise here — where they disagree, believe it.
Committed the three steps together at `4c1f9ab`. Suite is 214 passing, 0 skipped,
run with `.venv/bin/pytest -q`.

Step 4 is the matching engine, `tessera/match/engine.py`. Josh authorized step 4
and only step 4 this session.

**The thing that blocks step 4.** `tessera/match/candidates.py` is half built. The
scoring function is written and tested; the tie breaker below it is a `TODO`
stub that returns the first candidate. Step 4 consumes that function, so it has
to be finished before the engine can be built on top of it.

**Deliberately failing.** `tests/test_fuzzy.py::test_unicode_names` is marked
xfail. It stays xfail until the normalization decision below is made — it is not
a regression and should not be "fixed" by changing the assertion.

**Already tried and dropped.** Step 2 used `rapidfuzz` for the matcher. It pulls
a C extension that breaks the Alpine container build, so it came out again and
the decision is stdlib `difflib`. Do not reintroduce it; the build failure is
not obvious until the image is built in CI.

**Protected.** `tessera/config/rates.py` is owner edited. Write is permission
denied and a pre-commit hook rejects any commit touching it. When step 2 needed a
change there, we wrote `tessera/config/rates_proposed.py` alongside it and Josh
applied it by hand. Do the same if step 4 needs one.

**Needs Josh, cannot be done by an agent.** The production reconciliation run
needs a credential rotated in the bank's web console. There is no API for it and
the agent has no browser or credentials. If step 4 gets far enough to want a real
run: prepare everything up to the point of the run, write the exact steps Josh
needs to click into `_memory/currentState/currentTaskState.md`, and stop there.

**Open, not decided.** Unicode name normalization: NFKC, or strip diacritics
before comparing. NFKC is more correct and keeps names readable in the output;
stripping matches more aggressively, which is what the reconciliation actually
wants but produces output a human cannot verify by eye. Josh has not chosen. This
decides the xfail test above.

**Standing instructions.** Do not commit — Josh reviews before anything lands. Do
not start step 5. Keep `_memory/currentState/currentTaskState.md` current.

**Bar for done.** Step 4 implemented per the plan with tests, `candidates.py`
tie breaker finished, full suite green, task state updated so a fresh agent could
take step 5, and a final report covering what was built, the test count, any
deviations from the plan, and anything needing Josh's decision.
