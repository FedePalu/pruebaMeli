from baseDeDatosService import *
from manejoArchivos import *
from usuarioService import *
from unittest.mock import MagicMock, Mock
import json
   
#   Los test se corren ejecutando 'pytest'

class TestHandler():
    def __init__(self):
        with open('config.json', "r") as readFile:
            config = json.load(readFile)
            self.idRutaDrive = config['idRutaDrive']
            self.archivosHandle = ManejoArchivos(self.idRutaDrive)   
            self.mailHandle = UsuarioService(config['mailUsuario'], config['passUsuario'])
            self.baseHandle = BaseDeDatosService(config['rutaDB'], self.mailHandle, self.archivosHandle)
    
handler = TestHandler()

def test_creoBaseYTabla():
    # Creo la base
    handler.baseHandle.crearBaseDeDatos()
    handler.baseHandle.crearTablaArchivosDrive()
    # Verifico que existe
    assert handler.baseHandle.existeLaBase("archivos")
    assert handler.baseHandle.existeLaTabla("archivos_drive")

def test_seSubieronTodosLosArchivosDrive():
    # Cargar todos los archivos del drive
    handler.baseHandle.cargarTodosLosArchivosDelDrive()
    # Por cada archivo fijarme si el registro entero de los campos esta
    assert handler.baseHandle.seCargaronTodosLosArchivosDelDrive()

def test_cargoArchivoConModificaciones():
    pass

def test_cargoArchivoSinModificaciones():
    pass

def test_cargoArchivoPublico():
    # baseHandle(mock, ...)
    #file = crear
    #mockDrive = Mock()
    #mockMailSender = Mock()
    #baseHandle = BaseDeDatosService(config['rutaDB']??, mockMailSender, mockDrive)

    #mockDrive.visibilidadDe = 'Publico'
    pass

#def test_insertoEnTablaArchivosDrive():
#    # Creo el archivo
#    nombre = "testing" + str(random.randrange(1000,5000,66))
#    handler.archivosHandle.crearArchivo(nombre)
#    # Lo encuentro
#    file = handler.archivosHandle.encontrarArchivoPorNombre(nombre)
#    # Lo inserto en la tabla "ArchivosDrive"
#    handler.baseHandle.insertarEnArchivosDrive(file)
#    # Compruebo su existencia en la tabla "ArchivosDrive"
#    assert handler.baseHandle.enLaBaseEstaElArchivo(file, "archivosdrive")
#    # Borro el archivo de Google Drive y de la base de datos
#    handler.archivosHandle.eliminarArchivoDelDrive(file)
#    #handler.baseHandle.eliminarArchivoDeLaBase(file,"archivosdrive")
    
#def test_insertoEnTablaHistorialPublico():
#    # Creo el archivo
#    nombre = "testing" + str(random.randrange(1000,5000,66))
#    file = handler.archivosHandle.crearArchivo(nombre)
#    # Lo encuentro
#    file = handler.archivosHandle.encontrarArchivoPorNombre(nombre)
#    # Lo inserto en la tabla "HistorialArchivosPublicos"
#    handler.baseHandle.insertarEnHistorialArchivosPublicos(file)
#    # Compruebo su existencia en la tabla "HistorialArchivosPublico"
#    assert handler.baseHandle.enLaBaseEstaElArchivo(file, "HistorialArchivosPublicos")
#    # Borro el archivo de Google Drive y de la base de datos
#    handler.archivosHandle.eliminarArchivoDelDrive(file)
#    #handler.baseHandle.eliminarArchivoDeLaBase(file,"HistorialArchivosPublicos")

#def test_insertoArchivoPublicoEnArchivosDriveYComprueboHistorial():
#    # Creo archivo publico
#    nombre = "testing" + str(random.randrange(1000,5000,66))
#    handler.archivosHandle.crearArchivoPublico(nombre)
#    # Encuentro el file
#    file = handler.archivosHandle.encontrarArchivoPorNombre(nombre)
#    # Lo inserto en la tabla "ArchivosDrive"
#    handler.baseHandle.insertarEnArchivosDrive(file)
#    # Compruebo su existencia en la tabla "HistorialPublico"
#    assert handler.baseHandle.enLaBaseEstaElArchivo(file, "HistorialArchivosPublicos")
#    # Borro el archivo de Google Drive y de la base de datos
#    handler.archivosHandle.eliminarArchivoDelDrive(file)
#    handler.baseHandle.eliminarArchivoDeLaBase(file,"archivosdrive")
#    #handler.baseHandle.eliminarArchivoDeLaBase(file,"HistorialArchivosPublicos")


