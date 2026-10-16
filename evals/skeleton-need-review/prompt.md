---
name: skeleton-need-review
description: An overwhelmed learner asked for a skeleton mid-Session; at the end the tutor records saw-solution and marks Need Review with a reason.
tags: [practice-log, need-review]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

I'm practising LeetCode 3. Longest Substring Without Repeating Characters with you. Here is our Session so far, from your First Response onwards:

> **Tutor:** Which approach would you like to start with?
> **Me:** Brute force: check every substring for repeats.
> **Tutor:** That's O(n³), or O(n²) with a set. When you hit a repeated character, do you really need to restart from the next index?
> **Me:** I don't know. I've been at this for an hour and I'm exhausted. Can you just give me a code skeleton for the optimal solution? I'll fill in the blanks.
> **Tutor:** Sure, here's a sliding-window skeleton:
>
> ```python
> def lengthOfLongestSubstring(s):
>     last = {}
>     left = best = 0
>     for right, ch in enumerate(s):
>         if ch in last and last[ch] >= left:
>             left = ...
>         last[ch] = right
>         best = ...
>     return best
> ```
>
> **Me:** Thanks. I filled it in.

Here's my final code. LeetCode accepted it:

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = best = 0
        for right, ch in enumerate(s):
            if ch in last and last[ch] >= left:
                left = last[ch] + 1
            last[ch] = right
            best = max(best, right - left + 1)
        return best
```

I'm happy with the Key Takeaway you'd write and have nothing to add. Let's wrap up the Session and save it.
