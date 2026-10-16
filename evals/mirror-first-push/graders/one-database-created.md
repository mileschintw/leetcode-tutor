---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-create-database"'
match: count:1
---

The first push creates exactly one database of its own.
