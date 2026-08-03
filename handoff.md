What you are picking up:
You are wiring the eval suite for the handoff skill up to Inspect AI, the UK AISI evaluation framework, against the three cases that already exist. Josh chose Inspect over the alternatives and approved this scope; the suite itself is written and open as draft PR #4 on branch handoff-evals.

Read first:
Read evals/README.md first, because it describes how the suite is meant to run and is authoritative over this briefing wherever the two disagree. Then read evals/rubric.md, which holds the 21 assertions you are turning into a scorer, and evals/calibration/README.md, which states the thresholds the grader has to reproduce. Then read one full case, evals/cases/01-midstream-implementation/session.md together with its expected.md, to see the input and output shape before you write any code. Then read evals/lint_handoff.py, because you are reusing it rather than reimplementing it. Read AGENTS.md for the working agreements; NoPlaceholdersWithoutApproval applies directly to scorers. Inspect's documentation is linked from https://github.com/UKGovernmentBEIS/inspect_ai and is authoritative over anything this file says about its API, which is described here from a summary rather than from having used it.

State you inherit:
The branch is handoff-evals at ba7da9b, open as draft PR #4 with base handoff-skill. It retargets to main automatically when PR #2 merges. PR #2 carries the skill itself, is three files, and is MERGEABLE and CLEAN against main; it is not yours to touch.

Under evals/ there is README.md, rubric.md, lint_handoff.py, three cases each holding session.md and expected.md, a calibration pair, and a baseline.

lint_handoff.py is finished and verified. It passes evals/calibration/good.md with 0 failed and 0 warned, and fails evals/calibration/bad.md with 9 failed and 3 warned. It exits 0 on pass, 1 on failure or an unreadable file, and 2 when called with no arguments. Its check() function yields tuples of level, line number, and message, which is the interface to build the deterministic scorer on.

The rubric has never been run end to end. No handoff has been generated from a case and graded. The thresholds in evals/calibration/README.md, good at 18 or above and bad at 10 or below, are guesses that have never been tested against a real grader.

evals/baseline/SKILL.md is the pre-rewrite skill, the control arm for an A/B. Read evals/baseline/README.md before using it: it was recovered from a session transcript rather than from version control, because its only copy was overwritten, so it is a high-confidence reconstruction and not a git-attested artifact.

Python is 3.14.3. There is a .venv in the main working copy at the repository root, untracked. There is no ANTHROPIC_API_KEY in the environment.

Your scope:
Add Inspect AI as a dependency scoped to the eval, and build one Task whose dataset is the three cases, whose solver generates a handoff with the skill text as the system prompt and the case session.md as the user message, and which carries two scorers. The first is deterministic and wraps lint_handoff.check(); import it, do not rewrite it. The second is model graded against the 21 assertions in rubric.md, using forced structured output rather than parsing prose, and it must report per-assertion results rather than only a total, because the per-assertion failure rate is the diagnostic the suite exists to produce.

Then calibrate before trusting anything: score evals/calibration/good.md and evals/calibration/bad.md through the rubric scorer and record the actual numbers. If they contradict the 18 and 10 thresholds, correcting those numbers in evals/calibration/README.md and evals/README.md with the evidence is in scope and wanted. Then run the three cases and report per-assertion failure rates with bootstrap confidence intervals, which Inspect provides natively.

Stop there. Do not build the pairwise or A/B arm, do not write new cases, do not edit skills/handoff/SKILL.md or anything in PR #2, and do not add dependencies anywhere outside the eval. Commit on handoff-evals only, and leave PR #4 in draft unless Josh says otherwise.

Standing constraints:
There is no ANTHROPIC_API_KEY in the environment and you cannot obtain one. Inspect calls the API directly, so nothing runs until Josh supplies a key. Prepare everything up to that point, and if you reach it, say exactly what you need and stop rather than working around it.

Do not force-push handoff-skill or handoff-evals, and do not push to main. Both branches are pushed and under review; PR #2 deliberately carries an add-then-remove commit pair rather than a rewritten history for this reason.

Four approaches were considered and ruled out, and reopening one needs an argument rather than a fresh look. promptfoo fits the prompt-matrix shape best but OpenAI agreed to acquire it in 2026. DeepEval's metric catalogue is RAG-shaped and pulls toward a hosted dashboard. The hosted platforms, Braintrust and LangSmith and Weave, add an account dependency. A hand-rolled runner shelling out to claude -p was rejected on methodology: Claude Code's own system prompt sits above every generation as an uncontrolled variable, and a measured trivial call cost 0.11 dollars.

Keep the dependency inside the eval. The repository README records that the installer was deliberately dropped and the always-on rules carry no tooling.

Open questions:
Whether the A/B against evals/baseline/SKILL.md is in scope at all is Josh's call. He was interested but approved only the three-case wiring, and the baseline is preserved so the option stays open.

Three cases cannot support a claim that the rewrite is better; a paired A/B at that size will produce a confidence interval on the difference that straddles zero. Josh has been told this. Whether to grow the set to fifteen or thirty cases before or after the harness is his decision, not yours.

The generator model, the judge model, the temperature, and the number of samples per case are all undecided. Whether the judge should be a different model from the generator, to limit self-preference bias, is worth raising with him rather than settling quietly.

Definition of done:
Inspect runs end to end across all three cases and produces per-assertion results and a viewable log. The deterministic scorer calls lint_handoff.py rather than duplicating it. A calibration run is recorded with real numbers, and the thresholds are either confirmed or corrected with the evidence attached. evals/README.md describes the runner as the primary path, with the manual procedure either kept or removed as a deliberate choice rather than left stale beside it. The work is committed on handoff-evals and pushed, and PR #4's description says what is now verified and what still is not.

Report back with the commands you ran, the actual calibration numbers, which assertions failed and how often, anything you changed about the thresholds and why, the cost and wall-clock of a full run, and whatever needs Josh's decision. Then stop.
