#!/usr/bin/env bash
# A Practice Workspace where Two Sum has one earlier Attempt: the learner saw the solution, so it is marked Need Review.
set -euo pipefail
mkdir -p problems/leetcode/two-sum review-sheets
: > review-sheets/.gitkeep
cat > practice-log.json <<'JSON'
{
  "version": 1,
  "mirror": {
    "notion_database_id": null
  }
}
JSON
cat > README.md <<'MD'
# Practice Log

My coding-interview practice, recorded by LeetCode Tutor.
MD
cat > problems/leetcode/two-sum/notes.md <<'MD'
---
id: leetcode:two-sum
title: Two Sum
difficulty: easy
tags: [array, hash-table]
link: https://leetcode.com/problems/two-sum/
lists: [Grind 75]
need_review: true
need_review_reason: Saw the solution on 2026-09-01.
---

## Key Takeaway

Use a hash map from value to index, and look up `target - value` before inserting the current value, for O(1) complement checks.

## Attempts

### 2026-09-01 hash map

- date: 2026-09-01
- mode: session
- outcome: saw-solution
- approach: hash map
- mistakes: Inserted each value before looking up its complement, so `[3, 3]` matched an element with itself; asked for the solution after that.
- language: python
- code: 2026-09-01-hash-map.py
MD
cat > problems/leetcode/two-sum/2026-09-01-hash-map.py <<'PY'
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []
PY
