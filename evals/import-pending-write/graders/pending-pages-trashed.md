---
type: regex
target: mock_calls
pattern: '^(?=[\s\S]*"tool":\s*"(?:[\w-]+__)?notion-(?:delete-pages|move-pages|update-page)".*b2000000-?0000-?4000-?8000-?0000000000ff)(?=[\s\S]*"tool":\s*"(?:[\w-]+__)?notion-(?:delete-pages|move-pages|update-page)".*b2000000-?0000-?4000-?8000-?0000000000fe)'
---

Once imported, both pending pages are moved to Notion's trash, so a re-import or the next push can't bring them back.
