import os
import ffmpeg
import re
import json
import subprocess
import ffmpeg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def create_driver():
    # Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Path to chromedriver
    webdriver_service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options, desired_capabilities=caps)
    return driver

def get_full_link_m3u8_link(url):
    # Get page
    driver = create_driver()
    driver.get(url)

    print(url)
    sleep(30)
    count = 0
    for item in driver.get_log("performance"):
      message_json = json.loads(item['message'])['message']
      if 'params' in message_json:
        if 'request' in message_json['params']:
          if 'url' in message_json['params']['request']:
            count += 1
    print(count)
    # log = [item for item in driver.get_log("performance") if 'm3u8' in str(item)]
    # print(len(log))
    # result_url = json.loads(log[0]['message'])['message']['params']['request']['url']
    driver.quit()
 
    return result_url

def search(url):
    download_url = get_full_link_m3u8_link(url)
    print(download_url)
    # stream = ffmpeg.input(download_url)
    # stream = ffmpeg.hflip(stream)
    # stream = ffmpeg.output(stream, './test.mp4')
    # ffmpeg.run(stream)

    return


def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

if __name__ == '__main__':
  stream = os.popen('twitch-dl videos hanryang1125')
  output = stream.read()
  output_list = output.split('\n')
  link_list = []
  for string in output_list:
    if string.find('https') >= 0:
      escape_ansi_string = escape_ansi(string)
      search(escape_ansi_string)
      break
