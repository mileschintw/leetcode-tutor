---
type: regex
pattern: '^(?=[\s\S]*^id: leetcode:valid-parentheses[ \t]*$)(?=[\s\S]*^title: Valid Parentheses[ \t]*$)(?=[\s\S]*^difficulty: easy[ \t]*$)(?=[\s\S]*^tags: \[(?=[^\]\n]*\bstack\b)(?=[^\]\n]*\bstring\b)[^\]\n]*\][ \t]*$)(?=[\s\S]*^lists: \[\][ \t]*$)(?=[\s\S]*^need_review: false[ \t]*$)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/valid-parentheses/notes.md }
---

The new Problem has its Problem ID, title, difficulty, algorithm tags, Problem Lists and need_review, with tags and lists written as [a, b].
