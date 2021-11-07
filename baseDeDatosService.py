from manejoArchivos import *
from usuarioService import *
import mysql.connector

from datetime import *     

class BaseDeDatosService:

    def __init__(self, nombreBase, nombreTabla): # tener en el config, recibir host, user y pass de la db
        #self.conexionSQL = mysql.connector.connect(host="localhost", user="root", passwd="", database= "archivos")
        self.nombreBase = nombreBase
        self.nombreTabla = nombreTabla

    def armarEntorno(self):
        if(not self.existeLaBase()):
            self.crearBaseDeDatos()
        if(not self.existeLaTabla()):
            self.crearTablaArchivosDrive()


    def existeLaBase(self):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="") 
        cursor1 = conexion1.cursor()
        cursor1.execute("show databases")
        #De aca para abajo esta todo mal
        for base in cursor1:
            if (base[0] == self.nombreBase):
                conexion1.close()
                return True
        conexion1.close()
        return False


    def existeLaTabla(self):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("show tables")
        #De aca para abajo esta todo mal
        for table in cursor1:
            if (table[0] == self.nombreTabla):
                conexion1.close()
                return True
        conexion1.close()
        return False


    def crearBaseDeDatos(self):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")
        cursor1 = conexion1.cursor()
        cursor1.execute("CREATE DATABASE %s" % self.nombreBase)
        conexion1.close()
        

    def crearTablaArchivosDrive(self):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("CREATE TABLE %s (id INT AUTO_INCREMENT PRIMARY KEY, file_id VARCHAR(255), nombre VARCHAR(255), ext VARCHAR(255), owner VARCHAR(255), visibilidad VARCHAR(255), fecha_modificacion DATETIME)" % self.nombreTabla)
        conexion1.close()
        

    def conexionSQL(self):
        return mysql.connector.connect(host="localhost", user="root", passwd="", database= self.nombreBase)

    
    def guardarSiNoExiste(self, file):
        if(not self.existeArchivoEnTabla(file) or self.seModifico(file)):
            self.guardarArchivo(file)
    

    def existeArchivoEnTabla(self, file):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT file_id FROM " + self.nombreTabla)
        archivos = cursor1.fetchall()
        #De aca para abajo esta todo mal
        for archivo in archivos:
            if(archivo[0] == file['id']):
                conexion1.close()
                return True
        conexion1.close()
        return False


    def seModifico(self, file):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT fecha_modificacion FROM archivos_drive WHERE file_id = '%s'" % file['id'])
        fechasModificaciones = cursor1.fetchall()
        modificacionReciente = fechasModificaciones[0][0]
        #De aca para abajo esta todo mal
        for fecha in fechasModificaciones:
            if(fecha[0] > modificacionReciente):
                modificacionReciente = fecha[0]
                
        conexion1.close()
        return modificacionReciente < datetime.strptime(file['modifiedDate'][0:19],'%Y-%m-%dT%H:%M:%S') 
        #Formato RFC 3339 '%Y-%m-%dT%H:%M:%S.%fZ'
        #Se le debe colocar el [0:19] dado que el file['modifiedDate'] trae consigo milesimas de segundos (.%f) que no son captados por archivo[1] por el tipo de datetime de la base de datos
        
    
    def guardarArchivo(self, file):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        
        query ="insert into archivos_drive(nombre, ext, owner, visibilidad, fecha_modificacion, file_id) values (%s,%s,%s,%s,%s,%s)"
        datos = (file['title'], file['fileExtension'], ' '.join(file['ownerNames']), self.visibilidadDe(file), file['modifiedDate'], file['id'])        
        cursor1.execute(query, datos)

        conexion1.commit()
        conexion1.close()

    def visibilidadDe(self, file):
        if (file['shared']):
            return 'Publico'
        else:
            return 'Privado'


    def drop(self):
        if(self.existeLaBase()):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")
            cursor1 = conexion1.cursor()
            cursor1.execute("DROP DATABASE %s" % self.nombreBase)
            conexion1.close()


    def getArchivos(self):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT * FROM %s" % self.nombreTabla) 
        registroArchivos = cursor1.fetchall()
        conexion1.close()
        return registroArchivos #TODO: convertir a objetos
