"""
Tests for labelling related stuffs
"""
import json
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from tests.utils.helpers import *


def test_missing_label_validation(browser):
    project_name = unique_project_name("test_missing_label")
    create_project(browser, project_name)
    project_label = browser.find_element_by_partial_link_text(project_name)
    browser.execute_script("arguments[0].click();", project_label)
    prediction = [
        {
            "predictions": [
                {
                    "created_username": "admin",
                    "created_ago": "2020-11-24T04:55:51.276Z",
                    "lead_time": 7.026,
                    "result": [
                        {
                            "value": {
                                "start": 8,
                                "end": 13,
                                "text": "faith",
                                "labels": ["CARDINAL_duplicate"],
                            },
                            "id": "hfhsY870H5",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        }
                    ],
                    "honeypot": "false",
                    "id": 1,
                }
            ],
            "created_at": "2020-11-24 04:55:17",
            "created_by": "admin",
            "data": {
                "text": "To have faith is to trust yourself to the water",
                "title": "",
            },
            "id": 0,
        }
    ]
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")
    wait_for_import_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(prediction))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-button"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "upload-dialog-msg"))
    )
    assert (
        "Error: can't upload/process file on server side. Reasons:"
        in browser.find_element_by_id("upload-dialog-msg").text
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "upload-done-button"))
    ).click()
    completions = [
        {
            "completions": [
                {
                    "created_username": "admin",
                    "created_ago": "2020-11-24T04:55:51.276Z",
                    "lead_time": 7.026,
                    "result": [
                        {
                            "value": {
                                "start": 8,
                                "end": 13,
                                "text": "faith",
                                "labels": ["CARDINAL_duplicate"],
                            },
                            "id": "hfhsY870H5",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        }
                    ],
                    "honeypot": "false",
                    "id": 1,
                }
            ],
            "predictions": [],
            "created_at": "2020-11-24 04:55:17",
            "created_by": "admin",
            "data": {
                "text": "To have faith is to trust yourself to the water",
                "title": "",
            },
            "id": 0,
        }
    ]
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "url-input"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(completions))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-button"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "upload-dialog-msg"))
    )
    assert (
        "Error: can't upload/process file on server side. Reasons:"
        in browser.find_element_by_id("upload-dialog-msg").text
    )
    delete_project(browser, project_name)


def test_space_labeling(browser):
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    project_name = unique_project_name("test_space_labeling")
    create_project(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "test_space_labeling")
        )
    ).click()
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")
    wait_for_import_page_load(browser)
    task = [
        {
            "created_at": "2020-05-19 12:15:42",
            "created_by": "admin",
            "data": {
                "text": "To have faith is to trust yourself to the water",
                "title": "",
            },
            "id": 0,
        }
    ]
    WebDriverWait(browser, LONG_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "url-input"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-button"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "upload-dialog-msg"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    task_url = browser.current_url
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    )
    browser.find_element_by_xpath("//span[text()='CARDINAL']").click()
    browser.maximize_window()
    content = browser.find_element_by_class_name("htx-text")
    content_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element(content).move_by_offset(
        10, 56
    ).double_click().perform()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-menu"))
    )
    assert (
        "Nothing selected"
        in browser.find_element_by_class_name("ls-menu").text
    )
    browser.get(task_url)
    delete_project(browser, project_name)


def test_double_labeling(browser):
    project_name = unique_project_name("test_double_labelling")
    create_project_with_task(browser, project_name)
    browser.find_element_by_partial_link_text("Task 1").click()  # Task 1 click
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='CARDINAL']"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    )
    browser.find_element_by_xpath("//span[text()='CARDINAL']").click()
    content = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-text"))
    )
    content1_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 70, (content1_size["height"] / 2)
    ).double_click().perform()  # select text
    element1 = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='LOC']"))
    )
    browser.find_element_by_xpath("//span[text()='LOC']").click()
    content2 = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-text"))
    )
    content2_size = content2.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content2, 70, (content2_size["height"] / 2)
    ).double_click().perform()  # select text

    element2 = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    )
    css_selector_element = browser.find_element_by_css_selector(
        ".ant-btn.ls-submit-btn.ant-btn-primary"
    )
    browser.execute_script("arguments[0].click();", css_selector_element)
    assert element1 == element2
    delete_project(browser, project_name)


