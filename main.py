# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
from GoogleTextScrapper import GoogleTextScraper
import os


webdriver_path = os.path.normpath(os.getcwd()+"\\webdriver\\chromedriver.exe")
csv_path =  os.path.normpath(os.getcwd()+"\\data.csv")
search_keys= ["apple","microsoft","netflix"]
headless = False
web_scrapper = GoogleTextScraper(webdriver_path,csv_path,headless)

#search key, description, addition info
for search_key in search_keys:
    result = web_scrapper.get_info(search_key)
    web_scrapper.save_info(result)

