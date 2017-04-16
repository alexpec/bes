


#===============================================================================
# GeometricParameter
#===============================================================================
class SystemParameter(object):
    @property
    def name(self):
        return self._name
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def param_type(self):
        return self._param_type
    
    
    def __init__(self, name, tag):
        self._name = name
        self._tag = tag
        self._param_type = str
        