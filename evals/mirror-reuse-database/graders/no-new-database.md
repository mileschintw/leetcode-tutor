---
type: regex
target: mock_calls
pattern: notion-create-database
match: not_contains
---

A later push reuses the stored database and never creates another.
