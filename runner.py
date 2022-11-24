from pathlib import Path
import argparse
import os

from .checker import *
from .validator_helper import *

class Runner:
    TIMEOUT_STATUS = 137

    def __init__(self, exec: Path, args: list[str]):
        """
        exec: Absolute path to executable target
        """
        self.exec = exec.relative_to(RunnerEnv.CHROOT_DIR)
        self.args = args
        self.status = 0


    def run(self, timeout: int):
        """
        Timeout in seconds
        """
        assert timeout > 0
        uid = os.getenv("SUDO_UID")
        gid = os.getenv("SUDO_GID")
        cmd = [
            "chroot", f"--userspec={uid}:{gid}", "--", RunnerEnv.CHROOT_DIR,
            "timeout", "-s", "9", "--", timeout,
            self.exec, *self.args
        ]
        return exec_prog(cmd)


def parse_args():
    """
    Configure argument options and return the argparse object
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", "--ipaddr", dest="ip", required=True,
        help="IP address for inter-module communication")
    parser.add_argument("-p", "--port", dest="port", default=RunnerEnv.DEF_PORT,
        help="Port number for inter-module communication")
    parser.add_argument("-t", "--timeout", dest="timeout",
        default=RunnerEnv.DEF_TIMEOUT, help="Execution timeout in seconds")
    parser.add_argument("-e", "--exec", dest="exec", required=True,
        help="Path to executable inside chroot")

    return parser.parse_args()


def main():
    if os.geteuid() != 0 or "SUDO_USER" not in os.environ:
        print("Please execute this script with sudo")
        exit(1)

    args = parse_args()

    sock = None # To be implemented
    # Connect to backend

    try:
        runner = Runner(Path(args["exec"]).resolve(), [])
        """
        Do NOT use shell=True with bash redirection
        Using redirection will allow malicious program to escape the chroot jail
        """
        proc = runner.run(args["timeout"])
        with open(RunnerEnv.OUTPUT_DIR / RunnerEnv.F_STDOUT) as stdout:
            stdout.write(proc.stdout)
        with open(RunnerEnv.OUTPUT_DIR / RunnerEnv.F_STDERR) as stderr:
            stderr.write(proc.stderr)
    except ValueError:
        # ValueError caused by exec path not being under CHROOT
        # May write some code later to handle this
        pass

    try:
        checked_res = CheckerBase().collect_result()
    except ValueError:
        # ValueError caused by bug in find_cio_pairs()
        # Shouldn't happen unless running environment not constructed correctly
        pass

    # Do stuff to wrap checked_res into TCResult()
    # Then do stuff to send that result to backend via sock


if __name__ == "__main__":
    main()
