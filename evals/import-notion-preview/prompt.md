---
name: import-notion-preview
description: The learner asks to import a Notion export; the skill shows a preview and writes nothing before they confirm.
tags: [import]
max_turns: 40
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Import my old records from my Notion "Leetcode Records" export in `legacy/notion-export` into my Practice Log. In that database, Level is the difficulty and Collection is the Problem List. Ignore Status, Times, Done, Created and Last updated.
