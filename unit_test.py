from baseDeDatosService import *
from importador import Importador
from manejoArchivos import *
from usuarioService import *
from unittest.mock import MagicMock, Mock
import pytest

import json
   
#   Los test se corren ejecutando 'pytest'

class TestHandler:
    def __init__(self):
        self.driveService = Mock()
        self.driveService.fileList.return_value = []
        self.mailService = Mock()
        self.baseService = BaseDeDatosService("archivos_test", "archivos_drive")
        self.importador = Importador(self.driveService, self.baseService, self.mailService)
            
handler = TestHandler()
archivoPublico = { "id": '1', "title": 'filePrivado.txt', "shared": True, "fileExtension": 'txt', "ownerNames": ["Federico"], "modifiedDate": datetime.now() }
        

@pytest.fixture(autouse=True)
def run_around_tests():
    handler = TestHandler() # ver esto  
    handler.baseService.drop()
    yield
    handler.baseService.drop()

def test_seCreaEntorno():
    assert not handler.baseService.existeLaBase()
    handler.importador.run()
    assert handler.baseService.existeLaBase()
    assert handler.baseService.existeLaTabla()

def test_seGuardanArchivosPrivados():
    handler.driveService.fileList.return_value = [
        {"id": '1', "title": 'filePrivado.txt', "shared": False, "fileExtension": 'txt', "ownerNames": ["Federico"], "modifiedDate": datetime.now() },
        {"id": '2', "title": 'filePublico.txt', "shared": False, "fileExtension": 'txt', "ownerNames": ["Federico"], "modifiedDate": datetime.now() }
    ]
    handler.importador.run()
    archivos = handler.baseService.getArchivos() 
    # TODO: hacer un assert mas copado
    assert len(archivos) == 2 


def test_seDuplicanRegistrosArchivosPublicos():
    handler.driveService.fileList.return_value = [archivoPublico]
    handler.importador.run()
    archivos = handler.baseService.getArchivos() 
    # TODO: hacer un assert mas copado
    assert len(archivos) == 2

def test_envioMailPorCambioVisibilidad():
    handler.driveService.fileList.return_value = [archivoPublico]
    handler.importador.run()

    handler.mailService.enviarCorreoCambioDeVisibilidad.assert_called_once_with()

def test_cargoArchivoConModificaciones():
    pass

def test_cargoArchivoSinModificaciones():
    pass
