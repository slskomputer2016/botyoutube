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
    options.add_argument(f"user-agent={user_agent}")

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
        wait_seconds(5)
        password_input = driver.find_element("name", "Passwd")
        driver.execute_script("arguments[0].scrollIntoView();", password_input)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        wait_seconds(8)
    except Exception as e:
        raise e

def youtubeComment(driver,channel_url,email):
    link_motor = load_file('./files/link_motor.txt')
    time.sleep(2)
    config = get_config('./config/config.json')
    comment_path = config['comment_path']
    data_comment = load_file(f'./files/{comment_path}')
    data_video = get_link(driver,channel_url)

    driver.get(channel_url)
    time.sleep(3)
    wait = WebDriverWait(driver, 4);
    jum = 0
    video_done = set()
    while jum<3:
        comment = random.choice(data_comment)
        url = random.choice(data_video)
        if url not in video_done:
            driver.get(channel_url)
            time.sleep(3)
            driver.get(url)
            jum+=1
            driver.implicitly_wait(10)
            time.sleep(2)
            #video_xpath = driver.find_elements("xpath", '//*[@id="contents"]')
            video_xpath = driver.find_elements("xpath", '//a[@id="video-title"]')
            if video_xpath != None:
                for vid in video_xpath:
                    try:
                        href = vid.get_attribute("href")
                        print(href)
                    except:
                        pass
                    
                    else:
                        print('---')
            else:
                print('No Video Xpath !!!')

            time.sleep(random.uniform(170,200))
            driver.execute_script("window.scrollTo(0, window.scrollY + 150)")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, window.scrollY - 50)")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, window.scrollY - 50)")
            time.sleep(random.uniform(6,8))

            #-----------------------------------------------
            comment_box = EC.presence_of_element_located((By.CSS_SELECTOR, '#placeholder-area'))
            WebDriverWait(driver, 10).until(comment_box)
            comment_box1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#placeholder-area')))
            ActionChains(driver).move_to_element(comment_box1).click(comment_box1).perform()
            add_comment_onit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contenteditable-root')))
            add_comment_onit.send_keys(comment)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#submit-button'))).click()
            print('')
            print('------------------------------------')
            print('')
            print(jum)
            print(email)
            print(url)
            print(comment," - Comment done. ")
            print('')
            print('------------------------------------')
            print('')
            time.sleep(random.uniform(50,60))

def get_config(config_path):
    """Read configuration file"""

    try:
        with open(config_path, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        with open(config_path, 'r') as file:
            data = json.load(file)
    
    return data


def main():
    #banner()
    config = get_config('./config/config.json')
    email = config['email']
    password = config['password']
    proxy = config['proxy']
    channel_url = config['channel_url']

    driver = setup_driver(proxy)
    #driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": "Asia/Jakarta"})
    login_to_youtube(driver, email, password)

    #driver.get('https://whoer.net')
    time.sleep(1)
    youtubeComment(driver,channel_url,email)
    driver.quit()

if __name__ == "__main__":
    main()

