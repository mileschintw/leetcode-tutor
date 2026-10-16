#!/usr/bin/env bash
# A workspace pushed to GitHub (origin in .git/config) with no Mirror yet: no database id, no repository.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both; imported_notion
mirror_config null
git_origin git@github.com:learner/practice-log.git
