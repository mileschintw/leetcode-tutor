---
name: mirror-no-github
description: A workspace with no GitHub remote; the skill explains it must be pushed to GitHub first and writes nothing to Notion.
tags: [mirror]
max_turns: 30
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Push my Practice Log to Notion.
