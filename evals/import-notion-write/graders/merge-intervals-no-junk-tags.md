---
type: regex
pattern: '(?:contest|\bl[345]\b)'
flags: mi
match: not_contains
target: { source: file, path: problems/leetcode/merge-intervals/notes.md }
---

Non-algorithm tags (contest weeks, job levels) are dropped.
