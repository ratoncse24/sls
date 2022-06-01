# from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://portal.studer-innotec.com/User/Login'
USERNAME = "microenergy.kirchhoff@gmail.com"
PASSWORD = "Dharcelona"
DELAY = 3

# visit login page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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

# use beautiful soup
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# print(len(soup.find_all("table")))
# print(soup.find("table", {"id": "expanded_standings"}))

# close window
driver.close()
driver.quit()
