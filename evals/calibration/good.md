What you are picking up:
You are continuing a six step rewrite of the reconciler in tessera, a Python CLI that reconciles invoices against a ledger. Steps 1 through 3 are done and committed at 4c1f9ab. Josh has authorized step 4, and only step 4.

Read first:
Read _memory/knowledgeBase/designs/ReconcilerRewrite.md before anything else. It is the plan, step 4 is your scope within it, and it is authoritative over this briefing wherever the two disagree. Then read _memory/currentState/currentTaskState.md for where things stood at the end of the last session. Then skim tessera/match/candidates.py and tessera/match/engine.py, in that order, because the first one blocks the second.

State you inherit:
Steps 1 through 3 are complete and committed together at 4c1f9ab. The suite is 214 passing, 0 skipped, run with .venv/bin/pytest -q.

tessera/match/candidates.py is half built, and it blocks everything else. The scoring function is written and tested; the tie breaker below it is a TODO stub that returns the first candidate. Step 4 consumes that function, so finishing the tie breaker comes before any work on the engine.

tests/test_fuzzy.py::test_unicode_names is xfail deliberately, pending the normalization decision below. It is not a regression, and it must not be made to pass by changing the assertion.

Your scope:
Finish the tie breaker in tessera/match/candidates.py first. Then build the matching engine at tessera/match/engine.py as step 4 of the plan describes, with tests for both.

Do not start step 5, and do not commit; Josh reviews before anything lands. Keep _memory/currentState/currentTaskState.md current as you go. If step 4 turns out to need a change in a protected file, stop and propose it rather than working around it, as described below.

Standing constraints:
tessera/config/rates.py is owner edited. Write is permission denied on it, and a pre-commit hook rejects any commit that touches it. When step 2 needed a change there, the change went into tessera/config/rates_proposed.py alongside it and Josh applied it by hand. Do the same rather than trying to edit the original.

Do not reintroduce rapidfuzz. Step 2 used it for the matcher and it came out again because it pulls a C extension that breaks the Alpine container build. That failure does not surface until the image builds in CI, so it looks harmless locally. Stdlib difflib is the decision.

The production reconciliation run needs a credential rotated in the bank's web console. There is no API for it, and you have neither a browser nor the credentials. If step 4 gets far enough to want a real run, prepare everything up to the run, write the exact steps Josh needs to click into _memory/currentState/currentTaskState.md, and stop there.

Open questions:
Unicode name normalization is undecided, and it is Josh's call rather than yours. NFKC is more correct and keeps names readable in the reconciliation output. Stripping diacritics before comparing matches more aggressively, which is closer to what reconciliation actually wants, but produces output a human cannot check by eye. This decides tests/test_fuzzy.py::test_unicode_names, so leave that test xfail until he chooses.

Definition of done:
The tie breaker in tessera/match/candidates.py is finished and tested. Step 4 is implemented as the plan describes, with tests. The full suite is green, with the unicode test still xfail. _memory/currentState/currentTaskState.md is updated well enough that a fresh agent could take step 5 from it alone. Your final report to Josh covers what was built, the test count, any deviations from the plan, and anything needing his decision. Then stop.
