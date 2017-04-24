import subprocess
from Utils.TerminalBuffer import TerminalBuffer





class TerminalRunner(object):
    
    @property
    def context(self):
        return self._context
    
    @property
    def buffer(self):
        return self._buffer
    
    def __init__(self, context):
        self._context = context
        self._buffer = TerminalBuffer()
        
    
    def Runner(self, command, output_pipeline):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        while True:
            nextline = process.stdout.readline()
            self._buffer.AddLine(nextline)
            if (nextline == '' and process.poll() is not None):
                break
            
            
    
