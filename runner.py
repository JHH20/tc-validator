from .checker import *

class Checker(CheckerBase):
    """
    Testcase-specific extension of the base class

    Potential extension
    - CheckerBase.diff() to support regular expression matching
    - CheckerBase.build_run_cmd() to supply arguments
    - CheckerBase.collect_result() to include/exclude validation target
    """
    pass
