from importador import *
import json


with open('config.json', "r") as readFile: # poner en un metodo?
    config = json.load(readFile)
    idRutaDrive = config['idRutaDrive']
    driveService = ManejoArchivos(idRutaDrive)   
    mailService = UsuarioService(config['mailUsuario'], config['passUsuario'])
    baseService = BaseDeDatosService("archivos", "archivos_drive")
    importador = Importador(driveService, baseService, mailService)

importador.run()
print("Se cargaron todos los archivos")







#datos = {
#    'idRutaDrive' : '1J1YYeIfMgXIU-i9gC7kpSO3bouZ7MBgz',
#    'mailUsuario' : 'fedepalu87@gmail,com',
#    'passUsuario' : 'rdismuvhwhjhhcjd',
#    'rutaDB' : 'archivos'
#}
#
#with open('config.json', 'w') as file:
#    json.dump(datos, file)