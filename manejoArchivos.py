from logging import error
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class ManejoArchivos:

    def __init__(self, idRuta):
        self.idRuta = idRuta
        self.gauth = GoogleAuth() # Toma la informacion del 'client_secrets.json', es decir, linkea la credencial con la app
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        
    # La lista de archivos debe ser un metodo calculable dado que tiene que estar actualizada siempre que se llama
    def fileList(self):
        return filter(self.esFile,self.allFiles())
    
    def allFiles(self):
        return self.drive.ListFile({'q': f"'{self.idRuta}'" + " in parents and trashed=false"}).GetList()
    
    def esFile(self, file):
        return file['mimeType'] != 'application/vnd.google-apps.folder'

    def quitarPermisos(self, file):
        file['shared'] = False
        permissions = file.GetPermissions()
        for permission in permissions:
            if (permission['id'] != file['owners'][0]['permissionId']):
                file.DeletePermission(permission['id'])
        

    def cambiarVisibilidadAPrivada(self, file):
        self.quitarPermisos(file)       
        file.UpdateMetadata()
        file.Upload()
            