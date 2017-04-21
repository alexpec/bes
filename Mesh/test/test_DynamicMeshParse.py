import os
import pytest
import shutil

from Mesh.DynamicMeshParser import DynamicMeshParser
from Parameters.ScalarParameter import ScalarParameter
from Parameters.StringParameter import StringParameter

#=======================================================================================================================
# FIXTURES
#=======================================================================================================================

@pytest.fixture(scope='module')
def create_model_file(tmpdir_factory):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.split(curr_dir)[0]
    
    file = os.path.join(modules_dir, r'_data/CreatedSalomeScriptModel.py')
    fn = tmpdir_factory.mktemp('tmp_data')#.join('model.py')
    shutil.copy2(file, str(fn))
    
    return fn

#=======================================================================================================================
# TESTS
#=======================================================================================================================


def test_MeshScriptParser(create_model_file):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.split(curr_dir)[0]
    
    file_path = os.path.join(modules_dir, r'_data')
    tagged_file = os.path.join(file_path, r'DynamicSensor_Tagged.py')
    
    created_file = create_model_file.join(r'created.py')
    model_file = create_model_file.join(r'CreatedSalomeScriptModel.py')
    
    #Creating the file
    dataPath            = StringParameter('dataPath', '%%%systemParameter_data_path%%%')
    UNV_MeshName        = StringParameter('UNV_MeshName', '%%%systemParameter_UNV_MeshName%%%')
    
    b                   = ScalarParameter('b', '%%%geometricParam_b%%%', float)
    BarrelCenterline    = ScalarParameter('BarrelCenterline', '%%%geometricParam_BarrelCenterline%%%', float)
    BarrelRadius        = ScalarParameter('BarrelRadius', '%%%geometricParam_BarrelRadius%%%', float)
    VoidCenterline      = ScalarParameter('VoidCenterline', '%%%geometricParam_VoidCenterline%%%', float)
    VoidRadius          = ScalarParameter('VoidRadius', '%%%geometricParam_VoidRadius%%%', float)
    
    parser = DynamicMeshParser(tagged_file)
    parser.AddParameter(dataPath)
    parser.AddParameter(UNV_MeshName)
    parser.AddParameter(b)
    parser.AddParameter(BarrelCenterline)
    parser.AddParameter(BarrelRadius)
    parser.AddParameter(VoidCenterline)
    parser.AddParameter(VoidRadius)
    
    
    param_dict = {
            'dataPath'           : "r'%s'" %file_path,
            'UNV_MeshName'       : "'Mesh_1.Unv'",
            'b'                  : 9.0,
            'BarrelCenterline'   : 15.0,
            'BarrelRadius'       : 5.0,
            'VoidCenterline'     : 20.0,
            'VoidRadius'         : 4.0,
        }
    
    parser.ParseParameters(param_dict, str(created_file))
    
    #Parsing and comparing the file
    model = open(str(model_file), 'r')
    create = open(str(created_file), 'r')
    
    read_model = model_file.read()
    read_created = created_file.read()
    
    assert read_model == read_created
    
    #line_model = model.readline()
    #line_created = create.readline()
    #
    #while line_model:
    #    import pdb;pdb.set_trace()
    #    assert line_model == line_created
    #    line_model = model.readline()
    #    line_created = create.readline()
        
    model.close()
    create.close()
    
    

