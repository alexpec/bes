from Parameters.ScalarParameter import ScalarParameter




#=======================================================================================================================
# FieldParameter
#=======================================================================================================================
class FieldParameter(ScalarParameter):
    '''
    Implements the field parameter in order to allow the change of values
    in the master document in field values
    '''
    def __init__(self, name, tag, param_type=float, dimension=None):
        '''
        Field Parameter initializer
        Inherits from Scalar Parameter
        
        :param param_type: {str} - Defines the type of each parameter of the list
        '''
        super(ScalarParameter, self).__init__(name, tag, param_type, dimension)



    def _isParam(self, param):
        
        val_list = isinstance(param, list)
        if not val_list:
            return False
        
        val_itens = all(isinstance(item, self._param_type) for item in param)
        
        return val_list and val_itens
