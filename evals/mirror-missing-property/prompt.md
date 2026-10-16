---
name: mirror-missing-property
description: The stored Mirror database's Problem ID property was renamed, so the push stops before writing anything and asks the learner to rename it back.
tags: [mirror]
max_turns: 40
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Push my Practice Log to my Notion Mirror.
