---
type: regex
pattern: '^(?=[\s\S]*^id: leetcode:contains-duplicate[ \t]*$)(?=[\s\S]*^title: Contains Duplicate[ \t]*$)(?=[\s\S]*^difficulty: easy[ \t]*$)(?=[\s\S]*^tags: \[(?=[^\]\n]*\barray\b)(?=[^\]\n]*\bhash-table\b)(?=[^\]\n]*\bsorting\b)[^\]\n]*\][ \t]*$)(?=[\s\S]*^lists: \[\][ \t]*$)(?=[\s\S]*^need_review: false[ \t]*$)'
flags: m
match: contains
target: { source: file, path: problems/leetcode/contains-duplicate/notes.md }
---

The new Problem has its Problem ID, title, difficulty, algorithm tags, Problem Lists and need_review, with tags and lists written as [a, b].
