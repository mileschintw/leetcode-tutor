"""Command-line entry point: `python -m practice_log <subcommand>`."""

import argparse
import sys
from pathlib import Path

from practice_log import build


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(prog="practice-log")
    subcommands = parser.add_subparsers(dest="command", required=True)

    build_parser = subcommands.add_parser(
        "build", help="maintainer-only: check skill metadata (and later produce release outputs)"
    )
    build_parser.add_argument("--root", type=Path, default=Path("."), help="repository root (default: .)")

    args = parser.parse_args(argv)
    if args.command == "build":
        return build.run(args.root)
    parser.error(f"unknown command {args.command}")
