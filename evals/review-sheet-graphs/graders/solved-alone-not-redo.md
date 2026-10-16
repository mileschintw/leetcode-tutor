---
type: regex
pattern: '"file_path":"[^"]*review-sheets[^"]*\.md","content":"(?:[^"\\]|\\.)*## Redo(?:(?!\\n## )(?:[^"\\]|\\.))*clone-graph'
match: not_contains
target: trace
---

Clone Graph, solved alone, is not listed to redo.
