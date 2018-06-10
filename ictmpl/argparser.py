import os
import sys
import json
from argparse import ArgumentParser
from .__version__ import __version__

__all__ = ('init_parser',)


def init_parser(app):
    parser = ArgumentParser(os.path.basename(sys.argv[0]),
                            description='Project template manager')
    
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__),
                        help='Show version of script')
    
    _subparser = parser.add_subparsers(help='List of commands')
    
    _create = _subparser.add_parser(
        'create', help='Create new project by template')
    _create.add_argument('path', help='Path to new project')
    _create.add_argument('template', help='Template name or git repository')
    _create.set_defaults(func='create.create_project')
    
    return parser
