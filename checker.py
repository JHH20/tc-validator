#!/usr/bin/env python3
from pathlib import Path
import subprocess
import stat

class RunnerEnv:
    """
    Define constants and helper functions
    related to the runner's execution environment
    """
    HOME_DIR = Path.home()
    EXPECTED_DIR = Path("/expected")
    OUTPUT_DIR = Path("/actual")

    EXPECTED_CONSOLE = EXPECTED_DIR / "cio"
    EXPECTED_FILE = EXPECTED_DIR / "file"

    F_STDIN = "stdin.txt"
    F_STDOUT = "stdout.txt"
    F_STDERR = "stderr.txt"

    @staticmethod
    def check_dependency():
        """
        Check for presence of required dependencies
        Also check for POSIX binaries
        """
        raise NotImplementedError()


def exec(*args, **kwargs):
    """
    Wrap subprocess.run to capture output as text
    """
    exec_args = {**kwargs, "capture_output": True, "text": True}
    return subprocess.run(*args, **exec_args)


class CheckerBase:
    DIFF = "diff --no-dereference -s --".split()

    def __init__(self, target: Path, args: list[str]):
        self.target = target
        self.args = args
        self.status = None


    def get_perms(self, path: Path):
        """
        Return 4 octal digit permission as int
        """
        return stat.S_IMODE(path.lstat().st_mode)


    def diff(self, path1: Path, path2: Path):
        """
        Diff two files and return the result as (status, diff output)
        where status = 0 for identical, = 1 for different, = 2 for error
        """
        path1 = path1.resolve()
        path2 = path2.resolve()
        if not path1.is_file() or not path2.is_file():
            return 2, ""

        res = exec([*CheckerBase.DIFF, path1.as_posix(), path2.as_posix()])
        return res.returncode, res.stdout


    def diff_dir(self, path1: Path, path2: Path):
        """
        Compare two directories and return the result as (status, bitmask)
        where status = 0 for identical, = 1 for different, = 2 for error
        """
        path1 = path1.resolve()
        path2 = path2.resolve()
        if not path1.is_dir() or not path2.is_dir():
            return 2, 0

        perm1 = self.get_perms(path1)
        perm2 = self.get_perms(path2)
        status = 0 if perm1 == perm2 else 1
        return status, perm1 ^ perm2


    def find_cio_pairs(self):
        """
        Return list of file pairs that need to be compared
        eg) [(Path("a.txt"), Path("b.txt"))] -> `diff a.txt b.txt`

        Uses RunnerEnv.EXPECTED_CONSOLE to find targets excluding F_STDIN
        eg) EXPECTED_CONSOLE/F_STDOUT -> OUTPUT_DIR/F_STDOUT
        """
        results: list[tuple[Path, Path]] = []
        for file in RunnerEnv.EXPECTED_CONSOLE.iterdir():
            if file.name != RunnerEnv.F_STDIN:
                results.append((file, RunnerEnv.OUTPUT_DIR / file.name))

        return results

    def find_file_pairs(self) -> list[tuple[Path, Path]]:
        """
        Return list of file pairs that need to be compared
        eg) [(Path("a.txt"), Path("b.txt"))] -> `diff a.txt b.txt`

        Uses RunnerEnv.EXPECTED_FILE to find targets
        eg) EXPECTED_FILE/a/b/c.txt -> HOME_DIR/a/b/c.txt
        """
        results: list[tuple[Path, Path]] = []
        for file in RunnerEnv.EXPECTED_FILE.rglob("*"):
            part = file.relative_to(RunnerEnv.EXPECTED_FILE)
            results.append((file, RunnerEnv.HOME_DIR / part))

        return results


    def build_run_cmd(self) -> str:
        """
        Return command for executing user binary
        """
        return f"{self.target} {' '.join(self.args)}"


    def run(self, timeout = 5):
        """
        Execute user binary in chroot jail with timeout in seconds
        Return cpu time, exit status, stdout, stderr
        """
        raise NotImplementedError()


    def collect_result(self) -> dict:
        """
        Collect testcase result
        """
        results = {
            "console": {},
            "file": {},
            "status": None
        }

        check_cio = self.find_cio_pairs()
        for expected, actual in check_cio:
            if expected.name == RunnerEnv.F_STDOUT:
                results["console"]["stdout"] = self.diff(expected, actual)
            elif expected.name == RunnerEnv.F_STDERR:
                results["console"]["stderr"] = self.diff(expected, actual)
            else:
                raise ValueError("Unexpected console IO comparison")

        check_file = self.find_file_pairs()
        for expected, actual in check_file:
            part = expected.relative_to(RunnerEnv.EXPECTED_FILE).as_posix()
            if expected.is_file():
                results["file"][part] = self.diff(expected, actual)
            elif expected.is_dir():
                results["file"][part] = self.diff_dir(expected, actual)

        results["status"] = self.status

        return results


def main():
    pass


if __name__ == "__main__":
    main()
