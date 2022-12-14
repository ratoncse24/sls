import csv
import os
import shutil
import time
from pathlib import Path
import re

from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp

from bigquery_util import save_data


today = date.today()
start_date = today - timedelta(days=3)
end_date = today - timedelta(days=1)

filter_start_date = start_date.strftime("%d.%m.%Y")
filter_end_date = end_date.strftime("%d.%m.%Y")

ZIP_FILE_NAME = f"{'%02d' % start_date.day}{'%02d' % start_date.month}{start_date.year}-{'%02d' % end_date.day}{'%02d' % end_date.month}{end_date.year}"

file_date = end_date
CSV_FILE_NAME = f"LG{str(file_date.year)[2:4]}{'%02d' % file_date.month}{'%02d' % file_date.day}"


URL = 'https://portal.studer-innotec.com/User/Login'
USERNAME = "microenergy.kirchhoff@gmail.com"
PASSWORD = "Dharcelona"
DELAY = 3
DIR = mkdtemp()

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    downloadDir = "/tmp"
    # Make sure path exists.
    Path(downloadDir).mkdir(parents=True, exist_ok=True)

    # Set Preferences.
    preferences = {"download.default_directory": downloadDir,
                   "download.prompt_for_download": False,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True}

    options.add_experimental_option("prefs", preferences)
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={DIR}")
    options.add_argument(f"--data-path={DIR}")
    options.add_argument(f"--disk-cache-dir={DIR}")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome("/opt/chromedriver", options=options)

    # driver.get("https://example.com/")

    driver.get(URL)
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))


    # set login credentials
    driver.find_element(By.ID, "Email").send_keys(USERNAME)
    driver.find_element(By.ID, "Password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, "InstallationGridDatalogs_2_gridcommand5")))

    # visit datalog page by grid
    driver.find_element(By.XPATH, "//button[@id='InstallationGridDatalogs_2_gridcommand5']").click()
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, "download-button")))

    # go to download window
    driver.find_element(By.XPATH, "//button[@id='download-button']").click()
    time.sleep(DELAY)

    # download data
    # start_date = "10.04.2022"
    # end_date = "19.05.2022"
    driver.find_element(By.ID, "downloaderdate").clear()
    driver.find_element(By.ID, "downloaderdate").send_keys(filter_start_date + " ~ " + filter_end_date)
    driver.find_element(By.XPATH, "//button[@id='btnDownload']").click()
    time.sleep(DELAY)

    # close window
    driver.close()
    driver.quit()

    cmd = f"cd {downloadDir} && ls"
    os.system(cmd)

    cmd = 'ls'
    os.system(cmd)


    shutil.unpack_archive(f'/tmp/{ZIP_FILE_NAME}.zip', '/tmp')

    dateRegex = re.compile(r'\d\d.\d\d.\d\d\d\d')
    data = []
    with open(f'/tmp/{CSV_FILE_NAME}.CSV', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            mo = dateRegex.search(row['v7.4'])
            if mo:
                time_raw = row['v7.4']
                date_obj = datetime.strptime(time_raw, '%d.%m.%Y %H:%M')
                params = {
                    'time': str(date_obj),
                    'Bat_min_V': row['XT-Ubat- (MIN) [Vdc]'],
                    'Vin_VAC': row['XT-Uin [Vac]'],
                    'Iin_IAC': row['XT-Iin [Aac]'],
                    'Pout_kVA': row['XT-Pout+ [kVA]'],
                    'Fout_Hz_AC': row['XT-Fout [Hz]'],
                    'Fin_Hz_AC': row['XT-Fin [Hz]'],
                    'Bat_Vdc': row['XT-Ubat [Vdc]'],
                    'Ibat_Adc': row['XT-Ibat [Adc]'],
                    'Pin_kW': row['XT-Pin a [kW]'],
                }
                data.append(params)

    ret = save_data(json_data=data, dataset_id='sol-telemetry-prod.studer_dataset', table_id='ac_availability')
    print(ZIP_FILE_NAME)
    print(CSV_FILE_NAME)
    print(ret)

    return {
        "status": "OK"
    }
