from Utils.ParameterParser import ParameterParser
import os




class CaseTagReplacer(ParameterParser):
    @property
    def case_path(self):
        return self._case_path
    
    @property
    def parameters(self):
        return super(CaseTagReplacer, self)._parameters
    
    
    def __init__(self, case_path):
        super(CaseTagReplacer, self).__init__()
        self._case_path = case_path
        
    
    def ParseCase(self, param_dict):
        files_to_parse = []
        for root, dirs, files in os.walk(self._case_path, topdown=True):
            tmp_file_path = os.path.join(root, files)
            files_to_parse.append(tmp_file_path)
            
        
        for file in files_to_parse:
            self.ParseParameters(param_dict, file, file)
            
    
