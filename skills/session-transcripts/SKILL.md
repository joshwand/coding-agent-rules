---
name: session-transcripts
description: Search and read past Claude Code sessions stored as JSONL under ~/.claude/projects/. Use this whenever the user refers to earlier work you have no record of — "what did we decide about X", "we fixed this last week", "find the session where I set up the migrations", "why did we drop that approach", "summarize what I worked on yesterday", "which session touched this file" — or asks to recover a lost command, prompt, error, or decision from a previous conversation. Also use it before answering "we already talked about this" with a guess. Prefer this over grepping ~/.claude by hand; raw transcripts are enormous and contain secrets.
---

# Working with past session transcripts

Claude Code writes every session to disk. Those files are the only record of what
was decided, tried, and abandoned before this session started. Reading them well
is mostly about extracting the few hundred relevant tokens from a few hundred
megabytes without dumping credentials into context along the way.

## Layout

Under `~/.claude/` (or `$CLAUDE_CONFIG_DIR` if set):

| Path | Contents |
| --- | --- |
| `projects/<encoded-path>/<session-id>.jsonl` | Full transcript: every message, tool call, tool result |
| `projects/<encoded-path>/<session-id>/subagents/` | Subagent transcripts for that session |
| `projects/<encoded-path>/<session-id>/tool-results/` | Large tool outputs spilled to separate files |
| `projects/<encoded-path>/memory/` | Auto memory: Claude's own notes, not conversation |
| `history.jsonl` | Every prompt the user typed, with timestamp and project path |

The directory name is the project's absolute path with separators replaced by
dashes. That encoding is lossy — a project path containing dashes cannot be
reversed — so treat the `cwd` field recorded inside the file as authoritative.

## Never read a transcript file directly

A single session routinely runs to tens of megabytes: full file contents from
every read, complete stdout from every command. Transcripts are also plaintext
and unencrypted, so anything a tool touched is sitting in there verbatim,
including `.env` contents and printed credentials. `cat`, `head`, and bare `grep`
on these files burn context and leak secrets.

Use `scripts/transcripts.py` instead. It bounds output, strips common secret
shapes by default, and understands the entry structure.

## Workflow

Locate the session, then read only the part that matters.

**1. Find candidates.** Search by content when the user remembers what was said:

```bash
python3 scripts/transcripts.py search "connection pool" --since 14
python3 scripts/transcripts.py search "rate.?limit" --project myapp --role user
python3 scripts/transcripts.py search "ALTER TABLE" --tools --limit 10
```

Or list by recency when they remember when:

```bash
python3 scripts/transcripts.py index --since 3
python3 scripts/transcripts.py index --project myapp --grep migration
```

`--tools` extends the search to tool calls and results, which is how you find a
command that was run or a file that was edited. It is off by default because it
multiplies the searchable text by roughly ten.

**2. Read the session.** Start narrow and widen only if needed:

```bash
python3 scripts/transcripts.py show --session a1b2c3d4 --no-tools
python3 scripts/transcripts.py show --session a1b2c3d4 --last 6
python3 scripts/transcripts.py show --session a1b2c3d4 --role user
```

A session id prefix is enough. `--no-tools` gives the conversation alone, which
is usually what answers "what did we decide". Add tools back when the question is
"what did we actually run".

**3. Report with provenance.** Say which session and roughly when, and separate
what the user said from what you proposed. A suggestion you made in March is not
a decision they made, and transcripts contain plenty of ideas that were floated
and dropped.

Offer `claude --resume <session-id>` when they want the full context back rather
than a summary.

## Things that will mislead you

**Abandoned branches.** Editing a message or rewinding leaves the discarded turns
in the file. `show` reconstructs the surviving branch by walking `parentUuid`
back from the newest leaf, so what you see is what actually happened. Pass
`--all-branches` when the user specifically wants the road not taken — "what was
that other approach you suggested before I rewound?"

**Subagent turns.** Entries with `isSidechain: true` are subagent work, not the
main thread. Recent versions put them in a separate `subagents/` directory
instead. Use `--skip-sidechains` when they add noise.

**Truncated tool output.** Very large results are written to `tool-results/`
rather than inlined, so a tool result in the transcript may be a pointer. If a
result looks suspiciously short, check that directory.

**The 30-day sweep.** Transcripts older than `cleanupPeriodDays` (default 30) are
deleted at startup. If a search finds nothing from months ago, the session is
probably gone rather than mis-matched. Say so instead of hunting.

**Format drift.** The JSONL schema is internal to Claude Code and changes between
versions. If parsing looks wrong, run `python3 scripts/transcripts.py schema` —
it reports the entry types, keys, and content-block types actually present on
this machine. Read `references/format.md` for the field-by-field breakdown and
raw `jq` recipes if you need to go beyond what the script does.

## Prompt-only recall

When the user wants a command or prompt they typed rather than a whole
conversation, `~/.claude/history.jsonl` is smaller and survives the 30-day sweep.
One JSON object per prompt, carrying the prompt text, a timestamp, and the
project path. Field names vary by version, so print one line before filtering:

```bash
tail -1 ~/.claude/history.jsonl | python3 -m json.tool
grep -i "docker compose" ~/.claude/history.jsonl | tail -5 | python3 -m json.tool --json-lines
```

## Privacy

These are the user's own local files, so reading them on request is fine. Two
limits worth keeping: don't echo secrets back into the conversation just because
redaction is imperfect, and don't go trawling through other projects' sessions
when the question was scoped to this one.
