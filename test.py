import lxml.html
from lxml.cssselect import CSSSelector
from lxml import etree
import requests

menu_page = lxml.html.parse("http://nutrition.sa.ucsc.edu/menuSamp.asp?locationNum=25&locationName=Porter+Kresge&sName=UC+Santa+Cruz+Dining&naFlag=1")

breakfast = CSSSelector('body > table:nth-child(4) > tr > td:nth-child(1)')

lunch = CSSSelector('body > table:nth-child(4) > tr > td:nth-child(2)')

dinner = CSSSelector('body > table:nth-child(4) >tr > td:nth-child(3)')

break_menu= breakfast(menu_page)[0].find_class("menusamprecipes")
lunch_menu= lunch(menu_page)[0].find_class("menusamprecipes")
dinner_menu= dinner(menu_page)[0].find_class("menusamprecipes")

def get_text(x): return x.text_content()

break_menu = map(get_text, break_menu)
lunch_menu= map(get_text, lunch_menu)
dinner_menu = map(get_text, dinner_menu)
