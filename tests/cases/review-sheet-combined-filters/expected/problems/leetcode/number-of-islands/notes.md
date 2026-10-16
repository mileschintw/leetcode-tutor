---
id: leetcode:number-of-islands
title: Number of Islands
difficulty: medium
tags:
  - array
  - depth-first-search
  - breadth-first-search
  - graph
link: https://leetcode.com/problems/number-of-islands/
lists:
  - Grind 75
need_review: true
need_review_reason: Asked for the solution on 2026-09-20.
---

## Key Takeaway

Scan the grid; each unvisited land cell starts a flood fill that sinks its whole island, so the count of fills is the answer.

## Attempts

### 2026-09-20 dfs flood fill

- date: 2026-09-20
- mode: session
- outcome: saw-solution
- approach: dfs flood fill
- mistakes: Did not mark cells visited, so the recursion looped forever.
- language: python
- code: 2026-09-20-dfs-flood-fill.py

### 2026-10-05 bfs flood fill

- date: 2026-10-05
- mode: session
- outcome: solved-with-hints
- approach: bfs flood fill
- mistakes: Marked cells visited when popped instead of when pushed, so cells were queued twice.
- language: python
- code: 2026-10-05-bfs-flood-fill.py
