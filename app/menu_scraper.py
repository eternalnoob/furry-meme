import lxml.html
from lxml.cssselect import CSSSelector


def get_all_menus(date):
    all_menu = {}
    # Grab College 8 menu
    all_menu['8Oakes'] = get_menu(0, date)

    # Grab Porter Menu
    all_menu['Porter'] = get_menu(1, date)

    # Grab 9/10 Menu
    all_menu['NineTen'] = get_menu(2, date)

    # Grab Crown/Merrill Menu
    all_menu['CrownMerrill'] = get_menu(3, date)

    # Grab Cowell/Stevenson Menu
    all_menu['CowellStevenson'] = get_menu(4, date)
    return all_menu


def get_text(x): return x.text_content()


def get_menu(dining_hall, date):
    """
    Return all menus for a dining hall on a given date
    dining_hall: dining hall "index"
    0=College8, 1=Porter, 2=nine/ten, 3=crown/merrill, 4=cowell/stevenson
    Date: Python date object of date to find dining hall menu for
    """

    if dining_hall == 0:  # C8
        location = "30"  # Location num set to 30 for request to c8
    elif dining_hall == 1:  # Porter
        location = "25"  # Location num set to 25 for porter req
    elif dining_hall == 2:  # 9/10
        location = "40"  # Location num set to 40 for 9/10
    elif dining_hall == 3:  # Crown/Merill
        location = "20"  # Location num set to 20 for Crown/Merill
    elif dining_hall == 4:  # Stevenson
        location = "05"  # Location num set to 05 for Cowell/Steve
    else:
        return "Invalid Dining Hall Number"

    breakfast = CSSSelector('body > table:nth-child(4) > tr > td:nth-child(1)')

    lunch = CSSSelector('body > table:nth-child(4) > tr > td:nth-child(2)')

    dinner = CSSSelector('body > table:nth-child(4) > tr > td:nth-child(3)')

    menu_page = lxml.html.parse(
        "http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&dtdate={0}%2F{1}%2F{2}&locationNum={3}".format(
            date.month, date.day, date.year, location))  # make formatted call to menu page

    # Create all of our menus
    break_menu = breakfast(menu_page)  # [0].find_class("menusamprecipes")
    lunch_menu = lunch(menu_page)  # [0].find_class("menusamprecipes")
    dinner_menu = dinner(menu_page)  # [0].find_class("menusamprecipes")

    menu_dict = {}
    # embed()
    if len(lunch_menu) == 0:  # If Lunch Doesn't exist, we're closed
        return menu_dict

    elif len(dinner_menu) == 0:  # We only have Brunch and Dinner
        break_menu = map(get_text, break_menu[0].find_class("menusamprecipes"))
        dinner_menu = map(get_text, lunch_menu[0].find_class("menusamprecipes"))

        return {"Breakfast": break_menu, "Lunch": [],
                "Dinner": dinner_menu}  # need to return lunch menu because dinner doesn't exist!

    else:

        break_menu = map(get_text, break_menu[0].find_class("menusamprecipes"))
        lunch_menu = map(get_text, dinner_menu[0].find_class("menusamprecipes"))
        dinner_menu = map(get_text, dinner_menu[0].find_class("menusamprecipes"))

        return {"Breakfast": break_menu, "Lunch": lunch_menu, "Dinner": dinner_menu}
