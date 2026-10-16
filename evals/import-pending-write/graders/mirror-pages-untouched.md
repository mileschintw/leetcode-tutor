---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database|update-page|move-pages|delete-pages)"(?:(?!"verdict":).)*?a1000000-?0000-?4000-?8000-?00000000000[123]|"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database)"'
match: not_contains
---

Import touches only the pending pages: it creates nothing in Notion and leaves the generated Mirror pages to the next push.
