---
type: regex
pattern: '^(?=[\s\S]*^id: leetcode:two-sum[ \t]*$)(?=[\s\S]*^title: \S*Two Sum)(?=[\s\S]*^need_review: false[ \t]*$)'
flags: m
target: { source: file, path: problems/leetcode/two-sum/notes.md }
---

The notes file's frontmatter holds the Problem ID, the title and need_review.
