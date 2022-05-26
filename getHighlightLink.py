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
MAX_SEARCH_RECURSION=10

TEAM_NAME_MAP = {
  'REIMS': '랭스',
  'NICE': '니스',
  'NANTES': '낭트',
  'SAINT': '생테티엔',
  'LORIENT': '로리앙',
  'TROYES': '트루아',
  'LILLE': '릴',
  'RENNAIS': '스타드 렌',
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

def change_date_interface(date):
  # NOTE(Jinwook): Assume that both team has only one match in one month -> because it's league only.
  return date[0:4] + '.' + date[4:6]

def change_date_to_number(date):
  return date[0:4] + date[5:7] + date[8:10]

def check_match_name(first_team_korean, second_team_korean, searching_match_date, current_match_name, current_match_date):
    if current_match_date.find(searching_match_date) == -1:
      return False
    if current_match_name.find(first_team_korean) == -1:
      return False
    if current_match_name.find(second_team_korean) == -1:
      return False
    return True


def search_for_match(driver, searching_match_name):
    # ali_module_title
    searching_match_name_splitted = searching_match_name.split('_')

    searching_match_date = change_date_interface(searching_match_name_splitted[0])
    searching_match_date_milliseconds = datetime.strptime(searching_match_name_splitted[0], '%Y%m%d').timestamp()
    first_team_korean = TEAM_NAME_MAP[searching_match_name_splitted[1]]
    second_team_korean = TEAM_NAME_MAP[searching_match_name_splitted[2]]



    elements = driver.find_elements(By.XPATH, './/div[@class = "ali_module_w"]')
    for element in elements:
      current_match_date = element.find_element(By.XPATH, './/div[@class = "itxt_data"]').text
      current_match_date_milliseconds = datetime.strptime(change_date_to_number(current_match_date.split()[1]), '%Y%m%d').timestamp()
      date_diff = current_match_date_milliseconds - searching_match_date_milliseconds
      
      # NOTE(Jinwook): Assume that highlight is uploaded in 4 days.
      if date_diff > 4 * 24 * 60 * 60:
        continue
      
      if date_diff < -1 * 4 * 24 * 60 * 60:
        break

      current_match_name = element.find_element(By.XPATH, './/span[@class = "ali_module_title"]').text
      search_result = check_match_name(first_team_korean, second_team_korean, searching_match_date, current_match_name, current_match_date)
      if search_result == True:
        return element.find_element(By.XPATH, './/a[@class = "ali_module_link"]').get_attribute('href')
    
    return

def search(url, match_names):
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
    for match_name in match_names:
      result_link = search_for_match(driver, match_name[0])
      print(match_name, result_link)
      match_name.append(result_link)
      result.append(match_name)

    # Close browser
    driver.quit()

    return result



if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://programs.sbs.co.kr/sports/21ligue1/clips/69811',
                        help='URL of highlight videos')

    args = parser.parse_args()

    read_file = open('./ligue1.csv', 'r', encoding='utf-8')
    match_names = csv.reader(read_file)

    result = search(args.url, match_names)

    read_file.close()

    write_file = open('./ligue1_result.csv', 'w', encoding='utf-8')
    writer = csv.writer(write_file)
    for row in result:
      writer.writerow(row)
    
    write_file.close()
  