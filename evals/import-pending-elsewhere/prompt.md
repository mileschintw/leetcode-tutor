---
name: import-pending-elsewhere
description: Import finds no pending page in the stored Mirror but one in another Mirror-like database, and tells the learner where it is instead of losing it, changing nothing.
tags: [import, mirror, chat-platform]
max_turns: 40
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

I practised Two Sum in the Claude app on my phone yesterday and the tutor said it saved it to Notion as pending. Bring my pending Attempts into my Practice Log.
