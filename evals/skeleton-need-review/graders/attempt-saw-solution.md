---
type: regex
pattern: '^## Attempts[\s\S]*^### (?=[\s\S]*^- mode: session[ \t]*$)(?=[\s\S]*^- outcome: saw-solution[ \t]*$)(?=[\s\S]*^- code: \d{4}-\d{2}-\d{2}-[a-z0-9-]+\.py[ \t]*$)'
flags: m
target: { source: file, path: problems/leetcode/longest-substring-without-repeating-characters/notes.md }
---

Asking for a skeleton makes the Attempt's outcome saw-solution.
