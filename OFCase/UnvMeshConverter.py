from Utils.TerminalRunner import TerminalRunner
from Utils.REParser import REParser




class UnvMeshConverter(TerminalRunner):
    @property
    def of_environment_cmd(self):
        return self._of_environment_cmd
    
    @property
    def unv_mesh_path(self):
        return self._unv_mesh_path
    
    @property
    def buffer(self):
        return super(UnvMeshConverter, self).buffer
    
    @property
    def parser(self):
        return self._parser
    
    @property
    def parse_message(self):
        return self._parseMessage
    
    def _parseMessage(self, match, lines, index):
        return match.group(0)
    
    def _setUpParser(self):
        self._parser.AddPattern('W#01', 'Skipping section at line \d*', self.parse_message)
        self._parser.AddPattern('W#02', 'Starting reading units at line \d*', self.parse_message)
        self._parser.AddPattern('W#03', 'Unit factors*', self.parse_message)
        self._parser.AddPattern('W#04', 'Starting reading points at line \d*.', self.parse_message)
        self._parser.AddPattern('W#05', 'Points not in order starting at point \d*.', self.parse_message)
        self._parser.AddPattern('W#06', 'Starting reading cells at line \d*.', self.parse_message)
        self._parser.AddPattern('W#07', 'First occurrence of element type \d* for cell \d* at line \d*', self.parse_message)
        self._parser.AddPattern('W#08', 'Line: \d* element: \d* type: \d* collapsed from \d* to: \d*', self.parse_message)
        self._parser.AddPattern('W#09', 'Read \d* cells and \d* boundary face', self.parse_message)
        self._parser.AddPattern('W#10', 'For group \d* named (.*) trying to read \d* patch face indices.', self.parse_message)
        self._parser.AddPattern('W#11', 'Starting reading constraints at line \d*', self.parse_message)
        self._parser.AddPattern('W#12', 'For DOF set \d* named (.*) trying to read vertex indices.', self.parse_message)
        self._parser.AddPattern('W#13', 'Processing tag: (.*)', self.parse_message)
        self._parser.AddPattern('W#14', 'Skipping tag (.*) on line \d*', self.parse_message)
        self._parser.AddPattern('W#15', 'Using \d* DOF sets to detect boundary faces', self.parse_message)
        self._parser.AddPattern('W#16', 'Sorting boundary faces according to group (patch)', self.parse_message)
        self._parser.AddPattern('W#17', 'Writing boundary faces to OBJ file boundaryFaces.obj', self.parse_message)
        self._parser.AddPattern('W#18', 'Constructing mesh with non-default patches of size', self.parse_message)
        self._parser.AddPattern('W#19', 'Adding cell and face zones', self.parse_message)
        
        self._parser.AddPattern('E#01', 'Points not in order starting at point', self.parse_message)
        self._parser.AddPattern('E#02', 'Cannot open file', self.parse_message)
        self._parser.AddPattern('E#03', 'Cell \d* unv vertices \d* has some undefined vertices', self.parse_message)
        self._parser.AddPattern('E#04', 'Boundary face \d* unv vertices \d* has some undefined vertices', self.parse_message)
        self._parser.AddPattern('E#05', 'The face index \d* was not found amongst the cells. This kills the theory that \d* is a cell zone', self.parse_message)
        
    
    def __init__(self, unv_mesh_path, of_environment_cmd=None):
        super(UnvMeshConverter, self).__init__()
        
        self._unv_mesh_path = unv_mesh_path
        self._of_environment_cmd = of_environment_cmd
        
        self._parser = REParser()
        self._setUpParser()
        
        
    def Runner(self):
        if self._of_environment_cmd != None:
            cmd = '%s || ideasUnvToFoam %s' %(
                self._of_environment_cmd,
                self._unv_mesh_path)
        else:
            cmd = 'ideasUnvToFoam %s' %self._unv_mesh_path

        super(UnvMeshConverter, self).Runner(cmd)
        
        
    def ParseBuffer(self):
        results = self.parser.ParseBuffer(self.buffer)
        return results
        
    
    