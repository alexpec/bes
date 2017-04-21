import subprocess
import sys
import time
import os




#===============================================================================
# TUIRunner
#===============================================================================
class TUIRunner(object):
    '''
    Run Salome in second plane in order to generate the exported mesh file with the set parameters.
    '''
    @property
    def script_name(self):
        return self._script_name
    
    @property
    def salome_path(self):
        return self._salome_path
    
    
    def __init__(self, script_name, salome_path):
        self._script_name = script_name
        self._salome_path = salome_path    
    
    def Runner(self, output_filename):
        #Verify if the file exists, case positive delete it
        if os.path.isfile(output_filename):
            os.remove(output_filename)
        
        cmd = '%s -t %s' %(self.salome_path, self.script_name)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        while True:
            nextline = process.stdout.readline()
            if (nextline == '' and process.poll() is not None) or (os.path.isfile(output_filename)):
                break
            
            #if os.path.isfile(output_filename):
            #    break
            #else:
            #    nextline = process.stdout.readline()
            
            
            print nextline.replace('\n', '')
        
        print '*'*25    

                
if __name__ == '__main__':
    script_name = r'/home/alexpec/Development/Workspace/Bes/Mesh/_data/create.py'
    
    tui_runner = TUIRunner(script_name, r'/home/alexpec/Development/Software/salome/salome')
    tui_runner.Runner(r'/home/alexpec/Development/Workspace/Bes/Mesh/_data/Mesh_1.Unv')
    
                
    
        