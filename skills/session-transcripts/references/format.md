# Transcript JSONL format

Read this when `transcripts.py` isn't enough — a field it ignores, a one-off
aggregation, or a version whose shape has drifted. Verify against the machine
first with `python3 scripts/transcripts.py schema`; this format is internal to
Claude Code and carries no compatibility guarantee.

## Contents

- [File layout](#file-layout)
- [Entry shapes](#entry-shapes)
- [Message content blocks](#message-content-blocks)
- [Threading and branches](#threading-and-branches)
- [jq recipes](#jq-recipes)

## File layout

One JSON object per line, appended as the session progresses. Line order is
append order, not conversation order — see threading below.

```
~/.claude/projects/
  -Users-josh-work-myapp/                     # cwd with / replaced by -
    3f9c….jsonl                               # session transcript
    3f9c…/subagents/*.jsonl                   # subagent transcripts
    3f9c…/tool-results/*                      # spilled large tool output
    memory/MEMORY.md                          # auto memory, not conversation
```

On Windows the drive colon is also encoded, giving names like `C--Users-josh-…`.

## Entry shapes

Common top-level keys. Not all appear on every entry, and not every version
writes all of them.

| Key | Meaning |
| --- | --- |
| `type` | `user`, `assistant`, `summary`, `system`, and occasional internal types |
| `uuid` | This entry's id |
| `parentUuid` | Previous entry in the thread; `null` at the root |
| `message` | The Anthropic API message object: `{role, content, ...}` |
| `timestamp` | ISO 8601, UTC |
| `sessionId` | Matches the filename stem |
| `cwd` | Working directory — authoritative project path |
| `gitBranch` | Branch at the time of the entry |
| `version` | Claude Code version that wrote it |
| `isSidechain` | `true` for subagent turns interleaved in the main file |
| `isMeta` | Housekeeping entries, not user-authored text |
| `toolUseResult` | Structured result payload attached to some tool results |

A `summary` entry carries `summary` (the auto-generated session title) and
`leafUuid` (the branch tip it describes). Resuming a session appends a new
summary, so a file can hold several.

## Message content blocks

`message.content` is either a plain string or a list of blocks:

| Block `type` | Payload |
| --- | --- |
| `text` | `text` |
| `thinking` | `thinking` |
| `tool_use` | `name`, `input`, `id` |
| `tool_result` | `tool_use_id`, `content` (string or nested blocks), `is_error` |
| `image` | `source.data` — base64, often megabytes; never print it |

Tool results arrive as `user` entries. Filtering to `role == "user"` to find what
the human typed will pull in every tool result unless you also drop entries whose
content is only `tool_result` blocks.

## Threading and branches

`parentUuid` forms a tree, not a list. Editing a prompt or rewinding starts a new
child from an earlier node and leaves the old subtree in the file. Reconstruct
the live conversation by finding uuids that no entry claims as a parent (the
leaves), taking the newest, and walking parents back to the root.

Consequences worth remembering:

- Counting lines overstates conversation length on any session that was rewound.
- Two adjacent lines may belong to different branches.
- The last line in the file is on the live branch, but earlier lines may not be.

## jq recipes

Conversation text only, no tools:

```bash
jq -r 'select(.type=="user" or .type=="assistant")
       | .message.content
       | if type=="string" then . else (map(select(.type=="text").text)|join("\n")) end
       | select(. != "")' session.jsonl
```

Every command run in a session:

```bash
jq -r 'select(.message.content|type=="array")
       | .message.content[]
       | select(.type=="tool_use" and .name=="Bash")
       | .input.command' session.jsonl
```

Files touched, deduplicated:

```bash
jq -r 'select(.message.content|type=="array")
       | .message.content[]
       | select(.type=="tool_use" and (.name=="Edit" or .name=="Write"))
       | .input.file_path' session.jsonl | sort -u
```

Session-level metadata without reading the body:

```bash
head -1 session.jsonl | jq '{cwd, gitBranch, version, timestamp}'
```

Prompts across all projects in the last week:

```bash
jq -r 'select(.timestamp > (now - 604800))
       | "\(.project // "?")\t\(.display // .prompt)"' ~/.claude/history.jsonl
```

`history.jsonl` timestamps are epoch seconds in some versions and ISO strings in
others; check one line before filtering on them.
