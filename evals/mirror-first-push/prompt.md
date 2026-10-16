---
name: mirror-first-push
description: First push to Notion; the skill creates its own database, stores its id and the GitHub repository, and warns that Notion edits are overwritten.
tags: [mirror]
max_turns: 40
plugins: [notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Publish my Practice Log to Notion so I can browse it on my phone. Put the database at the top level of my Notion workspace.
