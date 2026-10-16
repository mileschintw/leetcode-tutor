---
type: regex
pattern: '^- origin: notion[ \t]*$'
flags: m
match: count:2
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

Two Sum gains both Notion Attempts: the merge goes into the existing Problem.
