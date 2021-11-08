from importador import *
import json


with open('config.json', "r") as readFile:
    config = json.load(readFile)
    idRutaDrive = config['idRutaDrive']
    driveService = ManejoArchivos(idRutaDrive)   
    mailService = UsuarioService(config['mailUsuario'], config['passUsuario'])
    baseService = BaseDeDatosService(config['baseName'], config['tableName'], config['hostDB'], config['userDB'], config['passDB'])
    importador = Importador(driveService, baseService, mailService)

importador.run()
print("Se cargaron todos los archivos")

