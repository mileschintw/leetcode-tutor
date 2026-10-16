---
type: regex
pattern: '^## Attempts[\s\S]*^### (?=[\s\S]*^- date: \d{4}-\d{2}-\d{2}[ \t]*$)(?=[\s\S]*^- mode: session[ \t]*$)(?=[\s\S]*^- outcome: solved-with-hints[ \t]*$)(?=[\s\S]*^- approach: \S)(?=[\s\S]*^- mistakes: \S)(?=[\s\S]*^- language: python[ \t]*$)(?=[\s\S]*^- code: \d{4}-\d{2}-\d{2}-[a-z0-9-]+\.py[ \t]*$)'
flags: m
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

The Attempt has every required field with a valid value: the learner needed hints, so the outcome is solved-with-hints, and the code file is named by date and approach.
