# Agent Skills (SKILL.md) platform support: research notes

Research date: 2026-10-15. Every citation below was accessed on 2026-10-15 unless noted otherwise.
Scope: whether to repackage the LeetCode Socratic-tutor system prompt as an Agent Skill (SKILL.md) and/or a Claude Code plugin.
Method: primary sources only (vendor docs, help centers, first-party blogs, official GitHub repos). Claims that only appeared in search-result summaries or third-party pages are listed in the final section as unverified.

## TL;DR

- **SKILL.md is now a cross-vendor open format.** Anthropic created it and published it as an open standard on 2025-12-18. The spec lives at agentskills.io, with the repo `agentskills/agentskills` (code Apache-2.0, docs CC-BY-4.0). The repo describes no formal governance body. Required frontmatter is `name` (max 64 chars, `a-z0-9-`, must match the folder name) and `description` (max 1024 chars). Optional fields are `license`, `compatibility`, `metadata` and `allowed-tools`. The recommended SKILL.md size is under 500 lines / about 5k tokens, with detail moved into `references/`, `scripts/` and `assets/`.
- **Every vendor the repo targets now has some product that accepts SKILL.md, but not on every consumer plan.** Individual learners on these plans can upload or install a skill:
  - **Gemini app:** personal Google accounts, no subscription needed. This is the most consumer-friendly target.
  - **Claude:** Free through Max per the newest help article, with code execution on. An older platform page omits Free.
  - **Local tools:** Claude Code, Codex, Gemini CLI/Antigravity, Copilot/VS Code and Cursor.
- **Two groups are not covered:**
  - **ChatGPT:** standalone skills are documented only for Business, Enterprise, Healthcare and Edu. Free, Plus and Pro are undocumented.
  - **Perplexity:** skills are a Perplexity Computer feature, which needs a subscription. Free users can't use them.
- **Consequence: a skill cannot fully replace the copy-paste prompt yet.** Keep the plain prompt for ChatGPT consumer tiers, non-Computer Perplexity users, and anyone who prefers Projects or custom instructions.
- **Platform changes since the repo was written:**
  - **Gemini Gems are being retired and replaced by skills.** Personal-account Gems end in November 2026 and auto-convert.
  - **Perplexity Spaces were renamed Projects** on 2026-07-30. They migrated with everything carried over; they were not retired.
- **Other constraints:**
  - Gemini app uploads can be SKILL.md, a folder or a .zip, up to 100 MB, and scripts can't use the internet.
  - Perplexity limits uploads to 10 MB.
  - Uploads to claude.ai and the Claude API **hard-fail** on any frontmatter field outside the six spec fields.
- **Plugins and marketplaces are vendor-specific; SKILL.md is the portable unit.**
  - Claude Code uses `.claude-plugin/marketplace.json` plus `.claude-plugin/plugin.json`.
  - Cursor uses `.cursor-plugin/marketplace.json`.
  - Antigravity uses `agy plugin install <github-url>`.
  - In ChatGPT, GitHub marketplace import is for workspace admins.
  - No single manifest serves every vendor. One repo can carry several manifests that all point at the same `skills/<name>/SKILL.md`.
- **Persisting a practice log only works reliably on local agents:** Claude Code, Codex, Gemini CLI/Antigravity, Copilot/VS Code and Cursor write to the project or home directory. Claude Code plugins also get `${CLAUDE_PLUGIN_DATA}`. Perplexity Projects have a persistent shared file system. claude.ai, ChatGPT and the Gemini app run skills in a sandbox, and no fetched source says files persist across conversations.
- **No official guidance was found** on keeping a SKILL.md and a copy-paste prompt in one source of truth, or on bilingual (en + zh-TW) skills. See sections 4 and 5 for the constraints that apply and a suggested approach.

## Platform support table

