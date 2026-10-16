# Review Sheet

How the tutor turns a learner's goal into a Review Sheet: a digest of the Problems they have done that fit the goal, with which to redo, plus suggestions for Problems not done yet. There is no schedule: the sheet says what to look at, not when.

## Contents

- When to use it
- No goal: suggest what to practise next
- Building the sheet
- The sheet's format
- After the sheet: start a Recap

## When to use it

The learner names a goal rather than one Problem: an upcoming interview, a company, topics ("graphs"), a Problem List, or a handful of Problems to go over. When they name a single Problem to recap, use Recap Mode instead (see [modes.md](modes.md)).

Find the Practice Workspace first, as the start of [practice-workspace.md](practice-workspace.md) says. Without one there is no Practice Log to build from: say so in a line, offer to create it as that file says (on a chat platform, offer none), and give suggestions as in the next section.

## No goal: suggest what to practise next

When the learner asks what to practise without a goal, don't build or save a sheet. Read the workspace's README.md (or the notes) and suggest, in chat, two or three Problems: Need Review Problems first, then Problems not done yet that fill a gap next to what they have done (a Problem List they are working through, a topic with few Problems). Give each one line on why, and end by asking which one to start.

## Building the sheet

1. **Turn the goal into filters.** Read the workspace's README.md: its "By Problem List" and "By Topic" sections name every Problem List and tag in the Practice Log. Without a README, read the `tags` and `lists` in the notes. Choose filters from those exact names:
   - `--tag` for each topic in the goal, including the closely related tags the workspace uses (for "graphs": `graph`, `topological-sort`, `breadth-first-search`, `depth-first-search`, `union-find`, whichever exist).
   - `--list` for a named Problem List, or a list named after the company when one exists.
   - **A company with no list of its own:** use the tags of the topics that company is known to ask about, and say in the reply that they are your guess, so the learner can correct them. When you can't guess, ask once which topics or Problems to include, and build nothing until they answer.
   - `--id` for Problems the learner names.

   Values of one kind match any of them; different kinds must all match, so `--list "Grind 75" --tag graph` means the Grind 75 Problems tagged graph. Every filter matches regardless of case; Problem IDs are written in lowercase in the notes.
2. **Choose the file.** `review-sheets/<date>-<goal slug>.md` in the workspace, with today's date and a short slug of the goal (`review-sheets/2026-10-15-graphs.md`). If that file exists, add `-2`, `-3` and so on before `.md`.
3. **Write the sheet.**
   - **With a shell,** use the command given in `SKILL.md`. First run `review-sheet --root <workspace>` with the filters and no `--output`: it prints the sheet, and a line on stderr for each filter value no Problem has. Fix a misspelt value or drop it, and repeat until no such line remains. Then run it once more with `--title "<the goal, in the learner's words>" --output <file>`, which writes the file; `--output` must name a file inside `review-sheets/`, and is never overwritten.
   - **Without a shell,** read every `problems/<source>/<slug>/notes.md` and write the same document yourself, exactly as "The sheet's format" says.
4. **Add suggestions.** Append a `## Suggestions` section to the file: three to six well-known Problems that fit the goal and are not in the Practice Log (no `problems/<source>/<slug>/` folder for their ID). Prefer Problems from a Problem List the learner uses. One line each:

   ```markdown
   - [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) `leetcode:course-schedule-ii` · Medium: <why it fits the goal, in one short clause>
   ```

   When every relevant Problem is already done, write one line saying so instead.
5. **Index.** Nothing to run: the workspace's README.md lists Problems, not Review Sheets, so saving a sheet changes nothing it shows.
6. **Mirror.** Offer a push exactly when step 7 of "End of a Session" in [practice-workspace.md](practice-workspace.md) would: when `practice-log.json` has a `mirror.notion_database_id`, or the learner has asked for a Notion Mirror before. The Mirror holds Problems, not Review Sheets, so the push carries the Practice Log as it is now, which keeps Notion current while they review. Push nothing yet: the reply asks (next step), and on yes you push with the `practice-log-mirror` skill. For every other learner, don't mention the Mirror.
7. **Reply.** Open with "Review Sheet saved to" and the file's path. Then, in a few lines: the filters you chose, the Problems to redo with their reason, and the suggestions. End on one question only: which Problem to start with. When step 6 offers a push, the same closing question also asks whether to push to the Mirror first, such as "Which one do you want to start with, and shall I push your Practice Log to the Notion Mirror before we begin?" Make it a question, not a remark that you could push. Don't ask yet whether they want a recap or a full Session; that comes once they pick (see the last section).

## The sheet's format

This is what `review-sheet` writes; write the same when you build a sheet by hand. Keep its English headings and labels, so every sheet has the same shape; your own text (the title, the suggestions' reasons) is in the learner's language.

```markdown
# <title>

<!-- Generated by `practice-log review-sheet` from the Practice Log. -->

Filters: tags graph, topological-sort.
4 Problems, 2 to redo.

## Redo

### [Number of Islands](../problems/leetcode/number-of-islands/notes.md)

`leetcode:number-of-islands` · Medium

- **Redo:** Need Review: Asked for the solution on 2026-09-20.
- **Key Takeaway:** <the notes' Key Takeaway, or "none recorded">
- **Approaches:** dfs flood fill (2026-09-20, session, saw-solution); bfs flood fill (2026-10-05, session, solved-with-hints)
- **Past mistakes:**
  - 2026-09-20: <the Attempt's mistakes>
- **Tags:** array, graph · **Problem Lists:** Grind 75

## Refresh

<the other selected Problems, in the same shape without the Redo line>
```

- **Selected:** every Problem matching the filters. With none, the line after the counts is `No Problems in the Practice Log match.` and there are no `## Redo` or `## Refresh` sections.
- **Redo:** a Problem goes under `## Redo` when it is Need Review (`Need Review: <reason>`), or else when an Attempt's outcome is `saw-solution` and no later `mode: session` Attempt was `solved-alone` (`Saw the solution on <date>, not solved alone since`). Imported Attempts can be `saw-solution` without Need Review, which is why both count. Every other Problem goes under `## Refresh`.
- **Order:** by title within each section. Attempts oldest first by date.
- **Links:** to the Problem's `notes.md`, relative to the sheet (Obsidian cannot link to a folder).
- **Approaches:** every Attempt as `approach (date, mode, outcome)`, or `no Attempts yet`.
- **Key Takeaway:** as written. One line stays on the bullet; a longer one goes on the lines below it, indented.
- **Past mistakes:** each Attempt's `mistakes` other than `none`, with its date, or `none recorded`, both when every Attempt says `none` and when none says anything.

The sheet is the learner's file once written: they may edit it, and the tutor never rewrites an existing sheet.

## After the sheet: start a Recap

When the learner picks a Problem from the sheet, start on it straight away:

- **A sheet entry** (under Redo or Refresh): follow Recap Mode in [modes.md](modes.md), using that Problem's notes as "Returning to a Problem" in [practice-workspace.md](practice-workspace.md) says. For a Redo entry, add one line in that first reply that a Recap won't take it off the redo list (nor clear Need Review): only a full Session solved alone does (see [need-review.md](need-review.md)), so they can switch to a full Session instead.
- **A suggestion:** it is a new Problem: give the First Response (see [first-response.md](first-response.md)).

Either way, the Session ends by recording an Attempt as usual.
