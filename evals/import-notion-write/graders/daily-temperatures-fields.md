---
type: regex
pattern: '^(?=[\s\S]*^id: leetcode:daily-temperatures[ \t]*$)(?=[\s\S]*^title: Daily Temperatures[ \t]*$)(?=[\s\S]*^difficulty: medium[ \t]*$)(?=[\s\S]*^tags: \[(?=[^\]\n]*\bstack\b)(?=[^\]\n]*\bmonotonic-stack\b)[^\]\n]*\][ \t]*$)(?=[\s\S]*^lists: \[Others\][ \t]*$)(?=[\s\S]*^need_review: false[ \t]*$)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/daily-temperatures/notes.md }
---

The new Problem has its Problem ID, title, difficulty, algorithm tags, Problem Lists and need_review, with tags and lists written as [a, b].
