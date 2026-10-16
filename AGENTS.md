# LeetCode Tutor

A Socratic coding-interview tutor packaged as agent skills, with a practice log the learner owns. v3 of [leetcode-tutor-prompt](https://github.com/mileschintw/leetcode-tutor-prompt).

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues for `mileschintw/leetcode-tutor`, via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Development

- Layout: `skills/<name>/SKILL.md` (the skills; `references/` holds what loads on demand), `.claude-plugin/` (Claude Code plugin and marketplace, the source for the other manifests), `skills/leetcode-tutor/scripts/practice_log/` (the `practice-log` CLI, Python standard library only; it lives inside the skill because upload zips carry only the skill folder), `tests/` (Seam 1), `evals/` (Seam 2).
- Seam 1 tests: `python -m unittest discover -s tests`. Each `tests/cases/<case>/` holds `case.json`, an `input/` fixture and golden `expected/`, `stdout.txt` and `stderr.txt`; `UPDATE_GOLDEN=1` rewrites the goldens. Tests run the CLI as a subprocess only, never import it.
- Build: `python skills/leetcode-tutor/scripts/practice_log build` checks the metadata, then generates every release artefact. These outputs are committed: `prompts/<skill>.md` (the copy-paste prompt: SKILL.md's body plus `references/*.md`), `plugin.json` (Agent Plugins manifest for Codex, Cursor and Antigravity), `.cursor-plugin/plugin.json` and `.agents/plugins/marketplace.json` (Codex; generated only when `.claude-plugin/plugin.json` has a `repository`). Never edit them by hand; rerun `build` after changing a skill or `.claude-plugin/plugin.json`. The upload zips go to the gitignored `dist/`: `<skill>-claude-ai.zip`, `<skill>-gemini-perplexity.zip` (SKILL.md at the zip root) and `<skill>-agents-skills.zip` (the `.agents/skills/` layout). `build --check` writes nothing and fails if a committed output is stale; CI runs it.
- Metadata rules: skill frontmatter may use only the six open-spec fields, with an ASCII `name` matching its folder and a `description` of at most 200 characters. Following `docs/research/agent-skills-platform-support.md`, build also rejects names over 64 characters or containing `anthropic`/`claude`, and XML tags in descriptions, which claude.ai refuses. It also rejects a top-level `bin/` directory, which makes claude.ai refuse the whole plugin. A skill that only works with another installed alongside it declares `metadata:` / `requires: <skill>`; build then generates no prompt or upload zips for it.
- Seam 2 evals: `claude plugin eval . --trust-plugin --no-publish --scaffold --allow-tools Write Edit`. It runs full Claude sessions, so it costs tokens. `--scaffold` runs each case's `scaffold.sh` to build its fixture workspace, and `Write Edit` let the tutor record Attempts; graders can't run commands, so they check the written files directly. Leave Bash ungranted: it needs a sandbox that native Windows lacks.
- CI (`.github/workflows/ci.yml`) runs the Seam 1 tests and `build --check` on Ubuntu and Windows, plus `claude plugin validate .`, on every push to `main` and every PR. Evals are not in CI: they cost tokens and need an API key, so run them by hand when `skills/` or `evals/` change.
