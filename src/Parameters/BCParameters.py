



class BCParameter(object):
    @property 
    def name(self):
        return self._name
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def param_type(self):
        return self._param_type
    
    def __init__(self, name, tag, param_type):
        
        '''Verify if the param_type is a class that implements the get_bc_string
        in order to replace the tag to the properly set-up bc'''
        method_get = getattr(param_type, 'get_bc_string')
        if not callable(method_get):
            raise Exception("Method get_bc_str not implemented!")
        
        self._name = name
        self._tag = tag
        self._param_type = param_type
        
        