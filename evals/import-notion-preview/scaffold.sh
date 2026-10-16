#!/usr/bin/env bash
# A workspace holding the LeetHub import, and the Notion export; Two Sum is in both.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/lib.sh"
workspace; two_sum leethub; imported_leethub; notion_export
