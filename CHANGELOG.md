# Changelog

All notable changes are documented here. Versions before v3.0 were a copy-paste prompt; their history is in [leetcode-tutor-prompt](https://github.com/mileschintw/leetcode-tutor-prompt/blob/main/CHANGELOG.md).

---

## [v3.0.1] — 2026-10-16

### Added
- **Project-scope install for Codex, Cursor and Antigravity.** The README now recommends keeping the skills to your Practice Workspace on every agent tool, not only Claude Code: unzip `leetcode-tutor-agents-skills.zip` into the workspace's folder, where all three tools read `.agents/skills/`.

### Changed
- `leetcode-tutor-agents-skills.zip` now carries all three skills (the tutor, Import and the Mirror) side by side, instead of the tutor alone.
- `init` also treats a folder holding only `.agents` or `.cursor` (besides `.git`, `.claude`, `.obsidian` and `.vscode`) as empty, so a project-scope install doesn't block setting up the workspace.

---

## [v3.0] — 2026-10-16

### The "Practice Log" Release

v2 was a system prompt pasted into a chat, so every chat started from zero: the tutor didn't know which Problems you had done, where you hit a wall or what Key Takeaway you wrote last time. v3 rebuilds the tutor as installable agent skills that keep a Practice Log you own, in a git repository, and can bring in the records you kept before. The teaching method (First Response, four phases, Key Takeaway, Recap Mode) carries over from v2.

### Added
- **Agent skills, one plugin.** `leetcode-tutor`, `practice-log-import` and `practice-log-mirror`, installable in Claude Code from this repository's marketplace.
- **Practice Workspace and Attempt recording.** The tutor offers to create a workspace (a git repository with one folder per Problem) and, at the end of every Session, records the Attempt: outcome, approach, the mistakes it saw, language and code, plus the Key Takeaway. It builds on your past Attempts when you return to a Problem.
- **Need Review.** Set automatically when you saw the solution, asked for a skeleton or jumped to the conclusion, with the reason; cleared when you say so or solve the Problem on your own later. Recap Mode never clears it.
- **Review Sheets.** Name a goal (a company, topics, a Problem List) and get a sheet of matching Problems with their Key Takeaways, approaches and past mistakes, which ones to redo, and suggestions you haven't done yet. Saved in the workspace.
- **Generated index README** listing Problems by Problem List and topic, readable on GitHub from any device. The workspace also opens as an Obsidian vault, and the README explains how to use it there.
- **Project-scope install** for a Practice Workspace, so the skills load only there.
- **Import of Legacy Records** from Notion, LeetHub or anything else, merged by Problem ID with a preview before anything is written. Re-running an import adds nothing new.
- **One-way Notion Mirror** in its own database, one page per Problem linking to its folder on GitHub. Columns run Lists, Difficulty, Problem, Tags, with coloured options, the most recently practised Problems first, and a By Date calendar.
- **Mirror without a connector:** `practice-log mirror-push` writes the Mirror through Notion's API with your own integration token (`NOTION_TOKEN`), and `mirror-pending` lets Import bring pending pages home the same way. `--changed` pushes only the pages that changed since the last push.
- **Chat-platform fallback.** On claude.ai, the Gemini app or ChatGPT the tutor teaches the same way, then prints an Attempt block for you to keep, or writes a pending Attempt to the Mirror for the next Import to bring home. It finds the Mirror by the GitHub repository it belongs to, and Import warns about pending pages left in any other database.
- **Multi-platform packaging** from one build: manifests for Codex, Cursor and Antigravity, upload zips for claude.ai and the Gemini app / Perplexity, and the copy-paste prompt in [prompts/leetcode-tutor.md](./prompts/leetcode-tutor.md).
- **`practice-log` CLI** (Python standard library only) behind the skills: `init`, `validate`, `index`, `review-sheet`, `mirror-plan`, `mirror-record`, `mirror-push`, `mirror-pending` and the maintainer's `build`.

### Changed
- Instructions are now English only; the tutor replies in the language you write in, so the separate zh-TW prompt is gone.
- By default you write and run your code on your judge platform (LeetCode, NeetCode). The tutor writes and runs local tests only for paywalled or self-authored Problems.
- The copy-paste prompt is generated from the skill instead of maintained by hand.

### Removed
- LeetHub runtime and memory figures are not imported: the Practice Log doesn't store them.
