

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
        
        self.question = question + ' '
        self.children = children
        
    def strparse(self, value):
        if self.vtype is not str and type(value) is self.vtype:
            return value
        
        if self.vtype in (list, tuple) \
                or (self.vtype is str and ',' in value):
            return [v.strip() for v in value.split(',') if v.strip()]
        elif self.vtype is bool:
            return value[:1].lower() == 'y'
        
        return self.vtype(value)
    
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