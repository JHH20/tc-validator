#!/usr/bin/env python3
from pathlib import Path
import stat

from notBaekjunCommon import *
from .validator_helper import *

class CheckerBase:
    DIFF = "diff --no-dereference -s --".split()

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
            return RunnerEnv.DIFF_ERR, ""

        res = exec_prog([*CheckerBase.DIFF, path1.as_posix(), path2.as_posix()])
        return res.returncode, res.stdout


    def diff_dir(self, path1: Path, path2: Path):
        """
        Compare two directories and return the result as (status, bitmask)
        where status = 0 for identical, = 1 for different, = 2 for error
        """
        path1 = path1.resolve()
        path2 = path2.resolve()
        if not path1.is_dir() or not path2.is_dir():
            return RunnerEnv.DIFF_ERR, 0

        perm1 = self.get_perms(path1)
        perm2 = self.get_perms(path2)
        status = RunnerEnv.DIFF_PASS if perm1 == perm2 else RunnerEnv.DIFF_FAIL
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
