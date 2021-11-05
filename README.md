# Título descriptivo del proyecto:
Evolución de los precios de los hidrocarburos en Europa y Reino Unido desde Enero 2005 hasta la actualidad.

# Integrantes:
  * Juan Francisco Nieto Mendoza
  * Marta Gómez Galán

# Descripción del proyecto y de los ficheros.

En este repositorio se encuentran los ficheros necesarios para la creación de un dataset con los precios de los derivados del petróleo de los paises miembros de la Unión Europea y Reino Unido desde enero 2005 a la actualidad. En dicho dataset se incluyen los precios (en euros), con y sin impuestos, de los hidrocarburos Super 95, Diesel y Diesel Calefacción. 

Los datos se han recopilado del Sitio Web https://datosmacro.expansion.com/ mediante la técnica web scrapping utilizando las librerias Requests y BeautifulSoap de Python.

Entre los ficheros se incluyen las carpetas con el código (src) así como los archivos de salida (output). Se incluye además una carperta (describe) con diversa información del sitio web utilizado, incluido el archivo robots.txt con los permisos. 

Dentro de la carperta src se encuentran el archivo general_scrapper.py con el código, escrito en python, necesario para la extración de los datos y la creación del dataset definitivo. Se incluye además el archivo imagenes_scarpper.py con el código necesario para la extracción de las imágenes de las banderas de los países incluidos en el dataset. Para evitar tener que realizar todas las peticiones (514 en total) durante la fase de optimización del código, se incluye el archivo requests_cache.sqlite, que almacena estas peticiones cuyo tiempo de vida son de un día en nuestro script. Finalmente, se incluye el archivo main.py con el código necesario para la ejecución de ambos scrappers. 

# Para la ejecución del script se requieren las siguientes librerias:

  * Requests. Con esta libreria hacemos peticiones al sitio web. 

  * BeautifulSoup. Con esta librería parseamos el html obtenido y navegamos a través del DOM para obtener la información deseada, y obtener nuevos links para iterar el proceso. 

  * Shutil. Esta librería nos permite almacenar las imágenes obtenidas por requests. 

  * Os. Mas concreto Os.path es utilizada para preguntar a nuestro sistema operativo si existe un fichero o directorio. En el caso de imagenes_scraper no descargamos una nueva imagen si ya existe, pues las imágenes de las banderas no son variables (a no ser que alguna cambie, cosa que pasa una vez cada X años), pues son muchas peticiones y queremos evitar un posible baneo por parte del sitio web.
  
  * requests-cache. Utilizada para reducir el número de peticiones al sitio web ahorrando las peticiones que se producen en el mismo día (por defecto). Se crea un fichero sqlite que almacena estas peticiones cuyo tiempo de vida son de un día en nuestro script. Asumimos que no se van a hacer más cambios en un periodo menor a un día.
 
  * random y time. Se incluyen para incorporar un tiempo de espera aleatorio entre las distintas peticiones y evitar una saturación del servidor y un posible bloqueo.


# La ejecución del script se tiene que llevar a cabo de la siguiente manera:

 Es necesario tener instalada una versión de Python3. Para la ejecución completa del proceso abriremos un terminal y nos colocaremos sobre la el directorio scrapper-expansion/src. 
 
 Como tenemos instalada un libreria que no está en el core de python debemos instalarla en el terminal con pip:

```pip install requests-cache```

Una vez allí, ejecutaremos el comando 

```python main.py```

Y tras la ejecución podremos ver que el fichero csv se encuentra en el directorio output/csv y las imágenes se encuentran en output/flag_pictures
