---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-database|update-data-source)"(?:(?!"verdict":).)*?Easy[\\'"]*\s*:\s*green'
---

Options carry the plan's colours: Easy is green.
