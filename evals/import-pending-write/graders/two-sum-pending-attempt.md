---
type: regex
pattern: '^### 2026-10-14 hash map\n\n?(?:- .*\n)*?- outcome: solved-with-hints\n(?:- .*\n?)*?- origin: mirror-pending[ \t]*$'
flags: m
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

The pending Two Sum Attempt is merged into the existing Problem with its own outcome and origin mirror-pending.