| Platform | SKILL.md support | Install scope | Filesystem / state | Source (all accessed 2026-10-15) |
|---|---|---|---|---|
| Claude Code (CLI, IDE, desktop Code tab) | Yes, native. Extra Claude-only frontmatter is allowed. | Project `.claude/skills/`, personal `~/.claude/skills/`, enterprise managed, plugin `<plugin>/skills/`. claude.ai-account skills sync into `~/.claude/skills/synced/`. | Full local filesystem and network. Plugins get a persistent `${CLAUDE_PLUGIN_DATA}` dir. | https://code.claude.com/docs/en/skills |
| Claude Code plugins / marketplaces | Plugin `skills/<name>/SKILL.md`. A SKILL.md at the plugin root also loads as a single skill. | User, project (`.claude/settings.json`), local or managed scope. Any git repo with `.claude-plugin/marketplace.json` can be a marketplace. | As above. `${CLAUDE_PLUGIN_ROOT}` changes on every update, so don't store state there. | https://code.claude.com/docs/en/plugins-reference, https://code.claude.com/docs/en/plugin-marketplaces |
| claude.ai web, Claude desktop, Claude mobile (chat and Cowork) | Yes. Upload a ZIP via Customize > Skills, or install a plugin via Customize > Plugins. | Account-level. Team/Enterprise can share with people or groups or publish org-wide (sources conflict, see 2.2). | Sandboxed container with code execution, which must be on. Network varies by plan. Persistence across chats is not documented. | https://support.claude.com/en/articles/12512180-using-skills-in-claude, https://claude.com/docs/plugins/platform-support |
| Claude API | Yes. `/v1/skills` upload, used with the code execution tool. | Workspace-wide. | Container with no network and no runtime package install. | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview |
| ChatGPT (web, desktop, mobile) | Yes (Agent Skills standard). Create with chat or the editor, or "Upload from your computer". Skills can also arrive inside plugins. | Account/workspace. Standalone skills are documented for eligible Business, Enterprise, Healthcare and Edu users. The plugin *directory* is "available across ChatGPT plans", but using a given plugin depends on plan, workspace, role and region. | Skills "can include … code"; the execution and persistence model is not documented. | https://help.openai.com/en/articles/20001066-skills-in-chatgpt, https://help.openai.com/en/articles/20001256-plugins-in-chatgpt |
| OpenAI Codex (CLI, IDE, app) | Yes, native, plus optional `agents/openai.yaml`. | Repo `.agents/skills` (walks up to the repo root), user `~/.agents/skills`, admin `/etc/codex/skills`, system. Plugins too. | Local. The default `workspace-write` sandbox can edit inside the workspace. | https://learn.chatgpt.com/docs/build-skills, https://learn.chatgpt.com/docs/sandboxing |
| Google Gemini app (web, Mac, mobile) | Yes. Settings > Skills > Upload accepts a SKILL.md, a folder or a .zip. Replaces Gems. | Personal Google accounts, age 18+, Keep Activity on. Work and school accounts are "later". No subscription needed. | Scripts may be included but "can't perform actions or requests on external websites". Persistence is not documented. | https://support.google.com/gemini/answer/17094296, https://support.google.com/gemini/answer/18560919 |
| Gemini CLI | Yes, native. | Workspace `.gemini/skills` or `.agents/skills`; user `~/.gemini/skills` or `~/.agents/skills`; extensions. `gemini skills install <git-url>`. | Local filesystem. **Consumer access ended 2026-06-18**, including Google AI Pro/Ultra subscribers. It remains only for Code Assist Standard/Enterprise and paid Gemini / Enterprise API keys. | https://geminicli.com/docs/cli/skills/, https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ |
| Google Antigravity (app, CLI `agy`, IDE) | Yes ("open standard"). | Workspace `.agents/skills` (legacy `.agent/skills`); global `~/.gemini/config/skills` or `~/.gemini/antigravity-cli/skills`. Plugins via `agy plugin install <github-url>`. | Local filesystem. | https://antigravity.google/docs/skills |
| Perplexity (Computer; Projects, formerly Spaces) | Yes. Plugins > Add custom > Skill > Upload accepts a .zip with SKILL.md at root, or a .md file, up to 10 MB. | Account. Org tab for enterprise. Requires a plan that includes Computer. | Projects have a "persistent, hierarchical file system" shared by humans and agents. | https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills, https://www.perplexity.ai/hub/blog/spaces-are-now-projects |
| Perplexity Agent API | Yes ("open Agent Skills format"). ZIP up to 32 MiB / 100 files. | Per API project. | Scripts run in the API sandbox. | https://docs.perplexity.ai/docs/agent-api/skills |
| GitHub Copilot (cloud agent, code review, CLI, app, VS Code/JetBrains agent mode) | Yes. | Project `.github/skills`, `.claude/skills` or `.agents/skills`; personal `~/.copilot/skills` or `~/.agents/skills`. | Local (IDE/CLI) or the cloud agent's repo checkout. | https://docs.github.com/en/copilot/concepts/agents/about-agent-skills |
| VS Code (Copilot Chat) | Yes. Skills appear as `/` commands. | Project `.github/skills`, `.claude/skills` or `.agents/skills`; personal `~/.copilot/skills`, `~/.claude/skills` or `~/.agents/skills`; extensions via `chatSkills`; agent plugins. | Local workspace. | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| Cursor | Yes. | Project `.agents/skills` or `.cursor/skills`; user `~/.agents/skills` or `~/.cursor/skills`. Compatibility paths `.claude/skills` and `.codex/skills`. GitHub install only via a plugin (`.cursor-plugin/marketplace.json`). | Local workspace. | https://cursor.com/docs/context/skills |

