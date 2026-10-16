---
name: mirror-reuse-database
description: A later push reuses the stored Notion database, rewrites its pages, leaves the pending page alone and warns that Notion edits are overwritten.
tags: [mirror]
max_turns: 40
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Push my Practice Log to my Notion Mirror.
