---
type: regex
target: mock_calls
pattern: '^(?=[\s\S]*"tool":\s*"(?:[\w-]+__)?notion-(?:update|create)-view"(?:(?!"verdict":).)*?SORT BY[\\"\s]+Last Attempt[\\"\s]+DESC)(?=[\s\S]*"tool":\s*"(?:[\w-]+__)?notion-create-view"(?:(?!"verdict":).)*?CALENDAR BY[\\"\s]+Last Attempt)'
---

A new Mirror gets the plan's views: a table sorted by Last Attempt, newest first, and a calendar on Last Attempt.
