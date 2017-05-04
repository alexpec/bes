import re
from time import sleep




class REParser(object):
    '''
    Regular expression reader
    '''
    @property
    def data(self):
        return self._data
    
    @property
    def results(self):
        return self._results
    
    
    
    def __init__(self):
        self._data = []
        self._results = {}
    
    
    
    def AddPattern(self, pattern_name, pattern, action):
        '''
        Adds a new pattern for regular expression processing
        :param pattern_name: {str} - A name for the RE. Used as identifier.
        :param pattern: {str} - The regular expression itself;
        :param action: {callable} - A callable that receives (match, lines, line_index)
                :param match: {re.match} - the match groups of the RE;
                :param lines: {list} - the lines that are being processed. All are passed in order to allow the free
                                      walk forward and back, in more complex parsed documents;
                :param line_index: {int} - the line that is being processed. A update in this line will update the
                                            parser itself. Useful when processing more complex documents
        '''
        try:
            p = re.compile(pattern)
        except:
            raise Exception("%s is not a valid regular expression!" %pattern)
        
        self._data.append((pattern_name, pattern, p, action)) 
        self._results[pattern_name] = []
        
        
        
    def ParseFile(self, filename):
        '''
        Parses a text file
        :param filename: {str} - full path and filename in order to open the file.
        '''
        try:
            file_ptr = open(filename, 'r')
        except:
            raise Exception("%s is not a valid filename!" %filename)
        
        patterns = self._data
        
        lines = file_ptr.readlines()
        file_ptr.close()
        
        line_index = 0
        while line_index < len(lines):
            for pattern in patterns:
                match = pattern[2].match(lines[line_index])
                
                if match != None:
                    result = pattern[3](match, lines, line_index)
                    self._results[pattern[0]].append(result)
                    break
            line_index += 1
            
        return self._results
    
    
    def ParseBuffer(self, buf):
        '''
        Parses a pipeline buffer
        :param buf: {klass} - a buffer class that implements ReadEntry() method which returns a string entry to be
                                asserted against a regular expression. The method must return a '\n' while waiting the 
                                end of the pipeline and a 'None' when the pipeline is exausted, otherwise the REParser
                                will entry in infinity loop.
        '''
        patterns = self._data

        while not buf.IsEmpty() or not buf.is_closed:
            if buf.IsEmpty():
                sleep(5)
            else:
                line = buf.ReadEntry()
                for pattern in patterns:
                    match = pattern[2].match(line)
                    if match != None:
                        result = pattern[3](match, line, None)
                        self._results[pattern[0]].append(result)
                        break
                    
                    
                    
        return self._results
    
    
    def ParseString(self, text):
        patterns = self._data
        text.strip()
        lines = text.split('\n')
        
        for idx, line in enumerate(lines):
            for pattern in patterns:
                
                match = pattern[2].match(line)
                
                if match != None:
                    result = pattern[3](match, lines, idx)
                    self._results[pattern[0]].append(result)
                    break
        return self._results