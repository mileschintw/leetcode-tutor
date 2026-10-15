---
id: custom:lru-cache
title: LRU Cache (my own harness)
difficulty:
tags: [design, linked-list, hash-table]
link:
lists:
need_review: yes
need_review_reason: Asked for a skeleton of the doubly linked list.  # set 2026-10-10
---

## Key Takeaway

A hash map to nodes plus a doubly linked list gives O(1) get and put.

## Attempts

### 2026-10-10 hash map + linked list

- date: 2026-10-10
- mode: session
- outcome: saw-solution
- approach: hash map + doubly linked list
- mistakes: Forgot to move a node to the front on get.
- language: python
- code: 2026-10-10-hash-map-linked-list.py
- origin: mirror-pending
