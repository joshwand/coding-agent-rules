# Case 02 — what the handoff must carry

Case level assertions, checked alongside `../../rubric.md`.

## Must appear

- The tiering is agreed and Josh approved it.
- `_memory/basicTruths/theBacklog.md` holds the tiers and is where to look.
- `_memory/currentState/currentEpic.md` for the offline tile cache epic.
- The three tier 1 items, named: blank grid while tiles fetch, over-aggressive
  retry on failed fetch, cache size setting not surviving restart.
- No code written, nothing committed, no tests run — stated plainly, not implied
  by omission.
- Nobody has checked whether the three tier 1 items are one change or three.
  This is the first real question the next agent hits.

## Must be presented as open

Whether tier 3 (route planner) gets built at all. Josh raised cutting it and did
not settle it. A handoff that lists it as upcoming work has converted an open
question into a commitment, which fails assertion 16.

## The point of this case

Four of the seven sections have thin material, and this is where a format with
required sections goes wrong. Grade hard on assertion 20 (no filler).

- **Standing constraints** must be one honest sentence saying none came up beyond
  `AGENTS.md`. Inventing plausible constraints fails assertion 5. Dropping the
  section fails the linter. Padding it fails 20.
- **State you inherit** must say the absence out loud. "No code was written" is
  load-bearing here: the next agent should not go looking for a branch.
- **Definition of done** has to be invented for the next stretch rather than
  recalled, because the session never set one. Scoping it to the tier 1 pass is
  right; a criterion the session cannot support is assertion 5 again.

A good handoff for this session is short. Under the old 200 to 400 word rule
this case scored fine and case 01 could not — which is roughly the argument for
dropping the cap.

## Common ways this case is failed

Standing constraints gets filled with generic advice about being careful with the
cache. The handoff reads as a summary of the tiering conversation rather than an
instruction to go do tier 1. Tier 3 appears in "Your scope" as later work. The
open question about whether tier 1 is one change or three — the actual first
thing to determine — is missing entirely.
