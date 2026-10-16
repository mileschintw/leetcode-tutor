---
name: session-clears-need-review
description: A full Session on a Problem marked Need Review ends solved alone; the tutor records the Attempt and clears the mark and its reason.
tags: [practice-log, need-review]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

I'm redoing LeetCode 1. Two Sum with you, the full way this time. Here is our Session so far, from your First Response onwards:

> **Tutor:** Which approach would you like to start with?
> **Me:** Brute force is checking every pair in O(n²), so I'll skip it. I'll keep a hash map from value to index, and for each number look up `target - num` before inserting it, so `[3, 3]` doesn't match an element with itself. That's O(n) time and O(n) space.
> **Tutor:** Go ahead and write it.
> **Me:** Done, and LeetCode accepted it on the first try. I also traced `[3, 3], target = 6` by hand: it returns `[0, 1]`.

Here's my final code:

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

I'm happy with the Key Takeaway as it is and have nothing to add. Let's wrap up the Session and save it.
