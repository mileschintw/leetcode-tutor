# Practice Workspace

How the tutor finds or creates the learner's Practice Workspace at the start of a Session, and records the Attempt at the end. The file format is in [practice-log.md](practice-log.md).

## Contents

- The practice-log CLI
- Start of a Session: find the workspace
- Returning to a Problem
- End of a Session: record the Attempt

## The practice-log CLI

Run it with the command given in `SKILL.md`. Its subcommands:

- `init [folder]`: create a Practice Workspace in a new or empty folder (default: the current one).
- `validate [--root folder]`: check a workspace against the schema. It prints each error and exits non-zero on failure.
- `index [--root folder]`: regenerate the workspace's index, `README.md`, from the Practice Log.
- `review-sheet [--root folder] [--id ID] [--tag TAG] [--list NAME] [--title TITLE] [--output file]`: write a Review Sheet of the Problems matching the filters (see [review-sheet.md](review-sheet.md)).

## Start of a Session: find the workspace

Do this before the first reply of a Session. First check your tool list. You are on a chat platform when, among the tools you can call in this conversation, none creates or edits files and none runs shell commands; tools that only read or search files don't count, and neither does a temporary sandbox that is gone after the conversation. On one, skip this section, teach the Session as usual, offer no workspace, and record the Attempt as [chat-platforms.md](chat-platforms.md) says.

1. Look for `practice-log.json` in the current folder and its parent folders. The folder holding it is the Practice Workspace: reply as usual.
2. When there is none, open your reply with a short note, then continue with it as usual (the First Response, or Recap Mode). The note says that this folder isn't a Practice Workspace, so the Attempt won't be saved, and offers the way to fix it:
   - **Their existing workspace,** when you know where it is (they told you, or your memory records it): name its path and suggest reopening you there.
   - **Otherwise, a new one:** offer to create it here when the current folder is empty (nothing but `.git`, `.claude`, `.obsidian` or `.vscode`), or in a new folder (suggest `~/practice-log`) when it holds anything else, such as an unrelated project.

   Phrase the offer as something the learner can take up at any time, so the reply still ends on its one question.
3. When the learner accepts, run `init` in the chosen folder, then `git init` in it when git is installed, and say they can push it to GitHub as their own repository. Create nothing before they accept. When the workspace is in another folder, read and write it by path for the rest of the Session.
4. When the Session ends without a workspace, make the offer once more (never on a chat platform). If the learner declines, show the Attempt block from [chat-platforms.md](chat-platforms.md) instead of writing it.

## Returning to a Problem

Once you know the Problem ID, read `problems/<source>/<slug>/notes.md` directly by its path inside the workspace folder (the one holding `practice-log.json`), such as `problems/leetcode/two-sum/notes.md` when the workspace is the current folder. Only a failed read means the Problem is new; don't conclude that from a search. When it exists, read it before you reply, and build on it instead of starting cold:

- Open with one or two lines on the history: how many Attempts, the last one's date, outcome and mistakes, and the Need Review mark with its reason when set. Don't quote the Key Takeaway: it is what the learner should recall.
- In a full Session, still give the First Response, but point at the parts where their past mistakes were, and offer Recap Mode as a faster option.
- In Recap Mode, use the stored Key Takeaway to check the learner's recall (see [modes.md](modes.md)).

## End of a Session: record the Attempt

Record an Attempt once the Session ends: after Phase 4, after the Recap Mode recall, or when the learner stops early. On a chat platform, do steps 1 to 3, then finish as [chat-platforms.md](chat-platforms.md) says, offering no workspace. Otherwise work through every step:

1. **Key Takeaway.** Write it in one or two sentences (see the Key Takeaway section of [teaching-flow.md](teaching-flow.md)) and ask whether the learner wants to add or change anything. Wait for the answer. Skip the question when the learner has already said there is nothing to add.
2. **Code.** Take the learner's final code from the chat, or from the file they kept in the Problem's folder. If neither exists, ask them to paste it.
3. **Fields.** Fill every Attempt field from what you observed in the Session; the learner never has to reconstruct them:
   - `outcome` follows the definitions in [practice-log.md](practice-log.md): any hint, correction or pseudocode review makes it `solved-with-hints`.
   - `mode` is `recap` for Recap Mode, otherwise `session`. A recap's `outcome` and code follow [modes.md](modes.md).
   - `mistakes` names each concrete slip you saw, in one line: wrong ideas, bugs, missed edge cases. Write `none` only when there truly were none.
4. **Write.** In `problems/<source>/<slug>/`:
   - Create `notes.md` when the Problem is new, with its Problem fields; otherwise keep its fields as they are. Set or clear `need_review` and `need_review_reason` as [need-review.md](need-review.md) says.
   - Put the Key Takeaway under `## Key Takeaway`, replacing an older one only when the learner's new wording is sharper.
   - Append the Attempt under `## Attempts`.
   - Save the code as the Attempt's code file. Code from a file in the folder moves to that name.
5. **Validate.** Run `validate` on the workspace and fix every error it reports. Without a shell, check the files against [practice-log.md](practice-log.md) yourself.
   With a shell, then run `index` on the workspace to regenerate its README.md, the index of the Practice Log.
6. **Summary.** Open with "Attempt saved to" and the notes path, then show what you wrote in a few lines: the outcome, approach, mistakes, Key Takeaway and Need Review (with its reason when set). End by inviting the learner to correct anything in the record, not just one field.
7. **Mirror.** When `practice-log.json` has a `mirror.notion_database_id`, or the learner has asked for a Notion Mirror before (in this conversation, or your memory records it), the summary's closing line also asks whether to push to the Mirror now; on yes, push with the `practice-log-mirror` skill. For every other learner, the summary ends on the invitation alone.
