---
type: regex
pattern: '^- date: 2024-03-01[ \t]*$[\s\S]*^- date: 2024-03-08[ \t]*$[\s\S]*^- date: 2024-04-02[ \t]*$'
flags: m
match: contains
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

The Attempt log stays oldest first, with the Notion Attempts placed around the LeetHub one by date.
