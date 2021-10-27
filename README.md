# Título del proyecto:
Evolución del Precio de los Derivados del Petróleo en Europa.

# Integrantes:
Juan Francisco Nieto Mendoza
Marta Gómez Galán

# Descripción del proyecto y de los ficheros.

En este repositorio se encuentran los ficheros necesarios para la creación de un dataset con los precios de los derivados del petróleo de los paises miembros de la Unión Europea y Reino Unido desde enero 2005 a la actualidad. En dicho dataset se incluyen los precios (en euros), con y sin impuestos, de los hidrocarburos Super 95, Diesel y Diesel Calefacción. 

Los datos se han recopilado del Sitio Web https://datosmacro.expansion.com/ mediante la técnica web scrapping utilizando las librerias Requests y BeautifulSoap de Python.

Entre los ficheros se incluyen las carpetas con el código (src) así como los archivos de salida (output). Se incluye además una carperta (describe) con diversa información del sitio web utilizado, incluido el archivo robots.txt con los permisos. 

Dentro de la carperta src se encuentran el archivo general_scrapper.py con el código, escrito en python, necesario para la extración de los datos y la creación del dataset definitivo. Se incluye además el archivo imagenes_scarpper.py con el código necesario para la extracción de las imágenes de las banderas de los países incluidos en el dataset. Se incluye un tercer archivo main.py con el código necesario para la ejecución de ambos scrappers. 

# Para la ejecución del script se requieren las siguientes librerias:
Incluir
# La ejecución del script se tiene que llevar a cabo de la siguiente manera:
Incluir
