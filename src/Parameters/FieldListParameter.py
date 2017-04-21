from Parameters.ScalarParameter import ScalarParameter




class FieldListParameter(ScalarParameter):
    '''
    Implements the field list parameters in order to allow the use of
    time dependent voundary conditions, for example
    This class maps values of the form:
    [ [0, [0,1,2]], [1, [0,4,6]], [3, [1,6,7]] ] 
    '''
    def __init__(self, name, tag, param_type=float, dimension=None):
        '''
        Inherits from Scalar Parameters
        '''
        super(ScalarParameter, self).__init__(name, tag, param_type, dimension)
        
    
    def isParam(self, param):
        val_list = isinstance(param, list)
        if not val_list:
            return False
        
        for id, val in param:
            if not isinstance(id, self._param_type):
                return False
            
            val_itens = all(isinstance(item, self._param_type) for item in val)
            
            return val_list and val_itens
