import csv
import os
import shutil
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp

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

    driver.get("https://example.com/")

    driver.get(URL)
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))


    # set login credentials
    driver.find_element(By.ID, "Email").send_keys(USERNAME)
    driver.find_element(By.ID, "Password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, "InstallationGridDatalogs_3_gridcommand4")))

    # visit datalog page by grid
    driver.find_element(By.XPATH, "//button[@id='InstallationGridDatalogs_3_gridcommand4']").click()
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.ID, "download-button")))

    # go to download window
    driver.find_element(By.XPATH, "//button[@id='download-button']").click()
    time.sleep(DELAY)

    # download data
    start_date = "10.04.2022"
    end_date = "19.05.2022"
    driver.find_element(By.ID, "downloaderdate").clear()
    driver.find_element(By.ID, "downloaderdate").send_keys(start_date + " ~ " + end_date)
    driver.find_element(By.XPATH, "//button[@id='btnDownload']").click()
    time.sleep(DELAY)

    # close window
    driver.close()
    driver.quit()

    cmd = f"cd {downloadDir} && ls"
    os.system(cmd)

    cmd = 'ls'
    os.system(cmd)

    #
    # shutil.unpack_archive('10042022-19052022.zip', '.')
    #
    # with open('LG220519.CSV', mode='r') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     line_count = 0
    #     for row in csv_reader:
    #         print(row)

    return {
        "status": "OK"
    }
