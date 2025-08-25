#--------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange, random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
from lxml.html import fromstring
from itertools import cycle
import time,datetime,json,random,os,requests,config,spintax
import undetected_chromedriver as uc
import numpy as np



def banner():
    print('')
    print('------------------------------------')
    print("Comment bot video, start. ")
    print('------------------------------------')
    print('')

def wait_seconds(seconds):
    time.sleep(seconds)

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



def youtubeLike(driver):
    url = "https://www.youtube.com/watch?v=ICjf-KV0C_4"
    driver.get(url)
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 6);
    subscribeText = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="subscribe-button"]/ytd-subscribe-button-renderer/yt-button-shape/button/div/span')))
    time.sleep(10)
    # Subscribe
    if subscribeText.text=='Subscribe':
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="subscribe-button"]/ytd-subscribe-button-renderer/yt-button-shape/button'))).click()
    time.sleep(20)

def check_exists_by_xpath(driver, xpath):
    try:
        driver.get('https://www.youtube.com/watch?v=AXHlsdfnC4E')
        wait = WebDriverWait(driver, 10);
        time.sleep(10)
        wait.until(EC.visibility_of_element_located((By.XPATH,xpath)))
    except NoSuchElementException:
        return False
    return True

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

def setup_driver(proxy):
    options = webdriver.ChromeOptions()
    data_useragent = load_file('./files/user_agent.txt')
    user_agent = random.choice(data_useragent)
    #user_agent = data_useragent[3]
    # preferences = {
    #     "webrtc.ip_handling_policy" : "disable_non_proxied_udp",
    #     "webrtc.multiple_routes_enabled": False,
    #     "webrtc.nonproxied_udp_enabled" : False
    # }
    # options.add_experimental_option("prefs", preferences)
    #options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    options.add_experimental_option('useAutomationExtension', False)
    # if proxy != None:
    #     options.add_argument(f'--proxy-server=socks5://{proxy}')
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
        driver.execute_script("arguments[0].scrollIntoView();", email_input)

        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        wait_seconds(4)
        password_input = driver.find_element("name", "Passwd")
        driver.execute_script("arguments[0].scrollIntoView();", password_input)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        wait_seconds(4)
    except Exception as e:
        raise e

def youtubeComment(driver,url_shorts,comment):

    driver.get(url_shorts)
    wait = WebDriverWait(driver, 5);
    time.sleep(75)
    #Ada 2 jenis
    #xpath = driver.find_elements("xpath", '//*[@id="comments-button"]/ytd-button-renderer/yt-button-shape/label/button')
    xpath = driver.find_elements("xpath", '//*[@id="button-bar"]/reel-action-bar-view-model/button-view-model[1]/label/button')
    if xpath != None:
        for x in xpath:
            x.click()
            time.sleep(10)
            wait = WebDriverWait(driver, 10);
            comment_box = EC.presence_of_element_located((By.CSS_SELECTOR, '#placeholder-area'))
            WebDriverWait(driver, 10).until(comment_box)
            comment_box1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#placeholder-area')))
            ActionChains(driver).move_to_element(comment_box1).click(comment_box1).perform()
            add_comment_onit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contenteditable-root')))
            add_comment_onit.send_keys(comment)
            time.sleep(10)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#submit-button'))).click()
            time.sleep(5)
            print('----------------------------')
            print(url_shorts)
            print(comment)
            print('----------------------------')

    time.sleep(50)

def get_config(config_path):
    """Read configuration file"""

    try:
        with open(config_path, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        with open(config_path, 'r') as file:
            data = json.load(file)
    
    return data

# data_shorts = ['https://www.youtube.com/shorts/kS0yYfLxUIw','https://www.youtube.com/shorts/qgwfSdrX2XI',
# 'https://www.youtube.com/shorts/RSuyRZ2VTGs']

def main():
    #banner()
    config = get_config('./config/config.json')
    email = config['email']
    password = config['password']
    proxy = config['proxy']
    comment = config['comment']
    data_shorts = load_file('./files/link_shorts.txt')

    driver = setup_driver(proxy)
    login_to_youtube(driver, email, password)
    time.sleep(40)
    for url_shorts in data_shorts:
        youtubeComment(driver,url_shorts,comment)
    driver.quit()

if __name__ == "__main__":
    main()

