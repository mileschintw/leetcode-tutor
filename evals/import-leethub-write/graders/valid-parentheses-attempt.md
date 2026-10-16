---
type: regex
pattern: '^## Attempts[\s\S]*^### \S+ (?=[\s\S]*^- date: 2024-03-10[ \t]*$)(?=[\s\S]*^- mode: session[ \t]*$)(?=[\s\S]*^- outcome: solved-alone[ \t]*$)(?=[\s\S]*^- approach: \S)(?=[\s\S]*^- language: python[ \t]*$)(?=[\s\S]*^- code: 2024-03-10-[a-z0-9-]+\.py[ \t]*$)(?=[\s\S]*^- origin: leethub[ \t]*$)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/valid-parentheses/notes.md }
---

The imported Attempt has every required field, its date from the source, the assumed outcome, and its origin.
