import argparse
import csv
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
MAX_SEARCH_RECURSION=8

TEAM_NAME_MAP = {
  'REIMS': '랭스',
  'NICE': '니스',
  'NANTES': '낭트',
  'SAINT': '생테티엔',
  'LORIENT': '로리앙',
  'TROYES': '트루아',
  'LILLE': '릴',
  'RENNAIS': '렌',
  'LENS': '랑스',
  'MONACO': '모나코',
  'CLERMONT': '클레르몽',
  'LYONNAIS': '리옹',
  'ANGERS': '앙제',
  'MONTPELLIER': '몽펠리에',
  'PSG': 'PSG',
  # NOTE(Jinwook): METZ has two korean names........ (FC 메츠, FC메츠)
  'METZ': '메스',
  # NOTE(Jinwook): BRESTOIS has two korean names........ (브레스트, 브레스투아)
  'BRESTOIS': '브레스',
  'BORDEAUX': '보르도',
  'STRASBOURG': '스트라스부르',
  'MARSEILLE': '마르세유',
}

def get_match_eng_name(match_name, match_date):
  match_date = change_date_to_number(match_date.lstrip('방송일 '))
  match_name = match_name[5:]
  [first_team, second_team] = match_name.split(' vs ')
  first_team_eng = ''
  second_team_eng = ''
  for i in range(len(TEAM_NAME_MAP)):
    curr_team_name = list(TEAM_NAME_MAP.values())[i]
    if first_team.find(curr_team_name) != -1:
      first_team_eng = list(TEAM_NAME_MAP.keys())[i]
    if second_team.find(curr_team_name) != -1:
      second_team_eng = list(TEAM_NAME_MAP.keys())[i]
    if first_team_eng and second_team_eng:
      break
  return match_date + '_' + first_team_eng + '_' + second_team_eng

def change_date_interface(date):
  # NOTE(Jinwook): Assume that both team has only one match in one month -> because it's league only.
  return date[0:4] + '.' + date[4:6]

def change_date_to_number(date):
  return date[0:4] + date[5:7] + date[8:10]

def search(url):
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

    # Get page
    driver.get(url)

    # Load more data to search.
    for recursion in range(MAX_SEARCH_RECURSION):
      more_button = driver.find_element(By.XPATH, '//*[@id = "program-front-common-more-more-button"]')
      more_button.click()
      # sleep to wait page to be loaded.
      sleep(0.2)

    result = list()

    matches_li = driver.find_elements(By.XPATH, './/div[@class = "ali_download_module_w"]')

    for match_li in matches_li:
      if len(match_li.find_elements(By.XPATH, './/*[@class = "notranslate ali_module_label_free"]')) > 0:
        continue
      match_name = match_li.find_element(By.XPATH, './/*[@class = "titprog_name"]').text
      match_date = match_li.find_element(By.XPATH, './/*[@class="itxt_data"]').text
      match_name_eng = get_match_eng_name(match_name, match_date)
      result.append([match_name_eng, match_li.find_element(By.XPATH, './/a[@class = "ali_module_link"]').get_attribute('href')])

    # Close browser
    driver.quit()

    return result

if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://programs.sbs.co.kr/sports/21ligue1/vods/69809',
                        help='URL of full videos')

    args = parser.parse_args()

    result = search(args.url)
    print(result)

    write_file = open('./ligue1.csv', 'w', encoding='utf-8')
    writer = csv.writer(write_file)
    for row in result:
      writer.writerow(row)
    
    write_file.close()
  