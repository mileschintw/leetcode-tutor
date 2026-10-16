---
type: llm
---

Judge only the agent's final reply to the learner. PASS only if every statement below is true:

1. It is a preview of the import: it does not say that anything has already been written or saved.
2. It covers all three Notion pages: Two Sum, Merge Intervals and Daily Temperatures (by title or by Problem ID such as `leetcode:two-sum`).
3. It says Two Sum already exists in the Practice Log and the Notion Attempts are added to (merged into) it, rather than creating a second Two Sum.
4. It lists Two Sum's two Notion Attempts, dated 2024-03-01 and 2024-04-02, and marks the new Attempts as coming from Notion (an origin such as `notion`).
5. It carries Merge Intervals' Need Review flag over (need_review true), and maps Collection to Problem Lists (Grind 75, Grind169, Others).
6. It says the tags "L3", "L4" and "Weekly Contest 312" are dropped, or lists the kept tags of every Problem without them.
7. It ends by asking the learner to confirm or correct the preview before writing.