def test_relation_labeling(browser):
    project_name = unique_project_name("test_relation_labeling")
    create_project_with_task(browser, project_name)
    browser.find_element_by_partial_link_text("test_relation_labeling").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='CARDINAL']"))
    )
    browser.find_element_by_xpath("//span[text()='CARDINAL']").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    )
    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 70, (content1_size["height"] / 2)
    ).double_click().perform()  # select text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='LOC']"))
    )
    browser.find_element_by_xpath("//span[text()='LOC']").click()
    content = browser.find_element_by_class_name("htx-text")
    content2_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 10, (content2_size["height"] / 2)
    ).double_click().perform()  # select text

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    ).click()
    try:
        WebDriverWait(browser, 3).until(
            EC.visibility_of_any_elements_located(
                (By.CLASS_NAME, "ls-entity-buttons")
            )
        )
    except:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
        ).click()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_any_elements_located(
                (By.CLASS_NAME, "ls-entity-buttons")
            )
        )
    button = browser.find_element_by_class_name("ls-entity-buttons")
    WebDriverWait(button, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "Button"))
    )
    button.find_element_by_tag_name("Button").click()
    browser.find_element_by_class_name("htx-highlight").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-submit-btn"))
    )
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_all_elements_located(
            (
                By.CLASS_NAME,
                'ant-divider-inner-text',
            )
        )
    )
    assert (
        "1"
        in browser.find_elements_by_class_name(
            "ant-divider-inner-text"
        )[1].text
    )
    delete_project(browser, project_name)


def test_label_double_click(browser):
    project_name = unique_project_name("test_label_double_click")
    create_project_with_task(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "test_label_double_click")
        )
    )
    project_label = browser.find_element_by_partial_link_text(
        "test_label_double_click"
    )
    browser.execute_script("arguments[0].click();", project_label)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    browser.find_element_by_partial_link_text("Task 1").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='CARDINAL']"))
    )
    browser.find_element_by_xpath("//span[text()='CARDINAL']").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    )
    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 70, (content1_size["height"] / 2)
    ).double_click().perform()  # select text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    )
    label = browser.find_element_by_class_name("htx-highlight")
    action_chains.move_to_element(label).double_click().perform()
    assert 1 == len(browser.find_elements_by_class_name("htx-highlight"))
    delete_project(browser, project_name)


def test_multiple_label_text(browser):
    project_name = unique_project_name("test_multiple_label_text")
    create_project_with_task(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "test_multiple_label_text")
        )
    )
    test_multiple_label_link = browser.find_element_by_partial_link_text(
        "test_multiple_label_text"
    )
    browser.execute_script("arguments[0].click();", test_multiple_label_link)
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    browser.find_element_by_partial_link_text("Task 1").click()
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='CARDINAL']"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    )
    browser.find_element_by_xpath("//span[text()='CARDINAL']").click()
    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 70, (content1_size["height"] / 2)
    ).double_click().perform()  # select text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='LOC']"))
    )
    browser.find_element_by_xpath("//span[text()='LOC']").click()
    browser.execute_script("document.getSelection().removeAllRanges();")
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 0, (content1_size["height"] / 1.3)
    ).click_and_hold().perform()
    action_chains.move_to_element_with_offset(
        content, content1_size["width"] / 1.2, (content1_size["height"] / 1.3)
    ).release().click().perform()
    action_chains.click().perform()
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    box_list = browser.find_elements_by_class_name("ant-divider-inner-text")
    for element in box_list:
        if "Regions" in element.text:
            assert "2" in element.text
            break
    delete_project(browser, project_name)


