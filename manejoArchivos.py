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
        return self.drive.ListFile({'q': f"'{self.idRuta}'" + " in parents and trashed=false"}).GetList()

    def verArchivosDrive(self):
        for file in self.fileList():
            print('ID: %s, Nombre: %s, Extension: %s, Owner: %s, Visibilidad: %s, Ultima modificacion: %s, Email del owner: %s' % ( file['id'], file['title'], file['fileExtension'], ' '.join(file['ownerNames']), file['shared'], file['modifiedDate'], file['owners'][0]['emailAddress']))

    def visibilidadDe(self, file):
        if (file['shared']):
            return 'Publico'
        else:
            return 'Privado'

    def cambiarVisibilidadAPrivada(self, file):
        try:
            file['shared'] = False
            permissions = file.GetPermissions()
            for permission in permissions:
                if (permission['id'] == file['owners'][0]['permissionId']):
                    next
                else:
                    file.DeletePermission(permission['id'])
            
            file.UpdateMetadata()
            file.Upload()
            
            print("Se modifico la visibilidad del archivo: %s a Privado" % file['title'])
        except error:
            print('No se pudo cambiar la visibilidad del archivo a Privada: %s' % error)
            return None

    def encontrarArchivoPorId(self, fileId):
        for archivo in self.fileList():
            if(archivo['id'] == fileId):
                return archivo
        print("No se ha podido encontrar el archivo en la lista")
        return None

    def encontrarArchivoPorNombre(self, nombre):
        for archivo in self.fileList():
            if(archivo['title'] == nombre):
                return archivo
        print("No se ha podido encontrar el archivo en la lista")
        return None

    def eliminarArchivoDelDrive(self, file):
        try:
            file.Delete()
            print("Se ha eliminado el archivo: %s del Google Drive" % file['title'])
        except:
            print("No se ha podido eliminar el archivo: %s del Google Drive" % file['title'])
    

    def crearArchivo(self, nombre):
        try:
            file = self.drive.CreateFile({"title": nombre, "parents": [{"kind": "drive#fileLink", "id": self.idRuta}]})
            file.Upload()
            print("Se subió a Google Drive el archivo: %s" % file['title'])
        except:
            print("No se ha podido subir a Google Drive el archivo: %s" % nombre)

    def crearArchivoPublico(self, nombre):
        try:
            file = self.drive.CreateFile({"title": nombre, "shared": True, "parents": [{"kind": "drive#fileLink", "id": self.idRuta}]})
            file.Upload()
            file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
            print("Se subió a drive el archivo: %s con visibilidad Publico" % file['title'])
        except:
            print("No se ha podido subir a drive el archivo: %s" % nombre)