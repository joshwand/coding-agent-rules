---
name: handoff
description: >
  Creates a markdown handoff document from the current conversation, designed to be read into a new Claude chat as a briefing. Trigger this skill whenever the user types /handoff, says "create a handoff", "write a handoff", etc. 
---

# Handoff Skill

## Purpose

The user is ending or pausing a session and wants to carry the full context into a new one. Your job is to read everything that was discussed in this conversation and produce a single plain-text file that a new Claude — with no prior context — could read and immediately understand: who the user is, what was worked on, what was decided, what is unfinished, and what to do next.

This document is a briefing, not a summary. Write it as if you are handing over to a capable colleague. Be specific and concrete. Do not be vague.

## Output format

The file must be plain text — no markdown, no headers with hashes, no bullet points, no bold, no dashes used as list markers. Write in complete sentences and paragraphs. Use plain section labels followed by a colon and a line break to separate sections.

Use exactly these five sections in this order:

Who this is for:
Write one or two sentences identifying the user by name if known, their role or context, and the broad nature of what they were working on during this session. Draw only from what the conversation reveals.

What we covered:
A single paragraph (three to six sentences) summarising the main topics, questions, and decisions from the session. This should read as a coherent narrative, not a list. If multiple distinct things were covered, weave them together rather than enumerating them.

What was confirmed:
Write in plain sentences the specific facts, conclusions, technical decisions, or agreements that were reached during the session — things that were settled and can be treated as ground truth in the next session. If nothing was definitively confirmed, say so honestly.

Still in progress:
Write in plain sentences anything that was started but not completed, flagged as uncertain, left open, or deprioritised. Include anything the user said they would do later. If nothing is pending, say so.

Next steps:
Write in plain sentences what the user should pick up in the next session. This should follow logically from what is still in progress. Be specific — name the task, file, decision, or question that needs attention next.

References to load:
Specific file paths to read into context at the beginning of the session. Give instructions to do so. 

## Rules — read these carefully

Do not invent anything. Every sentence must be grounded in something that actually appeared in the conversation. If a section has nothing to put in it, write a brief honest statement to that effect rather than padding it out.

Do not add a preamble before the first section. Do not add commentary or meta-explanation after the last section.

Be specific. Vague handoffs are useless. Name the thing, the file, the decision, the error, the next action — whatever it is, say it plainly.

Match the user's register. If the conversation was casual and direct, write casually and directly. If it was technical and precise, match that.

Keep it tight. A good handoff is usually between 200 and 400 words. Longer is only justified if the session was genuinely complex and the detail is needed.

## After producing the file

Once the file is written and saved, tell the user clearly where it is and that they can open and edit any section before refrerencing or pasting it into a new chat. 

Do not re-summarise the file back to the user in the chat; just a simple statement on what the next step will be. Just tell them it is ready and where it is.

## File output

Save the file as `handoff.md` in . If a `handoff.md` already exists, save as `handoff-2.md`, and so on. 
