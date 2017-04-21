



class ConstantParameter(object):
    @property
    def name(self):
        return self._name
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def data(self):
        stri =  'type    uniformFixedValue;\n'
        stri += 'uniformValue constant %f;' %self._data
        
        return stri
    
    
    def __init__(self, name, tag, data):
        '''
        Constant parameter initializer
        
        :param name: {str} - defines the name of the parameter
        :param tag: {str} - defines the tag that will be search in base document
        :param data: {float} - the constant data value
        '''
        self._name = name
        self._tag = tag
        self._data = data
        
