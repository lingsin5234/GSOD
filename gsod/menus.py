from menu import Menu, MenuItem
from django.urls import reverse
from . import views as gsod_vw


# add items to the menu
Menu.add_item("noaa", MenuItem("My Portfolio", url="/", weight=10))
Menu.add_item("noaa", MenuItem("NOAA Project", reverse(gsod_vw.project_markdown), weight=10))
Menu.add_item("noaa", MenuItem("Stations", reverse(gsod_vw.list_stations), weight=10))
Menu.add_item("noaa", MenuItem("Map of Edmonton", reverse(gsod_vw.map_test), weight=10))
