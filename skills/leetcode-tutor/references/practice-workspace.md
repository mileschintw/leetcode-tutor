# Practice Workspace

How the tutor finds or creates the learner's Practice Workspace at the start of a Session, and records the Attempt at the end. The file format is in [practice-log.md](practice-log.md).

## Contents

- The practice-log CLI
- Start of a Session: find the workspace
- End of a Session: record the Attempt

## The practice-log CLI

Run it with the command given in `SKILL.md`. Its subcommands:

- `init [folder]`: create a Practice Workspace in a new or empty folder (default: the current one).
- `validate [--root folder]`: check a workspace against the schema. It prints each error and exits non-zero on failure.

## Start of a Session: find the workspace

Do this before the first reply of a Session. Skip it when you have no file tools (a chat app): teach the Session as usual.

1. Look for `practice-log.json` in the current folder and its parent folders. The folder holding it is the Practice Workspace: reply as usual.
2. When there is none, open your reply with a short note, then continue with it as usual (the First Response, or Recap Mode). The note says that this folder isn't a Practice Workspace, so the Attempt won't be saved, and offers the way to fix it:
   - **Their existing workspace,** when you know where it is (they told you, or your memory records it): name its path and suggest reopening you there.
   - **Otherwise, a new one:** offer to create it here when the current folder is empty, or in a new folder (suggest `~/practice-log`) when it holds anything else, such as an unrelated project.

   Phrase the offer as something the learner can take up at any time, so the reply still ends on its one question.
3. When the learner accepts, run `init` in the chosen folder, then `git init` in it when git is installed, and say they can push it to GitHub as their own repository. Create nothing before they accept. When the workspace is in another folder, read and write it by path for the rest of the Session.
4. When the Session ends without a workspace, make the offer once more. If the learner declines, show the Attempt in chat in the notes format instead of writing it.

## End of a Session: record the Attempt

Record an Attempt once the Session ends: after Phase 4, after the Recap Mode recall, or when the learner stops early. Work through every step:

1. **Key Takeaway.** Write it (see the Key Takeaway section of [teaching-flow.md](teaching-flow.md)) and ask whether the learner wants to add or change anything. Wait for the answer. Skip the question when the learner has already said there is nothing to add.
2. **Code.** Take the learner's final code from the chat, or from the file they kept in the Problem's folder. If neither exists, ask them to paste it.
3. **Fields.** Fill every Attempt field from what you observed in the Session; the learner never has to reconstruct them:
   - `outcome` follows the definitions in [practice-log.md](practice-log.md): any hint, correction or pseudocode review makes it `solved-with-hints`.
   - `mode` is `recap` for Recap Mode, otherwise `session`.
   - `mistakes` names each concrete slip you saw, in one line: wrong ideas, bugs, missed edge cases. Write `none` only when there truly were none.
4. **Write.** In `problems/<source>/<slug>/`:
   - Create `notes.md` when the Problem is new, with its Problem fields and `need_review: false`; otherwise keep its fields as they are.
   - Put the Key Takeaway under `## Key Takeaway`, replacing an older one only when the learner's new wording is sharper.
   - Append the Attempt under `## Attempts`.
   - Save the code as the Attempt's code file. Code from a file in the folder moves to that name.
5. **Validate.** Run `validate` on the workspace and fix every error it reports. Without a shell, check the files against [practice-log.md](practice-log.md) yourself.
   Then run `index` on the workspace to regenerate its README.md, the index of the Practice Log.
6. **Summary.** Show what you wrote in a few lines: the notes path, outcome, approach, mistakes and Key Takeaway. Invite the learner to correct anything.