def test_consistent_labeling_for_repeated_token(browser):
    project_name = unique_project_name("test_consistent_labeling_for_repeated_token")
    create_project_with_task(
        browser, project_name
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.PARTIAL_LINK_TEXT,
                "test_consistent_labeling_for_repeated_token",
            )
        )
    ).click()
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    )
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "anticon-setting"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Label all occurrences of selected text']")
        )
    )
    chk_label_all = browser.find_element_by_xpath(
        "//input[@value='Label all occurrences of selected text']"
    )
    if chk_label_all.get_attribute("checked") != "true":
        chk_label_all.click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    ).click()
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='CARDINAL']"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    ).click()

    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    browser.maximize_window()
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 5, 5
    ).double_click().perform()  # select text
    hightlighted_elem = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )
    assert len(hightlighted_elem) == 3
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='EVENT']"))
    ).click()
    content = browser.find_element_by_class_name("htx-text")
    content3_size = content.size
    action_chains = ActionChains(browser)
    browser.maximize_window()
    # Select "the" words
    action_chains.move_to_element_with_offset(
        content, 5, 5
    ).double_click().perform()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )

    # 6 times "the" word present
    hightlighted_elem = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )
    assert len(hightlighted_elem) == 6
    browser.find_element_by_xpath("//span[text()='Undo']").click()
    assert len(browser.find_elements_by_class_name("htx-highlight-last")) == 3
    browser.find_element_by_xpath("//span[text()='Undo']").click()
    assert len(browser.find_elements_by_class_name("htx-highlight-last")) == 0
    browser.find_element_by_xpath("//span[text()='Redo']").click()
    browser.find_element_by_xpath("//span[text()='Redo']").click()
    hightlighted_elem = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )
    assert len(hightlighted_elem) == 6
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Label all occurrences of selected text']")
        )
    )
    chk_label_all = browser.find_element_by_xpath(
        "//input[@value='Label all occurrences of selected text']"
    )
    if chk_label_all.get_attribute("checked") == "true":
        chk_label_all.click()
   
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "ant-modal-close")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "ant-modal")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='DATE']")
        )
    ).click()

    content = browser.find_element_by_class_name("htx-highlight")

    action_chains = ActionChains(browser)
    action_chains.move_to_element(
        content
    ).double_click().perform()
    # select text
    element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-update-btn"))
    )
    browser.execute_script("arguments[0].click();", element)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )
    assert len(browser.find_elements_by_class_name("htx-highlight-last")) == 6
    delete_project(browser, project_name)


def test_label_region(browser):
    project_name = unique_project_name("test_label_region")
    create_project_with_task(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling?task_id=1")

    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    ).click()
    content = browser.find_element_by_class_name("htx-text")
    assert len(content.find_elements_by_class_name("htx-highlight")) == 0
    content1_size = content.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 70, (content1_size["height"] / 2)
    ).double_click().perform()
    assert len(browser.find_elements_by_class_name("htx-highlight")) == 1
    assert len(browser.find_elements_by_class_name("htx-no-label")) == 0
    result = []
    for count in range(2):
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
        ).click()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Show labels inside the regions']")
            )
        ).click()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
        ).click()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "ant-modal-content")
            )
        )
        assert len(browser.find_elements_by_class_name("htx-highlight")) == 1
        result.append(len(browser.find_elements_by_class_name("htx-no-label")))
    assert result.sort() == [1, 0].sort()
    delete_project(browser, project_name)


def test_deselect_all_label_of_same_text(browser):
    project_name = unique_project_name("test_deselect_all_label_of_same_text")
    create_project_with_task(browser, project_name)
    browser.find_element_by_partial_link_text("Task 1").click()
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Label all occurrences of selected text']")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "ant-modal-content")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//span[text()='CARDINAL']",
            )
        )
    )
    browser.find_element_by_xpath("//span[text()='CARDINAL']").click()
    content1 = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "htx-text",
            )
        )
    )
    content1_size = content1.size
    browser.maximize_window()
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content1, 5, 5
    ).double_click().perform()
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "htx-highlight",
            )
        )
    ).click()
    btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'ls-entity-buttons')]"
                "/button[contains(@class, 'ant-btn-danger')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "ant-popover-buttons")
        )
    )
    delete_button = browser.find_element_by_xpath(
        '//div[@class="ant-popover-buttons"]/button[2]'
    )
    browser.execute_script("arguments[0].click();", delete_button)
    assert len(browser.find_elements_by_class_name("htx-highlight")) == 0
    delete_project(browser, project_name)


