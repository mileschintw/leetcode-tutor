#!/usr/bin/env bash
# A workspace set to push its Mirror through a browser, in an agent that has only a Notion connector.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both; imported_notion
cat > practice-log.json <<'JSON'
{
  "version": 1,
  "mirror": {
    "notion_database_id": "5e0d8c2a-7f41-4b96-a3d2-1c9e6f4b8a70",
    "repository": "https://github.com/learner/practice-log",
    "via": "browser"
  }
}
JSON
git_origin https://github.com/learner/practice-log.git
