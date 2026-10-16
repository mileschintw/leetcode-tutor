---
type: regex
pattern: '^need_review_reason: \S'
flags: m
match: contains
target: { source: file, path: problems/leetcode/merge-intervals/notes.md }
---

The carried-over Need Review flag has a reason.
