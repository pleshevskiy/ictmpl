import os
import json
from re import compile, sub, _pattern_type
from os.path import abspath, isdir, join
from shutil import copytree, rmtree

__all__ = ('parse_ignore_file', 'copytree_with_ignore', 'treewalk')


RE_DOUBLESTAR = compile(r'\*\*')
RE_STAR = compile(r'\*')

RE_IF_CONDITION = compile(r'\s*%\s*(endif|if\s+(.+))\s*%')


def parse_ignore_file(filepath):
    regexes = []
    try:
        with open(abspath(filepath)) as file:
            lines = [line.strip() for line in file.readlines()]
    except:
        return regexes
    
    for line in lines:
        if not line or line.startswith('#'):
            continue
        
        line = RE_DOUBLESTAR.sub('.+?', line)
        line = RE_STAR.sub('[\w-]+?', line)
        if line.startswith('/'):
            line = '^'+line
        
        regexes.append(compile(line))
    return regexes


def treewalk(path):
    PATH_LEN = len(path)
    
    for root, dirs, files in os.walk(path):
        src_files = dirs + files
        filepaths = [
            '%s/%s' % (root[PATH_LEN:], filename)
            for filename in ([dir+'/' for dir in dirs] + files)
        ]
        
        yield root, dirs, files, zip(filepaths, src_files)


def copytree_with_ignore(src, dst, ignore_filepath='.ictmplignore', **kwargs):
    ignore_filepath = abspath(join(src, ignore_filepath))
    ignore_regexes = parse_ignore_file(ignore_filepath)
    SRC_PATHLEN = len(src)
    
    # TODO: Need refactoring on treewalk method
    def ignore(path, files):
        ignores = []
        files = (('%s/%s' % (path, file), file) for file in files)
        for filepath, file in files:
            if isdir(filepath):
                filepath += '/'
            filepath = filepath[SRC_PATHLEN:]
            
            for regex in ignore_regexes:
                if regex.search(filepath):
                    ignores.append(file)
                    break
        
        return ignores
        
    return copytree(src, dst, ignore=ignore, **kwargs)


def rmtree_without_ignore(path, ignore_filepath='.ictmplignore'):
    ignore_filepath = abspath(join(path, ignore_filepath))
    ignore_regexes = parse_ignore_file(ignore_filepath)
    
    if not ignore_regexes:
        return
    
    for root, dirs, files, all in treewalk(path):
        rmfiles = []
        for filepath, srcname in all:
            for regex in ignore_regexes:
                if regex.search(filepath):
                    rmfiles.append([filepath, srcname])
                    break
            
        for filepath, filename in rmfiles:
            if filename in dirs:
                rmtree(path+filepath, ignore_errors=True)
            elif filename in files:
                os.remove(path+filepath)
                    
                    
def replace_template_file(filepath, app):
    params = app.params
    with open(filepath, 'r') as file:
        filedata = file.read()
    
    # replace conditions
    cut_info = None
    cond_deep = 0
    start_index = 0
    while True:
        match = RE_IF_CONDITION.search(filedata[start_index:])
        if not match:
            break
        
        start, end = [start_index+v for v in match.span()]
        statement = match.group(1)
        if statement.startswith('if '):
            cond_deep += 1
            local = params.copy()
            exec('result__=bool({})'.format(match.group(2)), local)
            if local['result__']:
                filedata = filedata[:start] + filedata[end:]
                start_index = start
            elif cut_info is None:
                cut_info = (start, cond_deep)
                start_index = end
        else:
            if cut_info is not None \
                    and cut_info[1] is cond_deep:
                start = cut_info[0]
                cut_info = None
            filedata = filedata[:start] + filedata[end:]
            start_index = start
    
    # replace params
    for key, value in params.items():
        if isinstance(value, _pattern_type):
            continue
        elif value is None or isinstance(value, bool):
            value = str(value)
        else:
            value = json.dumps(value)
        filedata = sub(r'%%{}%%'.format(key), value, filedata)
    
    with open(filepath, 'w') as file:
        file.write(filedata)
    