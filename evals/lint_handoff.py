#!/usr/bin/env python3
"""Structural checks for a handoff document produced by the `handoff` skill.

Checks only what can be decided mechanically: the sections and their order, the
plain-prose rule, and a few cheap proxies for specificity. Substance is graded
against evals/rubric.md by a model. This catches the regressions that don't need
one, and it catches them in a tenth of a second.

Usage:
    python3 evals/lint_handoff.py handoff.md [more.md ...]

Exit status is 1 if any check FAILs, 0 otherwise. WARNs never fail the run; they
mark things worth a human look.
"""

import re
import sys

SECTIONS = [
    "What you are picking up:",
    "Read first:",
    "State you inherit:",
    "Your scope:",
    "Standing constraints:",
    "Open questions:",
    "Definition of done:",
]

# A handoff that names nothing the next agent can paste has failed at its job,
# so at least one of these has to appear somewhere in the document.
CONCRETE = [
    re.compile(r"[\w./-]+\.(?:md|py|js|jsx|ts|tsx|json|ya?ml|toml|sh|go|rs|rb|sql|txt)\b"),
    re.compile(r"\b[0-9a-f]{7,40}\b"),          # commit SHA
    re.compile(r"(?:^|\s)[\w-]+/[\w./-]+"),     # a path with a directory in it
]

# The old format's fingerprints. Any of these means it drifted back into writing
# a recap for the user instead of a briefing for the next agent.
RECAP_PHRASES = [
    "this is for",
    "what we covered",
    "in this session we",
    "during this session",
    "the user asked",
    "we discussed",
]

MARKDOWN = [
    (re.compile(r"^\s{0,3}#{1,6}\s"), "markdown header"),
    (re.compile(r"^\s*[-*+]\s+\S"), "bullet marker"),
    (re.compile(r"^\s*\d+[.)]\s+\S"), "numbered list item"),
    (re.compile(r"\*\*[^*\n]+\*\*"), "bold markup"),
    (re.compile(r"^\s*\|.*\|"), "table row"),
]

MIN_WORDS = 250


def find_sections(lines):
    """Map each section label to the line it starts on, or None if absent."""
    found = {}
    for label in SECTIONS:
        for i, line in enumerate(lines):
            if line.strip() == label or line.strip().startswith(label):
                found.setdefault(label, i)
    return found


def section_body(lines, found, label):
    start = found.get(label)
    if start is None:
        return ""
    later = [i for lbl, i in found.items() if i > start]
    end = min(later) if later else len(lines)
    return "\n".join(lines[start + 1 : end]).strip()


def check(text):
    """Yield (level, line_no_or_None, message). line_no is 1-indexed."""
    lines = text.splitlines()
    found = find_sections(lines)

    missing = [s for s in SECTIONS if s not in found]
    for label in missing:
        yield "FAIL", None, f"section missing: {label!r}"

    present = [(found[s], s) for s in SECTIONS if s in found]
    order = [s for _, s in sorted(present)]
    expected_order = [s for s in SECTIONS if s in found]
    if order != expected_order:
        yield "FAIL", None, f"sections out of order: got {' -> '.join(order)}"

    # No preamble: the document opens on the first section.
    for i, line in enumerate(lines):
        if line.strip():
            if not line.strip().startswith(SECTIONS[0]):
                yield "FAIL", i + 1, f"preamble before the first section: {line.strip()[:60]!r}"
            break

    for i, line in enumerate(lines):
        if line.strip() in SECTIONS:
            continue
        for pattern, what in MARKDOWN:
            if pattern.search(line):
                yield "FAIL", i + 1, f"{what} — output must be plain prose"
                break

    # "Standing constraints" is required, and required means it says something.
    # One honest sentence that there are none is a pass; an empty section is not.
    if "Standing constraints:" in found:
        body = section_body(lines, found, "Standing constraints:")
        if len(body) < 40:
            yield "FAIL", found["Standing constraints:"] + 1, (
                "'Standing constraints:' is empty or near-empty; if the session "
                "produced none, say so in a sentence"
            )

    if not any(p.search(text) for p in CONCRETE):
        yield "FAIL", None, (
            "no file path, command, or SHA anywhere; the next agent has nothing to open"
        )

    if "Read first:" in found:
        body = section_body(lines, found, "Read first:")
        if not any(p.search(body) for p in CONCRETE):
            yield "FAIL", found["Read first:"] + 1, "'Read first:' names nothing to read"

    lowered = text.lower()
    for phrase in RECAP_PHRASES:
        if phrase in lowered:
            yield "WARN", None, (
                f"recap phrasing {phrase!r} — write to the next agent, not about the session"
            )

    words = len(text.split())
    if words < MIN_WORDS:
        yield "WARN", None, f"{words} words; thin enough to be worth re-reading for omissions"

    if " you " not in lowered and not lowered.startswith("you "):
        yield "WARN", None, "no second-person address; a handoff is written to whoever picks it up"


def main(argv):
    paths = argv[1:]
    if not paths:
        print(__doc__.strip().splitlines()[0])
        print("\nusage: python3 evals/lint_handoff.py handoff.md [more.md ...]")
        return 2

    failed = False
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"{path}: cannot read: {exc}")
            failed = True
            continue

        results = list(check(text))
        fails = [r for r in results if r[0] == "FAIL"]
        warns = [r for r in results if r[0] == "WARN"]

        status = "FAIL" if fails else "PASS"
        print(f"{status} {path} ({len(fails)} failed, {len(warns)} warned)")
        for level, line_no, message in results:
            where = f"line {line_no}: " if line_no else ""
            print(f"  {level}: {where}{message}")
        if fails:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
