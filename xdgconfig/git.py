import os
import pathlib
import subprocess

from xdgconfig.exceptions import GitNotFound


class Git:
    def __init__(self, path: pathlib.Path):
        self.cwd: pathlib.Path = pathlib.Path(os.getcwd()).resolve()
        self.path = path
        try:
            subprocess.call(['git', '--version'])
        except subprocess.CalledProcessError:
            raise GitNotFound('git is not installed on this system')

    def add(self, glob: str) -> None:
        os.chdir(self.path)
        subprocess.call(['git', 'add', glob])
        os.chdir(self.cwd)

    def commit(self, message: str) -> None:
        os.chdir(self.path)
        subprocess.call(['git', 'commit', '-m', message])
        os.chdir(self.cwd)

    def push(self, branch: str = 'master', remote: str = 'origin') -> None:
        os.chdir(self.path)
        subprocess.call(['git', 'push', remote, branch])
        os.chdir(self.cwd)

    def has_remote(self, remote: str = 'origin') -> bool:
        os.chdir(self.path)
        out: str = subprocess.check_output(['git', 'remote'])
        os.chdir(self.cwd)
        return remote in out
