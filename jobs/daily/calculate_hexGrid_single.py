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
import datetime as dte
import djangoapps.settings as st
import json


# this is a weekly job that loads GHCND data for all station
class Job(DailyJob):
    help = "Calculate the Hex Grid based on the data for particular day"

    def execute(self):

        # for the job_runs database
        start_time = dte.datetime.now()
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
        d['loggingPrefs'] = {'browser': 'ALL'}
        browser = webdriver.Chrome(chrome_options=options, desired_capabilities=d)
        this_date = dte.date(2020, 1, 10)
        if st.DEBUG:
            URL = 'http://127.0.0.1:8000/calculate-hexGrid/' + str(this_date) + '/'
        else:
            # PRODUCTION
            URL = 'https://portfolio.sinto-ling.ca/gsod/calculate-hexGrid/' + str(this_date) + '/'

        print(URL)
        browser.get(URL)
        time.sleep(200)
        log_file = 'gsod/seleniumLog/' + str(dte.datetime.now().date()) + '.log'
        for entry in browser.get_log('browser'):
            print('CONSOLE LOG:', str(entry))
            with open(log_file, 'a') as outfile:
                outfile.write('CONSOLE LOG:' + str(entry) + '\n')
        delay = 500
        try:
            jsonTag = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'jsonData')))
            print("Calculations and API requests completed!")
            # print(jsonData.get_attribute('innerHTML'))
            jsonData = jsonTag.get_attribute('innerHTML')
            filename = 'hexGrid_' + str(this_date) + '.json'
            try:
                with open('gsod/posts/' + filename, 'w') as outfile:
                    json.dump(json.loads(jsonData), outfile, indent=4)
                    # json.dump(request.data['data'], outfile, indent=4)
            except Exception as e:
                print('POST write to file: Failed', e)
                with open(log_file, 'a') as outfile:
                    outfile.write('POST write to file: Failed' + str(e) + '\n')
                status = False
            else:
                print('POST write to file: Success!')
                with open(log_file, 'a') as outfile:
                    outfile.write('POST write to file: Success!' + '\n')
                status = True
        except TimeoutException:
            print("Loading took too much time!", this_date)
            dbt.log_gsod_job_run(job_id, str(this_date), start_time, 'FAILED')
        else:
            # after each completion, take a 10 minute break
            dbt.log_gsod_job_run(job_id, str(this_date), start_time, 'COMPLETED')

        browser.quit()
        return True
