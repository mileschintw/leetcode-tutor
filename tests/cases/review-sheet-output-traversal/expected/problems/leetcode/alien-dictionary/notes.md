---
id: leetcode:alien-dictionary
title: Alien Dictionary
difficulty: hard
tags: [graph, topological-sort]
link: https://leetcode.com/problems/alien-dictionary/
lists: []
need_review: false
need_review_reason:
---

## Key Takeaway

Compare adjacent words to get letter edges, then topologically sort the letters.

## Attempts

### 2026-09-28 topological sort

- date: 2026-09-28
- mode: session
- outcome: solved-with-hints
- approach: topological sort
- mistakes: Missed the invalid case where a word is followed by its own prefix.
- language: python
- code: 2026-09-28-topological-sort.py
