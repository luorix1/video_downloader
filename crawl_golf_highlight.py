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


def download(args):
    os.makedirs(args.output_dir, exist_ok=True)
    request.urlretrieve(args.url, os.path.join(
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
