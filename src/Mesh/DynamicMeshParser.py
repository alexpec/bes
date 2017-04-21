from Parameters.SystemParameter import SystemParameter
from Parameters.ScalarParameter import GeometricParameter





#===============================================================================
# DynamicMeshParser
#===============================================================================
class DynamicMeshParser(object):
    '''
    Parses the mesh file in order to deal with the geometric parameters.
    '''
    @property
    def tagged_file(self):
        return self._tagged_file
    
    @property
    def parameters(self):
        return self._parameters
    
    
    
    def __init__(self, tagged_file):
        self._parameters = {}
        self._tagged_file = tagged_file
    
    
    def AddParameter(self, parameter):
        self._parameters[parameter.name] = parameter


    
    def RemoveParameter(self, parameter):
        #Verify if the parameter is present
        if parameter.name not in self._parameters.keys():
            raise Exception("The parameter %s is not in the parameters list" %parameter.name)
        
        del self._parameters[parameter.name]
    

    
    def ParseParameters(self, param_dict, output_file):
        
        #Reading the original file
        input = open(self.tagged_file, 'r')
        input_data = input.read()
        input.close()
        
        for key, item in param_dict.iteritems():
            #Verify if the parameter exists
            if key not in self.parameters.keys():
                raise Exception("Parameter %s does not exist. You must add the parameter first" %key)
            
            param = self.parameters[key]
            
            #verify if the input value is the same type of parameter
            if param.param_type != type(item):
                raise Exception("Parameter type %s is not the same type of input type %s" %(str(param.param_type), str(type(item))))
                
            input_data = input_data.replace(param.tag, str(item))   
            
        output = open(output_file, 'w')
        output.write(input_data)
        output.close()
        
        
        
        
if __name__ == '__main__':
    dataPath            = SystemParameter('dataPath', '%%%systemParameter_data_path%%%')
    UNV_MeshName        = SystemParameter('UNV_MeshName', '%%%systemParameter_UNV_MeshName%%%')
    
    b                   = GeometricParameter('b', '%%%geometricParam_b%%%', float)
    BarrelCenterline    = GeometricParameter('BarrelCenterline', '%%%geometricParam_BarrelCenterline%%%', float)
    BarrelRadius        = GeometricParameter('BarrelRadius', '%%%geometricParam_BarrelRadius%%%', float)
    VoidCenterline      = GeometricParameter('VoidCenterline', '%%%geometricParam_VoidCenterline%%%', float)
    VoidRadius          = GeometricParameter('VoidRadius', '%%%geometricParam_VoidRadius%%%', float)
    
    parser = DynamicMeshParser(r'/home/alexpec/Development/Workspace/Bes/src/Mesh/_data/DynamicSensor_Tagged.py')
    parser.AddParameter(dataPath)
    parser.AddParameter(UNV_MeshName)
    parser.AddParameter(b)
    parser.AddParameter(BarrelCenterline)
    parser.AddParameter(BarrelRadius)
    parser.AddParameter(VoidCenterline)
    parser.AddParameter(VoidRadius)
    
    
    param_dict = {
            'dataPath'           : "r'/home/alexpec/Development/Workspace/Bes/src/Mesh/_data'",
            'UNV_MeshName'       : "'Mesh_1.Unv'",
            'b'                  : 9.0,
            'BarrelCenterline'   : 15.0,
            'BarrelRadius'       : 5.0,
            'VoidCenterline'     : 20.0,
            'VoidRadius'         : 4.0,
        }
    
    parser.ParseParameters(param_dict, r'/home/alexpec/Development/Workspace/Bes/src/Mesh/_data/create.py')
    
        
            
            