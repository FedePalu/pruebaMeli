# Prerrequisitos:
   1. [python](https://www.python.org/downloads/) 3.10 o superior 
   2. Motor de base de datos MySQL
   3. Instalar todas las dependencias 'requirements.txt' ejecutando `pip install -r requirements.txt`  
   4. Seguir los pasos para descargar el .json de acceso a la utilización de su drive, cambiarle el nombre a 'client_secrets.json' y colocarlo en la misma dirección que los '.py':
        https://medium.com/@chingjunetao/simple-way-to-access-to-google-service-api-a22f4251bb52
   5. Haber generado un archivo 'config.json' con los siguientes datos:
      
      - `idRutaDrive`: id de la carpeta de Google Drive donde estarán los archivos a analizar. "root" para directorio principal. 
          El id se puede conseguir parándote en la carpeta de Drive y ver la URL: www.../folders/[id]
      
      - `baseName`: nombre de la base de datos.

      - `tableName`: nombre de la tabla.

      - `mailUsuario`: mail que se utilizará para el envío de notificaciones. Por ejemplo "example@gmail.com".
      
      - `passUsuario`: contraseña de la credencial del mail para su utilización a través de algún servicio. En caso de gmail: https://techexpert.tips/es/python-es/python-enviar-correo-electronico-usando-gmail/ 
       
      - `hostDB`: host de la base de datos, por default "localhost" 
      
      - `userDB`: user de la base de datos, por default "root"
      
      - `passDB`: contraseña de la base de datos, por default ""

# Funciones:
   1. El programa se corre ejecutando `python main.py` 
   
   2. Los test se corren ejecutando `pytest`


# Documentación

La documentación para el realizado de este proyecto es la siguiente:

## API drive:
- https://towardsdatascience.com/how-to-manage-files-in-google-drive-with-python-d26471d91ecd
- https://developers.google.com/drive/api/v2/reference/files
- https://pythonhosted.org/PyDrive/filemanagement.html
- https://medium.com/@chingjunetao/simple-way-to-access-to-google-service-api-a22f4251bb52

## Envio de mails:
- https://uniwebsidad.com/libros/python/capitulo-14/envio-de-e-mail-desde-python
- https://techexpert.tips/es/python-es/python-enviar-correo-electronico-usando-gmail/

## Manejo de base de datos:
- https://www.tutorialesprogramacionya.com/pythonya/detalleconcepto.php?punto=81&codigo=81&inicio=75
- https://docs.hektorprofe.net/python/bases-de-datos-sqlite/consultas-sql-basicas/

## Testing:
- https://realpython.com/pytest-python-testing/
- https://docs.python.org/3/library/unittest.mock.html
- https://www.oulub.com/es-ES/Python/library.unittest.mock-examples

## Manejo archivos json:
- https://www.analyticslane.com/2018/07/16/archivos-json-con-python/



