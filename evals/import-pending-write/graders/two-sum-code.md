---
type: regex
pattern: 'def twoSum\(self, nums: list\[int\], target: int\) -> list\[int\]:\n        seen = \{\}\n        for i, num in enumerate\(nums\):\n            if target - num in seen:\n                return \[seen\[target - num\], i\]\n            seen\[num\] = i\n        return \[\]'
target: { source: file, path: problems/leetcode/two-sum/2026-10-14-hash-map.py }
---

The pending page's code is copied exactly into the Attempt's code file, so the page itself was read.
