"""
Tests for tags related stuffs
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils.helpers import *


def test_detach_tag_from_task(browser):
    project_name = unique_project_name("test_detach_tag_from_task")
    create_tag(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='chk-1']"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "task_status_button")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_tags"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "assign_tags"))
    ).click()

    elements = browser.find_elements_by_class_name("list-li")
    for element in elements:
        if "Test Tag" in element.text:
            WebDriverWait(element, DRIVER_TIMEOUT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fa-times-circle"))
            ).click()
            break

    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "tasks"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "tr"))
    )
    labels = browser.find_elements_by_class_name("label-tag")
    assert len(labels) == 0
    delete_project(browser, project_name)


def test_delete_tag_from_project(browser):
    project_name = unique_project_name("test_delete_tag_from_project")
    create_tag(browser, project_name)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    )
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownTagsFilter"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "dropdownTagsFilter"))
    ).click()

    elements = browser.find_elements_by_class_name("list-li")
    for element in elements:
        if "Test Tag" in element.text:
            WebDriverWait(element, DRIVER_TIMEOUT).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "tag_more_option_block")
                )
            ).click()
            WebDriverWait(element, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "tag_more_option")
                )
            )
            WebDriverWait(element, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "delete_tag"))
            )
            WebDriverWait(element, DRIVER_TIMEOUT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "delete_tag"))
            ).click()
            break
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn-delete-tag"))
    ).click()

    tags = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownTagsFilter"))
    )

    assert "Test Tag" not in tags.text
    assert (
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "label-tag"))
        )
        is True
    )
    delete_project(browser, project_name)


def test_detach_tag_from_multiple_tasks(browser):
    project_name = unique_project_name("test_detach_tag_from_multiple")
    create_tag_assign_to_all_tasks(browser, project_name)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='chk-1']"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='chk-2']"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "task_status_button")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "dropdownTagsAssigner"))
    ).click()
    assign_tags_body = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownTagsAssignerBody"))
    )
    elements = assign_tags_body.find_elements_by_class_name("list-li")
    for element in elements:
        if "Test Tag" in element.text:
            element.find_element_by_class_name("fa-times-circle").click()
            break

    browser.refresh()
    wait_for_task_page_load(browser)
    labels = browser.find_elements_by_class_name("label-tag")
    assert len(labels) == 0
    delete_project(browser, project_name)


def test_predefined_tag(browser):
    project_name = unique_project_name("test_predefined_tag")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    create_sample_task(browser, project_name)
    create_task(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownTagsFilter"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "dropdownTagsFilter"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownTagsFilterBody"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//li[contains(@value,"Validated")]')
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//li[contains(@value,"Corrections Needed")]')
        )
    )
    delete_project(browser, project_name)


def test_create_and_attach_tag(browser):
    project_name = unique_project_name("test_create_and_attach_tag")
    create_project_with_task(browser, project_name)
    browser.find_element_by_xpath("//*[@id='chk-1']").click()

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
    browser.find_element_by_id("btn_update_group").click()
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")

    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownTagsFilter"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "dropdownTagsFilter"))
    ).click()
    labels = browser.find_elements_by_class_name("dropdown_menu")
    hasLabel = False
    for label in labels:
        if "Test Tag" in label.text:
            hasLabel = True
            break
    if not hasLabel:
        assert "Test Tag" in labels.text
    delete_project(browser, project_name)


def test_attach_tag_using_filter(browser):
    project_name = unique_project_name("test_attach_tag_using_filter")
    create_project_with_task(browser, project_name)
    browser.find_element_by_id("task_search").send_keys("1")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, "TASK 1"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )
    browser.find_element_by_xpath('//*[@id="ckbCheckAll"]').click()

    tag_block = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "assign_tags"))
    )
    browser.execute_script("arguments[0].click();", tag_block)
    add_more = browser.find_element_by_xpath(
        '//button[contains(text(), "Add more")]'
    )
    browser.execute_script("arguments[0].click();", add_more)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "TagModal"))
    )
    txt_tagname = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_name"))
    )
    txt_tagname.send_keys("Test Tag Filter")
    browser.find_element_by_class_name("generate_color_icon").click()
    browser.find_element_by_id("btn_update_group").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "label-tag"))
    )
    assert (
        "Test Tag Filter"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "tasks")))
        .text
    )
    delete_project(browser, project_name)
