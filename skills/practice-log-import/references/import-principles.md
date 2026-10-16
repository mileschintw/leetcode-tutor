# Import principles

How to turn Legacy Records into Problems and Attempts. They apply to every source; nothing here is specific to one tool. The target format is the `leetcode-tutor` skill's Practice Log schema.

## Contents

- Problems
- Problem fields
- Attempts
- Merging and re-runs
- Uncertain matches
- Preview

## Problems

- **Problem ID first.** Give every record its Problem ID, `<source>:<slug>`, before mapping anything else. Take the slug from the Problem's URL when the record has one (`leetcode.com/problems/two-sum/` → `leetcode:two-sum`); otherwise from a folder or file name that carries it (`0001-two-sum` → `leetcode:two-sum`, dropping the number); otherwise from the title. A record you can't tie to one Problem ID with confidence is an uncertain match.
- **One Problem per ID.** Records from any number of sources with the same Problem ID become one Problem.

## Problem fields

- **Ambiguous field names.** Map a field when its name or values make its meaning clear (`Level: Easy` is the difficulty). Ask the learner once, in one message, about the rest. Fields with no place in the schema, such as a status, a done checkbox, an attempt counter or created and updated times, are dropped: the Attempt count comes from the log and times come from git.
- **title:** as the source writes it, without a leading problem number (`1. Two Sum` → `Two Sum`).
- **difficulty:** `easy`, `medium` or `hard`, lowercase; empty when the source has none.
- **tags:** algorithm and data-structure tags only, lowercase and hyphenated (`Hash Table` → `hash-table`). Drop every other tag: contest names and weeks (`Weekly Contest 350`), job levels (`L4`), companies, statuses and personal labels.
- **lists:** a collection, folder or study-plan field becomes `lists`, each value kept as the learner wrote it (`Grind169` stays `Grind169`).
- **List style:** write `tags` and `lists` as flow lists, `[a, b]`, and an empty one as `[]`.
- **need_review:** a review flag that is set (a checkbox, a "review" tag) becomes `need_review: true` with `need_review_reason: Marked for review in <source> before import`. Otherwise `false`.
- **Key Takeaway:** a callout, summary or "takeaway" note on the Problem becomes the Key Takeaway, word for word apart from a label such as `Key Takeaway:`. Never write one yourself: leave the section empty when no source has one.

## Attempts

- **What counts as an Attempt.** Every dated entry about solving the Problem: a dated toggle or heading with an approach or code, a committed solution, a dated row. One entry, one Attempt.
- **date:** from the entry itself. When the source has no other dates, take the date of the commit that added or last changed the solution file in its git history, as `git log --date=short` prints it. An entry with no date anywhere is an uncertain match.
- **origin:** the source's name, lowercase and hyphenated (`notion`, `leethub`). Attempts written to the Mirror from a chat app and marked pending come back with `origin: mirror-pending`.
- **mode:** `session`.
- **outcome:** take it from the record when it says (`saw solution`, `with hints`). When it doesn't, use `solved-alone` and say so in the preview so the learner can change it.
- **approach:** the entry's own approach name, lowercased. When there is none, name the approach from the code in two or three words (`hash map`, `two pointers`).
- **mistakes:** from the entry's own notes on what went wrong; leave the line out when there are none. Runtime and memory figures (`Time: 3 ms (98%)`) have no field; drop them.
- **language:** from the code fence or the file extension, lowercase (`python`, `cpp`).
- **code:** every Attempt needs its code in its own file, `<date>-<approach slug>.<ext>`, with `-2`, `-3` before the extension when the name is taken. Copy the code exactly. An entry with no code is an uncertain match.
- **Order.** Keep the Attempt log oldest first, putting imported Attempts among the existing ones by date. The heading is `### <date> <approach>`, then the `- key: value` lines.

## Merging and re-runs

- **Merge by Problem ID.** When the workspace already has the Problem, add the new Attempts to its log and keep every existing Attempt and field. Add new `tags` and `lists` values to the existing ones. Set `need_review` to `true` when a source flags it; never clear it during import. Fill an empty Key Takeaway; when the Problem already has a different one, keep it and show the imported one in the preview so the learner can choose.
- **Keep every Attempt.** The same Problem from two sources keeps the Attempts of both, each with its own `origin`, even on the same date.
- **Idempotent.** An Attempt is already imported when the Problem has an Attempt with the same `origin` and `date` (and, when several share them, the same code). Skip it, and skip Problem field changes that are already there. Running the same import again adds nothing and writes nothing.

## Uncertain matches

List, rather than import, every record you can't place with confidence, and say why: two records that may be the same Problem under different IDs (a NeetCode copy of a LeetCode Problem, a renamed title), a record with no Problem ID, date or code. The learner decides each one; import it only after they do.

## Preview

Before writing, show:

- **Totals:** Problems to create, Problems to merge into, Attempts to add per origin, and records skipped as already imported.
- **Per Problem:** its Problem ID, whether it is new or merged, the fields it gets (difficulty, tags, lists, need_review and its reason), and each Attempt to add as `date, approach, origin, code file`.
- **Dropped:** the tags and fields you drop, by name.
- **Assumed:** every default you applied, such as `outcome: solved-alone` where the source doesn't say.
- **Uncertain matches**, with the question for each.

End with one question asking the learner to confirm or correct it. When there is nothing new to import, say so instead and write nothing.