def test_label_all_occurences_setting_option_should_be_dynamic(browser):
    project_name = unique_project_name("test_dynamic_label_all_occurences_setting")
    create_project_with_task(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Show hotkey tooltips']")
        )
    )
    assert (
        len(
            browser.find_elements_by_xpath(
                "//span[text()='Label all occurrences of selected text']"
            )
        )
        == 1
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    ).click()
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    content = """<View>
        <Text name="text" value="$text" />
        <Choices name="sentiment" toName="text" showInLine="true">
            <Choice value="Positive" />
            <Choice value="Negative" />
            <Choice value="Neutral" />
        </Choices>
        <Choices name="other-props" toName="text"
            choice="single" showInLine="true"
                visibleWhen="choice-selected"
                whenTagName="sentiment">
            <View style="width:100%">
            <Header value="Other properties of the text" />
            </View>
            <Choice value="Descriptive" />
            <Choice value="Emotional" />
        </Choices>
        </View>
    """
    validate_config_content(browser, project_name, content)
    # hack to wait for the validation api to be called
    time.sleep(2)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and not(@disabled)]")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    ).click()
    assert (
        "saved"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Tasks"))
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    wait_for_labeling_page_load(browser)
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    )
    panel = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-panel"))
    )
    WebDriverWait(panel, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[text()='Show hotkey tooltips']")
        )
    )
    assert (
        len(
            browser.find_elements_by_xpath(
                "//span[text()='Label all occurrences of selected text']"
            )
        )
        == 0
    )
    delete_project(browser, project_name)


def test_case_sensitivty_of_selected_label_occurances(browser):
    project_name = unique_project_name("test_case_sensitivty_of_selected_label_occurances")
    create_project_with_task(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, project_name))
    ).click()
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Label all occurrences of selected text']")
        )
    )
    chk_label_all = browser.find_element_by_xpath(
        "//input[@value='Label all occurrences of selected text']"
    )
    if chk_label_all.get_attribute("checked") != "true":
        chk_label_all.click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    ).click()
    browser.maximize_window()
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    ).click()

    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    browser.maximize_window()
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 5, 5
    ).double_click().perform()  # select text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-submit-btn"))
    )
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )
    assert len(browser.find_elements_by_class_name("htx-highlight-last")) == 3
    regions = browser.find_elements_by_xpath(
        '//span[contains(@class, "Entities_node__")]/span[2]'
    )
    regions_text = [region.text for region in regions]
    assert regions_text.sort() == ["The", "the", "the"].sort()
    delete_project(browser, project_name)


def test_label_all_occurrences_of_the_selected_text(browser):
    project_name = unique_project_name("test_label_all_occurrences_of_the_selected_text")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    browser.find_element_by_partial_link_text(project_name).click()
    browser.get(browser.current_url.replace("setup", "import"))
    task = {
        "text": "To have faith is to trust yourself to the water\n\nTo have faith is to trust yourself to the water\n\nTo have faith is to trust yourself to the water"
    }
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Label all occurrences of selected text']")
        )
    )
    chk_label_all = browser.find_element_by_xpath(
        "//input[@value='Label all occurrences of selected text']"
    )
    if chk_label_all.get_attribute("checked") != "true":
        chk_label_all.click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    ).click()
    browser.maximize_window()
    browser.refresh()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    ).click()

    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    browser.maximize_window()
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 5, (content1_size["height"] / 2)
    ).double_click().perform()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-submit-btn"))
    )
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    WebDriverWait(browser, 10).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "htx-highlight-last")
        )
    )
    assert len(browser.find_elements_by_class_name("htx-highlight-last")) == 9
    regions = browser.find_elements_by_xpath(
        '//span[contains(@class, "Entities_node__")]/span[2]'
    )
    for region in regions:
        assert regions[0].text.lower() == region.text.lower()
    delete_project(browser, project_name)


