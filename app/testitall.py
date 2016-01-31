from app_start import *
import datetime
import menu_scraper

date = datetime.date(2016, 1, 29)
z = menu_scraper.get_all_menus(date)['Porter Kresge']['Lunch']
