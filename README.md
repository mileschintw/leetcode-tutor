# LeetCode Tutor

> **Work in progress: v3 is being built.** The tutor skill installs in Claude Code today and records each Session in your Practice Log, and the import skill brings in your Legacy Records. Review Sheets and the Notion Mirror are still to come.

A Socratic coding-interview tutor, packaged as agent skills, that keeps a practice log you own.
v3 succeeds the copy-paste prompt in [leetcode-tutor-prompt](https://github.com/mileschintw/leetcode-tutor-prompt) (v2).

## Install in Claude Code

In Claude Code (2.1.275 or later), run:

```
/plugin install leetcode-tutor --marketplace mileschintw/leetcode-tutor
```

On older versions, add the marketplace first:

```
/plugin marketplace add mileschintw/leetcode-tutor
/plugin install leetcode-tutor@leetcode-tutor
```

Then name a Problem, for example "Let's do LeetCode 1. Two Sum". The tutor starts with a structured overview, then guides you with questions instead of answers. You write and run your code on LeetCode or NeetCode. Write in any language: the tutor replies in the language you use.

The tutor keeps your practice in a Practice Workspace, a git repository you own with one folder per Problem. If you start a Session outside one, it offers to create one for you. At the end of each Session it saves the Attempt (outcome, approach, the mistakes it saw, your code) and the Key Takeaway there.

To bring in your Legacy Records, the practice history you kept before, ask to import them and name the source: a Notion export or connector, a LeetHub repository, or anything else. The `practice-log-import` skill merges them into your Practice Log by Problem ID, keeping every Attempt and where it came from. It shows a preview and writes nothing until you confirm, and running it again adds nothing new.

## Other platforms

These installs should work, but haven't been tested by hand yet.

- **Codex:** `codex plugin marketplace add mileschintw/leetcode-tutor`, then install `leetcode-tutor` from the Plugins Directory.
- **Antigravity:** `agy plugin install https://github.com/mileschintw/leetcode-tutor`.
- **Cursor:** add this repo as a plugin (team admins: Dashboard → Plugins & MCPs → Import from Repo), or unzip `leetcode-tutor-agents-skills.zip` (see the next item for how to build it) into your project or home directory.
- **claude.ai, the Gemini app and Perplexity:** upload a skill zip. Run `python skills/leetcode-tutor/scripts/practice_log build` and it writes them to `dist/`: `leetcode-tutor-claude-ai.zip` for claude.ai, `leetcode-tutor-gemini-perplexity.zip` for the Gemini app and Perplexity.
- **The import skill** works only with the tutor skill installed alongside it, because it uses the tutor's Practice Log schema and `practice-log` CLI. Install both: the plugin installs above do. It has no upload zip or copy-paste prompt of its own.
- **ChatGPT and anything else:** paste [prompts/leetcode-tutor.md](./prompts/leetcode-tutor.md) into a Project's instructions or your first message.

## Project docs

- [CONTEXT.md](./CONTEXT.md): the project's domain language
- [docs/adr/](./docs/adr/): architecture decisions
- [docs/research/](./docs/research/): platform research behind those decisions

## License

[MIT](./LICENSE)
