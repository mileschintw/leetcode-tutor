# Shared fixtures for the practice-log-import cases. Each case's scaffold.sh sources this file
# and calls the functions it needs, in the scaffold's working directory.
#
# Legacy Records: a small LeetHub repository (legacy/LeetCodeRecord) and a small Notion export
# (legacy/notion-export). Two Sum is in both. Imported states: the Practice Log after importing
# one source or both, written the way the import skill should write it. tests/cases/validate-imported-workspace
# holds the state after both imports (workspace; two_sum both; imported_notion; imported_leethub):
# regenerate it when this file changes.

# --- Code shared by the sources and the imported Practice Log ---

code_two_sum_brute_force() {
cat <<'PY'
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
PY
}

code_two_sum_hash_map_notion() {
cat <<'PY'
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        index = {}
        for i, num in enumerate(nums):
            if target - num in index:
                return [index[target - num], i]
            index[num] = i
PY
}

code_two_sum_leethub() {
cat <<'PY'
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i
        return []
PY
}

code_valid_parentheses() {
cat <<'PY'
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in s:
            if ch in pairs:
                if not stack or stack.pop() != pairs[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack
PY
}

code_contains_duplicate() {
cat <<'PY'
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for n in nums:
            if n in seen:
                return True
            seen.add(n)
        return False
PY
}

code_merge_intervals() {
cat <<'PY'
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged
PY
}

code_daily_temperatures() {
cat <<'PY'
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        stack = []
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                answer[j] = i - j
            stack.append(i)
        return answer
PY
}

indent() { sed 's/^/    /'; }

# --- An empty Practice Workspace, as `practice-log init` creates it ---

workspace() {
  mkdir -p problems review-sheets
  : > problems/.gitkeep
  : > review-sheets/.gitkeep
  cat > practice-log.json <<'JSON'
{
  "version": 1,
  "mirror": {
    "notion_database_id": null
  }
}
JSON
  cat > README.md <<'MD'
# Practice Log

My coding-interview practice, recorded by LeetCode Tutor.
MD
}

# --- Legacy Records ---

leethub_repo() {
  local repo=legacy/LeetCodeRecord
  mkdir -p "$repo/0001-two-sum" "$repo/0020-valid-parentheses" "$repo/0217-contains-duplicate"
  cat > "$repo/README.md" <<'MD'
# LeetCodeRecord
Collection of LeetCode questions to ace the coding interview! - Created using [LeetHub v3](https://github.com/raphaelheinz/LeetHub-3.0)
<!---LeetCode Topics Start-->
# LeetCode Topics
## Array
|  |
| ------- |
| [0001-two-sum](https://github.com/mileschintw/LeetCodeRecord/tree/master/0001-two-sum) |
| [0217-contains-duplicate](https://github.com/mileschintw/LeetCodeRecord/tree/master/0217-contains-duplicate) |
## Hash Table
|  |
| ------- |
| [0001-two-sum](https://github.com/mileschintw/LeetCodeRecord/tree/master/0001-two-sum) |
| [0217-contains-duplicate](https://github.com/mileschintw/LeetCodeRecord/tree/master/0217-contains-duplicate) |
## Sorting
|  |
| ------- |
| [0217-contains-duplicate](https://github.com/mileschintw/LeetCodeRecord/tree/master/0217-contains-duplicate) |
## String
|  |
| ------- |
| [0020-valid-parentheses](https://github.com/mileschintw/LeetCodeRecord/tree/master/0020-valid-parentheses) |
## Stack
|  |
| ------- |
| [0020-valid-parentheses](https://github.com/mileschintw/LeetCodeRecord/tree/master/0020-valid-parentheses) |
## Weekly Contest 350
|  |
| ------- |
| [0020-valid-parentheses](https://github.com/mileschintw/LeetCodeRecord/tree/master/0020-valid-parentheses) |
## L4
|  |
| ------- |
| [0217-contains-duplicate](https://github.com/mileschintw/LeetCodeRecord/tree/master/0217-contains-duplicate) |
<!---LeetCode Topics End-->
MD
  cat > "$repo/0001-two-sum/README.md" <<'MD'
<h2><a href="https://leetcode.com/problems/two-sum">1. Two Sum</a></h2><h3>Easy</h3><hr><p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>
MD
  cat > "$repo/0020-valid-parentheses/README.md" <<'MD'
<h2><a href="https://leetcode.com/problems/valid-parentheses">20. Valid Parentheses</a></h2><h3>Easy</h3><hr><p>Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.</p>
MD
  cat > "$repo/0217-contains-duplicate/README.md" <<'MD'
<h2><a href="https://leetcode.com/problems/contains-duplicate">217. Contains Duplicate</a></h2><h3>Easy</h3><hr><p>Given an integer array <code>nums</code>, return <code>true</code> if any value appears <strong>at least twice</strong> in the array, and return <code>false</code> if every element is distinct.</p>
MD
  code_two_sum_leethub > "$repo/0001-two-sum/0001-two-sum.py"
  code_valid_parentheses > "$repo/0020-valid-parentheses/0020-valid-parentheses.py"
  code_contains_duplicate > "$repo/0217-contains-duplicate/0217-contains-duplicate.py"
}

notion_page() { # title collection level number tags link need-review times created takeaway
  cat <<MD
# $1

Collection: $2
Level: $3
Problem: $4. $1
Tags: $5
Link: $6
Need Review: $7
Status: Done
Times: $8
Done: Yes
Created: $9
Last updated: ${9}

<aside>
💡 ${10}

</aside>

## Thought

MD
}

notion_toggle() { # heading, code on stdin
  echo "- $1"
  echo "    "
  echo '    ```python'
  indent
  echo '    ```'
  echo "    "
}

notion_export() {
  local dir="legacy/notion-export/Leetcode Records"
  mkdir -p "$dir"
  cat > "legacy/notion-export/Leetcode Records 8a1f2c.csv" <<'CSV'
Problem,Collection,Created,Done,Last updated,Level,Link,Need Review,Status,Tags,Times
1. Two Sum,Grind 75,"March 1, 2024 9:03 PM",Yes,"April 2, 2024 10:12 PM",Easy,https://leetcode.com/problems/two-sum/,No,Done,"Array, Hash Table, L3",2
56. Merge Intervals,Grind169,"March 15, 2024 8:40 PM",Yes,"March 15, 2024 9:55 PM",Medium,https://leetcode.com/problems/merge-intervals/,Yes,Done,"Array, Sorting, Weekly Contest 312",1
739. Daily Temperatures,Others,"March 20, 2024 7:15 PM",Yes,"March 20, 2024 8:01 PM",Medium,https://leetcode.com/problems/daily-temperatures/,No,Done,"Stack, Monotonic Stack, L4",1
CSV
  {
    notion_page "Two Sum" "Grind 75" Easy 1 "Array, Hash Table, L3" https://leetcode.com/problems/two-sum/ No 2 \
      "March 1, 2024 9:03 PM" "Key Takeaway: store each value's index in a hash map and look up target - value before inserting the current value."
    code_two_sum_brute_force | notion_toggle "2024-03-01 Brute force"
    code_two_sum_hash_map_notion | notion_toggle "2024-04-02 Hash map"
  } > "$dir/Two Sum 3c9d41.md"
  {
    notion_page "Merge Intervals" Grind169 Medium 56 "Array, Sorting, Weekly Contest 312" https://leetcode.com/problems/merge-intervals/ Yes 1 \
      "March 15, 2024 8:40 PM" "Key Takeaway: sort by start, then extend the last merged interval while the next one starts before it ends."
    code_merge_intervals | notion_toggle "2024-03-15 Sort and merge"
  } > "$dir/Merge Intervals 77b0e3.md"
  {
    notion_page "Daily Temperatures" Others Medium 739 "Stack, Monotonic Stack, L4" https://leetcode.com/problems/daily-temperatures/ No 1 \
      "March 20, 2024 7:15 PM" "Key Takeaway: keep a stack of indices of days still waiting for a warmer one; each warmer day pops and answers them."
    code_daily_temperatures | notion_toggle "2024-03-20 Monotonic stack"
  } > "$dir/Daily Temperatures 0e5a92.md"
}

# --- The imported Practice Log ---

attempt() { # date approach origin code-file
  cat <<MD

### $1 $2

- date: $1
- mode: session
- outcome: solved-alone
- approach: $2
- language: python
- code: $4
- origin: $3
MD
}

# Two Sum after importing the given sources: two_sum notion | two_sum leethub | two_sum both
two_sum() {
  local dir=problems/leetcode/two-sum lists="[]" takeaway=""
  mkdir -p "$dir"
  if [ "$1" != leethub ]; then
    lists="[Grind 75]"
    takeaway="Store each value's index in a hash map and look up target - value before inserting the current value."
  fi
  {
    cat <<MD
---
id: leetcode:two-sum
title: Two Sum
difficulty: easy
tags: [array, hash-table]
link: https://leetcode.com/problems/two-sum/
lists: $lists
need_review: false
need_review_reason:
---

## Key Takeaway

$takeaway

## Attempts
MD
    if [ "$1" != leethub ]; then attempt 2024-03-01 "brute force" notion 2024-03-01-brute-force.py; fi
    if [ "$1" != notion ]; then attempt 2024-03-08 "hash map" leethub 2024-03-08-hash-map.py; fi
    if [ "$1" != leethub ]; then attempt 2024-04-02 "hash map" notion 2024-04-02-hash-map.py; fi
  } > "$dir/notes.md"
  if [ "$1" != leethub ]; then
    code_two_sum_brute_force > "$dir/2024-03-01-brute-force.py"
    code_two_sum_hash_map_notion > "$dir/2024-04-02-hash-map.py"
  fi
  if [ "$1" != notion ]; then code_two_sum_leethub > "$dir/2024-03-08-hash-map.py"; fi
}

problem() { # slug title difficulty tags lists need_review reason takeaway date approach origin code-fn
  local dir="problems/leetcode/$1" file="$9-$(echo "${10}" | tr ' ' '-').py"
  mkdir -p "$dir"
  {
    cat <<MD
---
id: leetcode:$1
title: $2
difficulty: $3
tags: $4
link: https://leetcode.com/problems/$1/
lists: $5
need_review: $6
need_review_reason: $7
---

## Key Takeaway

$8

## Attempts
MD
    attempt "$9" "${10}" "${11}" "$file"
  } > "$dir/notes.md"
  "${12}" > "$dir/$file"
}

imported_notion() {
  problem merge-intervals "Merge Intervals" medium "[array, sorting]" "[Grind169]" true \
    "Marked for review in Notion before import" \
    "Sort by start, then extend the last merged interval while the next one starts before it ends." \
    2024-03-15 "sort and merge" notion code_merge_intervals
  problem daily-temperatures "Daily Temperatures" medium "[stack, monotonic-stack]" "[Others]" false "" \
    "Keep a stack of indices of days still waiting for a warmer one; each warmer day pops and answers them." \
    2024-03-20 "monotonic stack" notion code_daily_temperatures
}

imported_leethub() {
  problem valid-parentheses "Valid Parentheses" easy "[string, stack]" "[]" false "" "" \
    2024-03-10 "stack" leethub code_valid_parentheses
  problem contains-duplicate "Contains Duplicate" easy "[array, hash-table, sorting]" "[]" false "" "" \
    2024-03-12 "hash set" leethub code_contains_duplicate
}

# --- The Mirror ---

# The workspace config with a Mirror database id and repository: mirror_config <id|null> [repository]
mirror_config() {
  local id=null
  if [ "$1" != null ]; then id="\"$1\""; fi
  if [ -n "${2:-}" ]; then
    printf '{\n  "version": 1,\n  "mirror": {\n    "notion_database_id": %s,\n    "repository": "%s"\n  }\n}\n' "$id" "$2"
  else
    printf '{\n  "version": 1,\n  "mirror": {\n    "notion_database_id": %s\n  }\n}\n' "$id"
  fi > practice-log.json
}

# A git repository's config with an origin remote, written by hand: git_origin <url>
git_origin() {
  mkdir -p .git
  cat > .git/config <<CFG
[core]
	repositoryformatversion = 0
	bare = false
[remote "origin"]
	url = $1
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
	remote = origin
	merge = refs/heads/main
CFG
}

# --- Pending Attempts from a chat app ---

# Two Sum's pending Attempt from the Mirror (evals/import-pending-*/mocks), as Import writes it.
imported_pending_two_sum() {
  local dir=problems/leetcode/two-sum
  cat >> "$dir/notes.md" <<'MD'

### 2026-10-14 hash map

- date: 2026-10-14
- mode: session
- outcome: solved-with-hints
- approach: hash map
- mistakes: Planned to return the values instead of their indices; inserted before looking up, so [3, 3] matched an element with itself.
- language: python
- code: 2026-10-14-hash-map.py
- origin: mirror-pending
MD
  cat > "$dir/2026-10-14-hash-map.py" <<'PY'
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []
PY
}
