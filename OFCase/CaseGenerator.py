import shutil
import os




class CaseGenerator(object):
    @property
    def base_folder(self):
        return self._base_folder
    
    @property
    def case_destination(self):
        return self._case_destination
    
    @property
    def overwrite_folder(self):
        return self._overwrite_folder
    
    @property
    def mesh_file(self):
        return self._mesh_file
    
    
    
    def _VerifyFileExistance(self, file):
        return os.path.exists(file)
    
    
    def _CopyFolderTree(self, src, dest):
        exists = self._VerifyFileExistance(self._case_destination)
        if exists and self._overwrite_folder == False:
            raise Exception("The destination file already exists and I'm not allowed to overwrite it")
        
        if exists:
            shutil.rmtree(dest)
            
        shutil.copytree(src, dest, False)
        
        
    def _CopyMeshFile(self, dest_dir):
        
        msh_filename = os.path.split(self._mesh_file)[1]
        
        file_in_dest_folder = os.path.join(dest_dir, msh_filename)
        exist_dest_file = self._VerifyFileExistance(file_in_dest_folder)
        
        
        if exist_dest_file:
            os.remove(file_in_dest_folder)
            
        shutil.copy2(self._mesh_file, file_in_dest_folder)
        
        
    
    def __init__(self, base_folder, case_destination, mesh_file, overwrite_folder=False):
        '''
        Initializes the tool used to copy the base case
        :param base_folder: {str} - path to the folder where the base case is;
        :param case_destination: {str} - path to the folder where the case will be copied in order to run
        :param mesh_file: {str} - path to the parsed mesh file;
        :param overwrite_folder: {str} - if the file already exists defines if it will be overwrite;
        '''
        self._base_folder = base_folder
        self._case_destination = case_destination
        self._mesh_file = mesh_file
        self._overwrite_folder = overwrite_folder
        
        
    def CopyCase(self):
        self._CopyFolderTree(self._base_folder, self._case_destination)
        self._CopyMeshFile(self._case_destination)
        
        
    