Other listed adopters (agentskills.io client showcase, https://agentskills.io/home): Junie (JetBrains), OpenCode, OpenHands, Amp, Goose, Letta, Factory, Roo Code, Kiro, TRAE, Mistral Vibe, Databricks, Snowflake Cortex Code, Spring AI, Tabnine, Laravel Boost and others.

---

## 1. The Agent Skills / SKILL.md format

### 1.1 Who maintains it, and is it an open standard?

- The agentskills.io site says the format "was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products", and that it "is open to contributions from the broader ecosystem" (https://agentskills.io/home, accessed 2026-10-15).
- Anthropic announced it on 2025-12-18: "We're also publishing Agent Skills as an open standard", with the spec at agentskills.io (https://claude.com/blog/organization-skills-and-directory; Claude release notes entry 2025-12-18, https://support.claude.com/en/articles/12138966-release-notes, both accessed 2026-10-15).
- The spec repo is `github.com/agentskills/agentskills`. Its code is Apache-2.0 and its docs are CC-BY-4.0, contributions go through CONTRIBUTING.md and a Discord is linked. The README names no formal governance or steering body and no foundation affiliation (https://github.com/agentskills/agentskills, accessed 2026-10-15).
- Anthropic's example skills are at `github.com/anthropics/skills`. That repo is also a Claude Code plugin marketplace (`/plugin marketplace add anthropics/skills`). Most of its skills are Apache-2.0, but the document skills are source-available (https://github.com/anthropics/skills, accessed 2026-10-15).

### 1.2 Directory layout

```
skill-name/
├── SKILL.md          # required: YAML frontmatter + Markdown body
├── scripts/          # optional: executable code
├── references/       # optional: docs loaded on demand
├── assets/           # optional: templates, images, data
└── ...               # any other files
```
Source: https://agentskills.io/specification (accessed 2026-10-15).

### 1.3 Frontmatter fields (spec)

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1-64 chars. Lowercase `a-z`, `0-9` and `-` only. No leading or trailing hyphen, no `--`. **Must match the parent directory name.** |
| `description` | Yes | 1-1024 chars, non-empty. Should say what the skill does **and when to use it**. |
| `license` | No | A license name or a bundled license file. |
| `compatibility` | No | 1-500 chars. Environment requirements. |
| `metadata` | No | Map from string to string. |
| `allowed-tools` | No | Space-separated pre-approved tools. Experimental; support varies. |

Source: https://agentskills.io/specification (accessed 2026-10-15).

Vendor-specific additions and restrictions:
- **Anthropic (claude.ai, API):** `name` cannot contain XML tags or the reserved words "anthropic" or "claude". `description` cannot contain XML tags (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, accessed 2026-10-15).
- **Claude Code:** accepts many extra fields, including `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context: fork`, `agent`, `hooks`, `paths` and `shell`. It silently ignores unknown fields. But "Outside Claude Code, only six fields are allowed … Uploads to claude.ai, the Skills API, or packaging with `package_skill.py` fail with a hard error if other fields are present." The combined `description` + `when_to_use` is truncated at 1,536 chars in the listing (https://code.claude.com/docs/en/skills, accessed 2026-10-15).
- **VS Code:** optional `argument-hint`, `user-invocable`, `disable-model-invocation` and `context`. An invalid `name` makes the skill fail to load silently (https://code.visualstudio.com/docs/copilot/customization/agent-skills, accessed 2026-10-15).
- **Cursor:** optional `paths`, `disable-model-invocation`, `icon`, `color` and `metadata` (https://cursor.com/docs/context/skills, accessed 2026-10-15).
- **Codex:** optional `agents/openai.yaml` for UI metadata, an invocation policy and tool dependencies (https://learn.chatgpt.com/docs/build-skills, accessed 2026-10-15).
- **Antigravity:** `name` is optional (defaults to the folder name) and `description` is required (https://antigravity.google/docs/skills, accessed 2026-10-15).
- **Gemini app:** the name must be lowercase and hyphenated, and SKILL.md must be in the upload's root folder (https://support.google.com/gemini/answer/17094296, accessed 2026-10-15).
- **Perplexity:** the name is 1-64 chars, lowercase and hyphens. The description decides when the skill activates (https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills, accessed 2026-10-15).

### 1.4 Progressive disclosure

1. **Metadata** (about 100 tokens): `name` and `description` load at startup for every skill.
2. **Instructions** (under 5,000 tokens recommended): the SKILL.md body loads on activation.
3. **Resources** (as needed): files in `scripts/`, `references/` and `assets/` load or run only when referenced.

The spec says: "Keep your main `SKILL.md` under 500 lines". It also says to keep file references one level deep and use relative paths from the skill root (https://agentskills.io/specification, accessed 2026-10-15). Anthropic's authoring guide repeats this, and adds that descriptions should be written in the third person, that reference files over 100 lines should start with a table of contents, and that paths should use forward slashes (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, accessed 2026-10-15). Validation tool: `skills-ref validate ./my-skill` (https://agentskills.io/specification).

### 1.5 Cross-client discovery convention

The client-implementation guide recommends scanning a client-specific directory plus `.agents/skills/` at both project and user level. It says: "The `.agents/skills/` paths have emerged as a widely-adopted convention for cross-client skill sharing", but the spec "does not mandate where skill directories live". Some clients also scan `.claude/skills/` "for pragmatic compatibility" (https://agentskills.io/client-implementation/adding-skills-support.md, accessed 2026-10-15).

Implication: in a project repo, `.agents/skills/` is read by Codex, Gemini CLI, Antigravity, Copilot, VS Code and Cursor. `.claude/skills/` is read by Claude Code, Copilot, VS Code and Cursor. The full raw Claude Code skills page (`skills.md`, about 109.5k chars, grepped on 2026-10-15) never mentions `.agents`, so Claude Code needs `.claude/skills/` or a plugin (https://code.claude.com/docs/en/skills, accessed 2026-10-15). A repo that wants both groups of tools covered without a plugin needs both directories, for example `.agents/skills/` as the real one with `.claude/skills/` symlinked to it. Claude Code supports symlinked skill folders (same page).

---

## 2. Platform-by-platform

### 2.1 Claude Code

**Skill locations** (https://code.claude.com/docs/en/skills, accessed 2026-10-15):
- Personal: `~/.claude/skills/<name>/SKILL.md`
- Project: `.claude/skills/<name>/SKILL.md`, loaded from the working directory and each parent up to the repo root.
- Enterprise: managed settings.
- Nested: `<subdir>/.claude/skills/`.
- `--add-dir` directories.
- Plugin: `<plugin>/skills/<name>/SKILL.md`, invoked as `/plugin-name:skill-name`.
- claude.ai-account skills: synced to `~/.claude/skills/synced/`.

Precedence is enterprise > personal > project. Plugin skills are namespaced and never collide. Symlinked skill folders are supported. Custom commands have been merged into skills.

**Plugins** (https://code.claude.com/docs/en/plugins-reference, accessed 2026-10-15):
- The manifest is `.claude-plugin/plugin.json`. It is optional, and `name` is its only required key. Other keys include `version`, `description`, `author{name,email,url}`, `homepage`, `repository`, `license`, `keywords`, `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `userConfig` and `defaultEnabled`.
- The default layout is `skills/`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json` and `bin/`. Component directories go at the plugin root, not inside `.claude-plugin/`.
- "A plugin with `SKILL.md` at its root, no `skills/`, and no `skills` key loads as a single skill."
- Reserved names: plugin names starting `claude-`, `anthropic-` or `cc-plugin-` are errors, and `claude` or `anthropic` as a whole word elsewhere produces a warning.
- A root `CLAUDE.md` is not loaded as context.

**Marketplaces** (https://code.claude.com/docs/en/plugin-marketplaces, https://code.claude.com/docs/en/plugins/host-marketplace, accessed 2026-10-15):
- A marketplace is "a directory or repository with a `.claude-plugin/marketplace.json` file". Required keys are `name`, `owner` and `plugins[]`, and each entry needs a `name` and a `source`.
- Source types are a relative path (from the marketplace root, no `..`), `github`, `git-subdir`, `url`, `archive`, `npm` and `command`.
- Users run `/plugin marketplace add owner/repo` (optionally `#ref`), then `/plugin install <plugin>@<marketplace>`. The marketplace name comes from `marketplace.json`, not from the repo name.
- `claude plugin validate .` checks the manifests.
- The `anthropics/skills` repo shows that one GitHub repo can serve as both marketplace and plugin source (https://github.com/anthropics/skills).
- **Keep the entry name and the `plugin.json` name identical.** A mismatch breaks installs.
- Names reserved for official Anthropic marketplaces are refused.

**Install scopes** (https://code.claude.com/docs/en/plugins/install, accessed 2026-10-15):
- User scope writes `~/.claude/settings.json`.
- Project scope writes `.claude/settings.json`, which is committed. Each collaborator still runs `claude plugin install <name>@<mkt> --scope project` once.
- Local scope writes `.claude/settings.local.json`.
- `claude plugin marketplace add owner/repo --scope project` registers the marketplace for everyone who trusts the folder (https://code.claude.com/docs/en/plugins/host-marketplace).
- Cloud sessions don't load locally installed or repo-enabled plugins.

**Versions:** if `version` is set, users stay on it until it changes. If `version` is omitted, a git-hosted plugin's version is its commit SHA (https://code.claude.com/docs/en/plugins/loading, accessed 2026-10-15).

### 2.2 claude.ai, Claude desktop and Claude mobile

- **Plans and enabling.** The newest help article says skills are available on Free, Pro, Max, Team and Enterprise, and that the feature "requires code execution to be enabled". Free/Pro/Max users turn it on in Settings > Capabilities. Team/Enterprise owners turn it on in Organization settings > Plugins & skills. Custom skills are uploaded as a ZIP via Customize > Skills > + > Create skill > Upload a skill. Common failures are a folder name that doesn't match the skill name, a missing SKILL.md, and invalid characters. No numeric size limit is given (https://support.claude.com/en/articles/12512180-using-skills-in-claude, "Updated over 3 weeks ago", accessed 2026-10-15).
- **Conflict.** The platform overview says custom skills are uploaded "through Settings > Features" and are "Available on Pro, Max, Team, and Enterprise plans". It also says they are "individual to each user", "not shared organization-wide" and can't be centrally managed, and that "Custom Skills do not sync across surfaces" (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, accessed 2026-10-15). Newer sources contradict these points:
  - The help article above describes Team/Enterprise sharing and publishing.
  - The 2025-12-18 blog describes admin provisioning (https://claude.com/blog/organization-skills-and-directory).
  - The Claude Code docs describe claude.ai skills and plugins syncing into Claude Code (https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/plugins/loading).

  Treat the overview page as stale on these points.
- **Description length conflict.** The "Creating custom skills" help article caps `description` at **200 characters** (https://support.claude.com/en/articles/12512198-creating-custom-skills, accessed 2026-10-15). The spec and the platform docs say 1024. The same help article's example `skill.md` uses a "## Metadata" heading instead of the YAML frontmatter it requires, which makes it a weaker source. Still, a description of 200 characters or fewer satisfies every source.
- **Desktop and mobile.**
  - Code execution and file creation is available on web, Claude Desktop and Claude Mobile (iOS/Android) (https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude, accessed 2026-10-15).
  - Release note 2026-09-16 ("Claude Cowork comes to every conversation") is rolling out "on web, desktop, and mobile" and says "skills carry over" (https://support.claude.com/en/articles/12138966-release-notes, accessed 2026-10-15). A search summary said this rollout is limited to Pro and Max; the fetched summary didn't confirm that, so it is unverified.
  - No fetched article explicitly lists custom-skill *upload* on mobile.
- **Plugins in claude.ai.** In Customize > Plugins, users can add a GitHub, GitHub Enterprise, or public GitLab/Bitbucket repo as a marketplace (up to 25 per account), or upload a plugin zip (200 MB / 5,000 files max). Chat loads plugin skills but ignores agents and hooks. **A top-level `bin/` makes chat and Cowork refuse the whole plugin.** A plugin installed on the account also appears in Claude Code as `<name>@synced` (https://claude.com/docs/plugins/platform-support, accessed 2026-10-15).

### 2.3 OpenAI ChatGPT and Codex CLI

- **ChatGPT.** Skills "are available to eligible ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability" (https://help.openai.com/en/articles/20001066-skills-in-chatgpt, updated about 2 months before access, accessed 2026-10-15).
  - To find skills: sidebar > Plugins > Skills tab.
  - To create: with chat, with the editor, or "Upload from your computer". Uploaded skills are scanned and may be marked "Needs Review" or "Blocked".
  - Skills can be shared to the workspace.
- **Agent Skills standard and sync.** OpenAI Academy says ChatGPT skills follow the Agent Skills open standard and can be exported and imported into Codex. It also says skills "don't sync across products yet" (https://academy.openai.com/public/resources/skills, last updated 2026-09-17, accessed 2026-10-15).
- **Plugins.** The plugin directory "is available across ChatGPT plans", but individual plugin use depends on plan, workspace, role and region. Plugin ZIP upload and GitHub marketplace import are workspace-admin features (https://help.openai.com/en/articles/20001256-plugins-in-chatgpt, accessed 2026-10-15).
- **Codex skill paths** (https://learn.chatgpt.com/docs/build-skills, formerly developers.openai.com/codex/skills, accessed 2026-10-15):
  - REPO: `$CWD/.agents/skills` and parents up to the repo root
  - USER: `$HOME/.agents/skills`
  - ADMIN: `/etc/codex/skills`
  - SYSTEM: bundled
- **Codex skill format.** `name` and `description` are required. Optional extras are `scripts/`, `references/`, `assets/` and `agents/openai.yaml`.
- **Codex install and invocation.** Install with `$skill-installer`, or distribute via plugins. Invoke explicitly with `$` or `/skills` in Codex, or `@` in ChatGPT; skills also trigger implicitly.
- **Where Codex skills appear.** Standalone skills appear in the ChatGPT desktop app, Codex CLI and the IDE extension. Plugin-bundled skills also appear in ChatGPT web, desktop and mobile. The skills list uses up to 2% of context (8,000 chars fallback).

### 2.4 Google Gemini app (Gems → skills) and Gemini CLI / Antigravity

- **Gemini app skills** (https://support.google.com/gemini/answer/17094296, accessed 2026-10-15):
  - Ways to create: in chat, with "Create with Gemini", from a template, or by uploading "a `SKILL.md` file, or a folder or `.zip`" with SKILL.md in its root.
  - Upload limits: 100 MB total. Plain text (`.py`, `.sh`, `.json`, `.yaml`, `.md`), PDFs and images are supported; `.docx` and `.xlsx` are not.
  - Scripts: "scripts that require internet access aren't supported".
  - Eligibility: 18+, signed in, Keep Activity on. "Skills don't require a Google AI subscription."
  - Invocation: `/` (moving to `@`) or automatic. Skills can be stacked.
  - Export: skills can be downloaded as a .zip.
  - Surfaces: the page says skills are available in the Gemini mobile app, the Mac app and the web app. Its upload steps describe the computer Skills page.
- **Gems transition** (https://support.google.com/gemini/answer/18560919, accessed 2026-10-15):
  - Gems end for personal accounts in November 2026, for Workspace business, enterprise and nonprofit in March 2027, and for Workspace education in June 2027.
  - Gems auto-convert to skills, including supported knowledge files.
  - Unlimited skills can be created; 100 can be active at once.
  - Skills are "available now to individuals over 18 with personal accounts"; work and school accounts come later.
  - Sharing is "expected in the coming weeks".
  - Confirmed by the Gems overview page (https://gemini.google/overview/gems/, accessed 2026-10-15).
- **Gemini Enterprise** has its own "Upload skill" flow that accepts .md or .zip (https://support.google.com/g/answer/18067667). Not fetched in detail.
- **Gemini CLI** (https://geminicli.com/docs/cli/skills/, accessed 2026-10-15):
  - Precedence: built-in < extension < user (`~/.gemini/skills`, `~/.agents/skills`) < workspace (`.gemini/skills`, `.agents/skills`).
  - Install: `gemini skills install <git-url> [--path] [--scope user|workspace]`.
  - Activation: via the `activate_skill` tool, with a consent prompt.
- **Antigravity transition.** Google moved consumer users from Gemini CLI to Antigravity CLI. Gemini CLI "stop[s] serving requests for affected consumer users on June 18, 2026", including Google AI Pro and Ultra subscribers and Code Assist for individuals. It remains only for Code Assist Standard/Enterprise licenses and paid Gemini / Gemini Enterprise Agent Platform API keys. Agent Skills carry over, and extensions become Antigravity plugins (https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/, 2026-05-19, accessed 2026-10-15).
- **Antigravity paths** (https://antigravity.google/docs/skills, accessed 2026-10-15):
  - Workspace: `.agents/skills/` (legacy `.agent/skills/` still read).
  - Global: `~/.gemini/config/skills/` (app/IDE) or `~/.gemini/antigravity-cli/skills/` (CLI).
  - Plugin install: `agy plugin install https://github.com/<owner>/<repo>`.

### 2.5 Perplexity

- **Spaces → Projects.** "Spaces have been renamed Projects", an evolution "for long-running work in Computer". Project instructions hold project-wide context, and Skills hold repeatable processes. Each Project has "a persistent, hierarchical file system that humans and agents share" (https://www.perplexity.ai/hub/blog/spaces-are-now-projects, 2026-07-30, accessed 2026-10-15).
- **Computer Skills** (https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills, accessed 2026-10-15):
  - Availability: "available on every plan that includes Computer".
  - Upload path: Plugins > Add custom > Skill > Upload skill.
  - Accepted files: a .zip with SKILL.md at the root, or a .md file, max 10 MB.
  - Name: 1-64 chars, lowercase and hyphens.
  - Workflows were replaced by skills on 2026-09-23.
- **Plugins page.** Connectors and Skills pages merged into a single Plugins page. This is rolling out to individual plans and Self-Serve Enterprise first (https://www.perplexity.ai/help-center/en/articles/2026100703-where-did-connectors-and-skills-go, accessed 2026-10-15).
- **Computer access.** Computer requires an active subscription. Pro gets weekly usage, and Max gets 10,000 monthly credits. It is available on web desktop, iOS and Android (https://www.perplexity.ai/help-center/en/articles/13837784-what-is-computer, accessed 2026-10-15).
- **Agent API.** Custom skills "use the open Agent Skills format", with ZIP bundles up to 32 MiB and 100 files (https://docs.perplexity.ai/docs/agent-api/skills, accessed 2026-10-15).
- **Not established:** whether plain (non-Computer) Perplexity search threads use skills.

### 2.6 GitHub Copilot, VS Code and Cursor

- **GitHub Copilot.** Skills are supported in the Copilot cloud agent, code review, Copilot CLI, the Copilot app, and agent mode in VS Code and JetBrains. Project paths are `.github/skills`, `.claude/skills` and `.agents/skills`; personal paths are `~/.copilot/skills` and `~/.agents/skills` (https://docs.github.com/en/copilot/concepts/agents/about-agent-skills, accessed 2026-10-15).
- **VS Code.**
  - Project paths are the same as Copilot's. Personal paths add `~/.claude/skills`.
  - `chat.agentSkillsLocations` is deprecated.
  - Extensions can contribute skills via `chatSkills`.
  - Plugin skills are namespaced, e.g. `/my-plugin:skill`.
  - Source: https://code.visualstudio.com/docs/copilot/customization/agent-skills (accessed 2026-10-15).
- **Cursor.**
  - Reads `.agents/skills`, `.cursor/skills`, `~/.agents/skills` and `~/.cursor/skills`, plus the compatibility paths `.claude/skills`, `.codex/skills`, `~/.claude/skills` and `~/.codex/skills`.
  - Skills from GitHub must be packaged as a plugin with `.cursor-plugin/marketplace.json`.
  - Source: https://cursor.com/docs/context/skills (accessed 2026-10-15).

---

## 3. Can a skill persist state (e.g. a practice log)?

| Platform | Can write files that persist? | Basis (all accessed 2026-10-15) |
|---|---|---|
| Claude Code | **Yes.** The full local filesystem (e.g. `practice-log.md` in the repo or home dir). Plugins also get `${CLAUDE_PLUGIN_DATA}` (`~/.claude/plugins/data/<id>/`), "kept across plugin updates" and deleted on uninstall from the last scope. Don't write to `${CLAUDE_PLUGIN_ROOT}`, which changes on every update. | https://code.claude.com/docs/en/plugins-reference, https://code.claude.com/docs/en/plugins/loading |
| Claude Code caveat | `${CLAUDE_PLUGIN_DATA}` and `${CLAUDE_PLUGIN_ROOT}` are substituted inline in skill Markdown, but "aren't present in the environment of commands Claude runs through the Bash tool". A SKILL.md body that uses them would show literal `${...}` text on other platforms. | https://code.claude.com/docs/en/plugins-reference |
| Codex | **Yes, within the workspace.** In `workspace-write`, Codex "can read files, edit within the workspace, and run routine local commands". | https://learn.chatgpt.com/docs/sandboxing |
| Gemini CLI / Antigravity | **Yes.** Local agents. Gemini CLI adds the skill dir to allowed paths on activation. | https://geminicli.com/docs/cli/skills/ |
| Copilot (IDE/CLI), VS Code, Cursor | **Yes.** Local workspace agents. (Persisting from the cloud agent means committing to the repo.) | Docs above; persistence is inferred from local workspace access. |
| Perplexity Computer (Projects) | **Likely yes.** Projects have a persistent shared file system, and Computer "saves changes back" to files. | https://www.perplexity.ai/hub/blog/spaces-are-now-projects |
| claude.ai / desktop / mobile | **Not documented.** Skills run in a sandboxed container. Files "remain available for download throughout your conversation", and nothing says they persist across conversations. A user could download the log and re-upload it each time. | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude |
| Claude API | **No** network, no package install, container-scoped. | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview |
| ChatGPT | **Not documented.** Skills "can include … code". The execution and persistence model is not described. | https://help.openai.com/en/articles/20001066-skills-in-chatgpt |
| Gemini app | **Not documented.** Scripts can be bundled but can't reach the internet. Reference files can only be changed by re-uploading the whole skill. | https://support.google.com/gemini/answer/17094296 |

Design implication: treat the practice log as an **optional** feature. When a writable filesystem is available, write to a project-local file. Otherwise, fall back to printing a log entry for the user to copy. Don't hard-code `${CLAUDE_PLUGIN_DATA}` into the shared SKILL.md body.

---

## 4. One source of truth for a SKILL.md and a copy-paste prompt

**No official guidance was found** from Anthropic, agentskills.io, OpenAI, Google or Perplexity on sharing one source between a SKILL.md and a plain system prompt. The closest official guidance:

- **On sources:** "Synthesize from existing project artifacts" (https://agentskills.io/skill-creation/best-practices.md, accessed 2026-10-15). This is about feeding material in, not about maintaining one shared source.
- **On how a prompt differs from a skill:** "Unlike prompts (conversation-level instructions for one-off tasks), Skills load on demand" (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, accessed 2026-10-15).

Documented constraints that shape any approach:
- **Plugin cache copies.** Marketplace plugins are copied into a cache, and "Files outside the plugin directory aren't copied" (https://code.claude.com/docs/en/plugins/loading).
- **Symlinks to elsewhere in the marketplace repo are dereferenced, for git-hosted installs only.** "Local-path" and `command`-copy installs keep only symlinks that resolve inside the plugin (https://code.claude.com/docs/en/plugins/host-marketplace, accessed 2026-10-15). Note: Windows symlinks need Developer Mode or elevation (same page).
- **Upload platforms take a ZIP or folder.** On claude.ai, ChatGPT, Gemini and Perplexity, the uploaded package must contain everything (sections 2.2 to 2.5).
- **Some features don't port.** Claude-Code-only frontmatter fails claude.ai/API uploads (https://code.claude.com/docs/en/skills). Claude-only substitutions such as `${CLAUDE_SKILL_DIR}`, `` !`cmd` `` and `${CLAUDE_PLUGIN_DATA}` are not part of the spec.

Suggested approach (inferred, not an official recommendation):
1. Keep the canonical tutor instructions as plain Markdown in the SKILL.md body. Use only the six spec fields, with a `description` of 200 characters or fewer.
2. Put long material in `references/*.md`.
3. Generate the copy-paste prompt (SKILL.md body plus inlined references) with a small build script or CI step, rather than editing two files by hand. Commit the generated file so non-technical users can still copy it.
4. Have the Claude Code plugin's `marketplace.json` point at the same skill directory, so the plugin doesn't need a second copy.

---

## 5. Bilingual skills (en + zh-TW): one skill or two?

**No official guidance was found** on multilingual or localized skills. Pages checked: the agentskills.io spec, best practices and optimizing-descriptions pages, and Anthropic's authoring best practices. None mentions language or localization (all accessed 2026-10-15).

Relevant constraints:
- **`name` is effectively ASCII.** The spec says `name` "may only contain unicode lowercase alphanumeric characters (`a-z`, `0-9`) and hyphens" (https://agentskills.io/specification). CJK characters have no lowercase form, and every vendor doc says lowercase a-z with hyphens, so treat `name` as ASCII in practice. A zh-TW name like `力扣家教` won't work. The language can appear only as a suffix, such as `leetcode-tutor-zh-tw`.
- **`description` limits are tight for bilingual text.** The Perplexity Agent API counts `description` as 1-1,024 **bytes** (https://docs.perplexity.ai/docs/agent-api/skills). zh-TW characters take 3 bytes each in UTF-8, so that is about 340 CJK characters. claude.ai's help article caps descriptions at 200 characters, which leaves little room for both languages.
- **The description drives triggering.** "The description carries the entire burden of triggering" (https://agentskills.io/skill-creation/optimizing-descriptions.md). A description in only one language may trigger less reliably on prompts in the other language. This is inferred and untested.
- **Scope guidance:** "Design coherent units … Skills scoped too narrowly force multiple skills to load for a single task, risking overhead and conflicting instructions" (https://agentskills.io/skill-creation/best-practices.md). If both en and zh-TW skills are installed, both may activate and conflict.
- **Name collisions.** Two skills with the same name collide (project overrides user), so two language variants need distinct names (https://agentskills.io/client-implementation/adding-skills-support.md).

Options (inferred):
- **(a) One skill.** English instructions, a bilingual `description` that contains both English and zh-TW trigger phrases, and a rule to "reply in the user's language". The description must stay at 200 characters or fewer to pass claude.ai, so it can hold only a few short phrases per language; elsewhere the limit is 1024 chars, or 1024 bytes on the Perplexity API. Language-specific phrasing or examples go in `references/zh-TW.md`, loaded only when the user writes in Chinese.
- **(b) Two skills** (`leetcode-tutor` and `leetcode-tutor-zh-tw`). Best when users install only one, for example via separate zips on upload platforms. Avoid installing both at once.

Option (a) matches the "coherent unit" and progressive-disclosure guidance. Option (b) matches today's two copy-paste prompts.

---

## Unverified / open questions

These items came only from secondary sources or search-result summaries, or are gaps in the primary docs:

1. **Codex default network policy** in `workspace-write`. A search summary said network is off by default, but the fetched sandboxing page did not say so (https://learn.chatgpt.com/docs/sandboxing).
2. **Perplexity Projects instruction limit** of 8,000 characters. Seen only in a search summary; the help article was not fetched.
3. **Gemini skills rollout dates.** Secondary coverage (Android Central, pasqualepillitteri.it) gives Workspace on 2026-10-05, the Gemini app on 2026-10-13, and Gems moving into Settings on 2026-11-17. The Google help pages say only "November" for personal accounts.
4. **Perplexity importing Claude Code/Codex SKILL.md unchanged.** Claimed by hunted.space (third-party). The Perplexity help docs only require a name and description.
5. **Antigravity accepting existing skills "with no schema changes".** Claimed by mcp.directory (third-party). Google's blog only says Agent Skills carry over.
6. **ChatGPT Plus/Pro access to standalone skills.** The official help article lists Business, Enterprise, Healthcare and Edu only. A community forum feature request suggests Plus and Pro lack it, but that is not official. It is also unclear whether Plus/Pro can use skill-only *plugins*.
7. **Skills launch date.** 2025-10-16, cited in search summaries of anthropic.com/news/skills. The page itself was not fetched.
8. **Agent Skills governance.** No primary source ties the spec to the Agentic AI Foundation or Linux Foundation; the AAIF donation that was found concerns MCP. A formal governance or versioning policy is not documented.
9. **Custom skill upload on Claude mobile.** Code execution works on mobile, and the 2026-09-16 release note says skills "carry over" on mobile, but no article confirms uploading on mobile. The "Pro and Max only" scope of that rollout came from a search summary and is unverified.
10. **File persistence across conversations** on claude.ai, ChatGPT and the Gemini app. Not documented on any of the three.
11. **Gemini app script execution.** Scripts may be bundled, but how and where they run isn't described.
12. **claude.ai skill ZIP size limit.** The help article mentions size limits without giving a number.
13. **Conflicting claude.ai docs.** These may be resolved by the time the decision is made:
    - The platform overview vs the help center on plans (Free included or not), menu path (Settings > Features vs Customize > Skills) and org sharing.
    - The 200 vs 1024 description limit.
