---
type: regex
pattern: '^(?=[\s\S]*^id: leetcode:merge-intervals[ \t]*$)(?=[\s\S]*^title: Merge Intervals[ \t]*$)(?=[\s\S]*^difficulty: medium[ \t]*$)(?=[\s\S]*^tags: \[(?=[^\]\n]*\barray\b)(?=[^\]\n]*\bsorting\b)[^\]\n]*\][ \t]*$)(?=[\s\S]*^lists: \[Grind169\][ \t]*$)(?=[\s\S]*^need_review: true[ \t]*$)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/merge-intervals/notes.md }
---

The new Problem has its Problem ID, title, difficulty, algorithm tags, Problem Lists and need_review, with tags and lists written as [a, b].
