#!/usr/bin/env bash
# A workspace holding the Notion import, and the LeetHub repository; Two Sum is in both.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum notion; imported_notion; leethub_repo