def test_prev_next_buttons(browser):
    project_name = unique_project_name("test_prev_next_buttons")
    create_project(browser, project_name, True)

    browser.find_element_by_partial_link_text(project_name).click()
    task = [
        {"text": "This is first task"},
        {"text": "This is second task"},
        {"text": "This is third task"},
    ]
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "tasks"))
    )

    setup_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/setup"))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )
    # Add collaborate to team as annotator
    members_info = {"collaborate": ["Annotator"]}
    add_to_team(browser, members_info)

    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()
    # Assign assignee to task
    assign_assignee = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_assignee"))
    )
    assign_assignee.click()
    WebDriverWait(assign_assignee, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "list-li"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "toastModalMessage"))
    )

    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling?task_id=1")
    wait_for_labeling_page_load(browser)
    btn_save_completion_element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-save-completion"))
    )
    browser.execute_script(
        "arguments[0].click();", btn_save_completion_element
    )
    element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-submit-completion"))
    )
    # Submit Completion
    browser.execute_script("arguments[0].click();", element)
    model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-modal-footer"))
    )
    WebDriverWait(model, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-btn-primary"))
    ).click()

    current_task_id = browser.current_url.split("=")[1]
    assert "1" == current_task_id
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    ).click()
    wait_for_labeling_page_load(browser)
    current_task_id = browser.find_element_by_class_name(
        "edit_title"
    ).text
    assert "2" in current_task_id
    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_pagination(browser):
    project_name = unique_project_name("test_pagination")
    create_project(browser, project_name)
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    wait_for_import_page_load(browser)
    task = {
        "text": "This first page. This second page. This third page."
    }
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()

    assert (
        "Tasks created:1"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="upload-dialog-msg"]')
            )
        )
        .text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    wait_for_labeling_page_load(browser)


    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-select-selection-item"))
    ).click()

    word_count_dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "ant-select-dropdown")
        )
    )

    WebDriverWait(word_count_dropdown, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ant-input"))
    ).send_keys("3")

    WebDriverWait(word_count_dropdown, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-plus"))
    ).click()


    WebDriverWait(word_count_dropdown, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "ant-select-item-option-content"))
    )

    for dd_value in browser.find_elements_by_class_name("ant-select-item-option-content"):
        if "3 words" in dd_value.text:
            dd_value.click()

    WebDriverWait(word_count_dropdown, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "ant-select-open"))
    )

    content = browser.find_element_by_class_name("htx-text")
    element = browser.find_element_by_class_name("ant-pagination")
    # 3 pages with prev and next button
    assert 3 == len(element.find_elements_by_tag_name("li"))
    assert "This first page." == content.text
    next_button = browser.find_elements_by_class_name(
        "ant-pagination-item-link"
    )[1]
    browser.execute_script("arguments[0].click();", next_button)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "htx-text"), "This second page."
        )
    )
    assert (
        "This second page."
        == browser.find_element_by_class_name("htx-text").text
    )
    next_button = browser.find_elements_by_class_name(
        "ant-pagination-item-link"
    )[1]
    browser.execute_script("arguments[0].click();", next_button)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "htx-text"), "This third page."
        )
    )
    assert (
        "This third page."
        == browser.find_element_by_class_name("htx-text").text
    )
    delete_project(browser, project_name)


def test_normalization(browser):
    project_name = unique_project_name("test_normalization")
    create_project_with_task(browser, project_name)
    # Task 1 click
    browser.find_element_by_partial_link_text("Task 1").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    ).click()

    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    browser.maximize_window()
    action_chains = ActionChains(browser)
    # select 'To' text
    action_chains.move_to_element_with_offset(
        content, 5, (content1_size["height"] / 2)
    ).double_click().perform()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "htx-highlight-last"))
    ).click()
    entity_block = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-entity-buttons"))
    )
    WebDriverWait(entity_block, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-plus"))
    ).click()
    # set normalization value
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-input"))
    ).send_keys("normalization value")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Add']"))
    )
    add_element = browser.find_element_by_xpath("//span[text()='Add']")
    browser.execute_script("arguments[0].click();", add_element)
    # verify normalization value is set
    assert (
        "normalization value"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-typography"))
        )
        .text
    )
    btn_save_completion = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-save-completion"))
    )
    browser.execute_script("arguments[0].click();", btn_save_completion)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn-submit-completion"))
    )

    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn-submit-completion"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "htx-highlight-last"))
    ).click()

    # verify again that normalized value is present
    assert (
        "normalization value"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-typography"))
        )
        .text
    )
    delete_project(browser, project_name)


