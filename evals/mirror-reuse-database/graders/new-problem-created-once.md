---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-create-pages"(?:(?!"verdict":).)*?leetcode:valid-parentheses'
match: count:1
---

Valid Parentheses, new since the last push, gets exactly one new page.
