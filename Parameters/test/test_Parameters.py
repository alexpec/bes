import pytest
from Parameters.ScalarParameter import ScalarParameter
from Parameters.StringParameter import StringParameter
from Parameters.FieldParameter import FieldParameter
from Parameters.ScalarListParameter import ScalarListParameter
from Parameters.FieldListParameter import FieldListParameter



classes = [
        ScalarParameter,
        FieldParameter,
        ScalarListParameter,
        FieldListParameter
    ]

properties_names = [
        'name',
        'tag',
        'param_type',
        'dimension',
    ]

method_names = []

def test_numerical_instantiation():
    name        = 'test'
    tag         = '%%test%%'
    param_type  = float
    dimension   = [0,0,0,0,0,0,0,0,0]
    
    #Test with dimension None
    for k in classes:
        a = k(name, tag, param_type)
        
        assert a.name == name
        assert a.tag == tag
        assert a.param_type == param_type
        assert a.dimension == None
        
        del a 
        
    #Test with given dimension
    for k in classes:
        a = k(name, tag, param_type, dimension)
        
        assert set(a.dimension) == set(dimension)
        
        del a
        
        
def test_string_instantiation():
    name        = 'test'
    tag         = '%%test%%'
    param_type  = str
    dimension   = None
    
    a = StringParameter(name, tag, param_type, dimension)
    assert a.name == name
    assert a.tag == tag
    assert a.param_type == param_type
    assert a.dimension == None
    
        
