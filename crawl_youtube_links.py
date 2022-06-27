import csv
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
    webdriver_service = Service('/usr/local/bin/chromedriver')
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
    
    elements = driver.find_elements(By.XPATH, './/*[@class="yt-simple-endpoint style-scope ytd-video-renderer"]')
    for element in elements:
      # time = element.find_elements(By.XPATH, './/span[@class="style-scope ytd-thumbnail-overlay-time-status-renderer"]')
      # if len(time) > 0:
      #   print(time[0].text)
      # if len(time) > 0 and len(time[0].text) > 2:
      #   if (int(time[0].text.split(':')[0]) > 1):
      if element.get_attribute('title').find('예고') != -1:
        continue

      if result.count(element.get_attribute('href')) == 0:
        result.append(element.get_attribute('href'))
    return result


if __name__ == '__main__':
  read_file = open('./youtube.csv', 'r', encoding='utf-8')
  reader = csv.reader(read_file)
  result = []
  for read in reader:
    result.append(read[0])
  read_file.close()
  result = download('https://www.youtube.com/c/SBSNOW/search?query=%EB%9F%B0%EB%8B%9D%EB%A7%A8', result)
  print(result)

  write_file = open('./youtube.csv', 'w', encoding='utf-8')
  writer = csv.writer(write_file)
  for i in range(len(result)):
    temp = [result[i], 'running_man_' + str(i)]
    print(temp)
    writer.writerow(temp)

  write_file.close()
