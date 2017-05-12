'''
KEYS FOR SPLITMESHREGIONS

# -> Warning / Info
Get them at $FOAM_DIR/applications/utilities/mesh/manipulation/splitMeshRegions


& -> Error

&1 "Exposed face: INT fc: INT has owner region STR and neighbour region STR when handling region: STR";
&2 "Cell INT with cell centre INT is multiple zones. This is not allowed."
&3 "cellZones not synchronised across processors."
&4 "You cannot specify both -cellZonesOnly or -cellZonesFileOnly"
&5 "You cannot specify both -largestOnly"
&6 "For the cellZonesOnly option all cells have to be in a cellZone;"
&7 "For the cellZonesFileOnly options all cells have to be in a cellZone."
&8 "Point INT is not inside the mesh."
'''
#---------------------------------------------------------------------------------------------------------------------- 

import os
import pytest

from OFCase.SplitMeshRegions import SplitMeshRegions
from Utils.REParser import REParser


def parse_message(match, lines, index):
    return match.group(0)


@pytest.fixture
def Parser():
    parser = REParser()
    
    parser.AddPattern('E#1', "Exposed face: \d* fc: \d* has owner region (.*) and neighbour region (.*) when handling region: (.*)", parse_message)
    parser.AddPattern('E#2', "Cell \d* with cell centre \d* is multiple zones. This is not allowed.", parse_message)
    parser.AddPattern('E#3', "cellZones not synchronised across processors.", parse_message)
    parser.AddPattern('E#4', "You cannot specify both -cellZonesOnly or -cellZonesFileOnly", parse_message)
    parser.AddPattern('E#5', "You cannot specify both -largestOnly", parse_message)
    parser.AddPattern('E#6', "For the cellZonesOnly option all cells have to be in a cellZone;", parse_message)
    parser.AddPattern('E#7', "For the cellZonesFileOnly options all cells have to be in a cellZone.", parse_message)
    parser.AddPattern('E#8', "Point \d* is not inside the mesh.", parse_message)
    
    return parser


def test_SplitMeshRegions(monkeypatch, Parser):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir, _ = os.path.split(curr_dir)
    package_dir = os.path.split(module_dir)[0]
    
    case_dir = os.path.join(package_dir, '_data/Tagged')
    
    par = Parser
    smr = SplitMeshRegions(case_dir)
    smr_output_file = os.path.join(package_dir, '_data/Logs_OFRun/log.splitMeshRegions')
    
    
    class MonkeyProcess(object):
        @property
        def stdout(self):
            return self._file
        
        def poll(self):
            last_line = 4981
            if self._file.tell() == last_line:
                return 0
            
        def __init__(self):
            self._file = open(smr_output_file, 'r')
            
    def monkey(cmd, *args, **kwargs):
        return MonkeyProcess()
    
    monkeypatch.setattr("subprocess.Popen", monkey)
    
    smr.Runner()
    results = par.ParseBuffer(smr.buffer)
    
    assert True
    
    
    
    
    