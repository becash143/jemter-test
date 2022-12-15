"""
These tests are for running against annotationlab frontend
"""
import time
import docker
import pytest
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException
)
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


LOGOUT_ENDPOINT = "logout"
ANNOTATIONLAB_URL = "http://annotationlab:8200"
CHROME_PATH = "/usr/local/bin/chromedriver"
CLIENT = docker.from_env()
KEYCLOAK_IMAGE = "jboss/keycloak:16.1.1" # CHANGE THIS WHEN KEYCLOAK IS UPDATED TO NEW VERSION
ANNOTATIONLAB_DATABASE_IMAGE = "postgres:13.0-alpine"


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
    driver = webdriver.Chrome(ChromeDriverManager().install())
    login_as("admin", "admin", driver)
    return driver


@pytest.fixture
def teardown(self):
    return self.browser.close()


def is_element_present(browser, how, what):
    try:
        browser.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def test_keycloak_status(browser: webdriver.Chrome):
    for container in CLIENT.containers.list():
        container_info = CLIENT.containers.get(container.id)
        if container_info.attrs['Config']['Image'] == KEYCLOAK_IMAGE and container_info.attrs['Config']['Cmd']:
            container_info.stop()
            browser.refresh()
            assert browser.find_element(By.CSS_SELECTOR, '.container')
            container_info.start()
            time.sleep(5)
            browser.refresh()
            assert is_element_present(browser, By.CSS_SELECTOR, '.login-pf-page')


def test_datalabs_database_status(browser: webdriver.Chrome):
    browser.find_element_by_id("username").send_keys("admin")
    browser.find_element_by_id("password").send_keys("admin")
    browser.find_element_by_name("login").click()
    for container in CLIENT.containers.list():
        container_info = CLIENT.containers.get(container.id)
        if container_info.attrs['Config']['Image'] == ANNOTATIONLAB_DATABASE_IMAGE:
            container_info.stop()
            browser.refresh()
            assert browser.find_element(By.CSS_SELECTOR, '.container')
            container_info.start()
            time.sleep(3)
            browser.refresh()
            assert is_element_present(browser, By.CSS_SELECTOR,
                                      '.left-panel')
