import argparse
import csv
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Max try of clicking load_more button.
MAX_SEARCH_RECURSION=5

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


def change_date_to_number(date):
  return date[0:4] + date[5:7] + date[8:10]

def search_for_match(info):
    name = info.find_element(By.XPATH, './/*[@class = "ali_module_title"]').text
    date = change_date_to_number(info.find_element(By.XPATH, './/*[@class = "itxt_data"]').text)
    link = info.find_element(By.XPATH, './/*[@class = "ali_module_link"]').get_attribute('href')
    return [date, name, link]


def get_highlight_download_link(url):
    driver = create_driver()
    # Get page
    driver.get(url)

    full_link = driver.find_element(By.XPATH, '//*[@class = "ecf_link"]').get_attribute('href')
    driver.quit()

    return [url, full_link]


def search(url):
    driver = create_driver()

    # Get page
    driver.get(url)

    # Load more data to search.
    for recursion in range(MAX_SEARCH_RECURSION):
      button_elements = driver.find_elements(By.XPATH, '//*[@id = "program-front-golf-clips-favorite-more-button"]')
      if len(button_elements) == 0:
        break
      button_elements[0].click()
      # sleep to wait page to be loaded.
      sleep(0.2)

    infos = driver.find_elements(By.XPATH, '//*[@class= "ali_module_w"]')
    
    highlight_links = []
    for info in infos:
      info_result = search_for_match(info)
      highlight_links.append(info_result)
    # Close browser
    driver.quit()

    result = []
    for match in highlight_links:
      try:
        match_download_link = get_highlight_download_link(match[2])
        result.append([match[0], match_download_link[0], match_download_link[1]])
      except:
        print('unknown error at getting full link')

    return result

if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://programs.sbs.co.kr/sbsgolf/22klpgatour/clips/71977',
                        help='URL of highlight videos')

    args = parser.parse_args()

    write_file = open('./golf.csv', 'w', encoding='utf-8')
    writer = csv.writer(write_file)
    result = search(args.url)
    for row in result:
      writer.writerow(row)
    
    write_file.close()
  