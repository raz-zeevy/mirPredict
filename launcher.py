XPATH = 'xpath'
import os

def launch_chrome(base_url, headless=False, wait_time=15,
                  download_folder=None):
    '''
    launches a chrome window
    :return: (driver,wait)
    '''
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    DRIVER_PATH = r"C:\Users\Raz_Z\Projects\Lab\Lab Projects\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = DRIVER_PATH
    option = webdriver.ChromeOptions()
    if headless:
        option.add_argument('headless')
    if download_folder:
        prefs = {"download.default_directory": download_folder}
        option.add_experimental_option("prefs", prefs)
    # the download Path
    driver = webdriver.Chrome(DRIVER_PATH, options=option)
    driver.get(base_url)
    wait = WebDriverWait(driver, wait_time)
    return driver, wait


def long_wait(wait, selector, by=XPATH):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    while True:
        try:
            if by == XPATH:
                element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                 selector)))
                return element
        except TimeoutException:
            continue

def wait_for_download_path(download_path):
    '''
    waits for a file to be downloaded and returns its path
    :param download_path:
    :return: returns the new file_path
    '''
    while True:
        if not list(os.listdir(download_path)) or os.listdir(
                download_path)[0].endswith('.crdownload'):
            continue
        else:
            return os.path.join(download_path, os.listdir(download_path)[0])