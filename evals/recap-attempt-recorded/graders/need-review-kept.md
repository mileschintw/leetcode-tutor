---
type: regex
pattern: '^(?=[\s\S]*^need_review: true[ \t]*$)(?=[\s\S]*^need_review_reason: Saw the solution on 2026-09-01\.[ \t]*$)'
flags: m
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

A recap never clears Need Review, even when the recall is solved-alone: the mark and its reason stay as they were.
