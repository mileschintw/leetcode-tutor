---
name: practice-log-mirror
description: Pushes a learner's Practice Log to Notion as a one-way Mirror, a database it creates and regenerates on every push. Use when the learner asks to push, publish or sync to Notion. 同步 Notion
license: MIT
metadata:
  requires: leetcode-tutor
---

# Practice Log Mirror

You publish the learner's Practice Log to Notion as a Mirror: a database this skill creates and owns, with one page per Problem, each linking back to the Problem's folder on GitHub. The Mirror is one-way. The Practice Workspace is the only place the learner edits; every push regenerates every page from it, so edits made in Notion are overwritten.

The Practice Log format is defined by the `leetcode-tutor` skill, which is installed next to this one. This skill needs that one: if the `leetcode-tutor` skill's folder (`../leetcode-tutor/` relative to the folder holding this file) isn't there, ask the learner to install it as well, and push nothing until they have.

## Steps

1. **Find the Practice Workspace.** Look for `practice-log.json` in the current folder and its parent folders. If there is none, tell the learner the Mirror is published from a Practice Workspace and ask where theirs is.
2. **Check for Notion.** You need a Notion connector (MCP tools) that can create databases and pages. Without one, tell the learner to connect Notion to this app and ask again, and stop.
3. **GitHub repository.** Every page links to the workspace on GitHub, so the Mirror needs `"repository"` under `"mirror"` in `practice-log.json`.
   - When it is missing, read the workspace's `origin` remote: `git remote get-url origin` with a shell, otherwise the `url` under `[remote "origin"]` in `.git/config`. When it is a GitHub repository, write it to `mirror.repository` as `https://github.com/<owner>/<repo>`, keeping the rest of the file as it is.
   - With no GitHub remote, explain that the Mirror's pages link to the workspace on GitHub, so it has to be pushed to a GitHub repository first: create an empty repository on GitHub, then `git remote add origin <its URL>` and `git push -u origin HEAD` in the workspace. Push nothing to Notion until it is there.
   - Links show what is on GitHub. With a shell, when `git status -sb` shows the workspace ahead of `origin`, suggest `git push` first.
4. **Plan.** The plan is every page the Mirror should hold, as [references/mirror-pages.md](references/mirror-pages.md) defines it. With a shell, run `validate`, fix every error, then run `mirror-plan` and use its output exactly. Without a shell, read the reference and build the same plan from the notes yourself.
5. **Database.** Push only into the database this skill created, whose id is `mirror.notion_database_id` in `practice-log.json`:
   - **Id stored:** fetch that database and reuse it, whatever its title now: the learner may rename or move it. When it is gone or your connector can't reach it, say so and ask whether to create a new one; create nothing before the learner answers.
     Then compare its properties with the plan's. When `Problem ID` or `Pending` is missing (renamed or deleted), stop before writing anything: without `Problem ID` no page can be matched, so every page would be duplicated, and without `Pending` a push can't tell the pending pages it must leave alone. Name the missing property and ask the learner to rename it back in Notion, then push again. When it was deleted, its values are gone: offer a fresh Mirror instead, created as on a first push with its id replacing the stored one, after first bringing any pending pages home with the `practice-log-import` skill. When any other property is missing, say which, and offer to add it back with the plan's type before writing the pages.
   - **No id (first push):** tell the learner that the Mirror is a new Notion database you create and regenerate on every push, so they should edit their notes in the workspace, never in Notion. Then create a new database with the plan's title, description and properties, inside a page the learner names or wherever your connector puts new pages. Store its id in `mirror.notion_database_id` straight away, before writing any page, so a failed push never leaves a second database behind.
   - **The learner's own database:** when the learner points you at a database they already have, such as old practice notes, write nothing into it, because every push rewrites the database it writes to. Push into the Mirror's own database instead, as the two cases above say, creating it when there is no id yet, and tell the learner you did so. Then offer to bring the old database's records in with the `practice-log-import` skill, after which they can keep or archive it.
6. **Write the pages.** First make the data source's Tags and Lists options cover every value in the plan, as the Writing values section of [references/mirror-pages.md](references/mirror-pages.md) says (`notion-update-data-source`): Notion rejects a page whose multi-select value isn't an existing option, and a new database has none. Do this before the first page write of every push, keeping the options already there. Then list every page in the database (with Notion's own connector: fetch the database for its data source, then query that data source). Then:
   - **`Pending` checked:** an Attempt written to the Mirror from a chat platform, waiting for the next Import to bring it home. Set these pages aside first. A push never updates, moves or trashes a pending page, even when its Problem ID is in the plan, and never counts it as a duplicate. Mention how many there are, and offer to bring them into the Practice Log with the `practice-log-import` skill.
   - **In the plan:** match each remaining page to the plan by `Problem ID`. Update it in place: set every property to the plan's value and replace the page's whole content with the plan's body. A page already identical to the plan may be left as it is. Create a page only for a Problem ID that has no page yet.
   - **Not in the plan:** a Problem no longer in the Practice Log, or a second page for the same Problem ID. List them and ask before moving them to Notion's trash.
7. **Report.** Say how many pages were created and updated, link the database, and end with this warning in the learner's language: the Mirror is regenerated from the Practice Log on every push, so edits made in Notion are overwritten; change the notes in the Practice Workspace instead.

## The practice-log CLI

The CLI ships with the `leetcode-tutor` skill as `../leetcode-tutor/scripts/practice_log`, relative to the folder holding this file. Run it with Python 3, giving the full path to that folder: `python3 <tutor skill folder>/scripts/practice_log <command>` (`python` on Windows).

- `validate [--root folder]`: check a workspace against the schema; it prints each error and exits non-zero on failure.
- `mirror-plan [--root folder]`: print the plan as JSON. It reads only the workspace and never talks to Notion.
