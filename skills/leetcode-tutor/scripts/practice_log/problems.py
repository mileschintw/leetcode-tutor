"""The walk over a Practice Workspace's Problem folders that `validate`, `index`, `mirror-plan` and `review-sheet` share.

`read_problems(root)` yields one `ProblemFolder` per `problems/<source>/<slug>/` folder, sorted by
POSIX path. A folder whose notes can't be read carries the error to report instead of its notes.
"""

from practice_log.notes import NotesError, read_notes


class ProblemFolder:
    def __init__(self, folder, rel):
        self.folder = folder  # the folder's Path
        self.rel = rel  # POSIX path relative to the workspace root, such as problems/leetcode/two-sum
        self.notes_file = folder / "notes.md"
        self.notes_label = f"{rel}/notes.md"
        self.fields = None  # Problem fields from the frontmatter, when readable
        self.attempts = None  # the Attempt log, when readable
        self.error = None  # why the notes can't be read, prefixed with the path, when they can't


def read_problems(root):
    for folder in sorted((root / "problems").glob("*/*/"), key=lambda path: path.as_posix()):
        if not folder.is_dir():
            continue
        problem = ProblemFolder(folder, folder.relative_to(root).as_posix())
        if not problem.notes_file.is_file():
            problem.error = f"{problem.rel}: missing notes.md"
        else:
            try:
                problem.fields, problem.attempts = read_notes(problem.notes_file)
            except NotesError as error:
                problem.error = f"{problem.notes_label}: {error}"
        yield problem
