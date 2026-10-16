---
name: chat-no-mirror
description: On a chat platform with a Notion connector but no Mirror database yet, the tutor prints the Attempt block and says a Mirror needs a push from the Practice Workspace first.
tags: [practice-log, chat-platform, mirror]
max_turns: 30
plugins: ["../..", notion-stub]
allowed_tools: [Read, Glob, Grep, Skill]
disallowed_tools: [Write, Edit, NotebookEdit, Bash, PowerShell]
# Claude Code's own system prompt describes Write, Edit and Bash even when disallowed_tools removes them;
# a real chat app (claude.ai, Gemini, ChatGPT) never does. This environment-only line makes the fixture match one.
append_system_prompt: "You are running in a chat app. You have no tools that create or edit files on the user's computer and no shell. Files you produce exist only in this conversation. The user has connected Notion to this chat."
---

I'm practising LeetCode 1. Two Sum with you. Here is our Session so far, from your First Response onwards:

> **Tutor:** Which approach would you like to start with?
> **Me:** Nested loops over every pair, then something faster.
> **Tutor:** Checking every pair is O(n²). How could you avoid scanning the array again for each number?
> **Me:** Sort it and use two pointers? Then return the two numbers that add up to the target.
> **Tutor:** Two pointers works on a sorted array, but look at the expected output again: does it want the numbers or something else? And what does sorting do to that?
> **Me:** Oh, it wants indices, and sorting loses them. So a hash map from value to index instead?
> **Tutor:** Good. Write it and trace `nums = [3, 3], target = 6`.
> **Me:** My version puts each number in the map first and then looks up `target - num`, so for the first 3 it finds itself and returns [0, 0].
> **Tutor:** Right. What order fixes that?
> **Me:** Look up the complement first, then insert.

Here's my final code. LeetCode accepted it:

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []
```

I'm happy with the Key Takeaway you'd write and have nothing to add. Let's wrap up the Session and save it.
