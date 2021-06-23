# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#import helper libraries
import time
import urllib.request
import shutil
import os
import requests
import pandas as pd

#custom patch libraries
import patch 

class GoogleTextScraper():
    def __init__(self,webdriver_path,csv_path,headless=False):
        #check if chromedriver is updated
        while(True):
            try:
                #try going to www.google.com
                options = Options()
                options.add_argument('--headless')
                driver = webdriver.Chrome(webdriver_path, chrome_options=options)
                driver.get("https://www.google.com")
                driver.close()
                break
            except:
                #patch chromedriver if not available or outdated
                try:
                    driver
                except NameError:
                    is_patched = patch.download_lastest_chromedriver()
                else:
                    is_patched = patch.download_lastest_chromedriver(driver.capabilities['version'])
                if (not is_patched): 
                    print("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")
                    break
        #check parameter types
        self.webdriver_path = webdriver_path
        self.csv_path = csv_path
        self.url = "https://www.google.com/"
        self.headless=headless

    
    def get_info(self,search_key):
        result = []
        print("[INFO] Searching for %s."%(search_key))
        options = Options()
        if(self.headless):
            options.add_argument('--headless')
        try:
            driver = webdriver.Chrome(self.webdriver_path, chrome_options=options)
            driver.get(self.url)
            time.sleep(1)
        except:
            print("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        driver.find_element_by_name("q").send_keys(search_key)
        driver.find_element_by_name("q").send_keys(Keys.RETURN)
        try:
            description = str(driver.find_element_by_class_name("kno-rdesc").text)[11:]
            attributes = driver.find_elements_by_class_name("Z1hOCe")
            result.append([search_key, "description", description.lower().replace("\n","")])
            for attribute in attributes:
                if(attribute.text):
                    info = attribute.text.split(":",1)
                    result.append([search_key, info[0].lower().replace("\n",""), info[1].lower().replace("\n","")])
            time.sleep(1)
            driver.close()
            return result
        except NoSuchElementException:
            print("[INFO] No description found for %s."%(search_key))
            driver.close()
            return None
        
    def save_info (self, result):
        print("[INFO] Saving to %s."%self.csv_path)
        with open(self.csv_path,"a") as f:
            df=pd.DataFrame(result,columns=["search key","type","text"])
            df.to_csv(self.csv_path,index=False,mode="a",header=f.tell()==0)


    

