
from bs4 import BeautifulSoup
import numpy as np
import requests
# Como se han realizado muchas pruebas, se han realizado muchas peticiones. Para reducir el número y agilizar en sucesivas
# pruebas se usa requests_cache, que almacena las peticiones (por un dia por defecto) en una base de datos sqlite, en caso
# de que esté en tiempo de vida se recupera lo cacheado, por el contrario se hace la petición.
import requests_cache
import random
import time


 
class GeneralScraper():
    

    def __init__(self, index_url="", resource_url="", opts = {}):
        self._index_url = index_url
        self._resource_url = resource_url
        self._data_from_source = []
        self._tidy_data = []
        self._header_origin = []
        self._header_data = []
        self._visited_urls = []

        headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

        if opts["cache_expire_after"] == "no_cache":
            headers.update({'Cache-Control': 'no-cache'})
            self._session = requests.Session()
        elif opts["cache_expire_after"]:
            self._session = requests_cache.CachedSession('requests_cache', expire_after=opts["cache_expire_after"], headers=headers)
        else:
            self._session = requests_cache.CachedSession('requests_cache') # Por defecto expira en 1 día


    # Getters / Setters    

    @property                
    def index_url(self):
        return self._index_url

    @property                
    def resource_url(self):
        return self._resource_url

    @property            
    def data_from_source(self):
        return self._data_from_source

    @property            
    def tidy_data(self):
        return self._tidy_data

    @property                
    def visited_urls(self):
        return self._visited_urls

    @property            
    def header_origin(self):
        return self._header_origin

    @property            
    def header_data(self):
        return self._header_data

    @property            
    def session(self):
        return self._session
    
    @data_from_source.setter            
    def data_from_source(self, data_from_source):
        self._data_from_source = data_from_source
    
    @tidy_data.setter        
    def tidy_data(self, tidy_data):
        self._tidy_data = tidy_data
    
    @header_origin.setter        
    def header_origin(self, header):
        self._header_origin = header
    
    @header_data.setter        
    def header_data(self, header):
        self._header_data = header
        
    # END Getters / Setters

    # Añade una url (string) a la lista de urls visitadas       
    def add_visited_url(self, url):
        self._visited_urls.append(url)

    # Limpia las URL visitadas              
    def clear_visited_urls(self):
        self._visited_urls = []

    def get_data_raw(self):
        self.clear_visited_urls()
        self.data_from_source =  self.get_data_aux( [ self.index_url + self.resource_url], [])

    def get_data_aux(self, pending, acum):
        pending = pending

        # Caso base: no quedan urls pendientes de explorar (VISITED_URLS está vacio)
        if len(self.visited_urls) != 0 and len(pending) == 0:
            return acum
        else:
            current_url = pending.pop(0)

        # Caso recursivo: SKIP - la url que hemos obtenido de PENDIENTES ya ha sido explorada (VISITED_URLS)
        # Pasa algunas veces que la web nos manda a la misma página pudiendose crear un bucle infinito
        if current_url in self.visited_urls:
            return self.get_data_aux(pending, acum)
        else:
            self.add_visited_url(current_url)

        try:
            # Número aleatorio de segundos de 0 a 3. Para que no haya una constante que detecte un posible sistema antihacking
            # Se ha probado con más tiempo y el algoritmo tarda mucho tiempo en terminar.
            # En la sesión de control se habla de tiempos exponenciales, esto aumentaría muchísimo el tiempo de ejecución
            # ya que en para obtener el dataset se visitan 514 enlaces
            tts = (random.random() * 3) # Time to sleep
            time.sleep(tts)

            page = self._session.get(current_url, timeout=10) # 10 seconds
            soup = BeautifulSoup(page.content, features="lxml")
            
            
            table_sch = soup.find(class_='table-responsive').table
            table = table_sch.tbody
            headers = table_sch.thead

            # Si las cabeceras están vacías rellenemoslas, si no, comprobemos que las cabeceras del paso actual, sean iguales a las anteriores
            # por el contrario, SKIP
            # Una vez definidas las cabeceras que tendrá nuestra tabla desechamos los datos con cabeceras distintas (solo mergeamos dos tipos de tablas, no tenemos en cuenta más niveles)
            possible_header = [td.string for td in headers.tr.find_all('th')]

            # Fill header, si no contienen datos rellenemoslo
            if not self.header_origin:
                self.header_origin = [td.string for td in headers.tr.find_all('th')]
            elif not self.header_data:
                if self.header_origin != possible_header:
                    self.header_data = [td.string for td in headers.tr.find_all('th')]
            elif possible_header != self.header_origin and possible_header != self.header_data:
                # Nos hemos encontrado otro tipo de tabla que difiere de las dos anteriores por tanto SKIP (caso recursivo)
                return self.get_data_aux(pending, acum)



            rows = []
            for trs in table.find_all("tr"): 
                if trs.td.a and trs.td.a["href"]:
                    ## Algunas veces trs.td.a href contiene el path absoluto y otras el relativo por lo que eliminamos el dominio con "replace"
                    pending.append(self.index_url + trs.td.a["href"].replace(self.index_url, ""))

                # La siguiente linea almacena cada array de td's con el token.
                # Usamos un token para luego recostruir la tabla ej: "ORIGEN_espana" es padre de todas las "espana"
                # Lo usamos en el método process_tidy_data
                rows.append(self.tokenizing(current_url, pending) + [td.string for td in trs.find_all("td") if td.string])
            
            # Una vez hemos iterado sobre los links de cada tr vemos si hay navegación en el footer y si es así lo añadimo al final de PENDIENTES
            footer = soup.find(class_= "tablefooter")
            if footer and footer.td and footer.td.span and footer.td.span.a:
                pending.append(footer.td.span.a["href"])
            
            # En este momento actualizamos nuestro acum de nuestro algoritmo recursivo
            acum = rows + acum
            # Si nuestro pending tiene longitud 0 entramos en caso base y devolvemos el acumulador
            if len(pending)==0:
                return acum
            else:
                # Si no, Caso recursivo con nuestra lista de pendientes y acumulador actualizados
                return self.get_data_aux(pending, acum)

        except Exception as e:
            # Si ocurre alguna excepción ie: timeout, la página nos devuelve 500, 404 o algo raro pasamos al
            # siguiente caso recursivo nuestro algoritmo convergerá de todas formas puesto perderá urls de 
            # PENDIENTES aunque no sume a ACUM
            return self.get_data_aux(pending, acum)
        

    def tokenizing(self,current_url, pending):
        if current_url == (self.index_url + self.resource_url):
            return ["ORIGEN_" + pending[-1].split('/')[-1].split("?")[0]]
        else:
            return [ current_url.split('/')[-1].split("?")[0]]


    
    def process_tidy_data(self):
        # Obtenemos todos los tipos de tokens que tenemos, los vamos a iterar y a extraer la info
        origen_keys = filter(lambda y: y[0].startswith('ORIGEN'), self.data_from_source)
        keys = list(map(lambda x: x[0].replace("ORIGEN_", ""), origen_keys))
        result = []
        for k in keys:
            ocurrencias = list(filter(lambda y: y[0].replace('ORIGEN_', '') == k, self.data_from_source))
            if len(ocurrencias) == 1:
                # En caso de que solo haya casos de tipo ORIGEN, solo hay un nivel por lo que cogeremos los datos
                # completos de la row, con sus cabeceras (sin el token)
                first_dat = ocurrencias[0]
                first_dat[1] = first_dat[1].replace(" [+]", "")

                if len(first_dat[1:]) != len(self.final_header_ary()):
                        continue
                else:
                    result.append(first_dat[1:])
                
            else:
                # En caso de que haya dos niveles cogemos el primer dato de ORIGEN 
                # y los datos de la segunda tabla para formar la row final
                first_dat = list(filter(lambda y: y[0] == ('ORIGEN_'+k), self.data_from_source))
                index_descr = first_dat[0][1].replace(" [+]", "")
                for row in ocurrencias:
                    if row[0].startswith("ORIGEN"):
                        continue
                    row[0] = index_descr
                    if len(row) != len(self.final_header_ary()):
                        continue
                    else:
                        result.append(row)
        
        # Remove duplication
        dup_free = []
        for i in result:
            if i not in dup_free:
                dup_free.append(i)
        self.tidy_data = dup_free

    def data_to_csv(self, delimiter=";"):
        header = delimiter.join(self.final_header_ary())
        output_path = '../output/csv/' + self.resource_url[1:].replace("/", "_") + '.csv'
        np.savetxt(output_path, self.tidy_data, delimiter=delimiter, fmt = '%s', header=header)

    def final_header_ary(self):
        if self.header_origin and self.header_data:
            header_ary = [self.header_origin[0]] + self.header_data
        else:
            header_ary = self.header_origin
        return header_ary

    def resource_tokens(self):
        # Devuelve el total de tokens contenidos en el csv
        origen_keys = filter(lambda y: y[0].startswith('ORIGEN'), self.data_from_source)
        keys = list(map(lambda x: x[0].replace("ORIGEN_", ""), origen_keys))
        return list(set(keys))

    def scrape(self):
        self.get_data_raw()
        self.process_tidy_data()
        self.data_to_csv()

