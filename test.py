from baseDeDatosService import *
from manejoArchivos import *
from usuarioService import *
import json
import random

#   Prerrequisitos para el buen funcionamiento del test:
#       1. Haber generado un archivo 'config.json' con los siguientes datos:
#           a. 'idRutaDrive': ruta de la carpeta de Google Drive donde estarán los archivos a analizar.
#           b. 'mailUsuario': mail que se utilizará para el envío de notificaciones. Por ejemplo 'example@gmail.com'.
#           c. 'passUsuario': contraseña de la credencial del mail para su utilización a través de algún servicio.
#           d. 'rutaDB': ruta de la base de datos MySQL.
#       2. Haber instalado todas las dependencias setup.py
#       3. Tener el client-secret.json en la misma ruta que los .py
#
#   Los test se pueden correr con 'python -m pytest test.py'
#

class TestHandler():
    def __init__(self):
        with open('config.json', "r") as readFile:
            config = json.load(readFile)
            self.idRutaDrive = config['idRutaDrive']
            self.archivosHandle = ManejoArchivos(self.idRutaDrive)   
            self.mailHandle = UsuarioService(config['mailUsuario'], config['passUsuario'])
            self.baseHandle = BaseDeDatosService(config['rutaDB'], self.mailHandle, self.archivosHandle)
    
handler = TestHandler()

def test_insertoEnTablaArchivosDrive():
    # Creo el archivo
    nombre = "testing" + str(random.randrange(1000,5000,66))
    handler.archivosHandle.crearArchivo(nombre)
    # Lo encuentro
    file = handler.archivosHandle.encontrarArchivoPorNombre(nombre)
    # Lo inserto en la tabla "ArchivosDrive"
    handler.baseHandle.insertarEnArchivosDrive(file)
    # Compruebo su existencia en la tabla "ArchivosDrive"
    assert handler.baseHandle.enLaBaseEstaElArchivo(file, "archivosdrive")
    # Borro el archivo de Google Drive y de la base de datos
    handler.archivosHandle.eliminarArchivoDelDrive(file)
    handler.baseHandle.eliminarArchivoDeLaBase(file,"archivosdrive")
    
def test_insertoEnTablaHistorialPublico():
    # Creo el archivo
    nombre = "testing" + str(random.randrange(1000,5000,66))
    file = handler.archivosHandle.crearArchivo(nombre)
    # Lo encuentro
    file = handler.archivosHandle.encontrarArchivoPorNombre(nombre)
    # Lo inserto en la tabla "HistorialArchivosPublicos"
    handler.baseHandle.insertarEnHistorialArchivosPublicos(file)
    # Compruebo su existencia en la tabla "HistorialArchivosPublico"
    assert handler.baseHandle.enLaBaseEstaElArchivo(file, "HistorialArchivosPublicos")
    # Borro el archivo de Google Drive y de la base de datos
    handler.archivosHandle.eliminarArchivoDelDrive(file)
    handler.baseHandle.eliminarArchivoDeLaBase(file,"HistorialArchivosPublicos")

def test_insertoArchivoPublicoEnArchivosDriveYComprueboHistorial():
    # Creo archivo publico
    nombre = "testing" + str(random.randrange(1000,5000,66))
    handler.archivosHandle.crearArchivoPublico(nombre)
    # Encuentro el file
    file = handler.archivosHandle.encontrarArchivoPorNombre(nombre)
    # Lo inserto en la tabla "ArchivosDrive"
    handler.baseHandle.insertarEnArchivosDrive(file)
    # Compruebo su existencia en la tabla "HistorialPublico"
    assert handler.baseHandle.enLaBaseEstaElArchivo(file, "HistorialArchivosPublicos")
    # Borro el archivo de Google Drive y de la base de datos
    handler.archivosHandle.eliminarArchivoDelDrive(file)
    handler.baseHandle.eliminarArchivoDeLaBase(file,"archivosdrive")
    handler.baseHandle.eliminarArchivoDeLaBase(file,"HistorialArchivosPublicos")

