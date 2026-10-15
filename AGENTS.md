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

- Layout: `skills/<name>/SKILL.md` (the skills; `references/` holds what loads on demand), `.claude-plugin/` (Claude Code plugin and marketplace), `practice_log/` (the `practice-log` CLI, Python standard library only), `tests/` (Seam 1), `evals/` (Seam 2).
- Seam 1 tests: `python -m unittest discover -s tests`. Each `tests/cases/<case>/` holds `case.json`, an `input/` fixture and golden `expected/`, `stdout.txt` and `stderr.txt`; `UPDATE_GOLDEN=1` rewrites the goldens. Tests run the CLI as a subprocess only, never import it.
- Metadata check: `python -m practice_log build`. Skill frontmatter may use only the six open-spec fields, with an ASCII `name` matching its folder and a `description` of at most 200 characters.
- Seam 2 evals: `claude plugin eval . --trust-plugin --no-publish`. It runs full Claude sessions, so it costs tokens.
