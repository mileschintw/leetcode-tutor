---
type: regex
pattern: '^### 2024-03-20 .*$(?=(?:(?!^##)[\s\S])*?^- date: 2024-03-20[ \t]*$)(?=(?:(?!^##)[\s\S])*?^- mode: session[ \t]*$)(?=(?:(?!^##)[\s\S])*?^- outcome: solved-alone[ \t]*$)(?=(?:(?!^##)[\s\S])*?^- approach: \S)(?=(?:(?!^##)[\s\S])*?^- language: python[ \t]*$)(?=(?:(?!^##)[\s\S])*?^- code: 2024-03-20-[a-z0-9-]+\.py[ \t]*$)(?=(?:(?!^##)[\s\S])*?^- origin: notion[ \t]*$)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/daily-temperatures/notes.md }
---

The imported Attempt's own block, from its heading to the next heading, has every required field, its date from the source, the assumed outcome, and its origin.
