import pytest

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
from Utils.REParser import REParser
import subprocess
import os
from OFCase.UnvMeshConverter import UnvMeshConverter
from threading import Thread
from time import sleep
# from _pytest.monkeypatch import monkeypatch

def parse_message(match, lines, index):
    return match.group(0)


@pytest.fixture
def Parser():
    
    parser = REParser()
    
    parser.AddPattern('W#01', 'Skipping section at line \d*', parse_message)
    parser.AddPattern('W#02', 'Starting reading units at line \d*', parse_message)
    parser.AddPattern('W#03', 'Unit factors*', parse_message)
    parser.AddPattern('W#04', 'Starting reading points at line \d*.', parse_message)
    parser.AddPattern('W#05', 'Points not in order starting at point \d*.', parse_message)
    parser.AddPattern('W#06', 'Starting reading cells at line \d*.', parse_message)
    parser.AddPattern('W#07', 'First occurrence of element type \d* for cell \d* at line \d*', parse_message)
    parser.AddPattern('W#08', 'Line: \d* element: \d* type: \d* collapsed from \d* to: \d*', parse_message)
    parser.AddPattern('W#09', 'Read \d* cells and \d* boundary face', parse_message)
    parser.AddPattern('W#10', 'For group \d* named (.*) trying to read \d* patch face indices.', parse_message)
    parser.AddPattern('W#11', 'Starting reading constraints at line \d*', parse_message)
    parser.AddPattern('W#12', 'For DOF set \d* named (.*) trying to read vertex indices.', parse_message)
    parser.AddPattern('W#13', 'Processing tag: (.*)', parse_message)
    parser.AddPattern('W#14', 'Skipping tag (.*) on line \d*', parse_message)
    parser.AddPattern('W#15', 'Using \d* DOF sets to detect boundary faces', parse_message)
    parser.AddPattern('W#16', 'Sorting boundary faces according to group (patch)', parse_message)
    parser.AddPattern('W#17', 'Writing boundary faces to OBJ file boundaryFaces.obj', parse_message)
    parser.AddPattern('W#18', 'Constructing mesh with non-default patches of size', parse_message)
    parser.AddPattern('W#19', 'Adding cell and face zones', parse_message)
    
    parser.AddPattern('E#01', 'Points not in order starting at point', parse_message)
    parser.AddPattern('E#02', 'Cannot open file', parse_message)
    parser.AddPattern('E#03', 'Cell \d* unv vertices \d* has some undefined vertices', parse_message)
    parser.AddPattern('E#04', 'Boundary face \d* unv vertices \d* has some undefined vertices', parse_message)
    parser.AddPattern('E#05', 'The face index \d* was not found amongst the cells. This kills the theory that \d* is a cell zone', parse_message)
    
    return parser

def test_UnvMeshConverter(monkeypatch, Parser):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir, _ = os.path.split(curr_dir)
     
    mesh_file =  os.path.join(module_dir, '_data/Mesh_1.Unv')   
         
    par = Parser
    unv = UnvMeshConverter(mesh_file)
    unv_output_file = os.path.join(module_dir, '_data/Logs_OFRun/log.ideasUnvToFoam')
    
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
    results = par.ParseBuffer(unv.buffer)
    
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
        
    


    
    
    
    
    
    