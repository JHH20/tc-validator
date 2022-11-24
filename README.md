# tc-validator
테스트케이스 검증 모듈

이 모듈은 도커 안에서 하나의 테스트케이스에 대하여 동작하며 결과를 반환한다.

Directory structure는 다음과 같이 한다.
```
/
+- runner.py
|  ...
|
+- expected/
|   +- cio/
|       +- stdout.txt
|       +- stderr.txt
|   +- file/
|       +- file1.txt (as relative path)
|       +- file2.txt
|   ...
|
+- actual/
|   +- stdout.txt
|   +- stderr.txt
|
+- chroot/
    +- <system files>
    +- home/
        +- user/
            +- [사용자 실행파일]
```

이 모듈은 다음의 역할을 수행한다:
- [test program]을 실행한다
    - 제한시간 후 강제종료한다
- [test program]의 결과를 수합한다
    - console IO
    - file system
    - exit status
    - etc
- API를 통해 수합한 [test program]의 결과를 전달한다

# Dependency
- GNU coreutils
    - chroot
    - timeout
- sudo
    - Expects this script to be executed by sudo for resolving uid/gid of user