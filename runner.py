import argparse

from .checker import *
from .validator_helper import *

class Runner:
    TIMEOUT = "timeout -s 9 --".split()
    TIMEOUT_STATUS = 137

    def __init__(self, exec: Path, args: list[str]):
        self.exec = exec.relative_to(RunnerEnv.CHROOT_DIR)
        self.args = args
        self.status = 0


    def run(self, timeout: int):
        """
        Timeout in seconds
        """
        assert timeout > 0
        cmd = [*Runner.TIMEOUT, timeout, self.exec, *self.args]
        return exec(cmd)


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
    pass


if __name__ == "__main__":
    main()
