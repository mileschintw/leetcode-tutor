#!/usr/bin/env bash
# The graphs Practice Workspace with the graphs Review Sheet saved the day before (see _fixtures/review-sheet.sh).
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../_fixtures/review-sheet.sh"
graphs_workspace; graphs_sheet
