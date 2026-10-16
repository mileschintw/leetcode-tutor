# LeetCode Tutor

A Socratic coding-interview tutor, packaged as agent skills, that keeps a practice log you own.

v3.0 is the current version (see the [CHANGELOG](./CHANGELOG.md)). It succeeds the copy-paste prompt in [leetcode-tutor-prompt](https://github.com/mileschintw/leetcode-tutor-prompt) (v2), which is archived.

## Platforms

| Tier | Platforms | What you get |
|------|-----------|--------------|
| Officially tested | Claude Code | All three skills, and a Practice Log saved in your workspace |
| Should work | Codex, Cursor, Antigravity | All three skills, the same as Claude Code |
| Should work | claude.ai, the Gemini app | The tutor skill, uploaded as a zip; no Practice Log of its own (see [Chat apps](#chat-apps)) |
| Prompt only | ChatGPT, Perplexity, anything else | The tutor as a copy-paste prompt; no Practice Log of its own |

"Should work" means the files are built to each platform's documented format but haven't been tested by hand yet.

## Install

### Claude Code

In Claude Code (2.1.275 or later), run:

```
/plugin install leetcode-tutor --marketplace mileschintw/leetcode-tutor
```

On older versions, add the marketplace first:

```
/plugin marketplace add mileschintw/leetcode-tutor
/plugin install leetcode-tutor@leetcode-tutor
```

You also need Python 3 (the skills use a small `practice-log` tool built on its standard library) and git.

### Codex, Cursor and Antigravity

- **Codex:** `codex plugin marketplace add mileschintw/leetcode-tutor`, then install `leetcode-tutor` from the Plugins Directory.
- **Antigravity:** `agy plugin install https://github.com/mileschintw/leetcode-tutor`.
- **Cursor:** add this repo as a plugin (team admins: Dashboard → Plugins & MCPs → Import from Repo), or unzip `leetcode-tutor-agents-skills.zip` from the [latest release](https://github.com/mileschintw/leetcode-tutor/releases/latest) into your project or home directory (the zip holds the tutor skill only; Import and the Mirror need the plugin).

These need Python 3 and git too.

### claude.ai and the Gemini app

Download a zip from the [latest release](https://github.com/mileschintw/leetcode-tutor/releases/latest) and upload it as a skill: `leetcode-tutor-claude-ai.zip` for claude.ai, `leetcode-tutor-gemini-perplexity.zip` for the Gemini app (and for Perplexity, where your plan accepts skill uploads).

### ChatGPT, Perplexity and anything else

Attach [prompts/leetcode-tutor.md](./prompts/leetcode-tutor.md) to a Project as a file, or paste it as your first message. It is too long for most Project instruction fields.

### Updating

- **Claude Code:** `claude plugin marketplace update leetcode-tutor`, then `claude plugin update leetcode-tutor@leetcode-tutor`, and restart Claude Code.
- **Uploads and the prompt:** download the new zip from the latest release, or paste the prompt again.

## Practising

Name a Problem, for example "Let's do LeetCode 1. Two Sum". The tutor starts with a structured overview (the First Response), then guides you with questions instead of answers, from understanding the Problem through strategy and implementation to testing. It doesn't write your solution unless you ask. You write and run your code on LeetCode or NeetCode. For a paywalled or self-authored Problem, the tutor writes and runs local tests, using the Problem's own test harness if it has one. Write in any language: the tutor replies in the language you use.

- **Recap Mode:** say you already know a Problem and you get a short overview, then a prompt to recall your Key Takeaway, instead of a full Session.
- **Need Review:** when you saw the solution, asked for a skeleton or jumped to the conclusion, the tutor marks the Problem Need Review and tells you why. It clears the mark when you say you've got it or when you later solve the Problem on your own in a full Session. You can set or clear it yourself at any time. A Recap never clears it.
- **Review Sheets:** before an interview, name a goal ("Grind 75 graphs", "my Need Review problems", a company) and the tutor builds a Review Sheet. For each matching Problem it gives the Key Takeaway, approach and past mistakes, it flags which ones are worth redoing, and it suggests Problems you haven't done yet. You can start a Recap straight from any Problem on it.
- **What next:** ask what to practise and the tutor suggests Problems from your Practice Log and its gaps.

## Your Practice Log

The tutor keeps your practice in a Practice Workspace, a git repository you own. If you start a Session outside one, it offers to create one for you. At the end of each Session it saves the Attempt there (outcome, approach, the mistakes it saw, your code) with the Key Takeaway, and shows you what it wrote so you can correct it.

```
practice-log.json              workspace settings
README.md                      the generated index: every Problem by Problem List and topic
problems/<source>/<slug>/
  notes.md                     the Problem, its Key Takeaway and the Attempt log
  <date>-<approach>.<ext>      the code from each Attempt
review-sheets/                 saved Review Sheets
```

Push the workspace to GitHub and the index README shows your records on any device. The folder also opens as an [Obsidian](https://obsidian.md) vault, and the index's links lead to each Problem's `notes.md`.

### Importing your old records

To bring in your Legacy Records, the practice history you kept before, ask to import them and name the source: a Notion export or connector, a LeetHub repository, or anything else. The `practice-log-import` skill merges them into your Practice Log by Problem ID, keeping every Attempt and where it came from. It asks once about any field it can't map, shows a preview and writes nothing until you confirm. Running it again adds nothing new.

### The Notion Mirror

To browse your Practice Log in Notion, ask to push it there. The `practice-log-mirror` skill publishes a one-way Mirror through your Notion connector: on first use it creates its own database, and every push regenerates one page per Problem, each linking to the Problem's folder on GitHub. It never touches your old Notion database. Your Practice Workspace has to be on GitHub first. Edits made in Notion are overwritten by the next push, so change your notes in the workspace. Once the Mirror is set up, the tutor asks after each Session and Review Sheet whether to push.

You can rename or move the Mirror database: pushes find it by its id, not its name. In a chat app, though, the tutor finds it by searching for "Practice Log", so after renaming it, give the tutor the database's link. Don't rename or delete its properties, especially `Problem ID` and `Pending`.

The import and mirror skills only work with the tutor skill installed alongside them, which the plugin installs above do. They have no upload zips or prompts of their own.

## Chat apps

On claude.ai, the Gemini app, ChatGPT and other chat apps, the tutor teaches the same way, but it has no folder to save to. At the end of a Session it does one of two things:

- **With a Notion connector and a Mirror:** it writes the Attempt to the Mirror as a pending page.
- **Otherwise:** it prints an Attempt block for you to keep.

The next Import in your Practice Workspace brings pending pages home. Paste an Attempt block into an Import to bring it in too.

## Your data

The skills run no server and collect nothing. Your Practice Log is files in your own repository, and the `practice-log` tool only reads and writes files on your machine. Notion is reached only through your own Notion connector, and only when you ask for an Import or a Mirror push, or when the tutor saves a pending Attempt in a chat app. Import moves the pending pages it brought in to Notion's trash, and a push asks before trashing pages for Problems no longer in your log.

## Known limitations

- A very large first import gives an unwieldy preview ([#32](https://github.com/mileschintw/leetcode-tutor/issues/32)).
- Import has no guidance yet for records reachable only in a signed-in browser ([#29](https://github.com/mileschintw/leetcode-tutor/issues/29)).
- Every Mirror push sends every page through the connector, which costs tokens on a large log ([#33](https://github.com/mileschintw/leetcode-tutor/issues/33)).
- In a chat app, the tutor doesn't check which workspace a Mirror database belongs to ([#40](https://github.com/mileschintw/leetcode-tutor/issues/40)).

## Project docs

- [CHANGELOG.md](./CHANGELOG.md): what changed in each version
- [CONTEXT.md](./CONTEXT.md): the project's domain language
- [docs/adr/](./docs/adr/): architecture decisions
- [docs/research/](./docs/research/): platform research behind those decisions
- [AGENTS.md](./AGENTS.md): how to work on this repository

## License

[MIT](./LICENSE)
