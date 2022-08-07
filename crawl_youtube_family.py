import argparse
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pytube import YouTube


count = 0

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

def download(url, output_dir, count):
    driver = create_driver()
    # Get page
    driver.get(url)
    sleep(3)
    try:
      button = driver.find_element(By.XPATH, '//button[contains(@class, "ytp-large-play-button ytp-button")]')
      button.click()
    except:
      print('Error!!')

    for i in range(7):
      buttons = driver.find_elements(By.XPATH, './/*[@class="ytp-ad-skip-button ytp-button"]')
      if len(buttons) > 0:
        try:
          buttons[0].click()
        except:
          print('Error!')
      yt = YouTube(url)
      stream = yt.streams.filter(res="360p", progressive="True")[0]
      stream.download(output_path=output_dir+'/video', filename="running_man_"+str(count)+'.mp4')
      print('Download Complete!!', url, count)
      countAfter = count + 1
      return countAfter
    print('Download Failed due to unknown reason')
    return count

def get_links(url, result):
  driver = create_driver()
  # Get page
  driver.get(url)

  for i in range(10):
    driver.execute_script("window.scrollBy(0,10000)")
    sleep(1)
  
  elements = driver.find_elements(By.XPATH, './/*[@class="yt-simple-endpoint inline-block style-scope ytd-thumbnail"]')
  for element in elements:
    if result.count(element.get_attribute('href')) == 0 and isinstance(element.get_attribute('href'), str):
      result.append(element.get_attribute('href'))
  return result



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--output_dir', default='/data/data1/family',
                      help='directory to save video in')
  args = parser.parse_args()
  isExist = os.path.exists(args.output_dir)
  if isExist == False:
    os.makedirs(args.output_dir)
    os.makedirs(args.output_dir + '/video')
    # os.makedirs(args.output_dir + '/graph')

  links = get_links('https://www.youtube.com/playlist?list=PLiutUG5JYIAf3qeYytMvcXF3DNlw6Ee4j', [])
  for link in links:
    try:
      print(link)
      count = download(link, args.output_dir, count)
    except:
      print('Error at ', count)
  # plt.plot(x_axis, y_axis)
  # plt.show()
