from general_scraper import GeneralScraper
from imagenes_scraper import ImagenesScraper
from datetime import timedelta, datetime


start = datetime.now()
print("INICIO " + str(start))

# Scrapper genérico
# Desactivamos la cache por petición del profesor
gs = GeneralScraper("https://datosmacro.expansion.com", "/energia/precios-gasolina-diesel-calefaccion", opts={"cache_expire_after": "no_cache"})
gs.scrape()


# Scrapper de imágenes
img_scraper = ImagenesScraper(gs.resource_tokens())
img_scraper.get_images()


end = datetime.now()
print("FIN " + str(end))