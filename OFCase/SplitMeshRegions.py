from Utils.TerminalRunner import TerminalRunner
import os
from Utils.REParser import REParser




class SplitMeshRegions(TerminalRunner):
    @property
    def of_environment_cmd(self):
        return self._of_environment_cmd
    
    @property
    def ofcase_path(self):
        return self._ofcase_path
    
    @property
    def buffer(self):
        return super(SplitMeshRegions, self).buffer
    
    @property
    def parser(self):
        return self._parser
    
    @property
    def parse_message(self):
        return self._parseMessage
    
    
    def _parseMessage(self, match, lines, index):
        return match.group(0)
    
    
    def _setUpParser(self):
        self._parser.AddPattern('E#1', "Exposed face: \d* fc: \d* has owner region (.*) and neighbour region (.*) when handling region: (.*)", self._parseMessage)
        self._parser.AddPattern('E#2', "Cell \d* with cell centre \d* is multiple zones. This is not allowed.", self._parseMessage)
        self._parser.AddPattern('E#3', "cellZones not synchronised across processors.", self._parseMessage)
        self._parser.AddPattern('E#4', "You cannot specify both -cellZonesOnly or -cellZonesFileOnly", self._parseMessage)
        self._parser.AddPattern('E#5', "You cannot specify both -largestOnly", self._parseMessage)
        self._parser.AddPattern('E#6', "For the cellZonesOnly option all cells have to be in a cellZone;", self._parseMessage)
        self._parser.AddPattern('E#7', "For the cellZonesFileOnly options all cells have to be in a cellZone.", self._parseMessage)
        self._parser.AddPattern('E#8', "Point \d* is not inside the mesh.", self._parseMessage)
        
    
    def __init__(self, ofcase_path, of_environment_cmd=None):
        super(SplitMeshRegions, self).__init__()
        
        self._of_environment_cmd = of_environment_cmd
        self._ofcase_path = ofcase_path
        
        self._parser = REParser()
        self._setUpParser()
        
    def Runner(self, cellzones=True, overwrite=False):
        main_cmd = 'splitMeshRegion'
        
        if cellzones:
            main_cmd = main_cmd + ' -cellZones'
        if overwrite:
            main_cmd = main_cmd + ' -overwrite'
        path_cmd = main_cmd + ' -case %s' %self._ofcase_path
        
        if self._of_environment_cmd != None:
            cmd = '%s || %s' %(
                    self._of_environment_cmd,
                    path_cmd)
        else:
            cmd = path_cmd
            
        super(SplitMeshRegions, self).Runner(cmd)
        
    
    def ParseBuffer(self):
        results = self.parser.ParseBuffer(self.buffer)
        return results