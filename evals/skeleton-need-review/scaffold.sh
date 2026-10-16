#!/usr/bin/env bash
# The Practice Workspace that `practice-log init` creates, before any Problem.
set -euo pipefail
mkdir -p problems review-sheets
: > problems/.gitkeep
: > review-sheets/.gitkeep
cat > practice-log.json <<'JSON'
{
  "version": 1,
  "mirror": {
    "notion_database_id": null
  }
}
JSON
cat > README.md <<'MD'
# Practice Log

My coding-interview practice, recorded by LeetCode Tutor.
MD
