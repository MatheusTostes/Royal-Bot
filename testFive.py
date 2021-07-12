import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

import os
location = os.getcwd()
pathChrome = location + "\\data\\chromedriver.exe"
userDataDir = "user-data-dir=" + location + "\\data"

options = webdriver.ChromeOptions()
options.add_argument(userDataDir)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(pathChrome, options=options)
driver.get("http://painel.c-pro.site/")
time.sleep(1)

try:
  driver.find_element_by_name('username').send_keys("matheustostes")
  driver.find_element_by_name('password').send_keys('Matheus123')
  driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/div/div/div/form/div[4]/div/button').click()
except:
  pass

# gerar teste
def testFive():
  driver.get("http://painel.c-pro.site/users/add_trial")
  time.sleep(1)
  driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/h4/div/button').click()
  time.sleep(1)
  driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[2]/div/div/div/div/div/h4/div/div/button[3]').click()

testFive()
time.sleep(3)
testFive()

