# The Practice Workspace is the single source of truth; Notion is a one-way Mirror

Status: accepted, implemented in v3.0.

The tutor writes the Practice Log only as files in the learner's git-tracked Practice Workspace. Notion (and any future GUI) receives a one-way Mirror of it: edits made in Notion never flow back. We chose this because a single store keeps every feature (Review Sheet, Import, de-duplication by Problem ID) written once, and because two-way sync would force conflict resolution, the hardest part of any such system, onto a small prompt project.

## Considered Options

- **Notion as an optional backend** (tutor writes to files *or* Notion): would give chat-only users (claude.ai, ChatGPT with a Notion connector) persistence, but doubles every storage-touching feature. Rejected for v3.
- **Two-way sync** between the workspace and Notion: rejected; conflict resolution cost far outweighs the benefit.

## Consequences

- The Mirror always lives in a Notion database it creates and owns, with a fixed schema; it never writes into a learner's pre-existing database. Old databases are brought in once via Import and then kept or archived by the learner. This removes any per-user field mapping from the Mirror.
- Each Mirror page links back to its Problem folder on GitHub, so Notion stays a view, not a copy to maintain.
- Mirror pages are fully managed: changes a learner makes in Notion are overwritten on the next Mirror push unless they are brought back explicitly via Import.
- On chat platforms with no filesystem but a Notion connector, the tutor may write an Attempt straight to the Mirror. This does not make Notion a second store: those Attempts are pending until the next Import in a Practice Workspace brings them into the Practice Log.
