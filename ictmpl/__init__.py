from .param import Param
from .dependency import SysDep

__all__ = ('Param', 'SysDep')

if __name__ == '__main__':
    from .config import Config
    from .ictmpl import Ictmpl
    ictmpl = Ictmpl(Config())
    ictmpl.run()


    