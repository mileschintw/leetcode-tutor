---
type: regex
pattern: '"repository"\s*:\s*"https://github\.com/learner/practice-log"'
target: { source: file, path: practice-log.json }
---

The GitHub repository is stored in the workspace config as an https URL.
