from subprocess import Popen, PIPE


class SysDep:
    def __init__(self, packages, checkcmd=None, checkparams=None):
        self.packages = packages
        self.checkcmd = checkcmd
        self.checkparams = checkparams
    
    def check(self, app):
        if self.checkcmd:
            proc = Popen('command -v {}'.format(self.checkcmd), shell=True, stdout=PIPE)
            stdout = proc.communicate()[0]
            if not stdout:
                return True
        elif self.checkparams:
            if callable(self.checkparams):
                return bool(self.checkparams(app.params))
            elif isinstance(self.checkparams, str):
                return bool(app.params.get(self.checkparams))
        else:
            return True
        
        return False
            