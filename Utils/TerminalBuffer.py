



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
        
    @property
    def is_closed(self):
        return self._is_closed
    @is_closed.setter
    def is_closed(self, value):
        self._is_closed = value
    
    
    
    def __init__(self, limit=500):
        self._limit = limit
        self._buffer = []
        self._is_closed = False
        
    
    def ReadEntry(self):
        size = len(self._buffer)
        if size == 0:
            return '%%%EMPTY_BUFFER%%%'
        else:
            return self._buffer.pop(0)
    
    
    def AddLine(self, line):
        size = len(self._buffer)
        limit = self._limit
        
        if self._is_closed:
            raise Exception("The buffer is closed! Impossible to add another line!")
        
        while size > limit:
            self._buffer.pop(0)
            size = len(self._buffer)
            
        self._buffer.append(line)
        
        
    def IsEmpty(self):
        if len(self._buffer) == 0:
            return True
        else:
            return False  
        
