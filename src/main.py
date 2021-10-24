from general_scrapper import GeneralScrapper

#nc = GeneralScrapper("https://datosmacro.expansion.com", "/energia/precios-gasolina-diesel-calefaccion")
nc = GeneralScrapper("https://datosmacro.expansion.com", "/deuda")

nc.get_data_raw()
nc.process_tidy_data()
nc.data_to_csv()