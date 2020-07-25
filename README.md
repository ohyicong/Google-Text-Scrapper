# Google Text Scraper
 A library to scrap google text results
 
 Pre-requisites:
 1. Pip install Selenium Library
 2. Download Google Chrome 
 3. Download Google Webdriver based on your Chrome version
 
 
Usage:

from GoogleTextScrapper import GoogleTextScraper

import os


webdriver_path = os.getcwd()+"\\webdriver\\chromedriver.exe"

csv_path = os.getcwd()+"\\data.csv"

search_keys= ["apple","microsoft","netflix"]

headless = False

web_scrapper = GoogleTextScraper(webdriver_path,csv_path,headless)

for search_key in search_keys:

   result = web_scrapper.get_info(search_key)
    
   web_scrapper.save_info(result)

