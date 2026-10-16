---
name: import-notion-rerun
description: The learner repeats a Notion import that is already in the Practice Log; nothing is added or written.
tags: [import]
max_turns: 40
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Import my old records from my Notion "Leetcode Records" export in `legacy/notion-export` into my Practice Log. In that database, Level is the difficulty and Collection is the Problem List. Ignore Status, Times, Done, Created and Last updated.
