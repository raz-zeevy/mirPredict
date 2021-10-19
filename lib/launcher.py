import os

# Constants
XPATH = 'xpath'
DEFAULT_WAIT = 15

def launch_chrome(base_url, headless=False, wait_time=DEFAULT_WAIT,
                  download_folder=None):
    '''
    launches a chrome window
    :return: (driver,wait)
    '''
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    # OLD NEWS
    # DRIVER_PATH = CHROME_PATH
    # os.environ["webdriver.chrome.driver"] = DRIVER_PATH
    option = webdriver.ChromeOptions()
    if headless:
        option.add_argument('headless')
    if download_folder:
        # the download Path
        prefs = {"download.default_directory": download_folder}
        option.add_experimental_option("prefs", prefs)
    #log_level=0 is to silence the logs
    try:
        driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=option)
        driver.get(base_url)
        wait = WebDriverWait(driver, wait_time)
    except:
        raise Exception('ConnectionError')
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
        try:
            if not list(os.listdir(download_path)) or os.listdir(
                    download_path)[0].endswith('.crdownload') or os.listdir(
                download_path)[0].endswith('.tmp'):
                continue
            else:
                return os.path.join(download_path,
                                    os.listdir(download_path)[0])
        except IndexError as e:
            print(list(os.listdir(download_path)))
            raise e


if __name__ == '__main__':
    driver, wait = launch_chrome('https://google.com')
