from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime

import os
import config
import numpy as np
import spintax
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange, random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
from lxml.html import fromstring
import requests
from itertools import cycle
import json
import random

def banner():
    print('')
    print('------------------------------------')
    print("Comment bot, start. ")
    print('------------------------------------')
    print('')

def wait_seconds(seconds):
    time.sleep(seconds)

def load_config():
    with open("config.txt", "r") as f:
        lines = f.readlines()
    config = {}
    for line in lines:
        key, value = line.strip().split("=")
        config[key] = value
    return config["email"], config["password"]

def load_file(file_path):
    try:
        with open(file_path, 'r') as file:
            item = [line.strip() for line in file if line.strip()]
        if not item:
            print("No item found in the file.")
            return []
        return item
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def load_channel_url():
    with open("channel.txt", "r") as f:
        return f.read().strip()

def setup_driver():
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")  
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    return driver

def login_to_youtube(driver, email, password):
    try:
        x = datetime.datetime.now()
        print('')
        print('------------------------------------')
        print("Automation start !!! ")
        print(email)
        print(x)
        print('------------------------------------')
        print('')
        driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube")
        wait_seconds(5)
        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        wait_seconds(5)
        password_input = driver.find_element("name", "Passwd")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        wait_seconds(5)
    except Exception as e:
        raise e

def check_exists_by_xpath(driver, xpath):
    try:
        driver.get('https://www.youtube.com/watch?v=AXHlsdfnC4E')
        wait = WebDriverWait(driver, 10);
        time.sleep(10)
        wait.until(EC.visibility_of_element_located((By.XPATH,xpath)))
    except NoSuchElementException:
        return False
    return True

#----------------------------------------------------------------------
def get_link(driver, channel_url):
    link = []
    try:
        driver.get(channel_url)
        driver.implicitly_wait(5)
        time.sleep(5)
        video_links = driver.find_elements("xpath", '//a[@id="thumbnail" and contains(@href, "watch?v=")]')
        if video_links != None:
            for video in video_links:
                try:
                    href = video.get_attribute("href")
                    if href and href not in link:
                        link.append(href)
                except:
                    pass
                
                else:
                    print('-')
        return link

    except Exception as e:
        raise e

def mouse_move_down(driver):
    driver.execute_script("window.scrollTo(10, window.scrollY + 80)")
    time.sleep(random.uniform(2,5))
    driver.execute_script("window.scrollTo(0, window.scrollY + 50)")
    time.sleep(random.uniform(2,7))

def mouse_move_up(driver):
    driver.execute_script("window.scrollTo(10, window.scrollY - 50)")
    time.sleep(random.uniform(2,5))
    driver.execute_script("window.scrollTo(0, window.scrollY - 60)")
    time.sleep(random.uniform(2,7))

#--------------------------------------------------
def youtubeSubscribe(driver,url,email):
    time.sleep(5)
    wait = WebDriverWait(driver, 6);
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(random.uniform(200,220))
    mouse_move_down(driver)    
    mouse_move_up(driver)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="subscribe-button"]'))).click()
    print('')
    print('------------------------------------')
    print('')
    print(email)
    print("Subscribe done !!! ")
    print('')
    print('------------------------------------')
    print('')
    mouse_move_down(driver)    
    mouse_move_up(driver)
    time.sleep(random.uniform(50,60)) 

def main():
    banner()
    email_path = 'email.txt'
    password = 'asephendra77'
    data_email = load_file(f'./files/{email_path}')
    channel_url = 'https://www.youtube.com/@ahendra2012/videos'
    
    for email in data_email:
        try:
            driver = setup_driver()
            comment = random.choice(load_file('./files/comment.txt'))
            login_to_youtube(driver, email, password)
            link = get_link(driver, channel_url)
            link_sub = random.choice(link)
            youtubeSubscribe(driver,link_sub,email)

        finally:
            driver.quit()


if __name__ == "__main__":
    main()




