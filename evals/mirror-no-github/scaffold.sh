#!/usr/bin/env bash
# A workspace that was never pushed: no git remote and no repository in the config.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum both
mirror_config null
