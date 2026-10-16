---
name: import-notion-write
description: After the learner confirms the preview, the Notion import merges Two Sum by Problem ID and writes valid Problems.
tags: [import]
max_turns: 40
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Earlier in this conversation I asked you this:

> Import my old records from my Notion "Leetcode Records" export in `legacy/notion-export` into my Practice Log. In that database, Level is the difficulty and Collection is the Problem List. Ignore Status, Times, Done, Created and Last updated.

You read the export and showed me this preview:

> **Import preview: Notion (`legacy/notion-export`)**
>
> 2 Problems to create, 1 to merge into, 4 Attempts to add (origin `notion`), 0 skipped as already imported.
>
> - `leetcode:two-sum`: merge into the existing Problem. Add the list Grind 75 and the Key Takeaway from the callout (the Problem has none yet). Add 2024-03-01, brute force, notion, `2024-03-01-brute-force.py` and 2024-04-02, hash map, notion, `2024-04-02-hash-map.py`.
> - `leetcode:merge-intervals`: new. Merge Intervals, medium, tags [array, sorting], lists [Grind169], need_review true (marked for review in Notion), Key Takeaway from the callout. Add 2024-03-15, sort and merge, notion, `2024-03-15-sort-and-merge.py`.
> - `leetcode:daily-temperatures`: new. Daily Temperatures, medium, tags [stack, monotonic-stack], lists [Others], need_review false, Key Takeaway from the callout. Add 2024-03-20, monotonic stack, notion, `2024-03-20-monotonic-stack.py`.
>
> **Dropped:** the tags "L3", "L4" and "Weekly Contest 312"; the Status, Times, Done, Created and Last updated fields.
> **Assumed:** outcome `solved-alone` and mode `session` for every Attempt, since the pages don't record them.
> **Uncertain matches:** none.
>
> Shall I write this to your Practice Log?

Yes, that's all correct. Go ahead and write it.
