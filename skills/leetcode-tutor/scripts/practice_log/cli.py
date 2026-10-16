"""Command-line entry point: `python -m practice_log <subcommand>`."""

import argparse
import sys
from pathlib import Path

from practice_log import build, index, mirror, review_sheet, validate, workspace


def main(argv=None):
    # Skill files hold non-ASCII text; don't let a Windows console codepage mangle it, or add CRs to it.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", newline="\n")

    parser = argparse.ArgumentParser(prog="practice-log")
    subcommands = parser.add_subparsers(dest="command", required=True)

    build_parser = subcommands.add_parser(
        "build", help="maintainer-only: check skill metadata and generate release artefacts"
    )
    build_parser.add_argument("--root", type=Path, default=Path("."), help="repository root (default: .)")
    build_parser.add_argument(
        "--check", action="store_true", help="only verify the committed generated files are up to date"
    )

    init_parser = subcommands.add_parser("init", help="create a Practice Workspace in a new or empty folder")
    init_parser.add_argument("path", type=Path, nargs="?", default=Path("."), help="folder to create it in (default: .)")

    validate_parser = subcommands.add_parser("validate", help="check a Practice Workspace against the schema")
    validate_parser.add_argument("--root", type=Path, default=Path("."), help="workspace root (default: .)")

    index_parser = subcommands.add_parser("index", help="regenerate a Practice Workspace's README.md index")
    index_parser.add_argument("--root", type=Path, default=Path("."), help="workspace root (default: .)")

    mirror_parser = subcommands.add_parser(
        "mirror-plan", help="print, as JSON, every Notion page the Mirror should hold (it never talks to Notion)"
    )
    mirror_parser.add_argument("--root", type=Path, default=Path("."), help="workspace root (default: .)")
    mirror_parser.add_argument(
        "--format", choices=("json", "browser"), default="json",
        help="json for a connector (default), or browser: Markdown with every value to enter in Notion's UI",
    )
    mirror_parser.add_argument(
        "--changed", action="store_true",
        help="only the pages that differ from the last push recorded in mirror-state.json",
    )

    record_parser = subcommands.add_parser(
        "mirror-record", help="note Mirror pages as pushed in mirror-state.json, for `mirror-plan --changed`"
    )
    record_parser.add_argument("--root", type=Path, default=Path("."), help="workspace root (default: .)")
    record_parser.add_argument(
        "--id", dest="ids", action="append", default=[], metavar="ID",
        help="a Problem ID whose page was pushed, or trashed when it is no longer in the plan"
        " (repeatable; default: every page in the plan)",
    )

    sheet_parser = subcommands.add_parser(
        "review-sheet",
        help="select Problems by filters and write a Review Sheet",
        description="Filters of one kind match any of their values; different kinds must all match."
        " Every filter matches regardless of case. With no filters, every Problem is selected.",
    )
    sheet_parser.add_argument("--root", type=Path, default=Path("."), help="workspace root (default: .)")
    sheet_parser.add_argument("--id", dest="ids", action="append", default=[], metavar="ID", help="a Problem ID, written in lowercase in the notes (repeatable)")
    sheet_parser.add_argument("--tag", dest="tags", action="append", default=[], metavar="TAG", help="a tag (repeatable)")
    sheet_parser.add_argument(
        "--list", dest="lists", action="append", default=[], metavar="NAME", help="a Problem List name (repeatable)"
    )
    sheet_parser.add_argument("--title", default="Review Sheet", help="the sheet's heading (default: Review Sheet)")
    sheet_parser.add_argument(
        "--output", type=Path, help="the file to write inside the workspace's review-sheets/ folder, relative to the workspace root,"
        " such as review-sheets/2026-10-15-graphs.md (default: print it)"
    )

    args = parser.parse_args(argv)
    if args.command == "build":
        return build.run(args.root, check=args.check)
    if args.command == "init":
        return workspace.run(args.path)
    if args.command == "validate":
        return validate.run(args.root)
    if args.command == "index":
        return index.run(args.root)
    if args.command == "mirror-plan":
        return mirror.run(args.root, args.format, args.changed)
    if args.command == "mirror-record":
        return mirror.record(args.root, args.ids)
    if args.command == "review-sheet":
        return review_sheet.run(args.root, args.ids, args.tags, args.lists, args.title, args.output)
