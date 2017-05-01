from Utils.TerminalRunner import TerminalRunner




class UnvMeshConverter(TerminalRunner):
    @property
    def of_environment_cmd(self):
        return self._of_environment_cmd
    
    @property
    def unv_mesh_path(self):
        return self._unv_mesh_path
    
    @property
    def quiet(self):
        return self._quiet
    
    def __init__(self, unv_mesh_path, of_environment_cmd=None, quiet=False):
        super(UnvMeshConverter, self).__init__()
        
        self._unv_mesh_path = unv_mesh_path
        self._of_environment_cmd = of_environment_cmd
        self._quiet = quiet
        
        
    def Runner(self):
        if self._of_environment_cmd != None:
            cmd = '%s || ideasUnvToFoam %s' %(
                self._of_environment_cmd,
                self._unv_mesh_path)
        else:
            cmd = 'ideasUnvToFoam %s' %self._unv_mesh_path
            

        self.Runner(cmd)
        
    
    