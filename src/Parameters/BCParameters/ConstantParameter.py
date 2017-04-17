



class ConstantParameter(object):
    @property
    def name(self):
        return self._name
    
    @property
    def tag(self):
        return self._tag
    
    
    def __init__(self, name, tag):
        self._name = name
        self._tag = tag
        
       