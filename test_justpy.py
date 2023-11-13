from functools import partial
from generate_request import all_activities, activity_description_map


import justpy as jp

from gui import Gui, my_click, activity_str
from main_page import main_page

gui = Gui()

def _main_page():
    return main_page(gui)

jp.justpy(_main_page)
