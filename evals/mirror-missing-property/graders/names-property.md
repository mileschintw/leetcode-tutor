---
type: llm
---

Judge only the agent's final reply to the learner. PASS only if every statement below is true:

1. It says nothing was pushed (or the push stopped) because the Mirror database has no `Problem ID` property.
2. It asks the learner to rename the property back to `Problem ID` in Notion (it may notice it is now called `ID`), or to restore it, and then push again.
3. It does not say that any page was created or updated.
