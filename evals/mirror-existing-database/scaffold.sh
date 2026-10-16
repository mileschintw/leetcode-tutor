#!/usr/bin/env bash
# A workspace on GitHub with no Mirror yet; the learner's old Notion database also exists.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both
mirror_config null https://github.com/learner/practice-log
git_origin https://github.com/learner/practice-log.git
