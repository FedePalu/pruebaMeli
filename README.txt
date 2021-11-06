Prerrequisitos para el buen funcionamiento del test:
   1. Instalar MySQL y algún programa para administrar las bases de datos como por ejemplo PHPMyAdmin (junto con PHP y Apache)
   2. Haber instalado todas las dependencias 'requirements.txt' ejecutando 'pip install -r requirements.txt'  
   3. Tener el client-secret.json en la misma ruta que los '.py':
        https://medium.com/@chingjunetao/simple-way-to-access-to-google-service-api-a22f4251bb52
   4. Haber generado un archivo 'config.json' con los siguientes datos:
       a. 'idRutaDrive': id de la carpeta de Google Drive donde estarán los archivos a analizar. 'root' para directorio principal. 
          El id se puede conseguir parándote en la carpeta de Drive y ver la URL: www.../folders/[id]
       b. 'mailUsuario': mail que se utilizará para el envío de notificaciones. Por ejemplo 'example@gmail.com'.
       c. 'passUsuario': contraseña de la credencial del mail para su utilización a través de algún servicio.
       #d. 'rutaDB': ruta de la base de datos MySQL.

     Los test se corren ejecutando 'pytest'

La documentación para el realizado de este proyecto es la siguiente:

# API drive:
- https://towardsdatascience.com/how-to-manage-files-in-google-drive-with-python-d26471d91ecd
- https://developers.google.com/drive/api/v2/reference/files
- https://pythonhosted.org/PyDrive/filemanagement.html
- https://medium.com/@chingjunetao/simple-way-to-access-to-google-service-api-a22f4251bb52

# Envio de mails:
- https://uniwebsidad.com/libros/python/capitulo-14/envio-de-e-mail-desde-python
- https://techexpert.tips/es/python-es/python-enviar-correo-electronico-usando-gmail/

# Manejo de base de datos:
- https://www.tutorialesprogramacionya.com/pythonya/detalleconcepto.php?punto=81&codigo=81&inicio=75
- https://docs.hektorprofe.net/python/bases-de-datos-sqlite/consultas-sql-basicas/

# Testing:
- https://realpython.com/pytest-python-testing/
- https://docs.python.org/3/library/unittest.mock.html
- https://www.oulub.com/es-ES/Python/library.unittest.mock-examples

# Utilización de ambiente local (venv):
- https://programwithus.com/learn/python/pip-virtualenv-windows
- https://pypi.org/project/python-dotenv/

# Manejo archivos json:
- https://www.analyticslane.com/2018/07/16/archivos-json-con-python/

Para mi
- https://console.cloud.google.com/apis/credentials/consent?project=prueba-meli-330200&supportedpurview=project


