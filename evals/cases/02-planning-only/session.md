# Case 02 — planning only, no code state

A synthetic session record. Paste this into a fresh chat as the context, then ask
for a handoff (`.cn`).

This is the degradation case. Almost nothing happened that a handoff usually
carries: no commits, no tests, no constraints, no blockers. The format has to
stay honest under that instead of padding seven sections out to look complete.

---

Project `atlas`, a personal mapping side project.

**What happened this session.** Josh came back from a weekend of using the build
on his phone with nine notes. I added all nine to the triage section of
`_memory/basicTruths/theBacklog.md`, then reorganized that section into priority
tiers with his approval.

The tiering was grounded in the current epic state in
`_memory/currentState/currentEpic.md`: the offline tile cache is the open epic,
and six of the nine notes are about behaviour when the cache is cold, which is
what the epic's kill criterion turns on.

**The agreed tiers.** Tier 1 is cold cache correctness as one pass: the map
should not render a blank grid while tiles are fetching, the retry on a failed
tile fetch is far too aggressive, and the cache size setting in the UI does not
survive a restart. Tier 2 is display polish, deliberately not specified further
this session. Tier 3 is the route planner, which Josh said out loud he may cut
entirely rather than build.

**No code was written.** Nothing was committed. No tests were run. Tier 1 has not
been started, and nobody has looked at whether the three tier 1 items are one
change or three.

**Nothing was ruled out** and no constraint came up. Normal project rules apply
and they are in `AGENTS.md`; there is nothing special about this work.

**Open.** Whether tier 3 gets built at all is genuinely undecided — Josh raised
cutting it and did not settle it. Not urgent, but it should not quietly become a
commitment just because it is written in a backlog file.
