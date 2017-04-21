from Parameters.BCParameters.ConstantParameter import ConstantParameter




class TableParameter(ConstantParameter):
    def _formatTable(self):
        stri = '(\n'
        
        for i in self._data:
            stri += '(%s \t %s)\n' %(str(i[0]), str(i[1]))
        
        stri += ');\n'
        
        return stri
    
    
    
    @property
    def data(self):
        stri =  'type    uniformFixedValue;\n'
        stri += 'uniformValue table\n'
        stri += '%s' %self._formatTable()
        
        return stri 
    
    def __init__(self, name, tag, data):
        '''
        Table parameter initializer
        
        :param name: {str} - defines the name of the parameter
        :param tag: {str} - defines the tag that will be search in the base document
        :param data: {list} - a list of the data entries
               for scalar values: data = [[0, 1], [0.1, 2], [0.3, 10]]
               for field values: data = [[0, (10, 0, 0)], [0.1, (12, 0, 0)]]
        '''
        super(TableParameter, self).__init__(name, tag, data)
