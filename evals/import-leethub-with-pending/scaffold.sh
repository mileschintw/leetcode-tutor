#!/usr/bin/env bash
# The import-leethub-preview workspace, pushed to a Mirror that holds one pending page: a chat-platform
# Attempt for Two Sum (2026-10-14, hash map) not yet in the Practice Log.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum notion; imported_notion; leethub_repo
mirror_config 5e0d8c2a-7f41-4b96-a3d2-1c9e6f4b8a70 https://github.com/learner/practice-log
git_origin https://github.com/learner/practice-log.git
