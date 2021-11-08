from manejoArchivos import *
from usuarioService import *
import mysql.connector

from datetime import *     

class BaseDeDatosService:

    def __init__(self, nombreBase, nombreTabla, host, user, password):
        self.nombreBase = nombreBase
        self.nombreTabla = nombreTabla
        self.host = host
        self.user = user
        self.password = password

    def armarEntorno(self):
        if(not self.existeLaBase()):
            self.crearBaseDeDatos()
        if(not self.existeLaTabla()):
            self.crearTablaArchivosDrive()


    def existeLaBase(self):
        conexion1 = mysql.connector.connect(host= self.host, user=self.user, passwd=self.password) 
        query = "show databases"
        result = self.ejecutarQueryExist(query, self.nombreBase, conexion1)
        conexion1.close()
        return result


    def existeLaTabla(self):
        conexion1 = self.conexionSQL()
        query = "show tables"
        result = self.ejecutarQueryExist(query,self.nombreTabla,conexion1)
        conexion1.close()
        return result


    def crearBaseDeDatos(self):
        conexion1 = mysql.connector.connect(host= self.host, user=self.user, passwd=self.password)
        cursor1 = conexion1.cursor()
        cursor1.execute("CREATE DATABASE %s" % self.nombreBase)
        conexion1.close()
        

    def crearTablaArchivosDrive(self):
        query = "CREATE TABLE %s (id INT AUTO_INCREMENT PRIMARY KEY, file_id VARCHAR(255), nombre VARCHAR(255), ext VARCHAR(255), owner VARCHAR(255), visibilidad VARCHAR(255), fecha_modificacion DATETIME)" % self.nombreTabla
        self.ejecutarQuery(query)
        

    def conexionSQL(self):
        return mysql.connector.connect(host= self.host, user=self.user, passwd=self.password, database= self.nombreBase)

    
    def guardarSiNoExiste(self, file):
        if(not self.existeArchivoEnTabla(file) or self.seModifico(file)):
            self.guardarArchivo(file)
    

    def existeArchivoEnTabla(self, file):
        query = "SELECT file_id FROM " + self.nombreTabla
        archivos = self.ejecutarQueryFetchAll(query)
        for archivo in archivos:
            if(archivo[0] == file['id']):
                return True
        return False


    def seModifico(self, file):
        query = "SELECT fecha_modificacion FROM archivos_drive WHERE file_id = '%s'" % file['id']
        fechasModificaciones = self.ejecutarQueryFetchAll(query)
        modificacionReciente = fechasModificaciones[0][0]
        for fecha in fechasModificaciones:
            if(fecha[0] > modificacionReciente):
                modificacionReciente = fecha[0]
                
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
            conexion1 = mysql.connector.connect(host= self.host, user=self.user, passwd=self.password)
            cursor1 = conexion1.cursor()
            cursor1.execute("DROP DATABASE %s" % self.nombreBase)
            conexion1.close()


    def getArchivos(self):
        return self.ejecutarQueryFetchAll("SELECT * FROM %s" % self.nombreTabla) 

    def ejecutarQueryFetchAll(self, query):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute(query) 
        result = cursor1.fetchall()
        conexion1.close()
        return result
    
    def ejecutarQuery(self, query):
        conexion1 = self.conexionSQL()
        cursor1 = conexion1.cursor()
        cursor1.execute(query) 
        conexion1.close()

    def ejecutarQueryExist(self, query, value, conexion):
        cursor1 = conexion.cursor()
        cursor1.execute(query)
        for registro in cursor1:
            if (registro[0] == value):
                return True
        return False