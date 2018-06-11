import sys
import os

from setuptools import setup, find_packages

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    repo = '-r pypi'
    if sys.argv[-2] == 'test':
        repo = '-r pypitest'
        
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload {} dist/*'.format(repo))
    sys.exit()

here = os.path.abspath(os.path.dirname(__file__))
packages = find_packages()

about = {}
with open(os.path.join(here, 'ictmpl', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    zip_safe=False,
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    ictmpl=ictmpl.app:run
    """
)