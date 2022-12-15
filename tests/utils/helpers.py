import os
import json
import time
import pytest
import random
import logging
import requests
import platform
import psycopg2
from random import randint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import RemoteConnection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

from annotationlab.utils.keycloak_cookies import get_cookies
from selenium.common.exceptions import TimeoutException
from tests.utils.dummy_tasks import * 

OS_BASE = platform.system()
TAGS_BTN_XPATH = '//button[normalize-space()="Tags"]'
TAGS_DROPDOWN_CSS = ".show > .list-li"
TAGS_DROPDOWN_XPATH = (
    "//*[@id='tasks']/thead/tr/th/div/div[2]/div[1]/div[3]/details/ul"
)
CREATE_PROJECT_BTN_CSS = ".createProjectBtn"
LOGOUT_ENDPOINT = "logout"
ANNOTATIONLAB_URL = "http://annotationlab:8200"
CHROME_PATH = os.environ.get("CHROME_PATH", "/usr/local/bin/chromedriver")
DRIVER_TIMEOUT = 20
LONG_TIMEOUT = 150
SHORT_TIMEOUT = 5

EXPIRED_LICENSE_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE2MzE4NTg1OTMsImlhdCI6MTYyOTI2NjU5MywidW5pcXVlX2lkIjoiZjkzY2RmZmUtZmZlOS0xMWViLWIzZDgtOTYzN2U4ZjM2ZmIxIn0.As3wWRbrvjX260d75Ub6zS2lgMlRX7Dcu6JJAcTJQQgi99nn0wCAVTywbncBqt4IsCr_10GyUd2YmbPJNNqeOpvNQeBloe3EoGIcvVN12W6UU8yKBEP-P_LGxe2AhvrOfiLCOp5m2mEYzeZkckPtvN6Lg5JUMQb3ERMurAvQhS1daHE6v_w8LzLhPtF1JdPUd8tFJXuk_gzEYUxLscYJV7NSbs0hnoehBmTOIB2sQRJwKAk-hIpLR_z9yxBLdkhr7JEFvl26V9sADX0eHaoyFK4lzT7ctx-n8vnz4fX6CKKUlrwJpQrqQNXvd0g-_QtN-7R8Ky_NKlX9QbOZ5yFfIQ'


