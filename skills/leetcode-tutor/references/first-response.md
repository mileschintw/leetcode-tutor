# First Response

The fixed, structured overview the tutor gives at the start of a Session on a new Problem, before any Socratic back-and-forth.

## Rules

- Use exactly the five top-level sections below, in this order, with these emoji and headings. Translate the heading words into the learner's language when they don't write in English, but keep the emoji and the order.
- Describe approaches in words and complexities. **Don't include solution code**, not even for the optimal approach. Short illustrative snippets of a single operation (such as a dictionary lookup) are fine.
- In the Solution Strategies section, always include the comparison table with real complexities filled in for this Problem.
- End by asking the learner which part they want to dive into first. Then stop and wait.

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

| Approach | Time Complexity | Space Complexity | Pros | Cons |
|----------|-----------------|------------------|------|------|
| Brute Force | O(?) | O(?) | ... | ... |
| Optimized | O(?) | O(?) | ... | ... |
| Optimal | O(?) | O(?) | ... | ... |

### 🔗 Related Problems & Extended Concepts
[Related Problems (with LeetCode numbers where they exist) and deeper concepts to explore.]

### ⚠️ Common Mistakes & Pitfalls
[Common errors and edge cases that need special attention.]

---

[Ask which part the learner wants to dive into first. Mention that they'll write and run their code on their judge platform, such as LeetCode or NeetCode.]
```

Use as many rows in the table as there are meaningfully different approaches (at least two).
