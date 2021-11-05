#from socketserver import BaseServer
from manejoArchivos import *
from baseDeDatosService import *
from usuarioService import *
import json



with open('config.json', "r") as readFile: # poner en un metodo?
    config = json.load(readFile)
    idRutaDrive = config['idRutaDrive']
    archivosHandle = ManejoArchivos(idRutaDrive)   
    mailHandle = UsuarioService(config['mailUsuario'], config['passUsuario'])
    baseHandle = BaseDeDatosService(config['rutaDB'], mailHandle, archivosHandle)


# PASOS:
# 1. CREAR BASE
# baseHandle.crearBaseDeDatos()

# 2. CREAR TABLA
# baseHandle.crearTablaArchivosDrive()

# 3. SUBIR TODOS LOS ARCHIVOS DRIVE
# baseHandle.cargarTodosLosArchivosDelDrive()



#datos = {
#    'idRutaDrive' : '1J1YYeIfMgXIU-i9gC7kpSO3bouZ7MBgz',
#    'mailUsuario' : 'fedepalu87@gmail,com',
#    'passUsuario' : 'rdismuvhwhjhhcjd',
#    'rutaDB' : 'archivos'
#}
#
#with open('config.json', 'w') as file:
#    json.dump(datos, file)