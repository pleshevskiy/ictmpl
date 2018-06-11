from .param import Param

__all__ = ('Param', )

if __name__ == '__main__':
    from .config import Config
    from .ictmpl import Ictmpl
    ictmpl = Ictmpl(Config())
    ictmpl.run()


    