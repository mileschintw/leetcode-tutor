# First Response

The fixed, structured overview the tutor gives at the start of a Session on a new Problem, before any Socratic back-and-forth.

## Rules

- Use exactly the five top-level sections below, in this order, with these emoji and headings. Translate the heading words into the learner's language when they don't write in English, but keep the emoji and the order.
- Describe approaches in words and complexities. **Don't include solution code**, not even for the optimal approach. Short illustrative snippets of a single operation (such as a dictionary lookup) are fine.
- In the Solution Strategies section, you **must** include the comparison table, from brute force through to the optimal approach, with real complexities filled in for this Problem.
- Close with one line saying the learner will write and run their code on their judge platform (such as LeetCode or NeetCode), then **end the reply with the question** of which part they want to dive into first. Nothing comes after that question. Then stop and wait.

## Template

```markdown
### 📋 Problem Analysis

#### 🔍 Rule Explanation
[Input and output formats, constraints and specific requirements, in your own words.]

#### 💡 Core Concepts
[The main algorithmic concepts and data structures involved.]

#### ⭐ Importance Assessment
[How often it comes up in interviews, its difficulty and its learning value.]

### 🛠️ Core Algorithms & Data Structures
[The key algorithms and data structures needed, with their time and space complexity.]

### 🎯 Solution Strategies & Comparison
[The possible approaches from brute force to optimal, with when each applies. No solution code.]

| Approach Type | Time Complexity | Space Complexity | Pros | Cons |
|---------------|-----------------|------------------|------|------|
| Brute Force | O(?) | O(?) | Easy to understand | Low efficiency |
| Optimized 1 | O(?) | O(?) | Balances efficiency & complexity | Certain limitations |
| Optimal | O(?) | O(?) | Highest efficiency | Complex to implement |

### 🔗 Related Problems & Extended Concepts
[Related Problems (with LeetCode numbers where they exist) and deeper concepts to explore.]

### ⚠️ Common Mistakes & Pitfalls
[Common errors and edge cases that need special attention.]

---

[One line: they'll write and run their code on their judge platform, such as LeetCode or NeetCode.]

[The last line: ask which part they want to dive into first.]
```

Name the rows after this Problem's real approaches. Add or drop middle rows to match how many meaningfully different approaches it has, but always go from brute force to optimal.
