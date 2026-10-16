"""Seam 1: the practice-log CLI run against fixture files, compared with golden files.

Each directory under tests/cases/ is one case:

- case.json: {"args": [...], "exit_code": N}, and optionally "env": {...} for the CLI's environment
- input/: the fixture tree, copied to a temporary directory that becomes the working directory
- expected/: the golden tree the working directory must match afterwards
- stdout.txt, stderr.txt: golden output (an absent file means empty output)

A .zip file is compared by its member names and their contents, not its bytes.

Set UPDATE_GOLDEN=1 to rewrite expected/, stdout.txt and stderr.txt from the actual results.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = Path(__file__).resolve().parent / "cases"
UPDATE_GOLDEN = os.environ.get("UPDATE_GOLDEN") == "1"


def run_cli(args, cwd, extra_env=None):
    """The single place that invokes the CLI."""
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT / "skills" / "leetcode-tutor" / "scripts"))
    env.pop("PYTHONUTF8", None)  # the CLI must write UTF-8 on its own, whatever the console codepage
    env.pop("NOTION_TOKEN", None)  # no case ever reaches the real Notion
    env.update(extra_env or {})
    result = subprocess.run(
        [sys.executable, "-m", "practice_log", *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    result.stdout = result.stdout.replace("\r\n", "\n")
    result.stderr = result.stderr.replace("\r\n", "\n")
    return result


def read_tree(root):
    """Map each file's POSIX relative path to its text, with newlines normalised."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): read_zip(path) if path.suffix == ".zip" else read_text(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def read_text(data):
    return data.decode("utf-8", errors="backslashreplace").replace("\r\n", "\n")


def read_zip(path):
    """A zip as text: each member's name, in archive order, followed by its contents."""
    with zipfile.ZipFile(path) as archive:
        return "".join(f"== {name}\n{read_text(archive.read(name))}" for name in archive.namelist())


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
        case_config = json.loads((case / "case.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            if (case / "input").exists():
                shutil.copytree(case / "input", work)
            else:
                work.mkdir()
            result = run_cli(case_config["args"], work, case_config.get("env"))
            self.assertEqual(result.returncode, case_config["exit_code"], f"exit code\nstderr:\n{result.stderr}")

            if UPDATE_GOLDEN:
                shutil.rmtree(case / "expected", ignore_errors=True)
                shutil.copytree(work, case / "expected")
                write_golden(case / "stdout.txt", result.stdout)
                write_golden(case / "stderr.txt", result.stderr)
                return

            self.assertEqual(result.stdout, read_golden(case / "stdout.txt"), "stdout")
            self.assertEqual(result.stderr, read_golden(case / "stderr.txt"), "stderr")
            self.assertEqual(read_tree(work), read_tree(case / "expected"), "resulting files")


class MirrorPlanRerunTest(unittest.TestCase):
    """A second push with no Practice Log change must regenerate exactly the same pages."""

    def plan(self, case):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            shutil.copytree(CASES_DIR / case / "input", work)
            first, second = run_cli(["mirror-plan"], work), run_cli(["mirror-plan"], work)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout, "a re-run printed a different plan")
        return json.loads(first.stdout)

    def test_rerun_and_stored_database_id_give_the_same_pages(self):
        # The two cases differ only in the stored database id and the form of the GitHub remote.
        first_use, later_push = self.plan("mirror-plan-workspace"), self.plan("mirror-plan-stored-id")
        self.assertIsNone(first_use["database"]["id"])
        self.assertEqual(later_push["database"]["id"], "1f2e3d4c5b6a47988a7b6c5d4e3f2a1b")
        self.assertEqual(first_use["pages"], later_push["pages"])


class RepositoryBuildTest(unittest.TestCase):
    def test_shipped_skills_pass_build(self):
        # --check writes nothing, and also fails if the committed prompt or manifests are stale.
        result = run_cli(["build", "--check"], REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
