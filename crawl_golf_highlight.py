import argparse
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import urllib.request as request

def create_driver():
    # Setup chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set default download directory
    # prefs = {"download.default_directory" : f"/media/volume1/golf_highlight"}
    # chrome_options.add_experimental_option("prefs", prefs)

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Path to chromedriver
    webdriver_service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options, desired_capabilities=caps)
    return driver

def download(args):
    driver = create_driver()
    # Get page
    driver.get(args.url)

    button = driver.find_element(By.XPATH, '//button[contains(@id, "sbs-html5player")]')
    button.click()
    
    sleep(20)

    highlight_link = driver.find_element(By.XPATH, '//video[contains(@id, "sbs-html5player")]').get_attribute('src')

    os.makedirs(args.output_dir, exist_ok=True)
    request.urlretrieve(highlight_link, os.path.join(
        args.output_dir, args.filename))

    # FIXME
    sleep(120)



if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL of video to download')
    parser.add_argument('--output_dir', default='/media/volume1',
                        help='directory to save video in')
    parser.add_argument('--filename', default='default.mp4',
                        help='name of output file')

    args = parser.parse_args()

    download(args)
