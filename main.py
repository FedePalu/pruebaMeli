from manejoArchivos import *
from baseDeDatosService import *
from usuarioService import *
import json



with open('config.json', "r") as readFile:
    config = json.load(readFile)
    idRutaDrive = config['idRutaDrive']
    archivosHandle = ManejoArchivos(idRutaDrive)   
    mailHandle = UsuarioService(config['mailUsuario'], config['passUsuario'])
    baseHandle = BaseDeDatosService(config['rutaDB'], mailHandle, archivosHandle)





# PASOS:
# 1. CREAR TABLA

#baseHandle.crearTabla()

# 2. SUBIR TODOS LOS ARCHIVOS DRIVE

baseHandle.cargarTodosLosArchivosDelDrive()


#baseHandle.subirTodosLosArchivosDelDrive()


#Ruta de mi carpeta "Prueba MELI"
##idRutaDrive = '1J1YYeIfMgXIU-i9gC7kpSO3bouZ7MBgz'
#Base de datos propia
##base = "archivos"

#Mail.enviarCorreoCambiandoAPrivado("fedepalu87@gmail.com")


##archivos = ManejoArchivos(idRutaDrive)
#archivos.crearArchivo("1J1YYeIfMgXIU-i9gC7kpSO3bouZ7MBgz", "prueba.txt")
#archivos.cambiarVisibilidadAPrivada("1me9FiM9F3dblItPcmoLK0KRS9gdPZwvi")
#archivos.eliminarArchivoPorId("1-UmhaCGS16Gvn_XOkE76GyOunTZoa9Rb")
#archivos.verArchivosDrive()
#file = archivos.encontrarArchivoPorNombre("prueba.txt")
##DBS = BaseDeDatosService(base, Mail, archivos)
#DBS.insertarEnArchivosDrive(file)
#DBS.insertarEnHistorialArchivosPublicos(file)
#DBS.insertarEnArchivosDrive("kkkk","pepito",".jph","palu",True,"ayer")
#DBS.subirTodosLosArchivosDelDrive()

#DBS.eliminarArchivoDeLaBase(file,"archivosdrive")
#BaseDeDatosService.mostrarBaseDeDatos()
#BaseDeDatosService.insertarEnArchivosDrive("kkkk","pepito",".jph","palu","Publico","ayer")



#datos = {
#    'idRutaDrive' : '1J1YYeIfMgXIU-i9gC7kpSO3bouZ7MBgz',
#    'mailUsuario' : 'fedepalu87@gmail,com',
#    'passUsuario' : 'rdismuvhwhjhhcjd',
#    'rutaDB' : 'archivos'
#}
#
#with open('config.json', 'w') as file:
#    json.dump(datos, file)