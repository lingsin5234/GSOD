# CALCULATE THE HEX GRID
from django_extensions.management.jobs import DailyJob
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from gsod.oper import database_transactions as dbt
import time
import datetime as dt
import djangoapps.settings as st


# this is a weekly job that loads GHCND data for all station
class Job(DailyJob):
    help = "Calculate the Hex Grid based on the data for particular day"

    def execute(self):

        # for the job_runs database
        start_time = dt.datetime.now()
        query = "SELECT Id FROM jobs_dim WHERE job_name='calculate_hexGrid_migrate'"
        job_id = [n for (n,) in dbt.gsod_db_reader(query)][0]

        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')

        # start chrome browser
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = {'browser': 'ALL'}
        browser = webdriver.Chrome(chrome_options=options, desired_capabilities=d)
        this_date = dt.date(2020, 1, 1)
        if st.DEBUG:
            URL = 'http://127.0.0.1:8000/calculate-hexGrid/' + str(this_date) + '/'
        else:
            # PRODUCTION
            URL = 'https://portfolio.sinto-ling.ca/gsod/calculate-hexGrid/' + str(this_date) + '/'

        print(URL)
        browser.get(URL)

        time.sleep(1800)
        for entry in browser.get_log('browser'):
            print(entry)
        '''
        # TESTING browser
        delay = 500
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'done')))
            print("API GET Request successful!")
            print(myElem.get_attribute('outerHTML'))
        except TimeoutException:
            print("Something still wrong!", this_date)
            browser.quit()
            return False
        else:
            browser.quit()
            return True
        '''
        '''
        # wait for the "done" id to be generated
        time.sleep(1200)
        delay = 500
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'done')))
            print("Calculations and API requests completed!")
            print(myElem.get_attribute('outerHTML'))
        except TimeoutException:
            print("Loading took too much time!", this_date)
            dbt.log_gsod_job_run(job_id, str(this_date), start_time, 'FAILED')
        else:
            # after each completion, take a 10 minute break
            dbt.log_gsod_job_run(job_id, str(this_date), start_time, 'COMPLETED')

        return True
        '''
        browser.quit()
