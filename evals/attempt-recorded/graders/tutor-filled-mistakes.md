---
type: llm
focus: { source: file, path: problems/leetcode/two-sum/notes.md }
---

Judge the notes file. PASS only if every statement below is true:

1. It has a "Key Takeaway" section with one or two sentences about using a hash map to find each number's complement (target minus the number).
2. It has an Attempt whose `mistakes` line names at least one of the learner's slips from the Session: planning to return the numbers instead of their indices (or reaching for sorting, which loses the indices), or inserting into the map before looking up the complement, so `[3, 3]` matched an element with itself.
3. The Attempt's `outcome` is `solved-with-hints`.
