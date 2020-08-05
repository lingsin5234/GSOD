from menu import Menu, MenuItem
from django.urls import reverse
from . import views as gsod_vw


# add items to the menu
Menu.add_item("noaa", MenuItem("My Portfolio", url="/", weight=10))
Menu.add_item("noaa", MenuItem("NOAA Project", reverse(gsod_vw.project_markdown), weight=10))
Menu.add_item("noaa", MenuItem("US Hist. Weather Map", reverse(gsod_vw.new_map), weight=10))
