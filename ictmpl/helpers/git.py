from subprocess import Popen, PIPE, CalledProcessError
from shutil import rmtree

__all__ = ('Git', 'GitError')


class GitError(Exception):
    pass


class Git:
    def __init__(self, repository):
        self.repository = repository
        
    def clone_to(self, project_path):
        command = 'git clone {repository} {path} -q --depth=1'.format(
            repository=self.repository,
            path=project_path)
        
        pipes = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = pipes.communicate()
        if stderr:
            stderr = stderr.decode('utf-8').strip().split('\n')[-1]
            raise GitError(stderr)
        
        rmtree('%s/.git' % project_path, ignore_errors=True)
                
        