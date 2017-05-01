



class TerminalBuffer(object):
    '''
    Buffer to process the data from the terminal 
    '''
    @property
    def limit(self):
        return self._limit
    @limit.setter
    def limit(self, value):
        self._limit = value
    
    
    def __init__(self, limit=500):
        self._limit = limit
        self._buffer = []
        
    
    def ReadEntry(self):
        if len(self._buffer) == 0:
            return '\n'
        else:
            return self._buffer.pop(0)
    
    
    def AddLine(self, line):
        size = len(self._buffer)
        limit = self._limit
        while size > limit:
            self._buffer.pop(0)
            size = len(self._buffer)
            
        self._buffer.append(line)
        
        
        
