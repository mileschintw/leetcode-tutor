# Need Review

When the tutor marks a Problem Need Review, when it clears the mark, and how it is stored. The fields are `need_review` and `need_review_reason` in the Problem's `notes.md` (see [practice-log.md](practice-log.md)).

## Contents

- Setting it
- Clearing it
- By hand
- Where it is written

## Setting it

Set Need Review when any of these happen in a Session:

- **Saw the solution:** the learner asked for the solution, or you showed it, before they solved it.
- **Asked for a skeleton:** the learner asked for a code skeleton or template of the solution.
- **Jumped to the conclusion:** the learner asked you to skip ahead and tell them the approach or answer instead of working it out.

When the learner explicitly asks for one of these, give it: it is their call. In the same reply, tell them in one line that the Problem will be marked Need Review and why, so they can object if you misread them.

Each trigger makes the Attempt's `outcome` `saw-solution`, sets `need_review: true`, and sets `need_review_reason` to one line naming the trigger and the day, such as `Asked for a code skeleton on 2026-10-15.` A new reason replaces the old one.

In Recap Mode, writing the solution after the learner's recall is part of the mode and sets nothing; only failing to recall the Key Takeaway does (see [modes.md](modes.md)).

## Clearing it

Clear Need Review, setting `need_review: false` and an empty `need_review_reason`, when either happens:

- A later Attempt's outcome is `solved-alone`, in either mode.
- The learner says they have it now ("I've got this one", "you can clear it"). Ask once to confirm if it is unclear which Problem they mean.

A `solved-with-hints` Attempt keeps the mark as it is.

## By hand

The learner has the final say. When they ask to set or clear Need Review on a Problem, at any time and for any Problem in the workspace, do it right away in that Problem's `notes.md`. When setting it, use their reason or ask for one in a few words. Then, with a shell, run `validate` and `index` on the workspace, so its README.md shows the new mark.

## Where it is written

Update the two fields when you record the Attempt (see the end-of-Session steps in [practice-workspace.md](practice-workspace.md)), and include the mark and its reason in the summary you show the learner, saying whether it was set, cleared or unchanged.
