---
name: handoff
description: Write a standalone briefing that lets a fresh agent continue this work with no access to the current conversation. Use when invoked as .cn or /handoff, when asked for a handoff, a continuation prompt, or a prompt for the next agent, and when a chat has grown too long and the work is moving to a new one.
---

# Handoff

Produce one file that an agent with no memory of this conversation can read and then act on. It gets the repository and `_memory/`; it does not get the chat. Everything it needs that is not already written down somewhere it will read has to be in this file.

This is an instruction to that agent, not a report to me about the session. Write it in the second person, addressed to whoever picks the work up: "you are continuing", "in scope for you first". If a sentence describes the session rather than telling the next agent something it must know or do, cut it.

## Output format

Plain text. No markdown headers, no bullet points, no bold, no dashes as list markers. Complete sentences and paragraphs, with plain section labels followed by a colon and a line break.

The prose rule governs style, not precision. File paths, commands, commit SHAs, test counts, and error strings are reproduced exactly as they appear, never paraphrased or tidied up. Ordering that matters is carried in the sentence ("read X first, then Y"), not in a numbered list.

Use these seven sections, in this order.

**What you are picking up:** One or two sentences. What is being continued, roughly where it stands, and what I have already approved.

**Read first:** The exact paths and commands to load, in the order to load them, each with a short reason. Include the memory load (`.m`) if the project has a `_memory/`. Say which documents are authoritative over the handoff itself, so that where they disagree the agent believes them and not this file.

**State you inherit:** What is true right now, not the story of how it got that way. What is finished and committed, with SHAs. Test counts. What is half-built and at which path. What is known broken, and what is deliberately unfinished. Where a decision's reasoning still matters, attach it to the fact rather than narrating it separately.

**Your scope:** What to do, in order, and explicitly where to stop. Name the boundary: what not to start, what not to commit, what to bring back to me instead of deciding. This is the section that makes a handoff an instruction rather than a suggestion.

**Standing constraints:** What the agent must not do, and what will stop it if it tries: protected or owner-edited paths, permission and hook denials, services or credentials that are off limits, actions it cannot perform itself and has to hand back to me. Include anything already tried and ruled out, so it isn't attempted again. If the session genuinely produced no constraints, say so in one sentence rather than dropping the section.

**Open questions:** What is still undecided, with the options as they stood, and which of them need me specifically rather than a judgment call.

**Definition of done:** Verifiable exit criteria, and what the final report back to me should contain.

## Rules

Ground every sentence in something that actually happened in the conversation or exists in the repository. Do not invent. State established facts flatly and mark anything inferred as an inference.

Point rather than paraphrase. If `AGENTS.md`, a design document, or a memory file already says it, name that file and call it authoritative. Restating it here creates a second copy that will drift from the first.

Be specific enough to act on. Name the file, the command, the error, the decision. A path the next agent cannot paste is a broken handoff.

Match my register. If the session was casual and direct, write that way; if it was precise and technical, match that.

Length is whatever the state and the constraints require, with no filler. Most useful handoffs run four hundred to nine hundred words. A long constraints section is never the thing to cut.

No preamble before the first section and no commentary after the last.

Before saving, read it cold: could an agent with no other context carry out the first action in "Your scope" without asking a single question? Is every file, command, and identifier named? Fix it before writing the file.

## Relationship to memory

`.ts` and `_memory/currentState/` are the durable record of where the work stands, and they belong to the project. A handoff is a one-shot briefing aimed at a specific next step, written to be pasted into a new chat.

They overlap, and the handoff should lean on memory rather than duplicate it: update task state first if it is stale, then have the handoff point at it. What belongs in the handoff and nowhere else is the scope boundary, the standing constraints, and the definition of done for this particular stretch of work.

## File output

Save as `handoff.md` in the current working directory. If that exists, use `handoff-2.md`, then `handoff-3.md`, and so on.

Then say where the file is and that it can be edited before use. Do not summarise it back into the chat.
