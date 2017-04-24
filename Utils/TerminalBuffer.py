



class TerminalBuffer():
    '''
    Buffer to process the data from the terminal 
    '''
    
    def __init__(self):
        self._buffer = []
        
    
    def ReadEntry(self):
        if len(self._buffer) == 0:
            return '\n'
        else:
            return self._buffer.pop(0)
    
    
    def AddLine(self, line):
        self._buffer.append(line)
        
        
        
