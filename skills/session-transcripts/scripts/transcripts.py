#!/usr/bin/env python3
"""Read and search Claude Code session transcripts stored under ~/.claude/projects/.

Subcommands:
  index    list sessions with metadata (fast: does not parse whole files)
  search   full-text search across sessions, returns compact hits
  show     render one session as readable markdown
  schema   report the JSONL shapes actually present on this machine

Everything is designed to keep output small. Raw transcripts contain full file
contents and command output; dumping one into a context window is both wasteful
and a way to leak whatever a tool happened to read.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------


def config_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude"))


def projects_dir() -> Path:
    return config_dir() / "projects"


def session_files():
    """Yield (project_dir, jsonl_path) for every top-level session transcript.

    Subagent transcripts live in <session>/subagents/ and are skipped unless
    a path to one is passed explicitly.
    """
    root = projects_dir()
    if not root.is_dir():
        return
    for pdir in sorted(root.iterdir()):
        if not pdir.is_dir():
            continue
        for f in sorted(pdir.glob("*.jsonl")):
            yield pdir, f


def real_cwd(path: Path, limit: int = 40) -> str | None:
    """The project's actual working directory, read from the transcript.

    The directory name is the absolute path with separators replaced by dashes,
    which is lossy: a path containing dashes cannot be reversed reliably. The
    cwd recorded inside the file is authoritative.
    """
    for i, (_, e) in enumerate(iter_entries(path)):
        if e.get("cwd"):
            return str(e["cwd"])
        if i >= limit:
            break
    return None


def matches_project(pdir: Path, path: Path, needle: str | None) -> bool:
    if not needle:
        return True
    needle = needle.lower()
    if needle in pdir.name.lower():
        return True
    cwd = real_cwd(path)
    return bool(cwd and needle in cwd.lower())


# --------------------------------------------------------------------------
# Redaction
# --------------------------------------------------------------------------

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._\-]{20,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|token|client[_-]?secret)"
               r"\s*[:=]\s*['\"]?([^\s'\"]{8,})"),
    re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
]


def redact(text: str, enabled: bool = True) -> str:
    if not enabled or not text:
        return text
    for pat in SECRET_PATTERNS:
        text = pat.sub(lambda m: m.group(0)[:4] + "[REDACTED]", text)
    return text


# --------------------------------------------------------------------------
# Entry parsing (defensive: the on-disk format is undocumented and drifts)
# --------------------------------------------------------------------------


def entry_role(e: dict) -> str:
    msg = e.get("message")
    if isinstance(msg, dict) and msg.get("role"):
        return str(msg["role"])
    return str(e.get("type") or "unknown")


def block_text(block, include_tools: bool, max_tool_chars: int) -> str:
    if isinstance(block, str):
        return block
    if not isinstance(block, dict):
        return ""
    btype = block.get("type")
    if btype == "text":
        return block.get("text", "") or ""
    if btype == "thinking":
        return block.get("thinking", "") or ""
    if btype == "tool_use":
        if not include_tools:
            return ""
        inp = json.dumps(block.get("input", {}), ensure_ascii=False)
        if len(inp) > max_tool_chars:
            inp = inp[:max_tool_chars] + f"... [+{len(inp) - max_tool_chars} chars]"
        return f"[tool_use {block.get('name', '?')}] {inp}"
    if btype == "tool_result":
        if not include_tools:
            return ""
        content = block.get("content")
        if isinstance(content, list):
            content = "\n".join(block_text(c, include_tools, max_tool_chars) for c in content)
        content = str(content or "")
        if len(content) > max_tool_chars:
            content = content[:max_tool_chars] + f"... [+{len(content) - max_tool_chars} chars]"
        return f"[tool_result] {content}"
    if btype == "image":
        return "[image]"
    return ""


def entry_text(e: dict, include_tools: bool = False, max_tool_chars: int = 500) -> str:
    """Flatten one JSONL entry to plain text."""
    if e.get("type") == "summary":
        return str(e.get("summary") or "")
    msg = e.get("message")
    if isinstance(msg, str):
        return msg
    if not isinstance(msg, dict):
        return ""
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [block_text(b, include_tools, max_tool_chars) for b in content]
        return "\n".join(p for p in parts if p)
    return ""


def parse_ts(value) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def iter_entries(path: Path):
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield lineno, json.loads(line)
            except json.JSONDecodeError:
                continue


def tail_bytes(path: Path, n: int = 65536) -> list[str]:
    size = path.stat().st_size
    with path.open("rb") as fh:
        fh.seek(max(0, size - n))
        data = fh.read()
    return data.decode("utf-8", errors="replace").splitlines()


def count_lines(path: Path) -> int:
    total = 0
    with path.open("rb") as fh:
        while chunk := fh.read(1 << 20):
            total += chunk.count(b"\n")
    return total


# --------------------------------------------------------------------------
# index
# --------------------------------------------------------------------------


def session_meta(pdir: Path, path: Path, head_lines: int = 60) -> dict:
    """Cheap metadata for one session: head scan + tail scan, no full parse."""
    meta = {
        "session_id": path.stem,
        "file": str(path),
        "project_dir": pdir.name,
        "cwd": None,
        "git_branch": None,
        "version": None,
        "summary": None,
        "first_prompt": None,
        "started": None,
        "ended": None,
        "lines": None,
        "size_kb": round(path.stat().st_size / 1024, 1),
    }
    for i, (_, e) in enumerate(iter_entries(path)):
        if i >= head_lines * 5:
            break
        if i >= head_lines and meta["first_prompt"] and meta["started"]:
            break
        meta["cwd"] = meta["cwd"] or e.get("cwd")
        meta["git_branch"] = meta["git_branch"] or e.get("gitBranch")
        meta["version"] = meta["version"] or e.get("version")
        if e.get("type") == "summary" and not meta["summary"]:
            meta["summary"] = e.get("summary")
        ts = e.get("timestamp")
        if ts and not meta["started"]:
            meta["started"] = ts
        if not meta["first_prompt"] and entry_role(e) == "user" and not e.get("isMeta"):
            txt = entry_text(e).strip()
            # skip tool_result-only user entries and slash-command plumbing
            if txt and not txt.startswith("<"):
                meta["first_prompt"] = " ".join(txt.split())[:220]
    for line in reversed(tail_bytes(path)):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("timestamp"):
            meta["ended"] = e["timestamp"]
            break
    if not meta["ended"]:
        meta["ended"] = datetime.fromtimestamp(
            path.stat().st_mtime, tz=timezone.utc
        ).isoformat()
    meta["lines"] = count_lines(path)
    return meta


def cmd_index(args) -> int:
    cutoff = None
    if args.since:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.since)
    rows = []
    for pdir, path in session_files():
        try:
            meta = session_meta(pdir, path)
        except OSError:
            continue
        if not matches_project(pdir, path, args.project):
            continue
        ended = parse_ts(meta["ended"])
        if cutoff and ended and ended < cutoff:
            continue
        if args.grep:
            hay = f"{meta['summary'] or ''} {meta['first_prompt'] or ''}".lower()
            if args.grep.lower() not in hay:
                continue
        rows.append(meta)
    rows.sort(key=lambda m: m["ended"] or "", reverse=True)
    rows = rows[: args.limit]
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    if not rows:
        print("No sessions matched.")
        return 0
    for m in rows:
        when = (m["ended"] or "")[:16].replace("T", " ")
        title = m["summary"] or m["first_prompt"] or "(no prompt found)"
        print(f"{when}  {m['session_id']}")
        print(f"    {redact(title, not args.no_redact)[:150]}")
        print(
            f"    cwd={m['cwd'] or m['project_dir']}"
            f"  branch={m['git_branch'] or '-'}"
            f"  lines={m['lines']}  {m['size_kb']}KB"
        )
    print(f"\n{len(rows)} session(s). Resume one with: claude --resume <session_id>")
    return 0


# --------------------------------------------------------------------------
# search
# --------------------------------------------------------------------------


def cmd_search(args) -> int:
    try:
        pattern = re.compile(args.query, 0 if args.case_sensitive else re.IGNORECASE)
    except re.error as exc:
        print(f"Bad regex: {exc}", file=sys.stderr)
        return 2
    cutoff = None
    if args.since:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.since)

    hits = []
    for pdir, path in session_files():
        if args.session and args.session not in path.stem:
            continue
        if not matches_project(pdir, path, args.project):
            continue
        if cutoff:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                continue
        cwd = None
        per_session = 0
        for lineno, e in iter_entries(path):
            cwd = cwd or e.get("cwd")
            role = entry_role(e)
            if args.role and role != args.role:
                continue
            text = entry_text(e, include_tools=args.tools, max_tool_chars=args.max_chars)
            if not text:
                continue
            m = pattern.search(text)
            if not m:
                continue
            start = max(0, m.start() - args.context)
            end = min(len(text), m.end() + args.context)
            snippet = " ".join(text[start:end].split())
            hits.append(
                {
                    "session_id": path.stem,
                    "file": str(path),
                    "line": lineno,
                    "cwd": cwd or pdir.name,
                    "timestamp": e.get("timestamp"),
                    "role": role,
                    "snippet": redact(snippet, not args.no_redact),
                }
            )
            per_session += 1
            if per_session >= args.per_session:
                break
        if len(hits) >= args.limit:
            break

    hits.sort(key=lambda h: h["timestamp"] or "", reverse=True)
    hits = hits[: args.limit]
    if args.json:
        print(json.dumps(hits, indent=2))
        return 0
    if not hits:
        print("No matches. Try a looser pattern, --tools, or a wider --since.")
        return 0
    for h in hits:
        when = (h["timestamp"] or "")[:16].replace("T", " ")
        print(f"{when}  {h['role']:<9} {h['session_id']}  (line {h['line']})")
        print(f"    {h['cwd']}")
        print(f"    …{h['snippet']}…\n")
    print(f"{len(hits)} match(es). Read one with: show --session <session_id>")
    return 0


# --------------------------------------------------------------------------
# show
# --------------------------------------------------------------------------


def resolve_session(spec: str) -> Path | None:
    p = Path(spec)
    if p.is_file():
        return p
    matches = [f for _, f in session_files() if spec in f.stem]
    if not matches:
        return None
    matches.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return matches[0]


def active_branch(entries: list[dict]) -> list[dict]:
    """Return only the entries on the surviving conversation branch.

    Editing a message or rewinding leaves the abandoned turns in the file.
    parentUuid chains let us walk back from the newest leaf to the root.
    """
    by_uuid = {e["uuid"]: e for e in entries if e.get("uuid")}
    if not by_uuid:
        return entries
    referenced = {e.get("parentUuid") for e in entries if e.get("parentUuid")}
    leaves = [e for u, e in by_uuid.items() if u not in referenced]
    if not leaves:
        return entries
    leaves.sort(key=lambda e: e.get("timestamp") or "")
    chain, cur, seen = [], leaves[-1], set()
    while cur and cur.get("uuid") not in seen:
        seen.add(cur.get("uuid"))
        chain.append(cur)
        cur = by_uuid.get(cur.get("parentUuid"))
    chain.reverse()
    return chain


def cmd_show(args) -> int:
    path = resolve_session(args.session)
    if not path:
        print(f"No session matching {args.session!r}", file=sys.stderr)
        return 1

    entries = [e for _, e in iter_entries(path)]
    summaries = [e.get("summary") for e in entries if e.get("type") == "summary"]
    convo = [e for e in entries if e.get("type") in ("user", "assistant")]
    if not args.all_branches:
        convo = active_branch(convo)
    if args.skip_sidechains:
        convo = [e for e in convo if not e.get("isSidechain")]
    if args.role:
        convo = [e for e in convo if entry_role(e) == args.role]
    if args.last:
        convo = convo[-args.last :]

    meta = next((e for e in entries if e.get("cwd")), {})
    print(f"# Session {path.stem}")
    print(f"cwd: {meta.get('cwd', '?')}   branch: {meta.get('gitBranch', '-')}"
          f"   cli: {meta.get('version', '?')}")
    if summaries:
        print(f"summary: {summaries[0]}")
    print(f"showing {len(convo)} of {len(entries)} entries\n")

    for e in convo:
        role = entry_role(e)
        text = entry_text(e, include_tools=not args.no_tools, max_tool_chars=args.max_tool_chars)
        text = text.strip()
        if not text:
            continue
        if args.max_chars and len(text) > args.max_chars:
            text = text[: args.max_chars] + f"\n… [+{len(text) - args.max_chars} chars truncated]"
        when = (e.get("timestamp") or "")[:19].replace("T", " ")
        tag = "sidechain " if e.get("isSidechain") else ""
        print(f"## {tag}{role} — {when}")
        print(redact(text, not args.no_redact))
        print()
    return 0


# --------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------


def cmd_schema(args) -> int:
    """Report the entry types, keys, and content-block types actually on disk.

    Run this first if parsing looks wrong: the transcript format is internal to
    Claude Code and changes between versions.
    """
    files = [f for _, f in session_files()]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    files = files[: args.files]
    if not files:
        print(f"No transcripts under {projects_dir()}")
        return 1

    types: dict[str, int] = {}
    keys: dict[str, int] = {}
    blocks: dict[str, int] = {}
    versions: set[str] = set()
    scanned = 0
    for path in files:
        for i, (_, e) in enumerate(iter_entries(path)):
            if i >= args.lines:
                break
            scanned += 1
            types[str(e.get("type"))] = types.get(str(e.get("type")), 0) + 1
            for k in e:
                keys[k] = keys.get(k, 0) + 1
            if e.get("version"):
                versions.add(str(e["version"]))
            msg = e.get("message")
            if isinstance(msg, dict) and isinstance(msg.get("content"), list):
                for b in msg["content"]:
                    if isinstance(b, dict):
                        t = str(b.get("type"))
                        blocks[t] = blocks.get(t, 0) + 1

    print(f"config dir: {config_dir()}")
    print(f"scanned {scanned} entries across {len(files)} file(s)")
    print(f"claude code versions seen: {', '.join(sorted(versions)) or 'unknown'}\n")
    for label, d in (("entry types", types), ("top-level keys", keys),
                     ("content block types", blocks)):
        print(label + ":")
        for k, v in sorted(d.items(), key=lambda kv: -kv[1]):
            print(f"  {k:<24} {v}")
        print()
    return 0


# --------------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(prog="transcripts.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    common = dict(no_redact=False)

    pi = sub.add_parser("index", help="list sessions with metadata")
    pi.add_argument("--project", help="substring of the project path or dir name")
    pi.add_argument("--since", type=float, metavar="DAYS", help="only sessions touched in the last N days")
    pi.add_argument("--grep", help="substring filter on summary/first prompt")
    pi.add_argument("--limit", type=int, default=25)
    pi.add_argument("--json", action="store_true")
    pi.add_argument("--no-redact", action="store_true")
    pi.set_defaults(func=cmd_index)

    ps = sub.add_parser("search", help="full-text search across sessions")
    ps.add_argument("query", help="regex (case-insensitive by default)")
    ps.add_argument("--project", help="substring of the project path or dir name")
    ps.add_argument("--session", help="restrict to sessions whose id contains this")
    ps.add_argument("--since", type=float, metavar="DAYS")
    ps.add_argument("--role", choices=["user", "assistant"])
    ps.add_argument("--tools", action="store_true", help="also search tool calls and results")
    ps.add_argument("--context", type=int, default=160, help="chars of context each side")
    ps.add_argument("--max-chars", type=int, default=2000, help="cap per tool block when --tools")
    ps.add_argument("--per-session", type=int, default=3, help="max hits per session")
    ps.add_argument("--limit", type=int, default=20)
    ps.add_argument("--case-sensitive", action="store_true")
    ps.add_argument("--json", action="store_true")
    ps.add_argument("--no-redact", action="store_true")
    ps.set_defaults(func=cmd_search)

    ph = sub.add_parser("show", help="render one session as markdown")
    ph.add_argument("--session", required=True, help="session id, prefix, or file path")
    ph.add_argument("--last", type=int, help="only the last N turns")
    ph.add_argument("--role", choices=["user", "assistant"])
    ph.add_argument("--no-tools", action="store_true", help="drop tool calls and results")
    ph.add_argument("--max-tool-chars", type=int, default=400)
    ph.add_argument("--max-chars", type=int, default=4000, help="cap per turn")
    ph.add_argument("--all-branches", action="store_true",
                    help="include abandoned branches from edits and rewinds")
    ph.add_argument("--skip-sidechains", action="store_true", help="drop subagent turns")
    ph.add_argument("--no-redact", action="store_true")
    ph.set_defaults(func=cmd_show)

    pc = sub.add_parser("schema", help="report the JSONL shapes present on this machine")
    pc.add_argument("--files", type=int, default=5)
    pc.add_argument("--lines", type=int, default=400, help="entries to sample per file")
    pc.set_defaults(func=cmd_schema)

    args = p.parse_args()
    for k, v in common.items():
        if not hasattr(args, k):
            setattr(args, k, v)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
