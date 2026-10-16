#!/usr/bin/env bash
# A workspace whose Mirror already exists: the config holds its database id and repository. Valid
# Parentheses is new since the last push, so it has no page yet.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both; imported_notion
problem valid-parentheses "Valid Parentheses" easy "[string, stack]" "[]" false "" \
  "Push each opener; each closer must match the top of the stack." \
  2026-10-14 "stack" leethub code_valid_parentheses
mirror_config 5e0d8c2a-7f41-4b96-a3d2-1c9e6f4b8a70 https://github.com/learner/practice-log
git_origin https://github.com/learner/practice-log.git
