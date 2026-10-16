---
type: regex
target: mock_calls
pattern: '"tool":\s*"notion-create-database"'
match: count:1
---

The first push creates exactly one database of its own.
