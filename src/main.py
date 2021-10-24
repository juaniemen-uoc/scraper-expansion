from general_scraper import GeneralScraper
from imagenes_scraper import ImagenesScraper

# Scrapper genérico
gs = GeneralScraper("https://datosmacro.expansion.com", "/energia/precios-gasolina-diesel-calefaccion")
gs.scrape()


# Scrapper de imágenes
img_scraper = ImagenesScraper(include_list=gs.resource_tokens())
img_scraper.get_images()
