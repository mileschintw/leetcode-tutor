---
name: mirror-existing-database
description: The learner asks to push into their existing Notion database; the skill writes nothing there, creates its own database and offers Import for the old one.
tags: [mirror]
max_turns: 40
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Push my Practice Log into my existing Notion database "Leetcode Records" (https://www.notion.so/8a1f2c00111142228333444455556666), so all my practice is in one place. Go ahead without asking me anything.
