# Case 01 — what the handoff must carry

Case level assertions, checked alongside `../../rubric.md`. Each fact below either
survives into the handoff or the handoff loses something the next agent needs.

## Must appear, verbatim where it is an identifier

- Steps 1 through 3 done, committed at `4c1f9ab`.
- 214 passing, 0 skipped, and the command `.venv/bin/pytest -q`.
- `_memory/knowledgeBase/designs/ReconcilerRewrite.md`, named as authoritative
  over the handoff itself.
- Step 4 is the scope, and step 4 is `tessera/match/engine.py`.
- `tessera/match/candidates.py` is half built, the tie breaker is a stub, and it
  blocks step 4 — so it comes first.
- `tests/test_fuzzy.py::test_unicode_names` is xfail on purpose and must not be
  "fixed" by changing the assertion.
- `rapidfuzz` was tried and dropped over the Alpine C extension build failure;
  stdlib `difflib` is the decision.
- `tessera/config/rates.py` is owner edited, with the enforcement named (Write
  denied, pre-commit hook) and the `rates_proposed.py` workaround.
- The credential rotation is human only, with the instruction to prepare up to
  the run, write the click steps into
  `_memory/currentState/currentTaskState.md`, and stop.
- Do not commit. Do not start step 5.

## Must be presented as open, not resolved

The NFKC versus strip-diacritics decision, with both sides as they stood, marked
as Josh's to make. A handoff that picks one has failed assertion 16, however
sensible the pick.

## What this case is designed to stress

| Assertion | Why this case tests it |
|---|---|
| 1, 2 | The first action is the `candidates.py` tie breaker, not step 4 — a handoff that opens with "implement the matching engine" has buried the blocker |
| 8 | Three finished steps and one half-finished file, which have to read differently |
| 9 | A SHA, a test count, and a test node id are all available to lose |
| 10 | The xfail is unfinished on purpose; silence makes it look like a bug to fix |
| 11, 12 | "Step 4 only, do not commit" is the boundary; the credential rotation is the escalation |
| 13 | Two constraints with real mechanisms — a permission denial plus a hook, and a container build that fails only in CI |
| 14 | `rapidfuzz` is the dead end, and it is expensive to rediscover |
| 15 | The credential rotation cannot be done by any agent |
| 16, 17 | The normalization decision is Josh's and must survive unresolved |
| 18, 19 | The bar for done is stated and checkable, including what the report covers |

## Common ways this case is failed

The handoff leads with step 4 and mentions `candidates.py` later as a detail, so
the next agent starts on the engine and hits the stub. The `rapidfuzz` dead end
is dropped as "history", and gets reintroduced. The protected file is described
as "avoid editing `rates.py`" with no mechanism, so the agent tries anyway and
burns a turn on a permission denial it could have planned around. The
normalization question is silently resolved in favour of NFKC because it is the
more defensible answer.
