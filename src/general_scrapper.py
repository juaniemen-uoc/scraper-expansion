
from bs4 import BeautifulSoup
import numpy as np
import requests
import sys
import time
 
class GeneralScrapper():

    def __init__(self, index_url="", resource_url=""):
        self._index_url = index_url
        self._resource_url = resource_url
        self._data_from_source = ""
        self._tidy_data = []
        self._header_origin = []
        self._header_data = []
        self._visited_urls = []


    # Getters / Setters
    
    def index_url(self):
        return self._index_url
    
    def resource_url(self):
        return self._resource_url

    def data_from_source(self):
        return self._data_from_source

    def tidy_data(self):
        return self._tidy_data
    
    def visited_urls(self):
        return self._visited_urls
    
    def tidy_data(self):
        return self._tidy_data

    def header_origin(self):
        return self._header_origin

    def header_data(self):
        return self._header_data

    def set_data_from_source(self, data_from_source):
        self._data_from_source = data_from_source

    def set_tidy_data(self, tidy_data):
        self._tidy_data = tidy_data

    def set_header_origin(self, header):
        self._header_origin = header

    def set_header_data(self, header):
        self._header_data = header

    def add_visited_url(self, url):
        self._visited_urls.append(url)
        
    def clear_visited_urls(self):
        self._visited_urls = []

    # END Getters / Setters

    def get_data_raw(self):
        self.clear_visited_urls()
        self.set_data_from_source(   self.get_data_aux( [ self.index_url() + self.resource_url()], []) )

    def get_data_aux(self, missing, acum):
        missing = missing

        # Caso base: no quedan urls pendientes de explorar (VISITED_URLS está vacio)
        if len(self.visited_urls()) != 0 and len(missing) == 0:
            return acum
        else:
            current_url = missing.pop(0)

        # Caso recursivo: SKIP - la url que hemos obtenido de PENDIENTES ya ha sido explorada (VISITED_URLS)
        if current_url in self.visited_urls():
            return self.get_data_aux(missing, acum)
        else:
            self.add_visited_url(current_url)

        try:
            page = requests.get(current_url, timeout=10) # 10 seconds

            soup = BeautifulSoup(page.content, features="lxml")
            
            
            table_sch = soup.find(class_='table-responsive').table
            table = table_sch.tbody
            headers = table_sch.thead

            # Si las cabeceras están vacías rellenemoslas, si no, comprobemos que las cabeceras del paso actual, sean iguales a las anteriores
            # por el contrario, SKIP (no queremos tantas magnitudes diferentes en nuestros datos)
            possible_header = [td.string for td in headers.tr.find_all('th')]

            # Fill header, si no contienen datos rellenemoslo
            if not self.header_origin():
                self.set_header_origin([td.string for td in headers.tr.find_all('th')])
            elif not self.header_data():
                if self.header_origin() != possible_header:
                    self.set_header_data([td.string for td in headers.tr.find_all('th')])
            elif possible_header != self.header_origin() and possible_header != self.header_data():
                return self.get_data_aux(missing, acum)



            rows = []
            for trs in table.find_all("tr"): 
                if trs.td.a and trs.td.a["href"]:
                    ## Sometimes trs.td.a href is containing absolute path, sometimes relative so it's managed with "replace"
                    missing.append(self.index_url() + trs.td.a["href"].replace(self.index_url(), ""))

                rows.append(self.tokenizing(current_url, missing) + [td.string for td in trs.find_all("td") if td.string])
            
            footer = soup.find(class_= "tablefooter")
            if footer and footer.td and footer.td.span and footer.td.span.a:
                missing.append(footer.td.span.a["href"])

            acum = rows + acum
            if len(missing)==0:
                return acum
            else:
                return self.get_data_aux(missing, acum)

        except Exception as e:
            return self.get_data_aux(missing, acum)
        

    def tokenizing(self,current_url, missing):
        if current_url == (self.index_url() + self.resource_url()):
            return ["ORIGEN_" + missing[-1].split('/')[-1].split("?")[0]]
        else:
            return [ current_url.split('/')[-1].split("?")[0]]



    def process_tidy_data(self):
        breakpoint()
        origen_keys = filter(lambda y: y[0].startswith('ORIGEN'), self.data_from_source())
        keys = list(map(lambda x: x[0].replace("ORIGEN_", ""), origen_keys))
        
        result = []
        for k in keys:
            ocurrencias = list(filter(lambda y: y[0].replace('ORIGEN_', '') == k, self.data_from_source()))
            if len(ocurrencias) == 1:
                first_dat = ocurrencias[0]
                first_dat[1] = first_dat[1].replace(" [+]", "")

                if len(first_dat[1:]) != len(self.final_header_ary()):
                        continue
                else:
                    result.append(first_dat[1:])
                
            else:
                first_dat = list(filter(lambda y: y[0] == ('ORIGEN_'+k), self.data_from_source()))
                index_descr = first_dat[0][1].replace(" [+]", "")
                for row in ocurrencias:
                    if row[0].startswith("ORIGEN"):
                        continue
                    row[0] = index_descr
                    if len(row) != len(self.final_header_ary()):
                        continue
                    else:
                        result.append(row)

        self.set_tidy_data(result)
    
    def data_to_csv(self, delimiter=";"):
        header = delimiter.join(self.final_header_ary())
        np.savetxt('../' + self.resource_url()[1:].replace("/", "_") + '.csv', self.tidy_data(), delimiter=delimiter, fmt = '%s', header=header)

    def final_header_ary(self):
        if self.header_origin() and self.header_data():
            header_ary = [self.header_origin()[0]] + self.header_data()
        else:
            header_ary = self.header_origin()
        return header_ary
