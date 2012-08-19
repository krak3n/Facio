import contextlib
import sys


class DummyFile(object):
    def write(self, x):
        pass


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    save_stdin = sys.stdin
    sys.stderr = DummyFile()
    sys.stdout = DummyFile()
    sys.stdin = DummyFile()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr
    sys.stdin = save_stdin
