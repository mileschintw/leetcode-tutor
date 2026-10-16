---
name: chat-first-response
description: At the start of a Session on a chat platform, the tutor gives the full First Response and teaches, with no workspace check or offer.
tags: [first-response, chat-platform]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
disallowed_tools: [Write, Edit, NotebookEdit, Bash, PowerShell]
# Claude Code's own system prompt describes Write, Edit and Bash even when disallowed_tools removes them;
# a real chat app (claude.ai, Gemini, ChatGPT) never does. This environment-only line makes the fixture match one.
append_system_prompt: "You are running in a chat app. You have no tools that create or edit files on the user's computer and no shell. Files you produce exist only in this conversation."
---

Let's do LeetCode 121. Best Time to Buy and Sell Stock.
