# LeetCode Tutor

A Socratic tutor for coding-interview problems that teaches the reasoning behind a solution, and keeps a lasting record of what the learner has practised so it can be reviewed later.

## Language

### Practice

**Problem**:
A single coding exercise the learner works on. It may come from LeetCode or any other source, including self-authored exercises with their own test harness.
_Avoid_: Question, LeetCode problem (when the source isn't known to be LeetCode)

**Problem ID**:
The identity of a Problem, written `<source>:<slug>` (e.g. `leetcode:two-sum`, `custom:lru-cache`). Two records with the same Problem ID are the same Problem.
_Avoid_: Problem number, title

**Problem List**:
A curated set of Problems the learner studies from, such as Grind 75 or NeetCode 150. A Problem can belong to several.
_Avoid_: Collection, study plan, sheet

**Need Review**:
A mark on a Problem meaning the learner hit a wall on it and did not truly own the solution (e.g. asked for a skeleton or jumped to the answer).
_Avoid_: Status, starred, weak

**Attempt**:
The outcome of one Session on a Problem. A Problem has many Attempts over time.
_Avoid_: Submission, try, run

**Session**:
One tutoring conversation about one Problem, from the First Response through the Key Takeaway.
_Avoid_: Chat, lesson

**First Response**:
The fixed, structured overview the tutor gives at the start of a Session on a new Problem, before any Socratic back-and-forth.
_Avoid_: Intro, summary

**Key Takeaway**:
The one memorable sentence that distils a Problem's solution, used later as a retrieval cue.
_Avoid_: Summary, lesson learned

**Recap Mode**:
The fast-track variant of a Session for a Problem the learner says they already know: a short overview, then the learner recalls the Key Takeaway.
_Avoid_: Review mode, "I know this" mode

**Review Sheet**:
A quick-reference digest of Problems the learner chose for a goal (an upcoming interview, a topic), built from the Practice Log: each Problem's Key Takeaway, approach and past mistakes.
_Avoid_: Cheat sheet, review plan, schedule

### Records

**Chat platform**:
Anywhere the tutor runs without a folder it can save to: a chat app such as claude.ai, the Gemini app or ChatGPT, or the tutor pasted in as a prompt. It teaches fully there, and hands each Attempt over as a pending Mirror page or a printed Attempt block for the next Import.
_Avoid_: No-filesystem mode, chat-only mode

**Practice Log**:
The learner's own durable history of Problems they have practised, owned by the learner rather than by the tutor.
_Avoid_: History, progress, database

**Practice Workspace**:
A repository the learner owns that holds their Practice Log together with their solutions and tests for each Problem.
_Avoid_: Practice repo, LeetCode repo

**Mirror**:
A read-only copy of the Practice Log published to another tool (e.g. Notion) for browsing. Changes flow from the Practice Log to the Mirror, never back; the one exception is an Attempt written to it as pending from a chat platform, which only Import brings back.
_Avoid_: Sync, backup, backend

**Legacy Record**:
Practice history the learner kept before the Practice Log existed, in any format or tool (e.g. Notion pages, a LeetHub repo).
_Avoid_: Old notes, backup

**Import**:
Turning Legacy Records into Practice Log entries. It also brings home Attempts the tutor wrote to the Mirror as pending from a chat platform with no filesystem.
_Avoid_: Migration, sync
