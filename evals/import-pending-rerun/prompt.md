---
name: import-pending-rerun
description: A pending page whose Attempt is already in the Practice Log adds nothing on Import; nothing is written and the page is not trashed without asking.
tags: [import, chat-platform]
max_turns: 40
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

I practised in the Claude app on my phone and the tutor saved it to my Notion Mirror as pending. Bring my pending Attempts into my Practice Log.
