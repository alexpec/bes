from Parameters.ScalarParameter import ScalarParameter




#=======================================================================================================================
# ScalarListParameter
#=======================================================================================================================
class ScalarListParameter(ScalarParameter):
    '''
    Implements the scalar list parameters in order to allow the use
    of time dependent boundary conditions, for example.
    This class maps values of the form:
    [ [0,0], [0,1], [2,5], [4,7] ]
    '''
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
        Inherits from Scalar Parameter
        '''
        self._name = name
        self._tag = tag
        self._param_type = param_type
        self._dimension = dimension
        
        
    def isParam(self, param):
        val_list = isinstance(param, list)
        if not val_list:
            return False
        
        flat_list = reduce(lambda x,y: x+y,param)
        val_itens = all(isinstance(item, self._param_type) for item in param)
        
        return val_list and flat_list