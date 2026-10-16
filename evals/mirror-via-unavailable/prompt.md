---
name: mirror-via-unavailable
description: The workspace says to push through a browser, but only a Notion connector is available, so the push asks before using the connector and writes nothing yet.
tags: [mirror]
max_turns: 30
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Push my Practice Log to my Notion Mirror.
