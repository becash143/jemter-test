"""
These tests are for running against annotationlab ml
"""
import json
import time
import re
import pytest
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    UnexpectedAlertPresentException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

CREATE_PROJECT_BTN_CSS = ".createProjectBtn"
LOGOUT_ENDPOINT = "logout"
ANNOTATIONLAB_URL = "http://annotationlab:8200"
CHROME_PATH = "/usr/local/bin/chromedriver"


def login_as(username: str, password: str, browser: webdriver.Chrome):
    """
    Allows login as a specific user
    """
    browser.get(f"{ANNOTATIONLAB_URL}/{LOGOUT_ENDPOINT}")
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_name("login").click()


@pytest.fixture(scope="session")
def browser():
    mgr = ChromeDriverManager()
    driver = webdriver.Chrome(mgr.install())
    login_as("admin", "admin", driver)
    return driver


@pytest.fixture
def teardown(self):
    return self.browser.close()


def test_view_model(browser: webdriver.Chrome):
    browser.find_element_by_xpath('//*[@id="left-panel"]/i').click()
    log = browser.get_log("browser")
    browser.find_element_by_css_selector(CREATE_PROJECT_BTN_CSS).click()
    assert "setup" in browser.current_url

    browser.find_element_by_name("ProjectName").send_keys("ML_Test_Project")
    browser.find_element_by_xpath(
        '//*[@id="PSampling"]/option[3]'
    ).click()
    browser.find_element_by_name("ProjectDesc").send_keys(
        "ML Backend Test Project"
    )
    browser.find_element_by_name("ProjectInstruction").send_keys(
        "<p><b>ML Backend</b> Test Project</p>"
    )
    browser.find_element_by_css_selector(CREATE_PROJECT_BTN_CSS).click()
    ner_task_xpath = '//a[text()="Text classification"]'
    ner_task = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.XPATH, ner_task_xpath)))
    assert ner_task.text == "Text classification"
    ner_task.click()
    browser.find_element_by_id("proceed").click()
    submit_form = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "submit_form"))
    )
    submit_form.click()
    time.sleep(1)
    browser.get(browser.current_url.replace("import", "model"))
    e = browser.find_element_by_css_selector(
        '.button'
    ).text == "Add Backend"
    print(e)
    assert e == True


def test_check_invalid_ml_url(browser: webdriver.Chrome):
    browser.find_element_by_id("ml_backend_url").send_keys("test")
    browser.find_element_by_css_selector(".button").click()
    time.sleep(1)
    alert = browser.switch_to.alert
    assert "Specified string \"test\" doesn\'t look like URL." in alert.text
    alert.accept()
    browser.find_element_by_id("ml_backend_url").clear()
    browser.find_element_by_id("ml_backend_url").send_keys("http://localhost:8181")
    browser.find_element_by_css_selector(".button").click()
    time.sleep(1)
    alert = browser.switch_to.alert
    assert "ML backend with URL: \"http://localhost:8181\" is not connected." in alert.text
    alert.accept()
    browser.find_element_by_id("ml_backend_url").clear()


def test_training_prediction(browser: webdriver.Chrome):
    browser.find_element_by_id("ml_backend_url").send_keys("http://ml-backend-server:9090")
    browser.find_element_by_css_selector(".button").click()
    time.sleep(1)
    el1 = browser.find_element_by_xpath('//*[@id="right-panel"]/div/div[4]/div[1]/div/div[2]/div').text
    assert el1 == "Connected"
    browser.find_element_by_id("ml_backend_url").send_keys("http://ml-backend-server:9090")
    browser.find_element_by_css_selector(".button").click()
    time.sleep(1)
    el2 = browser.find_element_by_xpath('//*[@id="right-panel"]/div/div[4]/div[2]/div/div[2]/div').text
    assert el2 == "Connected"
    time.sleep(1)
    e1 = browser.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]').text
    assert e1 == 'Start Training'
    e2 = browser.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[3]/div[2]').text
    assert e2 == 'Start Predictions'
    browser.find_element_by_xpath('//*[@id="right-panel"]/div/div[4]/div[2]/div/div[1]/button').click()
    alert = browser.switch_to.alert
    alert.accept()
    browser.find_element_by_xpath('//*[@id="right-panel"]/div/div[4]/div[1]/div/div[1]/button').click()
    alert = browser.switch_to.alert
    alert.accept()

def test_delete_project(browser: webdriver.Chrome):
    browser.get("http://annotationlab:8200/projects")
    project_name = "ML_Test_Project"
    browser.find_element_by_class_name("tag_more_option_block").click()
    row_xpath = f"//*[@id='project_table']/table/tbody/tr[contains(., '{project_name}')]"
    del_xpath = "td[2]/span/ul/li[3][a[text() = 'Delete']]/a"
    browser.find_element_by_xpath(f"{row_xpath}/{del_xpath}").click()
    browser.find_element_by_id("proceedDialog").click()
    time.sleep(1)
    assert (
        project_name
        not in browser.find_element_by_xpath("//*[@id='project_table']").text
    )
