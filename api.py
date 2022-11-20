import stat

class JSONable:
    def toDict(self):
        raise NotImplementedError
    @classmethod
    def fromDict(cls, data: dict):
        raise NotImplementedError


class FileResult(JSONable):
    def __init__(self, fname: str, content: str, diff: str, perm: int = -1):
        assert perm < 0 or stat.S_IMODE(perm) == perm
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


    @classmethod
    def fromDict(cls, data: dict):
        cls.fname = data.keys()[0]
        cls.content = data[cls.fname]['content']
        cls.diff = data[cls.fname]['diff']
        cls.perm = data[cls.fname]['perm']
        assert cls.perm < 0 or stat.S_IMODE(cls.perm) == cls.perm
        return cls


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


    def stdout(self, output: FileResult):
        assert output.fname == "stdout"
        self.cio[0] = output


    def stderr(self, output: FileResult):
        assert output.fname == "stderr"
        self.cio[1] = output


    def addFileRes(self, fres: FileResult):
        self.fio.append(fres)


    def toDict(self):
        return {
            "result": self.result,
            "etime": self.etime,
            "pstatus": self.pstatus,
            "cio": {x.fname: x.toDict() for x in self.cio},
            "fio": {x.fname: x.toDict() for x in self.fio}
        }


    @classmethod
    def fromDict(cls, data: dict):
        cls.result = data["result"]
        cls.etime = data["etime"]
        cls.pstatus = data["pstatus"]
        cls.cio = [FileResult(fname=x, **data["cio"][x]) for x in ("stdout", "stderr")]
        cls.fio = [FileResult.fromDict({k: v}) for k, v in data["fio"].items()]
        return cls
