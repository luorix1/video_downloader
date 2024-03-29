import argparse
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pytube import YouTube

def create_driver():
    # Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set default download directory
    # prefs = {"download.default_directory" : f"/media/volume1/golf_highlight"}
    # chrome_options.add_experimental_option("prefs", prefs)

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Path to chromedriver
    webdriver_service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options, desired_capabilities=caps)
    return driver

def download(url, result):
    driver = create_driver()
    # Get page
    driver.get(url)

    for i in range(20):
      driver.execute_script("window.scrollBy(0,10000)")
      sleep(1)
    
    elements = driver.find_elements(By.XPATH, './/*[@class="yt-simple-endpoint style-scope ytd-grid-video-renderer"]')
    for element in elements:
      # time = element.find_elements(By.XPATH, './/span[@class="style-scope ytd-thumbnail-overlay-time-status-renderer"]')
      # if len(time) > 0:
      #   print(time[0].text)
      # if len(time) > 0 and len(time[0].text) > 2:
      #   if (int(time[0].text.split(':')[0]) > 1):
      if element.get_attribute('title').find('예고') != -1:
        continue
      if element.get_attribute('aria-label').find('year ago') != -1:
        break
      if element.get_attribute('href').find('shorts') != -1:
        continue

      if result.count(element.get_attribute('href')) == 0:
        result.append(element.get_attribute('href'))
    return result


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--link', default='https://www.youtube.com/c/SBSRunningMan/videos',
                      help='index of link to start save')
  parser.add_argument('--channel', default='running_man',
                      help='channel to save')
  args = parser.parse_args()

  csv_file = './' + args.channel + '.csv'
  if not os.path.exists(csv_file):
    write_file = open(csv_file, 'w', encoding='utf-8')

  read_file = open(csv_file, 'r', encoding='utf-8')
  reader = csv.reader(read_file)
  result = []
  for read in reader:
    result.append(read[0])
  read_file.close()
  result = download(args.link, result)
  print(result)

  write_file = open(csv_file, 'w', encoding='utf-8')
  writer = csv.writer(write_file)
  for i in range(len(result)):
    temp = [result[i], args.channel + '_' + str(i)]
    # print(temp)
    writer.writerow(temp)

  write_file.close()
