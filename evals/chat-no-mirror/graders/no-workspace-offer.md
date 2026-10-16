---
type: regex
pattern: '\b(?:I can|I could|I''ll|I will|shall I|should I|want me to|let me)\b[^.?!\n]{0,40}\b(?:create|set up|set one up|initiali[sz]e)\b[^.?!\n]{0,40}\bworkspace\b'
flags: i
match: not_contains
---

The tutor doesn't offer to create a Practice Workspace. (nothing-created checks that no Notion database is created.)
