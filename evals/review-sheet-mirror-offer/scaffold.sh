#!/usr/bin/env bash
# The graphs Practice Workspace (see _fixtures/review-sheet.sh) with a Mirror set up: the config holds a database id and repository.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/review-sheet.sh"
graphs_workspace
mirror_config 5e0d8c2a-7f41-4b96-a3d2-1c9e6f4b8a70 https://github.com/learner/practice-log
