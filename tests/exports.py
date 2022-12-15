"""
Tests for export related stuffs
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from tests.utils.helpers import *


def test_conll_export_task(browser):
    project_name = unique_project_name('test_conll')
    create_task_with_completion(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/export")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "export-format-dropdown"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='CONLL2003']"))
    ).click()
    
    export_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='export_block']/div[5]/button"))
    )
    browser.execute_script("arguments[0].click();", export_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='export_block']/div[5]/button"))
    )
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='export_block']/div[5]/button"))
    )
    delete_project(browser, project_name)


def test_tag_based_export(browser):
    project_name = unique_project_name("test_tag_based_export")
    create_task_with_completion(browser, project_name)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "chk-1"))
    ).click()

    assign_tags = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME,'assign_tags'))
    )
    assign_tags.click()

    tag_dropdown = assign_tags.find_elements_by_class_name("list-li")
    for element in tag_dropdown:
        if "Validated" in element.text:
            element.click()
            break
    labels = WebDriverWait(browser, 12).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "label-tag"))
    )
    assert "Validated" in labels.text

    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/export")
    tag_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txttag"))
    )
    tag_box.send_keys("Validated")
    export_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='export_block']/div[5]/button"))
    )
    browser.execute_script("arguments[0].click();", export_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='export_block']/div[5]/button"))
    )
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='export_block']/div[5]/button"))
    )
    delete_project(browser, project_name)
