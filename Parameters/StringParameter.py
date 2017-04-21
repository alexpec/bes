from Parameters.ScalarParameter import ScalarParameter




#=======================================================================================================================
# StringParameter
#=======================================================================================================================
class StringParameter(ScalarParameter):
    '''
    Parameter that defines a string 
    '''
    @property
    def name(self):
        return self._name
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def param_type(self):
        return str
    
    @property
    def dimension(self):
        return None
    
    
    def __init__(self, name, tag, param_type=str, dimension=None):
        '''
        String Parameter initializer
        :param name: {str} - defines the name of the parameter
        :param tag: {str} - defines the tag that will be search in base document
        :param param_type: {None} - not used, here just to implement the interface
        :param dimension: {None} - not used, here just to implement the interface
        '''
        self._name = name
        self._tag = tag
        self._param_type = str
        self._dimension = None