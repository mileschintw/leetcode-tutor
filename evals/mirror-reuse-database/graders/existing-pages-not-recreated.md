---
type: regex
target: mock_calls
pattern: '"tool":\s*"notion-create-pages".*leetcode:(two-sum|merge-intervals|daily-temperatures)'
match: not_contains
---

Problems that already have a page get no new page.
