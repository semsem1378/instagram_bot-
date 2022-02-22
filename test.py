from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_browser = webdriver.Chrome()
chrome_browser.maximize_window()
chrome_browser.get("https://www.seleniumeasy.com/test/ajax-form-submit-demo.html")
txt = chrome_browser.find_elements_by_class_name("form-control")
txt[0].send_keys("asd")
txt[1].send_keys("asd")
txt[1].send_keys(Keys.ENTER)
txt[1].submit()
time.sleep(10)