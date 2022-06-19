import argparse
import csv
import os
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pytube import YouTube


count = 0
heatmap = "M 0 100 C 1 95.8 2 80.8 5 78.8 C 8 76.7 11 87.7 15 89.7 C 19 91.7 21 88.8 25 88.9 C 29 89 31 89.8 35 90 C 39 90.2 41 90 45 90 C 49 90 51 90 55 90 C 59 90 61 90 65 90 C 69 90 71 90.1 75 90 C 79 89.9 81 89.7 85 89.7 C 89 89.7 91 89.9 95 90 C 99 90.1 101 90 105 90 C 109 90 111 91.7 115 90 C 119 88.3 121 81.5 125 81.5 C 129 81.5 131 88.3 135 90 C 139 91.7 141 90 145 90 C 149 90 151 90 155 90 C 159 90 161 90 165 90 C 169 90 171 90 175 90 C 179 90 181 90.5 185 90 C 189 89.5 191 87.6 195 87.6 C 199 87.6 201 89.5 205 90 C 209 90.5 211 90.7 215 90 C 219 89.3 221 87.8 225 86.3 C 229 84.7 231 81.7 235 82.2 C 239 82.8 241 87.5 245 88.9 C 249 90.3 251 89.7 255 89.1 C 259 88.6 261 86.1 265 86.2 C 269 86.2 271 89.1 275 89.2 C 279 89.3 281 87.6 285 86.6 C 289 85.6 291 83.3 295 84 C 299 84.7 301 88.8 305 90 C 309 91.2 311 90 315 90 C 319 90 321 90 325 90 C 329 90 331 90 335 90 C 339 90 341 90 345 90 C 349 90 351 91.9 355 90 C 359 88.1 361 94.1 365 80.3 C 369 66.5 371 29 375 21.2 C 379 13.3 381 30.8 385 41.2 C 389 51.6 391 68.6 395 73 C 399 77.4 401 68.4 405 63.1 C 409 57.7 411 48.7 415 46.2 C 419 43.6 421 46 425 50.2 C 429 54.5 431 62 435 67.6 C 439 73.2 441 74.3 445 78.4 C 449 82.6 451 86.1 455 88.4 C 459 90.7 461 89.7 465 90 C 469 90.3 471 90 475 90 C 479 90 481 91.4 485 90 C 489 88.6 491 84.8 495 83.2 C 499 81.6 501 80.8 505 81.9 C 509 83.1 511 93.6 515 89.1 C 519 84.6 521 77.1 525 59.3 C 529 41.5 531 7.1 535 0 C 539 -7.1 541 9.3 545 23.9 C 549 38.5 551 65.5 555 72.8 C 559 80.2 561 62.6 565 60.7 C 569 58.8 571 59.9 575 63.4 C 579 66.9 581 72.9 585 78.2 C 589 83.5 591 87.6 595 90 C 599 92.4 601 90 605 90 C 609 90 611 90 615 90 C 619 90 621 90 625 90 C 629 90 631 90 635 90 C 639 90 641 90 645 90 C 649 90 651 90 655 90 C 659 90 661 90 665 90 C 669 90 671 90 675 90 C 679 90 681 90 685 90 C 689 90 691 90 695 90 C 699 90 701 90 705 90 C 709 90 711 90 715 90 C 719 90 721 90.3 725 90 C 729 89.7 731 88.3 735 88.3 C 739 88.3 741 89.7 745 90 C 749 90.3 751 90 755 90 C 759 90 761 90 765 90 C 769 90 771 90 775 90 C 779 90 781 90 785 90 C 789 90 791 90 795 90 C 799 90 801 91 805 90 C 809 89 811 84.8 815 84.8 C 819 84.8 821 89 825 90 C 829 91 831 90 835 90 C 839 90 841 90 845 90 C 849 90 851 90.1 855 90 C 859 89.9 861 89.4 865 89.4 C 869 89.4 871 89.9 875 90 C 879 90.1 881 92.9 885 90 C 889 87.1 891 76.4 895 75.3 C 899 74.2 901 81.7 905 84.7 C 909 87.6 911 88.9 915 90 C 919 91.1 921 90 925 90 C 929 90 931 90 935 90 C 939 90 941 90 945 90 C 949 90 951 90 955 90 C 959 90 961 90.1 965 90 C 969 89.9 971 90.8 975 89.3 C 979 87.7 981 82.3 985 82.3 C 989 82.4 992 88.1 995 89.5 C 998 91 999 87.4 1000 89.5 C 1001 91.6 1000 97.9 1000 100"

def create_heatmap(element, output_dir, count):
    heatmap = element.get_attribute('d')
    heatmap_list = heatmap.split(" C ")
    heatmap_list.pop(0)
    resolved_heatmap = []
    x_axis = []
    y_axis = []
    for heatmap in heatmap_list:
      tempData = heatmap.split(' ')
      data = []
      for temp in tempData:
        data = data + temp.split(',')
      resolved_heatmap.append([(float(data[4]) - 5) / 1000, (100 - float(data[5])) / 100])
      x_axis.append((float(data[4]) - 5) / 1000)
      y_axis.append((100 - float(data[5]))/100)
      np.save(output_dir + '/running_man_' + str(count) + '.npy', [x_axis, y_axis])
      count += 1
      return count

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
      elements = driver.find_elements(By.XPATH, './/*[@class="ytp-heat-map-path"]')
      if len(elements) > 0:
        countAfter = create_heatmap(elements[0], output_dir+'/graph', count)
        print(count, countAfter)
        if count == countAfter:
          return count
        yt = YouTube(url)
        stream = yt.streams.filter(res="360p", progressive="True")[0]
        stream.download(output_path=output_dir+'/video', filename="running_man_"+str(count)+'.mp4')
        print('Download Complete!!', url, count)
        return countAfter
      sleep(5)



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--output_dir', default='/media/volume1/running_man',
                      help='directory to save video in')
  args = parser.parse_args()
  read_file = open('./youtube.csv', 'r', encoding='utf-8')
  links = csv.reader(read_file)
  isExist = os.path.exists(args.output_dir)
  if isExist == False:
    os.makedirs(args.output_dir)
    os.makedirs(args.output_dir + '/video')
    os.makedirs(args.output_dir + '/graph')

  count = 0
  for link in links:
    try:
      print(link)
      count = download(link[0], args.output_dir, count)
    except:
      print('Error')

  # plt.plot(x_axis, y_axis)
  # plt.show()
