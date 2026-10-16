---
type: regex
pattern: '^- origin: leethub[ \t]*$'
flags: m
match: count:1
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

Two Sum gains exactly one LeetHub Attempt: the merge goes into the existing Problem.
