# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
#import helper libraries
import time
import urllib.request
import shutil
import os
import requests
import pandas as pd

class GoogleTextScraper():
    def __init__(self,webdriver_path,csv_path,headless=False):
        #check parameter types
        self.webdriver_path = webdriver_path
        self.csv_path = csv_path
        self.url = "https://www.google.com/"
        self.headless=headless

    
    def get_info(self,search_key):
        #save images into file directory
        result = []
        print("GoogleTextScraper Notification: Searching for %s."%(search_key))
        options = Options()
        if(self.headless):
            options.add_argument('--headless')
        
        driver = webdriver.Chrome(self.webdriver_path, chrome_options=options)
        driver.get(self.url)
        driver.find_element_by_xpath("/html/body/div/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input").send_keys(search_key)
        driver.find_element_by_xpath("/html/body/div/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.RETURN)
        try:
            description = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[9]/div[1]/div[3]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/div/div/span[1]").text
            attributes = driver.find_elements_by_class_name("Z1hOCe")
            result.append([search_key, "description", description.lower()])
            for attribute in attributes:
                info = attribute.text.split(":",1)
                result.append([search_key, info[0].lower().replace("–","-"), info[1].lower().replace("–","-")])
            return result
        except NoSuchElementException:
            print("GoogleTextScraper Notification: No description found for %s."%(search_key))
            return None
    def save_info (self, result):
        print("GoogleTextScraper Notification: Saving...")
        
        try:
            df = pd.read_csv(self.csv_path)
            df=pd.concat([df,pd.DataFrame(result,columns=["search key","type","text"])])
            print(df)
            df.to_csv(self.csv_path,index=False)
        except:
            df=pd.DataFrame(result,columns=["search key","type","text"])
            df.to_csv(self.csv_path,index=False)

    