def test_create_relation(browser):
    project_name = unique_project_name('relation_among_entities')
    create_project(browser, project_name)
    select_relation_among_entities_config(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//div[@id='toastModalId']"
        ))
    )
    create_sample_task(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling?task_id=1")
    
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Subject']"))
    )
    browser.find_element_by_xpath("//span[text()='Subject']").click() # select label

    content1 = browser.find_element_by_class_name("htx-text")
    content1_size = content1.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content1, 70, (content1_size['height'] / 2)).double_click().perform()  # select text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()='Object']"))
    )
    browser.find_element_by_xpath("//span[text()='Object']").click() # select label

    content2 = browser.find_element_by_class_name("htx-text")
    content2_size = content2.size
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content2, 10, (content2_size['height'] / 2)).double_click().perform()  # select text
    
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    ).click() # select region
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_any_elements_located(
            (By.CLASS_NAME, "ls-entity-buttons"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "Entity_button__3c64R"))
    ).click() # create relation
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-highlight"))
    ).click() #select another region

    relation_overlay_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "text"))
    )
    browser.execute_script("arguments[0].scrollIntoView();", relation_overlay_button)
    relation_overlay_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.TAG_NAME, "text"))
    ).click()    

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "rc_select_1"))
    ).send_keys("is a") # search for label
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@title, 'Is A')]"))
    ).click() # select a label
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(@class, 'anticon-more')]"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(@class, 'ant-select-selection-item-content')]"))
    )
    assert (
        "Is A" in browser.find_element_by_xpath("//span[contains(@class, 'ant-select-selection-item-content')]").text
    )
    delete_project(browser, project_name)


def test_keep_label_select_option(browser):
    project_name = unique_project_name("test_keep_label_select_option")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    browser.find_element_by_partial_link_text(project_name).click()
    browser.get(browser.current_url.replace("setup", "import"))
    task = {
        "text": "To have faith is to trust yourself to the water\n\nTo have faith is to trust yourself to the water\n\nTo have faith is to trust yourself to the water"
    }
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "anticon-setting"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Keep label selected after creating a region']")
        )
    )
    chk_keep_label = browser.find_element_by_xpath(
        "//input[@value='Keep label selected after creating a region']"
    )
    if chk_keep_label.get_attribute("checked") != "true":
        chk_keep_label.click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    ).click()
    browser.maximize_window()
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='CARDINAL']"))
    ).click()

    content = browser.find_element_by_class_name("htx-text")
    content1_size = content.size
    browser.maximize_window()
    action_chains = ActionChains(browser)
    action_chains.move_to_element_with_offset(
        content, 5, (content1_size["height"] / 2)
    ).double_click().perform()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//span[@data-labels='CARDINAL']"))
    )
    
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='EVENT']"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//span[@data-labels='CARDINAL']"))
    )
    
    delete_project(browser, project_name)


def test_direct_submit(browser):
    project_name = unique_project_name("test_direct_submit")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    content = """<View oneClickSubmit="true">
        <Labels name="label" toName="text">
            <Label value="CARDINAL" model="ner_onto_100" background="#af906b"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project_name, content)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="submit_form"]'))
    ).click()

    message = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )

    assert "Project config saved" in message

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, "toastModalMessage"))
    )

    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(DUMMY_TASKS_FOR_AL))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()

    assert (
        "New completion"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "ant-collapse-content-box")
            )
        )
        .text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@id='btn-submit-next-completion' and not(@disabled)]"))
    )

    btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-submit-next-completion']"))
    )

    browser.execute_script("arguments[0].click();", btn)

    assert (
        "Submitted just now"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "ant-collapse-content-box")
            )
        )
        .text
    )

    delete_project(browser, project_name)


def test_accept_prediction(browser):
    project_name = unique_project_name("test_accept_prediction")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)

    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(DUMMY_PREDICTION_TASK))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()

    assert (
        "New completion"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "ant-collapse-content-box")
            )
        )
        .text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-accept-prediction"))
    ).click()

    browser.refresh()

    assert (
        "Submitted just now"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "ant-collapse-content-box")
            )
        )
        .text
    )

    delete_project(browser, project_name)
