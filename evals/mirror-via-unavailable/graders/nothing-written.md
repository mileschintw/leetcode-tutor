---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database|update-page|update-data-source|move-pages|delete-pages)"'
match: not_contains
---

The learner chose the browser, so nothing is written through the connector before they agree.
