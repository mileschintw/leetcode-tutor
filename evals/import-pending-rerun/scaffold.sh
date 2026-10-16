#!/usr/bin/env bash
# An earlier Import already brought Two Sum's pending Attempt home but couldn't trash its page, so the
# Mirror still shows it as pending.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both; imported_notion; imported_pending_two_sum
mirror_config 5e0d8c2a-7f41-4b96-a3d2-1c9e6f4b8a70 https://github.com/learner/practice-log
git_origin https://github.com/learner/practice-log.git
