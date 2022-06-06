import argparse
import csv
import json
from unittest import result
import ffmpeg
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def create_driver():
    # Setup chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Path to chromedriver
    webdriver_service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options, desired_capabilities=caps)
    return driver

def get_full_link_m3u8_link(url, id, pwd):
    # Get page
    driver = create_driver()

    login_url = 'https://cert.golf.sbs.co.kr/html/front/login/login1.jsp?gotourl=https%3A%2F%2Fgolf.sbs.co.kr%2F'
    driver.get(login_url)

    # Type ID and password
    id_box = driver.find_element(by=By.XPATH, value='//*[@id="loginId"]')
    pw_box = driver.find_element(by=By.XPATH, value='//*[@id="loginPw"]')

    id_box.send_keys(id)
    pw_box.send_keys(pwd)

    # Find submit button and click
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="loginBtn"]')
    submit_button.click()
    sleep(1)

    driver.get(url)

    button = driver.find_element(By.XPATH, '//button[@id = "undefined"]')
    button.click()
    sleep(1)

    log = [item for item in driver.get_log("performance") if 'chunklist' in str(item)]
    print(len(log))
    result_url = json.loads(log[0]['message'])['message']['params']['request']['url']
    driver.quit()

    return result_url

def search(url):
    download_url = get_full_link_m3u8_link(url, args.id, args.pwd)

    stream = ffmpeg.input(download_url)
    stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, args.filename)
    ffmpeg.run(stream)

    return

if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://programs.sbs.co.kr/sbsgolf/22klpgatour/vod/71322/22000449501?type=tv&cooper=sbs',
                        help='URL of full videos')
    parser.add_argument('--id', help='Id of sbs golf')
    parser.add_argument('--pwd', help='Pwd of sbs golf')
    parser.add_argument('--output_dir', default='/media/volume1',
                        help='directory to save video in')
    parser.add_argument('--filename', default='default.mp4',
                        help='name of output file')

    args = parser.parse_args()

    search(args.url)
