---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(create-database|create-pages|update-page|move-pages|delete-pages)"'
match: not_contains
---

Nothing is written to Notion before the learner says yes to the push.
