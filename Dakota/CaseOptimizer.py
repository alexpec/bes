from OFCase.CaseGenerator import CaseGenerator
import os
from Mesh.DynamicMeshParser import DynamicMeshParser
from OFCase.CaseTagReplacer import CaseTagReplacer
from OFCase.UnvMeshConverter import UnvMeshConverter
from OFCase.SplitMeshRegions import SplitMeshRegions





class CaseOptimizer(object):
    @property
    def parameters(self):
        return self._parameters
    
    @property
    def base_case(self):
        return self._base_case
    @base_case.setter
    def base_case(self, value):
        self._base_case = value
    
    @property
    def run_folder(self):
        return self._run_folder
    @run_folder.setter
    def run_folder(self, value):
        self._run_folder = value
        
    @property
    def mesh_file(self):
        return self._mesh_file
    @mesh_file.setter
    def mesh_file(self, value):
        self._mesh_file = value
        
    @property
    def dakota_input(self):
        return self._dakota_input
    @dakota_input.setter
    def dakota_input(self, value):
        self._dakota_input = value
    
    
    def __init__(self,
                 base_case,
                 run_folder,
                 mesh_file,
                 dakota_input
                 ):
        self._parameters = {}
        self._base_case = base_case
        self._run_folder = run_folder
        self._mesh_file = mesh_file
        self._dakota_input = dakota_input
        
        
    def AddParameter(self, parameter):
        self._parameters[parameter.name] = parameter
        
    def _RunCaseGenerator(self):
        base_case = self._base_case
        dest_case = self._run_folder
        mesh_file = self._mesh_file
        
        generator = CaseGenerator(base_case, dest_case, mesh_file, True)
        generator.CopyCase()
        
        return True
    
    def _MeshParser(self, param_dict):
        run_folder = self._run_folder
        mesh_file = self._mesh_file
        parameters = self._parameters
        
        _, mesh_file_name = os.path.split(mesh_file)
        created_mesh = os.path.join(run_folder, mesh_file_name)
        
        parser = DynamicMeshParser(mesh_file)
        
        for key, item in parameters.iteritems():
            parser.AddParameter(item)
            
        parser.ParseParameters(param_dict, str(created_mesh))
        
        return True
    
    def _CaseParser(self, param_dict):
        run_folder = self._run_folder
        parameters = self._parameters
        
        parser = CaseTagReplacer(run_folder)
        for key, item in parameters.iteritems():
            parser.AddParameter(item)
            
        parser.ParseCase(param_dict)
        
        return True
    
    def _UnvMeshConverter(self):
        run_folder = self._run_folder
        mesh_file = self._mesh_file
        parameters = self._parameters
        
        _, mesh_file_name = os.path.split(mesh_file)
        created_mesh = os.path.join(run_folder, mesh_file_name)
        
        unv = UnvMeshConverter(created_mesh)
        #Insert here the parser for UNV data
        
        
        return True
    
    
    def _SplitMeshRegions(self):
        run_folder = self._run_folder
        
        smr = SplitMeshRegions(run_folder, True, False)
        #Insert here the parser for SMR
        
        return True
        
        
        
    
    
    
    
        
        
        
    
    
    