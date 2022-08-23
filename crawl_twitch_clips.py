import argparse
import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def escape_ansi(line):
  ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
  return ansi_escape.sub('', line)

def create_driver():
  # Setup chrome options
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # Ensure GUI is off
  chrome_options.add_argument("--no-sandbox")

  caps = DesiredCapabilities.CHROME
  caps['goog:loggingPrefs'] = {'performance': 'ALL'}

  # Path to chromedriver
  webdriver_service = Service('/usr/bin/chromedriver')
  driver = webdriver.Chrome(
      service=webdriver_service, options=chrome_options, desired_capabilities=caps)
  return driver

def hms_to_seconds(hms):
  hms = hms.replace('h', ':')
  hms = hms.replace('m', ':')
  hms = hms.replace('s', '')
  h, m, s = hms.split(':')
  return int(h) * 3600 + int(m) * 60 + int(s)

def get_video_info(string):
  url_query = string.split('/')[-1].split('?') 
  result = {}
  result['video_id'] = url_query[0]
  for row in url_query:
    for clip_query in row.split('&'):
      if clip_query.split('=')[0] == 't':
        result['time'] = hms_to_seconds(clip_query.split('=')[1])
  return result

def get_full_link(url):
  driver = create_driver()
  # Get page
  print(url)
  driver.get(url)
  
  elements = driver.find_elements(By.XPATH, '//a[contains(@class, "ScCoreButton")]')
  for element in elements:
    print(element.get_attribute('data-test-selector'))
    if element.get_attribute('data-test-selector') and element.get_attribute('data-test-selector').find('clips-watch-full-button') != -1:
      if result.count(element.get_attribute('href')) == 0:
        result_string = element.get_attribute('href')
        return get_video_info(result_string)
  return None

def get_clip_data(data):
  result = {}
  for row in data:
    split_row = row.split(' ')
    if 'Clip' in split_row:
      result['clip_id'] = split_row[1]
    if 'Published' in split_row:
      result['length'] = int(split_row[split_row.index('Length:') + 1])
      result['views'] = int(split_row[split_row.index('Views:') + 1])
    if 'https' in split_row[0]:
      result['url'] = split_row[0]
  return result

def get_links(streamer, already_crawled):
  stream = os.popen('twitch-dl clips ' + streamer +' --all -P last_month')
  output = stream.read()
  result = []
  for data in output.split('\n\n'):
    escape_ansi_string = escape_ansi(data)
    clip_data = get_clip_data(escape_ansi_string.split('\n'))
    try:
      if 'url' in clip_data and clip_data['clip_id'] not in already_crawled:
        result.append(clip_data)
    except:
      print('get link failed!')
  return result  

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--output_dir', default='/data/data1/twitch',
                      help='directory to save video in')
  parser.add_argument('--streamer', default='zilioner',
                      help='twitch streamer to crawl')

  args = parser.parse_args()
  is_exist = os.path.exists(args.output_dir)
  streamer_output_dir = args.output_dir + '/' + args.streamer
  csv_output_dir = args.output_dir + '/' + args.streamer + '/clips.csv'
  if is_exist == False:
    os.makedirs(args.output_dir)
  is_exist_streamer = os.path.exists(streamer_output_dir)
  if is_exist_streamer == False:
    os.makedirs(streamer_output_dir)
  is_exist_streamer_csv = os.path.exists(csv_output_dir)
  if is_exist_streamer_csv == False:
    write_file = open(csv_output_dir, 'w', encoding='utf-8')
    write_file.close()
      
  read_file = open(csv_output_dir, 'r', encoding='utf-8')
  reader = csv.reader(read_file)
  result = []
  # clip_id / streamer / video_id / start_time(s) / end_time(s) / views
  for read in reader:
    if read[1] == args.streamer:
      result.append(read[0])
  read_file.close()

  links = get_links(args.streamer, result)
  write_file = open(csv_output_dir, 'a', encoding='utf-8')
  writer = csv.writer(write_file)
  for link in links:
    full_link_result = get_full_link(link['url'])
    if full_link_result:
      write_row = [link['clip_id'], args.streamer, full_link_result['video_id'], full_link_result['time'], full_link_result['time'] + link['length'], link['views']]
      writer.writerow(write_row)
      print(write_row)

  write_file.close()
