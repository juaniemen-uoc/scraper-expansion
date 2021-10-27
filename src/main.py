from general_scraper import GeneralScraper
from imagenes_scraper import ImagenesScraper

# Scrapper genérico
gs = GeneralScraper("https://datosmacro.expansion.com", "/energia/precios-gasolina-diesel-calefaccion")
gs.scrape()


# Scrapper de imágenes
breakpoint()
img_scraper = ImagenesScraper(gs.resource_tokens())
img_scraper.get_images()
