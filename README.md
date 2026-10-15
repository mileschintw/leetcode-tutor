# LeetCode Tutor

> **Work in progress: v3 is being built.** The tutor skill installs in Claude Code today. The Practice Log, Import and Notion Mirror are still to come.

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

## Project docs

- [CONTEXT.md](./CONTEXT.md): the project's domain language
- [docs/adr/](./docs/adr/): architecture decisions
- [docs/research/](./docs/research/): platform research behind those decisions

## License

[MIT](./LICENSE)
