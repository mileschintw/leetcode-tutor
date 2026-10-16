---
name: recap-attempt-recorded
description: A Recap Mode Session on a known Problem ends after an unaided recall; the tutor records a recap Attempt and keeps Need Review, which only a full Session can clear.
tags: [practice-log, recap, need-review]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

I asked you for a quick recap of LeetCode 1. Two Sum before my interview tomorrow. Here is our Recap Mode exchange so far, after your overview:

> **Tutor:** What's the one-sentence Key Takeaway for this Problem? Try it from memory.
> **Me:** Keep a hash map from value to index, and check whether `target - num` is already in it before adding `num`, so each lookup is O(1) and an element never pairs with itself.
> **Tutor:** Exactly right, including the order that tripped you up last time. Want the optimal code?
> **Me:** Yes, show me the Python.
> **Tutor:**
>
> ```python
> class Solution:
>     def twoSum(self, nums: list[int], target: int) -> list[int]:
>         seen = {}
>         for i, num in enumerate(nums):
>             if target - num in seen:
>                 return [seen[target - num], i]
>             seen[num] = i
>         return []
> ```
>
> **Me:** Yep, that's what I'd write.

The Key Takeaway is fine as it is; I have nothing to add. Let's wrap up and save it.