def get_logger():
    '''
    Configured only for dev purpose
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


logger = get_logger()


class wait_for_the_attribute_value(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(
                driver, self.locator
            ).get_attribute(self.attribute)
            return element_attribute == self.value
        except StaleElementReferenceException:
            return False


def login_as(username: str, password: str, browser):
    """
    Allows login as a specific user
    """
    browser.get(f"{ANNOTATIONLAB_URL}/{LOGOUT_ENDPOINT}")
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.url_contains("keycloak-local")
        )
    except:
        browser.get(f"{ANNOTATIONLAB_URL}/{LOGOUT_ENDPOINT}")
    while len(browser.find_elements_by_id("username")) != 1:
        browser.get(f"{ANNOTATIONLAB_URL}")
        WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )

    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_name("login").click()

    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "right-panel"))
        )
    except:
        browser.refresh()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.url_contains("/projects")
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "right-panel"))
        )
    if "User not found" in browser.find_element_by_id("right-panel").text:
        login_as(username, password, browser)
    if len(browser.find_elements_by_class_name("introjs-skipbutton")) == 1:
        close_tour(browser)


def close_tour(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "introjs-skipbutton"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "exit_guided_tour"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "exit_guided_tour"))
    ).click()
    browser.refresh()


@pytest.fixture(scope="session")
def browser():
    driver = None
    if os.getenv("EXECUTOR") == "remote":
        browser = os.getenv("BROWSER", "chrome")
        if browser == "chrome":
            caps = DesiredCapabilities.CHROME.copy()
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("window-size=1766,914")
            options.add_argument("--incognito")
            options.add_argument("--disable-dev-shm-usage")
        elif os.getenv("BROWSER") == "firefox":
            caps = DesiredCapabilities.FIREFOX.copy()
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("window-size=1766,914")
            options.add_argument("--private")
        caps["loggingPrefs"] = {"browser": "ALL"}

        address = os.getenv("NODE_HUB_ADDRESS", "localhost")
        driver = webdriver.Remote(
            RemoteConnection(
                f"http://{address}:4444/wd/hub", resolve_ip=False
            ),
            desired_capabilities=caps,
            options=options,
        )
        driver.implicitly_wait(5)
    else:
        options = webdriver.ChromeOptions()
        if os.environ.get("HEADLESS_CHROME"):
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)

    driver.maximize_window()
    login_as("admin", "admin", driver)
    yield driver
    driver.stop_client()
    driver.quit()


@pytest.fixture
def teardown(self):
    return self.browser.close()


def is_element_present(browser, how, what):
    try:
        browser.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def create_sample_task(browser, project: str):
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project}/import"
    retry = 1
    while retry < 5:
        try:
            browser.get(import_url)
            sample_task_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "add_sample_task"))
            )
            break
        except Exception:
            retry += 1
    browser.execute_script("arguments[0].click();", sample_task_btn)
    wait_for_task_page_load(browser)


def relation_labeling(browser, project: str):

    browser.get(browser.current_url.replace("setup", "import"))
    task = (
        "["
        "{"
        '"created_at": "2020-05-19 12:15:42",'
        '"created_by": "admin",'
        '"data": {'
        '"text": "To have faith is to trust yourself to the water",'
        '"title": ""'
        "},"
        '"id": 0'
        "}"
        "]"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()


def create_task_with_completion(browser, project: str):
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project}/import")
    completions = [
        {
            "completions": [
                {
                    "created_username": "admin",
                    "created_ago": "2021-09-08T11:44:49.054Z",
                    "lead_time": 11,
                    "result": [
                        {
                            "value": {
                                "start": 38,
                                "end": 47,
                                "text": "gentleman",
                                "labels": ["CARDINAL"],
                            },
                            "id": "rASQDyFNpp",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        },
                        {
                            "value": {
                                "start": 334,
                                "end": 342,
                                "text": "injuries",
                                "labels": ["GPE"],
                            },
                            "id": "Fmdq5gXdj1",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        },
                        {
                            "value": {
                                "start": 289,
                                "end": 297,
                                "text": "injuries",
                                "labels": ["GPE"],
                            },
                            "id": "9YPcaj7y9N",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        },
                    ],
                    "honeypot": False,
                    "id": 1,
                },
                {
                    "created_username": "admin",
                    "created_ago": "2021-09-08T11:45:07.180Z",
                    "lead_time": 15,
                    "result": [
                        {
                            "value": {
                                "start": 145,
                                "end": 152,
                                "text": "someone",
                                "labels": ["QUANTITY"],
                            },
                            "id": "KJc1-8dGK5",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        },
                        {
                            "value": {
                                "start": 382,
                                "end": 390,
                                "text": "adderall",
                                "labels": ["LOC"],
                            },
                            "id": "LfXkuNip-_",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        },
                    ],
                    "honeypot": False,
                    "id": 2,
                },
            ],
            "predictions": [],
            "created_at": "2021-09-08 11:44:49",
            "created_by": "admin",
            "data": {
                "text": "The patient is a pleasant 17-year-old gentleman who was playing basketball today in gym. Two hours prior to presentation, he started to fall and someone stepped on his ankle and kind of twisted his right ankle and he cannot bear weight on it now. It hurts to move or bear weight. No other injuries noted. He does not think he has had injuries to his ankle in the past. He was given adderall and accutane.",
                "title": "",
            },
            "id": 0,
        }
    ]

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(completions))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)


def create_task(browser, project: str):
    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project}/tasks"
    browser.get(task_url)
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "record"))
    )
    tasks_before = len(browser.find_elements(By.CLASS_NAME, "record"))
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project}/import"
    browser.get(import_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "add_sample_task"))
    )
    sample_task_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "add_sample_task"))
    )
    browser.execute_script("arguments[0].click();", sample_task_btn)
    wait_for_task_page_load(browser)
    tasks_after = len(browser.find_elements(By.CLASS_NAME, "record"))
    assert tasks_after - tasks_before == 1


def create_project(browser, project: str, sequential_sampling: bool = None):
    browser.get(ANNOTATIONLAB_URL)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/projects"))
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, "Create Project")
            )
        )
        create_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, "Create Project")
            )
        )
    except:
        browser.get(ANNOTATIONLAB_URL)
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.url_contains("/projects")
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.PARTIAL_LINK_TEXT, "Create Project")
            )
        )
        create_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, "Create Project")
            )
        )

    browser.execute_script("arguments[0].click();", create_btn)
    save_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "save_project"))
    )
    assert "setup" in browser.current_url

    browser.find_element_by_name("ProjectName").send_keys(project)
    browser.find_element_by_name("ProjectDesc").send_keys(
        "Named Entity Recognition Development Project"
    )
    if sequential_sampling:
        browser.find_element_by_xpath('//*[@id="PSampling"]/option[3]').click()
    browser.find_element_by_name("ProjectInstruction").send_keys(
        "<p><b>Named Entity Recognition</b> Development Project</p>"
    )
    browser.execute_script("arguments[0].click();", save_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains(f"{project}/setup")
    )
    browser.get(ANNOTATIONLAB_URL)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains(f"/project"))

    retry = 1
    while retry < 5:
        try:
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "project_tbl"))
            )
            table = (
                WebDriverWait(browser, DRIVER_TIMEOUT)
                .until(
                    EC.visibility_of_element_located((By.ID, f"tr_{project}"))
                )
                .text
            )
            break
        except Exception:
            browser.get(ANNOTATIONLAB_URL)
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.url_contains(f"/project")
            )
            retry += 1

    assert project in table


def create_project_with_task(browser, project: str):
    create_project(browser, project)
    create_sample_task(browser, project)
    create_task(browser, project)


def create_default_project(browser, project: str):
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    if "projects" not in browser.current_url:
        login_as("admin", "admin", browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Create Project")
        )
    ).click()
    assert "setup" in browser.current_url

    browser.find_element_by_name("ProjectName").send_keys(project)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "ProjectDesc"))
    ).send_keys("Named Entity Recognition Development Project")

    browser.find_element_by_name("ProjectInstruction").send_keys(
        "<p><b>Named Entity Recognition</b> Development Project</p>"
    )

    create_button_class = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, CREATE_PROJECT_BTN_CSS)
        )
    )
    browser.execute_script("arguments[0].click();", create_button_class)
    submit_form = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    browser.execute_script("arguments[0].click();", submit_form)


def create_tag(browser, project: str):
    create_project_with_task(browser, project)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "chk-1"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_tags"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "assign_tags"))
    ).click()
    assign_tags = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_tags"))
    )
    WebDriverWait(assign_tags, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary"))
    )
    WebDriverWait(assign_tags, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_name"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_name"))
    ).send_keys("Test Tag")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "generate_color_icon"))
    )
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_id("btn_update_group").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, "TagModal"))
    )
    labels = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "label-tag"))
    )
    assert "Test Tag" in labels.text


def create_tag_assign_to_all_tasks(browser, project: str):
    create_project_with_task(browser, project)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
    ).click()
    assign_tags = browser.find_element_by_class_name("assign_tags")
    assign_tags.click()
    WebDriverWait(assign_tags, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
    ).click()

    txt_tagname = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_name"))
    )
    txt_tagname.send_keys("Test Tag")
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_id("btn_update_group").click()
    labels = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "label-tag"))
    )
    assert "Test Tag" in labels.text


def edit_heading_clicker(browser):
    heading = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "edit_title"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "edit_title"))
    )
    browser.execute_script("arguments[0].click();", heading)


def update_title(browser, title):
    edit_heading_clicker(browser)
    edit_textbox = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "edit_textbox"))
    )
    actions = ActionChains(browser)
    actions.move_to_element(edit_textbox)
    actions.click()
    if OS_BASE == "Darwin":
        actions.key_down(Keys.COMMAND).send_keys("a").key_up(
            Keys.COMMAND
        ).send_keys(title).send_keys(Keys.ENTER).perform()
    else:
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).send_keys(title).send_keys(Keys.ENTER).perform()


def add_task_title(browser, project: str):
    create_project_with_task(browser, project)
    title = "New task title"
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                "Tasks",
            )
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.PARTIAL_LINK_TEXT,
                "Task 1",
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "ls-skip-btn",
            )
        )
    )
    update_title(browser, title)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                "Tasks",
            )
        )
    ).click()
    task_1 = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    assert title in task_1.text


def import_completion_task(browser, project: str, task: dict):

    create_project(browser, project)
    project_element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, project))
    )
    browser.execute_script("arguments[0].click();", project_element)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/import"))
    data = json.dumps(task)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/import"))
    data = json.dumps(task)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(data)
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@value='inprogress']")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@value='inprogress']"))
    )
    browser.find_element_by_xpath("//button[@value='inprogress']").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "tr"))
    )
    assert (
        "Nothing to display"
        not in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="tasks"]/tbody/tr')
            )
        )
        .text
    )


def delete_project(browser, project_name: str):
    retry = 1
    while retry < 5:
        try:
            browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup")
            delete_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "delete_btn"))
            )
            browser.execute_script("arguments[0].click();", delete_btn)
            break
        except Exception:
            browser.refresh()
            retry += 1

    proceed_confirm_element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "deleteProjectSuccessBtn"))
    )
    browser.execute_script("arguments[0].click();", proceed_confirm_element)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("/#/projects")
    )
    browser.get(ANNOTATIONLAB_URL)
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.url_contains("/#/projects")
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "tr"))
        )
        project_table = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "project_table"))
        )
    except:
        browser.refresh()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "tr"))
        )
        project_table = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "project_table"))
        )
    assert project_name not in project_table.text


def create_user(browser, username: str):
    login_as("admin", "admin", browser)
    profile_icon = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user_profile_icon"))
    )
    browser.execute_script("arguments[0].click();", profile_icon)
    manage_users = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Manage users"))
    )
    browser.execute_script("arguments[0].click();", manage_users)
    add_user_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Add User"))
    )
    assert browser.current_url.endswith("/users")
    add_user_btn.click()
    save_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "save_details"))
    )
    assert browser.current_url.endswith("/user")

    browser.find_element_by_id("txt_username").send_keys(username)
    browser.find_element_by_id("txt_first_name").send_keys("New")
    browser.find_element_by_id("txt_last_name").send_keys("User")
    save_btn.click()
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Groups"))
        )
    except:
        browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("user"))
    assert (
        username
        in browser.find_element_by_xpath(
            '//*[@id="right-panel"]/div[1]/div/div[1]/span'
        ).text
    )


def delete_user(browser, username: str):
    browser.get(f"{ANNOTATIONLAB_URL}/#/users")
    browser.find_element_by_id("txt_search_user").send_keys(username)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, "admin"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, username))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_delete_user"))
    ).click()
    # browser.switch_to.active_element
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    ).click()

    delete_user = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "share_delete_user"))
    )
    browser.execute_script("arguments[0].click();", delete_user)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    assert username not in browser.find_element_by_class_name("table").text


def assign_task_to_reviewer(browser, username, task_id):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"chk-{task_id}"))
    )
    task_chk_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, f"chk-{task_id}"))
    )
    browser.execute_script("arguments[0].click();", task_chk_box)
    if not task_chk_box.get_attribute("checked"):
        browser.execute_script("arguments[0].click();", task_chk_box)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, '//button[contains(@value,"inprogress")]')
        )
    )
    assign_reviewer = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_reviewer"))
    )
    browser.execute_script("arguments[0].click();", assign_reviewer)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//details[@class='assign_reviewer']"
                "//label[contains(@class, 'dropdown_item')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", dropdown)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    browser.refresh()
    wait_for_task_page_load(browser)
    assert (
        " Reviewers:"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="tasks"]/tbody')
            )
        )
        .text
    )


def assign_task_to_user(browser, username, task_id):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "tr"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, f"Task {task_id}")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"chk-{task_id}"))
    )
    checkbox = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.element_to_be_clickable((By.ID, f"chk-{task_id}")))
        .click()
    )
    if (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.element_to_be_clickable((By.ID, f"chk-{task_id}")))
        .get_attribute("checked")
        != "true"
    ):
        checkbox = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, f"chk-{task_id}"))
        )
        browser.execute_script("arguments[0].click();", checkbox)
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
        )
        assign_assignee = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "assign_assignee")
            )
        )
    except:
        checkbox = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, f"chk-{task_id}"))
        )
        if checkbox.get_attribute("checked") != "true":
            browser.execute_script("arguments[0].click();", checkbox)
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
        )
        assign_assignee = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "assign_assignee")
            )
        )
    browser.execute_script("arguments[0].click();", assign_assignee)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//details[@class='assign_assignee']"
                "//label[contains(@class, 'dropdown_item')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", dropdown)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "tr"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, f"Task {task_id}")
        )
    )
    assert (
        f"Assigned to {username}"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "tasks")))
        .text
    )


def add_to_team(browser, members_info):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )
    for user, scopes in members_info.items():
        username_field = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "txtuser"))
        )
        actions = ActionChains(browser)
        actions.move_to_element(username_field)
        actions.click()
        if OS_BASE == "Darwin":
            actions.key_down(Keys.COMMAND).send_keys("a").key_up(
                Keys.COMMAND
            ).send_keys(user).send_keys(Keys.ENTER).perform()
        else:
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(
                Keys.CONTROL
            ).send_keys(user).send_keys(Keys.ENTER).perform()
        username_list = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "username_list"))
        )
        WebDriverWait(username_list, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "span"))
        )
        for scope in scopes:
            chk_scope = browser.find_element_by_xpath(
                f"//input[@value = '{scope}']"
            )
            browser.execute_script("arguments[0].click();", chk_scope)

        share_project = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
        )
        browser.execute_script("arguments[0].click();", share_project)
        try:
            username_list = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "username_list"))
            )
            WebDriverWait(username_list, DRIVER_TIMEOUT).until(
                EC.invisibility_of_element_located((By.TAG_NAME, "span"))
            )
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "scope_tag"))
            )
        except:
            browser.refresh()
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "txtuser"))
            )
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "scope_tag"))
            )


def remove_from_team(browser, user):
    current_team = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "scope_tag"))
    )
    remove_member = False
    for member in current_team:
        if user in member.text:
            delete_button = member.find_element_by_tag_name("button")
            browser.execute_script("arguments[0].click();", delete_button)
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.ID, "revokeMemeberFromTeamModalBody")
                )
            )
            assert (
                'Are you sure you want to revoke "{0}" from this project?'.format(
                    user
                )
                in browser.find_element_by_id(
                    "revokeMemeberFromTeamModalBody"
                ).text
            )
            browser.find_element_by_id(
                "revokeMemeberFromTeamSuccessBtn"
            ).click()
            remove_member = True
            break
    assert remove_member
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Project Team"))
    ).click()


def validate_config_content(browser, project_name, config_content):
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectConfiguration"
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "lsPreviewSuccess")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("/setup#projectConfiguration")
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "4. Configuration")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "4. Configuration"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT * 2).until(
        EC.visibility_of_element_located((By.ID, "editor-wrap"))
    )
    div = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'CodeMirror-code')]"))
    )
    browser.execute_script("arguments[0].scrollIntoView();", div)
    actions = ActionChains(browser)
    actions.move_to_element(div)
    actions.click()
    time.sleep(2)
    if OS_BASE == "Darwin":
        actions.key_down(Keys.COMMAND).send_keys("a").key_up(
            Keys.COMMAND
        ).send_keys(config_content).perform()
    else:
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).send_keys(config_content).perform()


def delete_embeddings(embedding_name):
    CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    query = (
        f"select * from embeddings where embedding_name='{embedding_name}';"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    query = f"delete from embeddings where embedding_name='{embedding_name}';"
    cursor.execute(query)
    connection.commit()
    return result


def restore_deleted_embeddings(deleted_embeddings):
    CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    query = f"""
        insert into embeddings values(
        {deleted_embeddings[0]},
        '{deleted_embeddings[1]}',
        '{deleted_embeddings[2]}',
        '{datetime.now()}',
        '',
        'downloaded');
    """
    cursor.execute(query)
    connection.commit()
    connection.close()


def upload_expired_license():
    CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    query = f"""
        insert into jsl_license
        (license_key,license_type,uploaded_by)
        values (
        '{EXPIRED_LICENSE_KEY}',
        'Spark NLP for Healthcare',
        'admin'
        );
    """
    cursor.execute(query)
    connection.commit()
    connection.close()


def delete_existing_license():
    CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    query = f"""delete from jsl_license;"""
    cursor.execute(query)
    connection.commit()
    connection.close()


def create_dummy_active_server(license_id):
    CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    query = f"""
        insert into active_servers (nlp_license_used)
        values ('{license_id}')
        RETURNING id;
    """
    cursor.execute(query)
    created_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return created_id


def delete_dummy_active_server(license_id):
    CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()
    query = f"""
        delete from active_servers
        where nlp_license_used='{license_id}'
        ;
    """
    cursor.execute(query)
    connection.commit()
    connection.close()



def wait_for_task_page_load(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/tasks"))
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "tasks"))
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "tr"))
        )
    except:
        browser.refresh()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "tasks"))
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "tr"))
        )


def wait_for_import_page_load(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/import"))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "overwrite"))
    )


def wait_for_labeling_page_load(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/labeling"))
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
        )
    except:
        browser.refresh()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
        )


def wait_for_modelshub_page_load(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/models"))
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "card"))
        )
    except:
        browser.refresh()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "card"))
        )


def wait_for_projects_page_load(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/projects"))
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "project_table"))
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "tr"))
        )
    except:
        browser.refresh()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "project_table"))
        )
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.TAG_NAME, "tr"))
        )

def set_view_as(browser, permission):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownViewasFilter"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "dropdownViewasFilter"))
    ).click()
    drop_down = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownViewasFilterBody"))
    )
    assert permission in drop_down.text
    WebDriverWait(drop_down, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[@value='{permission}']"))
    ).click()
    permission_li = WebDriverWait(drop_down, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[@value='{permission}']"))
    )
    WebDriverWait(permission_li, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "fa-check"))
    )


def unique_project_name(name=""):
    return (
        name + "-" + str(randint(1, 1000)) if name else str(randint(1, 1000))
    )


def is_model_server_up():
    """
    Check if model server is up.
    """
    cookies = get_cookies()
    import_url = f"{ANNOTATIONLAB_URL}/api/mt/deployment_info"
    headers = {
        "Host": ANNOTATIONLAB_URL.replace("http://", ""),
        "Origin": ANNOTATIONLAB_URL,
        "Content-Type": "application/json",
    }
    r = requests.get(import_url, headers=headers, cookies=cookies)
    response_json = r.json()
    if r.status_code == 200 and response_json["deployment_info"] != {}:
        return True
    return False


def wait_for_model_server():
    count = 0
    MAX_TIME = 3 * 60  # 3 MINUTES
    while not is_model_server_up() and count <= MAX_TIME:
        time.sleep(5)
        count += 5

    # confirms model server is turned on
    assert count != MAX_TIME


def select_relation_among_entities_config(browser, project_name):
    configuration_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectConfiguration"
    browser.get(configuration_url)

    accordion_xpath = "//button[contains(@class,'accordion') and span[span[contains(text(), 'Other sources')]]]"

    accordion = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, accordion_xpath))
    )

    browser.execute_script("arguments[0].click();", accordion)
    config_element_xpath = (
        "//span[contains(text(), 'Relations among entities')]"
    )
    config_element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, config_element_xpath))
    )
    browser.execute_script("arguments[0].click();", config_element)

    # click yes on dialog box
    dialogue_box_yes_xpath = "//div[@id='confirm_config_template_replace_dialog']//div[text()='Yes']"
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, dialogue_box_yes_xpath))
    ).click()

    save_button_xpath = "//button[@id='submit_form']"
    save_button_element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, save_button_xpath))
    )
    save_button_element.click()


def delete_model_embeddings(browser, model_name, _type):
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    wait_for_modelshub_page_load(browser)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.PARTIAL_LINK_TEXT,
                "Available Models"
                if _type == "model"
                else "Available Embeddings",
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "card"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_input_search_models"))
    ).send_keys(model_name)
    id_prefix = "available_model_" if _type == "model" else "embedding="

    model_card_id = f"{id_prefix}{model_name}"
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, model_card_id))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//div[contains(@id, '{model_card_id}')]"
                "//div[contains(@class, 'tag_more_option_block')]"
            )
        )
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//div[contains(text(), "Delete")]')
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn-delete-group"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, model_card_id))
    )


def rename_trained_model(browser, model_name, new_name):
    browser.get(f"{ANNOTATIONLAB_URL}/models?s=available_models")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_input_search_models"))
    ).send_keys(model_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains(model_name))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//b[contains(text(), "{model_name}" )]')
        )
    )
    rename_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//li[@data-value='{model_name}' and contains(text(), 'Rename')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", rename_btn)
    text_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "txt_update_model_name"))
    )
    actions = ActionChains(browser)
    actions.move_to_element(text_box)
    actions.click()
    if OS_BASE == "Darwin":
        actions.key_down(Keys.COMMAND).send_keys("a").key_up(
            Keys.COMMAND
        ).send_keys(new_name).perform()
    else:
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).send_keys(new_name).perform()
    actions.key_down(Keys.ENTER).perform()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, f"txt_{model_name}"))
    )
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_input_search_models"))
    ).clear()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_input_search_models"))
    ).send_keys(new_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//b[contains(text(), "{new_name}" )]')
        )
    )


def wait_for_element_by_xpath(browser, xpath, refresh=False, num_of_iters=5):
    '''
    Waits until element is found
    If element not found, throws assertion error
    '''

    count = 0
    while count < num_of_iters:
        try:
            # wait until task has been created
            WebDriverWait(
                browser, DRIVER_TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            break
        except TimeoutException:
            count += 1
            if refresh:
                browser.refresh()

    element = browser.find_elements_by_xpath(xpath)
    assert len(element) > 0
    return element[0]
