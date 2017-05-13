'''
KEYS FOR IDEASUNVTOFOAM

# -> Warning / Info
& -> Error

#1 "Skipping section at line INT.";
#2 "Starting reading units at line INT.";
#3 "Unit factors:
       Length scale       : VALUE
       Force scale        : VALUE
       Temperature scale  : VALUE
       Temperature offset : VALUE";
#4 "Starting reading points at line INT.";
#5 "Points not in order starting at point INT";
#6 "Starting reading cells at line INT.";
#7 "First occurrence of element type INT for cell INT at line INT";
#8 "Line: INT element: INT type: INT collapsed from INT to: INT";
#9 "Read INT cells and INT boundary faces.";
#10 "For group INT named STR trying to read INT patch face indices.";
#11 "Starting reading constraints at line INT.";
#12 "For DOF set INT named STR trying to read vertex indices.";
#13 "Processing tag: STR";
#14 "Skipping tag STR on line INT";
#15 "Using INT DOF sets to detect boundary faces.";
#16 "Sorting boundary faces according to group (patch)";
#17 "Writing boundary faces to OBJ file boundaryFaces.obj";
#18 "Constructing mesh with non-default patches of size
      INT \t INT";
#19 "Adding cell and face zones
      Cell Zone STR INT";
      Face Zone STR INT";


&1 "Points not in order starting at point ";
&2 "Cannot open file ";
&3 "Cell INT unv vertices INT has some undefined vertices ";
&4 "Boundary face INT unv vertices INT has some undefined vertices ";
&5 "The face index INT was not found amongst the cells. This kills the theory that INT is a cell zone ";
'''
#---------------------------------------------------------------------------------------------------------------------- 


import os
import pytest
import subprocess

from OFCase.UnvMeshConverter import UnvMeshConverter
from Utils.REParser import REParser

def parse_message(match, lines, index):
    return match.group(0)


def test_UnvMeshConverter(monkeypatch):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir, _ = os.path.split(curr_dir)
    package_dir = os.path.split(module_dir)[0]
     
    mesh_file =  os.path.join(package_dir, '_data/Mesh_1.Unv')   
         
    unv = UnvMeshConverter(mesh_file)
    unv_output_file = os.path.join(package_dir, '_data/Logs_OFRun/log.ideasUnvToFoam')
    
    class MonkeyProcess(object):
        @property
        def stdout(self):
            return self._file
        
        def poll(self):
            last_line = 4113
            if self._file.tell() == last_line:
                return 0
            
            
        def __init__(self):
            self._file = open(unv_output_file, 'r')
        
    def monkey(cmd, *args, **kwargs):
        return MonkeyProcess()
    
    monkeypatch.setattr("subprocess.Popen", monkey)
    
    
    unv.Runner()
    results = unv.ParseBuffer()
    
    entries_expected = {
        'E#01' : 0,
        'E#02' : 0,
        'E#03' : 0,
        'E#04' : 0,
        'E#05' : 0,
        'W#01' : 1,
        'W#02' : 1,
        'W#03' : 1,
        'W#04' : 1,
        'W#05' : 0,
        'W#06' : 1,
        'W#07' : 5,
        'W#08' : 0,
        'W#09' : 1,
        'W#10' : 16,
        'W#11' : 0,
        'W#12' : 0,
        'W#13' : 0,
        'W#14' : 1,
        'W#15' : 0,
        'W#16' : 0,
        'W#17' : 0,
        'W#18' : 1,
        'W#19' : 1,
        
    }
    
    for key, item in results.iteritems():
        assert entries_expected[key] == len(item)
        
    


    
    
    
    
    
    