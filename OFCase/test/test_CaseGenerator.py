import pytest
import os
from OFCase.CaseGenerator import CaseGenerator




@pytest.fixture(scope='module')
def create_temporary_folder(tmpdir_factory):
    fn = tmpdir_factory.mktemp('tmp_data')
    
    return fn


def _walk_in_dir(dir):
    base_dict = {}
    initial_dir = os.path.split(dir)[1]
    
    
    for root, dirs, files in os.walk(dir, topdown=True):
        root_parse = os.path.split(root)[1]
        if root_parse == initial_dir:
            root_parse = 'BASE'
        base_dict[root_parse] = [[],[]]
        for name in files:
            base_dict[root_parse][0].append(os.path.join(root_parse, name))
            
        for name in dirs:
            base_dict[root_parse][1].append(os.path.join(root_parse, name))
            
    return base_dict



def test_CaseGenerator(create_temporary_folder):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.split(curr_dir)[0]
    
    base_folder = os.path.join(module_dir, r'_data/Tagged')
    case_destination = str(create_temporary_folder)
    
    mesh_file = os.path.join(module_dir, r'_data/Mesh_1.Unv')
    
    
    generator = CaseGenerator(base_folder, case_destination, mesh_file, True)
    generator.CopyCase()
    
    base_walk = _walk_in_dir(base_folder)
    copy_walk = _walk_in_dir(case_destination)
    
    
    for key, item in base_walk.iteritems():
        try:
            assert copy_walk.get(key) != None
        except:
            import pdb;pdb.set_trace()
        
        
        copy_items = copy_walk.get(key)
        for idx, file in enumerate(copy_items[0]):
            #Removing mesh file that is not in the original case
            if os.path.split(file)[1] == os.path.split(mesh_file)[1]:
                continue
            
            assert item[0][idx] == file
            
        for idx, dir in enumerate(copy_items[1]):
            assert item[1][idx] == dir
            
    
    
    