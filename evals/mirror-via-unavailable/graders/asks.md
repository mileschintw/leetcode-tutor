---
type: llm
---

Judge only the agent's final reply to the learner. PASS only if every statement below is true:

1. It says the workspace is set to push through Notion's API, and that it can't here (no NOTION_TOKEN set, or no shell to run mirror-push).
2. It asks whether to push through the Notion connector this time instead (or offers that and waits).
3. It does not say that anything was pushed or written to Notion.
