---
type: regex
pattern: '^(?=[\s\S]*^need_review: false[ \t]*$)(?=[\s\S]*^need_review_reason:[ \t]*(?:""|'''')?[ \t]*$)'
flags: m
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

A full Session solved alone clears Need Review: `need_review` is false and `need_review_reason` is empty.
