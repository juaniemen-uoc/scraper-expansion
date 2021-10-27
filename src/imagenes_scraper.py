from bs4 import BeautifulSoup
import requests
import shutil
import os.path
 
class ImagenesScraper():

    def __init__(self, include_lst):
        self._index_url="https://datosmacro.expansion.com"
        self._resource_url="/paises"
        self._include_list = include_lst


    @property
    def index_url(self):
        return self._index_url

    @property
    def resource_url(self):
        return self._resource_url

    @property
    def output_path(self):
        return "../output/flag_pictures/"

    @property
    def include_list(self):
        return self._include_list

    def get_images(self):
            page = requests.get(self.index_url + self.resource_url, timeout=10) # 10 seconds

            soup = BeautifulSoup(page.content, features="lxml")

            parent_div = soup.find(class_='flags')

            a_items = parent_div.find_all("a")
            breakpoint()
            for a in a_items:
                file_name = a["href"].split("/")[-1]
                if self.include_list and file_name not in self.include_list:
                    continue
                else:
                    if a.img: 
                        file_path = a.img["src"]
                        filepath_absolute = self.index_url + file_path
                        self.download_and_save(filepath_absolute, file_name)


    def download_and_save(self, url, file_name):
        # Si ya está descargada, no la bajamos de nuevo
        output = self.output_path + file_name + ".png"
        if os.path.isfile(output):
            print('Image was already downloaded: ',file_name)
            return

        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open(output,'wb') as f:
                shutil.copyfileobj(res.raw, f) 
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')

