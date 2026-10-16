"""Command-line entry point: `python -m practice_log <subcommand>`."""

import argparse
import sys
from pathlib import Path

from practice_log import build, validate, workspace


def main(argv=None):
    # Skill files hold non-ASCII text; don't let a Windows console codepage mangle it.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

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

    args = parser.parse_args(argv)
    if args.command == "build":
        return build.run(args.root, check=args.check)
    if args.command == "init":
        return workspace.run(args.path)
    if args.command == "validate":
        return validate.run(args.root)
