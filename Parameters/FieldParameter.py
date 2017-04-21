from Parameters.ScalarParameter import ScalarParameter




#=======================================================================================================================
# FieldParameter
#=======================================================================================================================
class FieldParameter(ScalarParameter):
    '''
    Implements the field parameter in order to allow the change of values
    in the master document in field values
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
        Field Parameter initializer
        Inherits from Scalar Parameter
        
        :param param_type: {str} - Defines the type of each parameter of the list
        '''
        self._name = name
        self._tag = tag
        self._param_type = param_type
        self._dimension = dimension



    def isParam(self, param):
        
        val_list = isinstance(param, list)
        if not val_list:
            return False
        
        val_itens = all(isinstance(item, self._param_type) for item in param)
        
        return val_list and val_itens
