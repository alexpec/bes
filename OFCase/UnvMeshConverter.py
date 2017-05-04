from Utils.TerminalRunner import TerminalRunner




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
    
    def __init__(self, unv_mesh_path, of_environment_cmd=None):
        super(UnvMeshConverter, self).__init__()
        
        self._unv_mesh_path = unv_mesh_path
        self._of_environment_cmd = of_environment_cmd
        
        
    def Runner(self):
        if self._of_environment_cmd != None:
            cmd = '%s || ideasUnvToFoam %s' %(
                self._of_environment_cmd,
                self._unv_mesh_path)
        else:
            cmd = 'ideasUnvToFoam %s' %self._unv_mesh_path

        super(UnvMeshConverter, self).Runner(cmd)
        
    
    