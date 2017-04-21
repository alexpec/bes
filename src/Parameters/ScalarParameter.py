


#===============================================================================
# GeometricParameter
#===============================================================================
class ScalarParameter(object):
    @property
    def name(self):
        return self._name
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def param_type(self):
        return self._param_type
    
    @property
    def dimension(self):
        return self._dimension
    
    
    
    def __init__(self, name, tag, param_type=float, dimension=None):
        '''
        Scalar Parameter initializer
        
        :param name: {str} - defines the name of the parameter
        :param tag: {str} - defines the tag that will be search in base document
        :param param_type: {type} - defines the type of param (float, int, str)
        :param dimension: {array} - defines the array of units from open foam
        '''
        self._name = name
        self._tag = tag
        self._param_type = param_type
        self._dimension = dimension


        
    def isParam(self, param):
        if isinstance(param, self._param_type):
            return True
        else:
            return False
    