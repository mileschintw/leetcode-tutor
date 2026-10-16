---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(create-database|create-pages|update-page|move-pages|delete-pages)"'
match: not_contains
---

Without a GitHub repository to link to, nothing is written to Notion.
