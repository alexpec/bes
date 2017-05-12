import pytest
from Parameters.ScalarParameter import ScalarParameter
from OFCase.CaseTagReplacer import CaseTagReplacer
import os
from OFCase.CaseGenerator import CaseGenerator





@pytest.fixture(scope='module')
def create_model_dir(tmpdir_factory):
    fn = tmpdir_factory.mktemp('tmp_data')
    
    return fn
    

def _assertData(tagged_case_path, expected_case_path, file_path):
    created_filepath = os.path.join(tagged_case_path, file_path)
    expected_filepath = os.path.join(expected_case_path, file_path)
    
    created_file = open(created_filepath, 'r')
    expected_file = open(expected_filepath, 'r')
    
    created_lines = created_file.readlines()
    expected_lines = expected_file.readlines()
    
    for idx, line in enumerate(expected_lines):
        assert line == created_lines[idx]


def test_CaseTagReplacer(create_model_dir):
    #Creating the Parameters
    artcr_t     = ScalarParameter('ARTCR_T', '%%%ARTCR_T%%%')
    crtw_t      = ScalarParameter('CRTW_T', '%%%CRTW_T%%%')
    
    barrel_h    = ScalarParameter('Barrel_hp', '%%%Barrel_hp%%%')
    barrel_cp   = ScalarParameter('Barrel_cp', '%%%Barrel_cp%%%')
    
    warhead_h   = ScalarParameter('Warhead_hp', '%%%Warhead_hp%%%')
    warhead_cp  = ScalarParameter('Warhead_cp', '%%%Warhead_cp%%%')
    warhead_rho = ScalarParameter('Warhead_rho', '%%%Warhead_rho%%%')
    
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir, _ = os.path.split(curr_dir)
    package_dir = os.path.split(module_dir)[0]
    
    tagged_case_path = os.path.join(package_dir, '_data/Tagged')
    case_destination = str(create_model_dir)
    mesh_file = os.path.join(package_dir, '_data/Mesh_1.Unv')
    
    expected_case_path = os.path.join(package_dir, '_data/Original')

    generator = CaseGenerator(tagged_case_path, case_destination, mesh_file, True)
    generator.CopyCase()

    parser = CaseTagReplacer(case_destination)

    parser.AddParameter(artcr_t)
    parser.AddParameter(crtw_t)
    parser.AddParameter(barrel_h)
    parser.AddParameter(barrel_cp)
    parser.AddParameter(warhead_h)
    parser.AddParameter(warhead_cp)
    parser.AddParameter(warhead_rho)
    
    param_dict = {
        'ARTCR_T'                   : 300.0,
        'CRTW_T'                    : 300.0,
        'Barrel_hp'                 : 0.0,
        'Barrel_cp'                 : 490.0,
        'Warhead_hp'                : 0.0,
        'Warhead_cp'                : 490.0,
        'Warhead_rho'               : 8000.0
    }
    
    
    parser.ParseCase(param_dict)
    
    #Testing First parameter replacement
    file_path = [
#         '0/Air_rotated/T',
#         '0/Calorimeter_rotated/T',
        'constant/Barrel_rotated/thermophysicalProperties',
#         'constant/Warhead_rotated/thermophysicalProperties'
    ]
    
    for file in file_path:
        _assertData(case_destination, expected_case_path, file)
    
    
    
    
    