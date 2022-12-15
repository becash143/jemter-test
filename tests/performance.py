import json
import requests
import pytest
from annotationlab.utils.keycloak_cookies import get_cookies
import logging
import time
from selenium import webdriver

logger = logging.getLogger(__name__)
cookies = get_cookies()
API_URL = 'http://annotationlab:8200'
headers = {
    'Host': API_URL.replace('http://', ''),
    'Origin': API_URL,
    'Content-Type': 'application/json'
}
PROJECT_NAMES = []


LOGOUT_ENDPOINT = "logout"
ANNOTATIONLAB_URL = "http://annotationlab:8200"
CHROME_PATH = "/usr/local/bin/chromedriver"

headers = {
    'Host': ANNOTATIONLAB_URL.replace('http://', ''),
    'Origin': ANNOTATIONLAB_URL,
    'Content-Type': 'application/json'
}
cookies = get_cookies()
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
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)
    login_as("admin", "admin", driver)
    return driver


@pytest.fixture
def teardown(self):
    return self.browser.close()


@pytest.fixture(scope='session')
def project_ids():
    yield range(1, 1002)


def test_create_project(project_ids):
    """
    Create 1000 projects,
    Verified not to create 1001th project
    """
    url = f'{API_URL}/api/projects/create'
    for project_id in project_ids:
        name = f"PerformanceProject{project_id}"
        data = {
            "project_name": name,
            "project_description": f"Desciption for PerformanceProject{project_id}",
            "project_sampling": "uniform",
            "project_instruction": ""
        }
        logger.info(f'Creating project: {name}')
        r = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            cookies=cookies
        )
        if project_id <= 1000:
            assert r.status_code == 201
            response = r.json()
            PROJECT_NAMES.append(response.get("project_name"))
        else:
            assert r.status_code == 406


def test_project_filter(browser: webdriver.Chrome):
    """
    Test case:
    - The project to display on per page (50, 100, All),
    - Filter the project using search term
    """
    project_per_page = '//*[@id="project_tbl"]/thead/tr/th/div/div[2]/div[2]/details/summary'
    assert (len(browser.find_elements_by_class_name("task-heading")) == 50)
    browser.find_element_by_xpath(project_per_page).click()
    browser.find_element_by_xpath(
        '//*[@id="project_tbl"]/thead/tr/th/div/div[2]/div[2]/details/ul/li[2]'
    ).click()
    assert (len(browser.find_elements_by_class_name("task-heading")) == 100)
    browser.find_element_by_xpath(project_per_page).click()
    browser.find_element_by_xpath(
        '//*[@id="project_tbl"]/thead/tr/th/div/div[2]/div[2]/details/ul/li[3]'
    ).click()
    assert (len(browser.find_elements_by_class_name("task-heading")) == 1000)

    browser.find_element_by_id("txt_search_project").send_keys("PerformanceProject999")
    time.sleep(2)
    assert (len(browser.find_elements_by_class_name("task-heading")) == 1)
    delete_project()


def delete_project():
    """
    Delete the created projects
    """
    for project_name in PROJECT_NAMES:
        logger.info(f'Deleting project name: {project_name}')
        delete_url = f'{API_URL}/api/projects/{project_name}/delete'
        requests.delete(
            delete_url,
            headers=headers,
            cookies=cookies
        )
