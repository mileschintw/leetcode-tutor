---
type: regex
pattern: '^(?=[\s\S]*^lists: \[Grind 75\][ \t]*$)(?=[\s\S]*^## Key Takeaway[ \t]*\n\s*[^\s#][\s\S]*^## Attempts)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

The merge adds the Problem List and the Key Takeaway from the callout to the existing Problem.
