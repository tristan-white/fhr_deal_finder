from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

og_url = "https://www.kayak.com/flights/WAS-LAX/2024-10-28/2024-11-04?sort=bestflight_a"

origin = "WAS"
dest = "LAX"
start_date = "2024-10-28"
end_date = "2024-11-04"

url = f"https://www.kayak.com/flights/{origin}-{dest}/{start_date}/{end_date}?sort=bestflight_a"

driver = webdriver.Firefox()
driver.get(url)

print(driver.page_source)