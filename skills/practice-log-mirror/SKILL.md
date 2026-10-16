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
   - With no GitHub remote, explain that the Mirror's pages link to the workspace on GitHub, so it has to be pushed to a GitHub repository first: create an empty repository on GitHub, then `git remote add origin <its URL>` and `git push -u origin main` in the workspace. Push nothing to Notion until it is there.
   - Links show what is on GitHub. With a shell, when `git status -sb` shows the workspace ahead of `origin`, suggest `git push` first.
4. **Plan.** The plan is every page the Mirror should hold, as [references/mirror-pages.md](references/mirror-pages.md) defines it. With a shell, run `validate`, fix every error, then run `mirror-plan` and use its output exactly. Without a shell, read the reference and build the same plan from the notes yourself.
5. **Database.** Push only into the database this skill created, whose id is `mirror.notion_database_id` in `practice-log.json`:
   - **Id stored:** fetch that database and reuse it. When it is gone or your connector can't reach it, say so and ask whether to create a new one; create nothing before the learner answers.
   - **No id (first push):** tell the learner that the Mirror is a new Notion database you create and regenerate on every push, so they should edit their notes in the workspace, never in Notion. Then create a new database with the plan's title, description and properties, inside a page the learner names or wherever your connector puts new pages. Store its id in `mirror.notion_database_id` straight away, before writing any page, so a failed push never leaves a second database behind.
   - **The learner's own database:** when the learner points you at a database they already have, such as old practice notes, write nothing into it. The Mirror always gets its own database; offer to bring the old one in with the `practice-log-import` skill, after which they can keep or archive it.
6. **Write the pages.** List the database's pages and match them to the plan by `Problem ID`:
   - **In the plan:** set every property to the plan's value and replace the page's whole content with the plan's body. A page already identical to the plan may be left as it is. Create the page when the database has none for that Problem ID.
   - **`Pending` checked:** an Attempt written to the Mirror from a chat app, waiting for the next Import to bring it home. Leave it untouched and mention how many there are.
   - **Not in the plan:** a Problem no longer in the Practice Log, or a duplicate. List them and ask before moving them to Notion's trash.
7. **Report.** Say how many pages were created and updated, link the database, and end with this warning in the learner's language: the Mirror is regenerated from the Practice Log on every push, so edits made in Notion are overwritten; change the notes in the Practice Workspace instead.

## The practice-log CLI

The CLI ships with the `leetcode-tutor` skill as `../leetcode-tutor/scripts/practice_log`, relative to the folder holding this file. Run it with Python 3, giving the full path to that folder: `python3 <tutor skill folder>/scripts/practice_log <command>` (`python` on Windows).

- `validate [--root folder]`: check a workspace against the schema; it prints each error and exits non-zero on failure.
- `mirror-plan [--root folder]`: print the plan as JSON. It reads only the workspace and never talks to Notion.
