import stat

class JSONable:
    def toDict(self):
        raise NotImplementedError
    def fromDict(self):
        raise NotImplementedError


class FileResult(JSONable):
    def __init__(self, fname: str, content: str, diff: str, perm: int):
        assert stat.S_IMODE(perm) == perm
        self.fname = fname
        self.content = content
        self.diff = diff
        self.perm = perm


    def toDict(self):
        return {
            "content": self.content,
            "diff": self.diff,
            "perm": self.perm
        }


    def fromDict(self):
        # TODO
        raise NotImplementedError


class TCResult(JSONable):
    SUCCESS = 0
    FAIL = 1
    TIMEOUT = 2
    ERROR = 3

    def __init__(self, result: int, etime: int, pstatus: int):
        assert result in (TCResult.SUCCESS, TCResult.FAIL, TCResult.TIMEOUT, TCResult.ERROR)
        self.result = result    # TC result
        self.etime = etime      # Execution time
        self.pstatus = pstatus  # Process exit status
        self.cio = ["", ""]     # type: list[str] [stdout, stderr]
        self.fio = []           # type: list[FileResult]


    def stdout(self, output: str):
        self.cio[0] = output


    def stderr(self, output: str):
        self.cio[1] = output


    def addFileRes(self, fres: FileResult):
        self.fio.append(fres)


    def toDict(self):
        return {
            "result": self.result,
            "etime": self.etime,
            "pstatus": self.pstatus,
            "cio": self.cio,
            "fio": {x.fname: x.toDict() for x in self.fio}
        }

    def fromDict(self):
        # TODO
        raise NotImplementedError
