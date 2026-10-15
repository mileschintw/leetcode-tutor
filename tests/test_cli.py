"""Seam 1: the practice-log CLI run against fixture files, compared with golden files.

Each directory under tests/cases/ is one case:

- case.json: {"args": [...], "exit_code": N}
- input/: the fixture tree, copied to a temporary directory that becomes the working directory
- expected/: the golden tree the working directory must match afterwards
- stdout.txt, stderr.txt: golden output (an absent file means empty output)

Set UPDATE_GOLDEN=1 to rewrite expected/, stdout.txt and stderr.txt from the actual results.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = Path(__file__).resolve().parent / "cases"
UPDATE_GOLDEN = os.environ.get("UPDATE_GOLDEN") == "1"


def run_cli(args, cwd):
    """The single place that invokes the CLI."""
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT), PYTHONUTF8="1")
    return subprocess.run(
        [sys.executable, "-m", "practice_log", *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def read_tree(root):
    """Map each file's POSIX relative path to its text, with newlines normalised."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes().decode("utf-8").replace("\r\n", "\n")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def read_golden(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.exists() else ""


def write_golden(path, text):
    if text:
        path.write_text(text, encoding="utf-8", newline="\n")
    elif path.exists():
        path.unlink()


class CliGoldenTest(unittest.TestCase):
    maxDiff = None

    def test_cases(self):
        cases = sorted(p for p in CASES_DIR.iterdir() if (p / "case.json").exists())
        self.assertTrue(cases, "no cases found")
        for case in cases:
            with self.subTest(case=case.name):
                self.check_case(case)

    def check_case(self, case):
        spec = json.loads((case / "case.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            if (case / "input").exists():
                shutil.copytree(case / "input", work)
            else:
                work.mkdir()
            result = run_cli(spec["args"], work)
            stdout = result.stdout.replace("\r\n", "\n")
            stderr = result.stderr.replace("\r\n", "\n")

            if UPDATE_GOLDEN:
                shutil.rmtree(case / "expected", ignore_errors=True)
                shutil.copytree(work, case / "expected")
                write_golden(case / "stdout.txt", stdout)
                write_golden(case / "stderr.txt", stderr)
                return

            self.assertEqual(result.returncode, spec["exit_code"], f"exit code\nstderr:\n{stderr}")
            self.assertEqual(stdout, read_golden(case / "stdout.txt"), "stdout")
            self.assertEqual(stderr, read_golden(case / "stderr.txt"), "stderr")
            self.assertEqual(read_tree(work), read_tree(case / "expected"), "resulting files")


class RepositoryBuildTest(unittest.TestCase):
    def test_shipped_skills_pass_build(self):
        result = run_cli(["build"], REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
