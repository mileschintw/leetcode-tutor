#!/usr/bin/env bash
# A workspace whose Notion Mirror holds no pending pages. A pending page for Two Sum went to an old copy of
# the Mirror instead ("Practice Log (old)"), which the mocks serve when Import searches for it.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both; imported_notion
mirror_config 5e0d8c2a-7f41-4b96-a3d2-1c9e6f4b8a70 https://github.com/learner/practice-log
git_origin https://github.com/learner/practice-log.git
