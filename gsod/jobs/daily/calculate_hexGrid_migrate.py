# CALCULATE THE HEX GRID
from django_extensions.management.jobs import DailyJob
from selenium import webdriver
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
    help = "Calculate the Hex Grid based on the data for particular day -- migration mode"

    def execute(self):

        # for the job_runs database
        start_time = dt.datetime.now()
        query = "SELECT Id FROM jobs_dim WHERE job_name='calculate_hexGrid_migrate'"
        job_id = [n for (n,) in dbt.gsod_db_reader(query)][0]

        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')

        # start chrome browser
        browser = webdriver.Chrome(chrome_options=options)

        # loop through dates
        start_date = dt.date(2020, 1, 1)
        end_date = (dt.datetime.now() - dt.timedelta(days=14)).date()  # date of migration - 14
        for this_date in daterange(start_date, end_date):

            if st.DEBUG:
                URL = 'http://127.0.0.1:8000/calculate-hexGrid/' + str(this_date) + '/'
                if str(this_date) == '2020-01-10':
                    break
            else:
                # PRODUCTION
                URL = 'https://portfolio.sinto-ling.ca/gsod/calculate-hexGrid/' + str(this_date) + '/'

            print(URL)
            browser.get(URL)

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
                time.sleep(600)

        return True


# get date range for for-loop
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)
