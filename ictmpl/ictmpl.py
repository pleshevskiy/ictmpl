import sys

from .config import Config
from .argparser import init_parser
from importlib import import_module


__all__ = ('Ictmpl',)


class Ictmpl:
    config = None
    
    def __init__(self, config:Config):
        self.config = config
        self.parser = init_parser(self)
        self.params = {}
    
    def getconf(self, name, default=''):
        return getattr(self.config, name, default)
    
    def run(self, **args):
        args = self.parser.parse_args(**args)
        try:
            if len(sys.argv) == 1:
                self.parser.print_help()
            elif callable(args.func):
                args.func(args, self)
            elif isinstance(args.func, str):
                module_name, fn_name = args.func.rsplit('.', 1)
                prefix = self.getconf('METHODS_MODULE_PREFIX')
                if prefix:
                    module_name = '%s.%s' % (prefix, module_name)
                
                module = import_module(module_name)
                func = getattr(module, fn_name)
                if callable(func):
                    func(args, self)
            
        except Exception as e:
            print("%s :: %s" % (e.__class__.__name__, str(e)))
            exit()
    
