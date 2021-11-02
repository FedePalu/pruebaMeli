from manejoArchivos import *
from usuarioService import *
from types import new_class
import mysql.connector

from datetime import *     

class BaseDeDatosService:

    def __init__(self, base, usuarioService, archivoService):
        self.baseDeDatos = base
        self.mailService = usuarioService
        self.archivoService = archivoService

    def mostrarBaseDeDatos():
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")
        cursor1 = conexion1.cursor()
        cursor1.execute("show databases")
        for base in cursor1:
            print(base)
        conexion1.close()
    
    # Método a ejecutar en algún main para la carga de todos los archivos drive a la database.
    def subirTodosLosArchivosDelDrive(self):
        for file in self.archivoService.fileList():
            self.insertarEnArchivosDrive(file)

    def insertarEnArchivosDrive(self,file):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database= self.baseDeDatos)
        cursor1 = conexion1.cursor()
        
        if(self.enLaBaseEstaElArchivo(file, "archivosdrive") and (not self.laFechaDeModificacionEsMasNueva(file))):
            print("El archivo de nombre: %s ya esta en la base y no tiene modificacion reciente" % file['title']) 
            return None        
        else:
            query ="insert into ArchivosDrive(nombre, ext, owner, visibilidad, fecha_modificacion, file_id) values (%s,%s,%s,%s,%s,%s)"
        
        if (file['shared']):
            visibilidad = "Publico"
            self.archivoService.cambiarVisibilidadAPrivada(file)
            mailAsunto = "Visibilidad de su archivo %s" % file['title']
            mailBody = "Se ha cambiado la visibilidad de su archivo con nombre: %s a Privado por causa de seguridad."
            self.mailService.enviarCorreo(file['owners'][0]['emailAddress'], mailAsunto, mailBody)
            self.insertarEnHistorialArchivosPublicos(file)
        else:
            visibilidad = "Privado"
        
        datos = (file['title'], file['fileExtension'], ' '.join(file['ownerNames']), visibilidad, file['modifiedDate'], file['id'])        
        cursor1.execute(query, datos)

        conexion1.commit()
        conexion1.close()
        print("Se ha agregado a la base de datos el archivo de id: %s y nombre: %s" % (file['id'], file['title']))
           

    def laFechaDeModificacionEsMasNueva(self, file):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database= self.baseDeDatos)
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT file_id, fecha_modificacion FROM archivosdrive")
        archivos = cursor1.fetchall()

        for archivo in archivos:
            if(archivo[0] == file['id']):
                conexion1.close()
                return archivo[1] < datetime.strptime(file['modifiedDate'][0:19],'%Y-%m-%dT%H:%M:%S') 
                #Formato RFC 3339 '%Y-%m-%dT%H:%M:%S.%fZ'
                #Se le debe colocar el [0:19] dado que el file['modifiedDate] trae consigo milesimas de segundos (.%f) que no son captados por archivo[1] por el tipo de datetime de la base de datos
                

        print("No se pudo encontrar el archivo de nombre: %s en la base de datos para comparar la fecha de modificacion" % file['title'])
        conexion1.close()
        return None  # No deberia de retornar acá nunca pero por las dudas

    def enLaBaseEstaElArchivo(self, file, tabla):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database= self.baseDeDatos)
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT file_id FROM " + tabla)
        archivos = cursor1.fetchall()

        for archivo in archivos:
            if(archivo[0] == file['id']):
                conexion1.close()
                return True
        conexion1.close()
        print("el archivo de id: %s no se encontro en la tabla: %s" % (file['id'],tabla))
        return False

    def insertarEnHistorialArchivosPublicos(self, file):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database= self.baseDeDatos)
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT file_id FROM historialarchivospublicos")
        archivos = cursor1.fetchall()

        for archivo in archivos:
            if(archivo[0] == file['id']):
                print("El archivo de nombre %s ya esta en la tabla HistorialArchivosPublicos" % file['title'])
                return # chequear

        query ="insert into HistorialArchivosPublicos(file_id, nombre, fecha_modificacion) values (%s,%s,%s)"
        datos = (file['id'], file['title'], file['modifiedDate'])        
        cursor1.execute(query, datos)

        conexion1.commit()
        conexion1.close()
        
        print("Se ha agregado al historial de archivos publicos el archivo de id: %s y nombre: %s" % (file['id'], file['title']))
            
    def eliminarArchivoDeLaBase(self, file, tabla):
        try:
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="", database= self.baseDeDatos)
            cursor1 = conexion1.cursor()
            cursor1.execute("DELETE FROM %s WHERE file_id='%s'" % (tabla, file['id']))
            conexion1.commit()
            conexion1.close()
            print("Se ha eliminado de la tabla: %s el archivo: %s con id: %s" % (tabla, file['title'], file['id']))
        except:
            print("No se ha podido eliminar de la base el archivo: %s con id: %s" % (file['title'], file['id']))    