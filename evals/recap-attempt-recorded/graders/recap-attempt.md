---
type: regex
pattern: '^### 2026-09-01 hash map[\s\S]*^- outcome: saw-solution[\s\S]*^### (?!2026-09-01)(?=[\s\S]*^- mode: recap[ \t]*$)(?=[\s\S]*^- outcome: solved-alone[ \t]*$)(?=[\s\S]*^- language: python[ \t]*$)(?=[\s\S]*^- code: (?!2026-09-01-)\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.py[ \t]*$)'
flags: m
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

The earlier Attempt is kept, and a new recap Attempt follows it: the learner recalled the Key Takeaway unaided, so its outcome is solved-alone, and it has its own code file.
