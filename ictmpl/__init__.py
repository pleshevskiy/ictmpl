from .config import Config
from .ictmpl import Ictmpl


ictmpl = Ictmpl(Config())

if __name__ == '__main__':
    ictmpl.run()


    