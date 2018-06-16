
class auto(str): pass


class Param:
    def __init__(self, name, default, vtype=None, question=None, children=None):
        self.name = name
        self.default = default
        self.vtype = vtype or type(default)
        
        if not question:
            question = 'SET {0}: ({1})'
        try:
            question = question.format(name, self.format(default))
        except:
            pass
        
        self.question = question.rstrip() + ' '
        self.children = children
        
    def strparse(self, value):
        if not isinstance(self.vtype, type) and callable(self.vtype):
            vtype = self.vtype(value)
        else:
            vtype = self.vtype
        
        if value is 'None':
            return None
        
        if type(value) is vtype:
            return value
        
        lvalue = value.lower()
        if vtype in (list, tuple) \
                or (vtype is auto and ',' in value):
            return [v.strip() for v in value.split(',') if v.strip()]
        elif vtype is bool \
                or (vtype is auto and lvalue in ('true', 'false')):
            return lvalue == 'y' or lvalue == 'true'
        
        return vtype(value)
    
    def format(self, value):
        type_ = type(value)
        if type_ in (list, tuple):
            value = ', '.join(value)
        elif type_ is bool:
            nvindex = int(not value)
            value = '/'.join(
                v.upper() if nvindex is i else v 
                for i, v in enumerate('yn'))
        
        return value