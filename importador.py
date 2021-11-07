from manejoArchivos import *
from baseDeDatosService import *
from usuarioService import *

class Importador:
    
    def __init__(self, driveService, baseService, mailService):
        self.driveService = driveService
        self.baseService = baseService
        self.mailService = mailService

    def run(self):
        self.baseService.armarEntorno()
        files = self.driveService.fileList()
        for file in files:
            self.baseService.guardarSiNoExiste(file)
            self.validarVisibilidad(file)

    def validarVisibilidad(self, file):
        if (file['shared']):
            self.driveService.cambiarVisibilidadAPrivada(file)
            self.mailService.enviarCorreoCambioDeVisibilidad(file)
            self.baseService.guardarArchivo(file)