---
name: practice-log-import
description: Imports a learner's Legacy Records (old notes from Notion, LeetHub or any export) and pending Attempts from the Notion Mirror into their Practice Log, merging by Problem ID. 匯入 舊紀錄 刷題紀錄
license: MIT
metadata:
  requires: leetcode-tutor
---

# Practice Log Import

You bring the learner's Legacy Records (practice history kept before the Practice Log, in Notion, a LeetHub repository or anything else) into their Practice Log, and the pending Attempts the tutor wrote to the Mirror from a chat platform. There is no adapter per source: read whatever the records hold and apply the principles in [references/import-principles.md](references/import-principles.md). Read it before you start.

The Practice Log format is defined by the `leetcode-tutor` skill, which is installed next to this one. Read its schema, `../leetcode-tutor/references/practice-log.md` relative to the folder holding this file, before you map anything. This skill needs that one: if the `leetcode-tutor` skill's folder isn't there, ask the learner to install it as well, and import nothing until they have.

## Steps

1. **Find the Practice Workspace.** Look for `practice-log.json` in the current folder and its parent folders. If there is none, ask whether to create one (the `init` command below) or where the existing one is. Create nothing before the learner answers. When they say to create one, run `init` in the chosen folder, then `git init` in it when git is installed, and tell them they can push the workspace to a GitHub repository of their own, which the Mirror needs for its links.
2. **Check for pending Attempts.** Every Import does this, whatever the learner asked to import. When `practice-log.json` has a `mirror.notion_database_id`:
   - **With a Notion connector:** fetch that database, list its pages with `Pending` checked, and fetch each one for its content. They join this import and its preview. Read only those; every other Mirror page is generated from the Practice Log.
   - **Without one:** carry on, and say in the preview (or the reply, when there is nothing to import) that you couldn't check the Mirror for pending Attempts.

   With no Mirror id there is no Mirror to check.
3. **Get the records.** For the records the learner asked for, use whatever access you have, in this order: a connector to the source (a Notion connector, a GitHub connector), a local export or clone the learner points to, then telling the learner how to export or clone it and waiting for them. When you clone a git repository yourself (such as a LeetHub one) on Windows, its repeated slug paths can fail with "Filename too long": clone with `git -c core.longpaths=true clone <url> <folder>`, or into a short path such as `C:\lh`. When a source's dates live only in git history and you can't run `git`, ask the learner to run `git log --date=short --name-only` in it and paste the output.
4. **Map.** Turn every record into Problems and Attempts, following the principles. Ask the learner once, in a single message, about every field whose meaning you can't tell; don't ask about fields you can map with confidence.
5. **Preview.** Show the preview the principles describe and ask the learner to confirm. Write nothing to the workspace before they say yes. If they correct anything, show the changed part again.
6. **Validate.** After the learner confirms, check the result before it touches the workspace:
   - **With a shell:** run `init` in a new temporary folder outside the workspace, copy the workspace's `problems/` folder into it, apply the import there exactly as previewed, and run `validate --root` on that folder. Fix every error, then delete the temporary folder.
   - **Without a shell:** check each notes file you are about to write against the schema yourself: required fields, enum values, dates, `need_review_reason`, and that every `code` names a file you are writing.
7. **Write.** Create or update the Problems in the workspace exactly as previewed. With a shell, run `validate` on the workspace afterwards, then `index` on it to regenerate its README.md, the index of the Practice Log. Without a shell, tell the learner the index is out of date until `index` runs.
   Then move each pending page you imported to Notion's trash, as the preview said, and each one skipped as already imported when the learner agreed to it. Never touch a pending page you listed as an uncertain match.
8. **Report.** Say how many Problems were created and merged, how many Attempts were added from each origin, what was skipped as already imported, how many pending pages were moved to Notion's trash, and the uncertain matches the learner still has to decide.

## The practice-log CLI

The CLI ships with the `leetcode-tutor` skill as `../leetcode-tutor/scripts/practice_log`, relative to the folder holding this file. Run it with Python 3, giving the full path to that folder: `python3 <tutor skill folder>/scripts/practice_log <command>` (`python` on Windows).

- `init [folder]`: create a Practice Workspace in a new or empty folder (one holding nothing but `.git`, `.claude`, `.obsidian` or `.vscode`).
- `validate [--root folder]`: check a workspace against the schema; it prints each error and exits non-zero on failure.
- `index [--root folder]`: regenerate the workspace's README.md from the Practice Log.
