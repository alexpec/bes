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
    def __init__(self, name, tag, param_type=float, dimension=None):
        '''
        Inherits from Scalar Parameter
        '''
        super(ScalarParameter, self).__init__(name, tag, param_type, dimension)
        
        
        
    def isParam(self, param):
        val_list = isinstance(param, list)
        if not val_list:
            return False
        
        flat_list = reduce(lambda x,y: x+y,param)
        val_itens = all(isinstance(item, self._param_type) for item in param)
        
        return val_list and flat_list