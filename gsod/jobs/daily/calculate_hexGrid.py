# CALCULATE THE HEX GRID
from django_extensions.management.jobs import DailyJob
# from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# this is a weekly job that loads GHCND data for all station
class Job(DailyJob):
    help = "Calculate the Hex Grid based on the data for particular day"

    def execute(self):

        # request
        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # start chrome browser
        browser = webdriver.Chrome(chrome_options=options)
        browser.get('http://127.0.0.1:8000/calculate-hexGrid/2020-05-11/')

        # check what HTML there is
        # element = browser.find_element_by_css_selector('#my_title')
        # print(element.get_attribute('outerHTML'))

        # wait for the "done" id to be generated
        delay = 200  # seconds
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'done')))
            print("Calculations and API requests completed!")
            print(myElem.get_attribute('outerHTML'))
        except TimeoutException:
            print("Loading took too much time!")

        return True
