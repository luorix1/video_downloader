import argparse
import json
import os
import re
import requests
# Run selenium and chrome driver to scrape data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
import urllib.request as request


def download(args):
    # Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # # Path to chromedriver
    webdriver_service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options, desired_capabilities=caps)

    # Get page
    driver.get(args.url)

    # Wait for a bit
    # time.sleep(2)

    browser_log = driver.get_log('performance')

    result = []
    for log in browser_log:
        msg = log['message']
        if len(msg) < 6000:
            continue
        comp = re.compile(
            r'"url":"(https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/[^"]+)')
        url = comp.findall(msg)
        if len(url) == 0:
            continue
        breakpoint()
        response = requests.get(url[0])
        comp = re.compile(
            r'"source":"https://b01-kr-naver-vod.pstatic.net/navertv[^"]+)')
        # result.append(comp.findall(response.text))
        result.append(response.text)

    assert len(result) > 0

    # Create directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Save video as file
    request.urlretrieve(result[0], os.path.join(
        args.output_dir, args.filename))


if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL of video to download')
    parser.add_argument('--output_dir', default='/Users/jwhwang/Desktop',
                        help='directory to save video in')
    parser.add_argument('--filename', default='default.mp4',
                        help='name of output file')

    args = parser.parse_args()

    download(args)
