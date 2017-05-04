from Utils.TerminalRunner import TerminalRunner
import os




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
    
    
    def __init__(self, ofcase_path, of_environment_cmd=None):
        super(SplitMeshRegions, self).__init__()
        
        self._of_environment_cmd = of_environment_cmd
        self._ofcase_path = ofcase_path
        
    def Runner(self):
        
        main_cmd = 'splitMeshRegion -cellZones -overwrite'
        path_cmd = main_cmd + ' -case %s' %self._ofcase_path
        
        if self._of_environment_cmd != None:
            cmd = '%s || %s' %(
                    self._of_environment_cmd,
                    path_cmd)
        else:
            cmd = path_cmd
            
        super(SplitMeshRegions, self).Runner(cmd)