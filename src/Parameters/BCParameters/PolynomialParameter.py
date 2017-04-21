from Parameters.BCParameters.ConstantParameter import ConstantParameter




class PolynomialParameter(ConstantParameter):
    def _formatTable(self):
        stri = '(\n'
        
        for i in self._data:
            stri += '(%s \t %s)\n' %(str(i[0]), str(i[1]))
            
        stri += ');\n'
        
        return stri
    
    
        
    
    @property
    def data(self):
        stri =  'type    uniformFixedValue;\n'
        stri += 'uniformValue polynomial\n'
        stri += '%s' %self._formatTable() #with no ; because it comes from formatTable
        
        return stri
    
    
    
    def __init__(self, name, tag, data):
        '''
        Polynomial parameter initializer
        :param name: {str} - defines the name of the parameter
        :param tag: {str} - defines the tag that will be search in the base document
        :param data: {list} - a list of the ai values and the power
                ex. 1*t^0 + 5*t^1 + 4*t^5 = [[1,0],[5,1],[4,5]]
        '''
        super(PolynomialParameter, self).__init__(name, tag, data)