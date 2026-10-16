---
id: custom:two-heaps
title: Running Median
difficulty: hard
tags: [heap-priority-queue]
link:
lists: []
need_review: false
need_review_reason:
---

## Key Takeaway

1. Keep a max-heap for the lower half and a min-heap for the upper half.
2. After each insert, rebalance so the sizes differ by at most one:
   - move the top of the larger heap to the other one.
3. The median is the top of the larger heap, or the mean of both tops.

Formula: $m = (a + b) / 2$

## Attempts

### 2026-10-01 two heaps

- date: 2026-10-01
- mode: session
- outcome: solved-alone
- approach: two heaps
- language: python
- code: 2026-10-01-two-heaps.py
