---
id: leetcode:alien-dictionary
title: Alien Dictionary
difficulty: hard
tags: [graph, topological-sort]
link: https://leetcode.com/problems/alien-dictionary/
lists: []
need_review: false
---

## Key Takeaway

Compare adjacent words to get letter edges, then topologically sort the letters.

## Attempts

### 2025-03-02 topological sort

- date: 2025-03-02
- mode: session
- outcome: solved-with-hints
- approach: topological sort
- mistakes: Missed the case where a longer word comes before its own prefix.
- language: python
- code: /tmp/2025-03-02-topological-sort.py
- origin: notion
