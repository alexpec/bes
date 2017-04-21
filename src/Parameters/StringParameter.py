from Parameters.ScalarParameter import ScalarParameter




#=======================================================================================================================
# StringParameter
#=======================================================================================================================
class StringParameter(ScalarParameter):
    '''
    Parameter that defines a string 
    '''
    @property
    def dimension(self):
        return None
    
    
    def __init__(self, name, tag):
        '''
        String Parameter initializer
        :param name: {str} - defines the name of the parameter
        :param tag: {str} - defines the tag that will be search in base document
        '''
        super(ScalarParameter, self).__init__(name, tag, str, None)