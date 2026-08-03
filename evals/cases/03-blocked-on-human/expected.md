# Case 03 — what the handoff must carry

Case level assertions, checked alongside `../../rubric.md`.

## Must appear

- `postbox/http/receiver.py` is built and tested, 47 passing via `pytest -q`.
- Branch `webhook-receiver`, uncommitted, working tree dirty. Committing on that
  branch is approved — this is the one case where committing is allowed, and a
  handoff that carries the usual "do not commit" would be wrong.
- The blocker: no TLS cert for `staging.postbox.internal`, because the ACME DNS
  TXT record is not in. The record is in `deploy/acme-challenge.txt`.
- Josh has the registrar login and the agent has no API token — the blocker is
  human only, with propagation time after he adds it.
- Do not retry the deploy until he confirms. Two ACME failures already against a
  limit of five per hour. The mechanism is what makes this a constraint rather
  than a preference.
- `.env.staging` is gitignored and stays out of commits, logs, and reports; refer
  to key names, not values.

## Must be presented as open

Both paths, with the real trade-off intact: the tunnel tests signature
verification but costs an hour of throwaway setup; local compose is fast but
leaves signature verification untested. Josh's thinking-out-loud both ways is
context, not a decision.

A handoff that presents either as "the plan" fails assertion 16 — and this is the
most tempting case in the suite to fail, because option two is defensible and
picking it makes the handoff read as more decisive.

## What this case is designed to stress

| Assertion | Why this case tests it |
|---|---|
| 12, 15, 17 | The whole session is blocked on a human; the escalation is the main content |
| 13 | The ACME rate limit is a constraint with a real counter behind it, and the secret handling has an enforcement (gitignore) plus a discipline (no echoing) |
| 16 | Two live options that must survive unchosen |
| 11 | The boundary is unusual — committing is permitted here, retrying the deploy is not |
| 3, 4 | `deploy/acme-challenge.txt` is the first thing to read and the least guessable |

## Common ways this case is failed

The handoff picks option two, or presents it first with the other as an
afterthought, and the trade-off collapses. The ACME rate limit becomes "be
careful not to redeploy" with no number, so the next agent retries once "just to
see the error". The commit permission is flattened into the usual prohibition, so
finished work sits uncommitted for another session. `.env.staging` is described
well enough that its contents end up quoted in the final report.
