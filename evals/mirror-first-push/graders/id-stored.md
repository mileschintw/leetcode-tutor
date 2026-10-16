---
type: regex
pattern: '"notion_database_id"\s*:\s*"2a7c41e9-?5b3d-?4f08-?9c61-?7e2d8a0b4f13"'
target: { source: file, path: practice-log.json }
---

The new database's id is stored in the workspace config, so later pushes reuse it.
