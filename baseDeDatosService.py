from mysql.connector import fabric
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
    def cargarTodosLosArchivosDelDrive(self):
        for file in self.archivoService.fileList():
            self.insertarEnArchivosDrive(file)

    def seCargoElArchivo(self, file):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        query = "SELECT file_id FROM archivos_drive WHERE file_id = %s, nombre = %s, ext %s, owner %s, visibilidad %s, fecha_modificacion = %s"
        datos = (file['id'], file['title'], file['fileExtension'], ' '.join(file['ownerNames']), self.archivoService.visibilidadDe(file), file['modifiedDate'])        
        cursor1.execute(query,datos)
        registro = cursor1.fetchone()
        if registro is not None:
            return True
        return False

    def seCargaronTodosLosArchivosDelDrive(self):
        files = self.archivoService.fileList()
        for file in files:
            if (not self.seCargoElArchivo(file)):
                return False
        return True

    def conexionSQL(self):
        return mysql.connector.connect(host="localhost", user="root", passwd="", database= self.baseDeDatos)

    def crearTabla(self): # pasar nombre por parametro?
        if(self.seCreoLaTabla("archivos_drive")):
            conexion1 = self.conexionSQL()
            cursor1 = conexion1.cursor()
            cursor1.execute("CREATE TABLE archivos_drive (id INT AUTO_INCREMENT PRIMARY KEY, file_id VARCHAR(255), nombre VARCHAR(255), ext VARCHAR(255), owner VARCHAR(255), visibilidad VARCHAR(255), fecha_modificacion DATETIME)")
            conexion1.close()
            print("Se creo la tabla: archivos_drive")
        else:
            print("La tabla archivos_drive ya existe.")

    def seCreoLaTabla(self, nombreTabla):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("show tables")
        for table in cursor1:
            if (table == nombreTabla):
                return True
        return False

    def cargarArchivo(self, file):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        
        query ="insert into archivos_drive(nombre, ext, owner, visibilidad, fecha_modificacion, file_id) values (%s,%s,%s,%s,%s,%s)"
        datos = (file['title'], file['fileExtension'], ' '.join(file['ownerNames']), self.archivoService.visibilidadDe(file), file['modifiedDate'], file['id'])        
        cursor1.execute(query, datos)

        conexion1.commit()
        conexion1.close()

        print("Se ha agregado a la base de datos el archivo de id: %s y nombre: %s" % (file['id'], file['title']))
        
        
    def insertarEnArchivosDrive(self,file):
        if(self.enLaBaseEstaElArchivo(file, "archivos_drive") and (not self.laFechaDeModificacionEsMasNueva(file))):
            print("El archivo de nombre: %s ya esta en la base y no tiene modificacion reciente" % file['title']) 
            return None        
        else:
            self.cargarArchivo(file)

        if (file['shared']):
            self.archivoService.cambiarVisibilidadAPrivada(file)
            self.mailService.enviarCorreoCambioDeVisibilidad(file)
            self.cargarArchivo(file)
           

    def laFechaDeModificacionEsMasNueva(self, file):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT fecha_modificacion FROM archivos_drive WHERE file_id = '%s'" % file['id'])
        fechasModificaciones = cursor1.fetchall()
        modificacionReciente = fechasModificaciones[0][0]
        
        for fecha in fechasModificaciones:
            if(fecha[0] > modificacionReciente):
                modificacionReciente = fecha[0]
                
        conexion1.close()
        return modificacionReciente < datetime.strptime(file['modifiedDate'][0:19],'%Y-%m-%dT%H:%M:%S') 
        #Formato RFC 3339 '%Y-%m-%dT%H:%M:%S.%fZ'
        #Se le debe colocar el [0:19] dado que el file['modifiedDate] trae consigo milesimas de segundos (.%f) que no son captados por archivo[1] por el tipo de datetime de la base de datos
                

        print("No se pudo encontrar el archivo de nombre: %s en la base de datos para comparar la fecha de modificacion" % file['title'])
        conexion1.close()
        return None  # No deberia de retornar acá nunca pero por las dudas

    def enLaBaseEstaElArchivo(self, file, tabla): #TODO: CAMBIAR PROBABLEMENTE
        conexion1 = self.conexionSQL()
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

    #def insertarEnHistorialArchivosPublicos(self, file):
    #    conexion1 = self.conexionSQL()
    #    cursor1 = conexion1.cursor()
    #    cursor1.execute("SELECT file_id FROM historialarchivospublicos")
    #    archivos = cursor1.fetchall()
    #
    #    for archivo in archivos:
    #        if(archivo[0] == file['id']):
    #            print("El archivo de nombre %s ya esta en la tabla HistorialArchivosPublicos" % file['title'])
    #            return # chequear
    #
    #    query ="insert into HistorialArchivosPublicos(file_id, nombre, fecha_modificacion) values (%s,%s,%s)"
    #    datos = (file['id'], file['title'], file['modifiedDate'])        
    #    cursor1.execute(query, datos)
    #
    #    conexion1.commit()
    #    conexion1.close()
    #    
    #    print("Se ha agregado al historial de archivos publicos el archivo de id: %s y nombre: %s" % (file['id'], file['title']))
            
    def eliminarArchivoDeLaBase(self, file): # Cambiar: tengo q traer todos los registros y borrar cada uno?
        try:
            conexion1 = self.conexionSQL()
            cursor1 = conexion1.cursor()
            cursor1.execute("DELETE FROM archivos_drive WHERE file_id='%s'" % file['id'])
            conexion1.commit()
            conexion1.close()
            print("Se ha eliminado de la tabla: archivos_drive el archivo: %s con id: %s" % (file['title'], file['id']))
        except:
            print("No se ha podido eliminar de la base el archivo: %s con id: %s" % (file['title'], file['id']))    