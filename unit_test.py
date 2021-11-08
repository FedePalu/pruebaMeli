from baseDeDatosService import *
from importador import Importador
from manejoArchivos import *
from usuarioService import *
from unittest.mock import Mock
import pytest
   
#   Los test se corren ejecutando 'pytest'

class TestHandler:
    def __init__(self):
        self.driveService = Mock()
        self.driveService.fileList.return_value = []
        self.mailService = Mock()
        self.baseService = BaseDeDatosService("archivos_test", "archivos_drive", "localhost", "root", "")
        self.importador = Importador(self.driveService, self.baseService, self.mailService)
            
handler = TestHandler()
archivoPublico = { "id": '1', "title": 'filePrivado.txt', "shared": True, "fileExtension": 'txt', "ownerNames": ["Federico"], "modifiedDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S') }
archivoPrivado = {"id": '1', "title": 'filePrivado.txt', "shared": False, "fileExtension": 'txt', "ownerNames": ["Federico"], "modifiedDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S') }
otroArchivoPrivado = {"id": '2', "title": 'filePublico.txt', "shared": False, "fileExtension": 'txt', "ownerNames": ["Federico"], "modifiedDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S') }
    

@pytest.fixture(autouse=True)
def run_around_tests():
    handler.driveService = Mock()
    handler.driveService.fileList.return_value = []
    handler.mailService = Mock()
    handler.importador = Importador(handler.driveService, handler.baseService, handler.mailService)
    handler.baseService.drop()
    yield
    handler.baseService.drop()

def test_seCreaEntorno():
    assert not handler.baseService.existeLaBase()
    handler.importador.run()
    assert handler.baseService.existeLaBase()
    assert handler.baseService.existeLaTabla()

def test_seGuardanArchivosPrivados():
    handler.driveService.fileList.return_value = [archivoPrivado, otroArchivoPrivado]
    handler.importador.run()
    archivos = handler.baseService.getArchivos() 
    assert len(archivos) == 2

def test_archivosPublicos():
    handler.driveService.fileList.return_value = [archivoPublico]
    handler.importador.run()

    handler.mailService.enviarCorreoCambioDeVisibilidad.assert_called_once_with(archivoPublico)
    handler.driveService.cambiarVisibilidadAPrivada.assert_called_once_with(archivoPublico)

def test_seDuplicanRegistrosArchivosPublicos():
    handler.driveService.fileList.return_value = [archivoPublico]
    handler.importador.run()
    archivos = handler.baseService.getArchivos() 
    assert len(archivos) == 2

def test_cargoArchivoConModificaciones():
    handler.driveService.fileList.return_value = [archivoPrivado]
    handler.importador.run()
    archivoPrivado['modifiedDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    handler.importador.run()
    archivos = handler.baseService.getArchivos() 
    assert len(archivos) == 2


def test_cargoArchivoSinModificaciones():
    handler.driveService.fileList.return_value = [archivoPrivado]
    handler.importador.run()
    handler.importador.run()
    archivos = handler.baseService.getArchivos() 
    assert len(archivos) == 1
