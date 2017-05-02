import subprocess
from Utils.TerminalBuffer import TerminalBuffer





class TerminalRunner(object):
    
    @property
    def buffer(self):
        return self._buffer
    
    
    def __init__(self):
        self._buffer = TerminalBuffer()
        self._is_running = False
    
    
    def IsRunning(self):
        return self._is_running
    
    
    def Runner(self, command, quiet=True):
        
        self._is_running = True
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        while True:
            nextline = process.stdout.readline()
            self._buffer.AddLine(nextline)
            if (nextline == '' and process.poll() is not None):
                self._is_running = False
                self._buffer.is_closed = True
                break
            
            
    
