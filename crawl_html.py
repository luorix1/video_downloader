import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def download(args):
    # Setup chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set default download directory
    # prefs = {"download.default_directory" : f"/media/volume1/{'sports_highlights' if args.video_type == 'highlight' else 'sports_full'}"}
    # chrome_options.add_experimental_option("prefs", prefs)

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # # Path to chromedriver
    webdriver_service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options, desired_capabilities=caps)

    # Get page
    driver.get(args.url)

    # click main button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="program-front-end-content-displayVodButtons-button-download"]'))).click()

    # click resolution button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="program-front-end-content-displayVodButtons-self"]/div[2]/div/div/a[3]'))).click()


    # Enter modal
    alert = driver.switch_to.alert
    alert.accept()

    # Type ID and password
    id_box = driver.find_element(by=By.XPATH, value='//*[@id="loginId"]')
    pw_box = driver.find_element(by=By.XPATH, value='//*[@id="loginPw"]')

    id_box.send_keys('luorix')
    pw_box.send_keys('Starcatcher')

    # Find submit button and click
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="loginBtn"]')
    submit_button.click()

    # click main button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="program-front-end-content-displayVodButtons-button-download"]'))).click()

    # click resolution button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="program-front-end-content-displayVodButtons-self"]/div[2]/div/div/a[3]'))).click()

    print("Page title is: ")
    print(driver.title)

    sleep(120)

    #close browser
    driver.quit()


if __name__ == '__main__':
    # Take arguments for downloading
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL of video to download')
    parser.add_argument('--output_dir', default='/Users/jwhwang/Desktop',
                        help='directory to save video in')
    parser.add_argument('--filename', default='default.mp4',
                        help='name of output file')
    parser.add_argument('--video_type', choices=['full', 'highlight'], default='highlight')

    args = parser.parse_args()

    download(args)
