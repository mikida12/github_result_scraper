from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementNotVisibleException, ElementNotSelectableException, \
    NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import functools
import time
import re
import github_wrapper
from time import sleep


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} with '{args[1]}' in {run_time:.4f} secs")
        return value
    return wrapper_timer


def extract_data(result_webelement):
    title = result_webelement.find_element_by_xpath(".//h3/a").text
    link = result_webelement.find_element_by_xpath(".//h3/a").get_attribute("href")
    try:
        description = result_webelement.find_element_by_xpath(".//p").text
        description = re.sub('[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', description)
    except NoSuchElementException as e:
        description = ""
    try:
        tags = result_webelement.find_element_by_xpath(".//div[@class='topics-row-container col-12 col-md-9 d-inline-flex flex-wrap flex-items-center f6 my-1']").text.split("\n")
    except NoSuchElementException as e:
        tags = []
    datetime = result_webelement.find_element_by_xpath(".//div[@class='d-flex flex-wrap']//relative-time").get_attribute("datetime")
    language = result_webelement.find_element_by_xpath(".//div[@class='flex-shrink-0 col-6 col-md-4 pt-2 pr-md-3 d-flex']//div[@class='text-gray flex-auto min-width-0']").text
    starts = result_webelement.find_element_by_xpath(".//div[@class='flex-shrink-0 col-6 col-md-4 pt-2 pr-md-3 d-flex']//a[@class='muted-link']").text
    res_obj = github_wrapper.ResultObject(title, link, description, tags, datetime, language, starts)
    return res_obj


class WebDriverObject:
    def __init__(self, browser):
        if browser == "firefox":
            caps = DesiredCapabilities.FIREFOX.copy()
            caps['marionette'] = True
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            try:
                self.driver = webdriver.Firefox(capabilities=caps, firefox_options=options)
                self.driver.maximize_window()
            except Exception as e:
                raise Exception("unable to initiate webdriver for {} - {}".format(browser, e))
    @timer
    def navigate_to_url(self, url):
        try:
            self.driver.get(url)
        except WebDriverException as e:
            print("error navigating to url '{}' - {}".format(url, e))

    def wait_for(self, element, delay=30):
        WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, element)))

    def find_element_by(self, element, element_type):
        try:
            return self.driver.find_element(element_type, element)
        except (ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException, StaleElementReferenceException) as e:
            print("unable to find element - {}".format(e))

    def click_on(self, element, element_type="xpath"):
        try:
            elem = self.find_element_by(element, element_type)
            elem.click()
        except (ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException, StaleElementReferenceException) as e:
            print("unable to click on element - {}".format(e))

    def type(self, element, element_type, string, clear_field_before=True):
        try:
            elem = self.find_element_by(element, element_type)
            elem.clear() if clear_field_before else None
            elem.send_keys(string)
        except (ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException, StaleElementReferenceException) as e:
            print("unable to find element - {}".format(e))

    @timer
    def press_key(self, key):
        key_selected = {"enter": Keys.ENTER, "space": Keys.SPACE, "escape": Keys.ESCAPE, "tab": Keys.TAB}.get(key)
        if key_selected is not None:
            ActionChains(self.driver).send_keys(key_selected).perform()

    def get_element_attribute(self, element, element_type, attribute):
        try:
            elem = self.find_element_by(element, element_type)
            elem.get_attribute(attribute)
        except (ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException, StaleElementReferenceException) as e:
            print("unable to get element attribute - {}".format(e))

    def wait_for_page_load(self, num_of_attempts=10):
        page_state = False
        tries = 0
        while page_state != "complete" and tries < num_of_attempts:
            page_state = self.driver.execute_script("return document.readyState")
            sleep(1)
            tries += 1

    def close_browser(self):
        self.driver.quit()