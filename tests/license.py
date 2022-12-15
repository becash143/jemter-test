"""
Tests for license page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils.helpers import *
import os
import ast


def test_license_upload(browser):

    # not a super admin user, can't upload license
    login_as("collaborate", "collaborate", browser)
    profile_icon = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user_profile_icon"))
    )
    browser.execute_script("arguments[0].click();", profile_icon)
    collaborate_user = []
    left_menu_item = browser.find_elements_by_class_name("left-menu-item")
    for item in left_menu_item:
        collaborate_user.append(item.text)
    assert "License" not in collaborate_user

    # user with admin role can upload license
    login_as("admin", "admin", browser)
    profile_icon = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user_profile_icon"))
    )
    browser.execute_script("arguments[0].click();", profile_icon)
    manage_users = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "License"))
    )
    browser.execute_script("arguments[0].click();", manage_users)
    JSL_LICENSE = os.environ.get("JSL_LICENSE")
    if not JSL_LICENSE:
        raise Exception("Set JSL_LICENSE in environment")
    delete_existing_license()
    data = json.dumps(ast.literal_eval(JSL_LICENSE))
    browser.find_element_by_id("json-input").send_keys(data)
    browser.find_element_by_id("input-button").click()
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//td[contains(text(), 'Spark NLP for Healthcare' )]")
        )
    )
    assert "Spark NLP for Healthcare" in submit_button.text

    # license is already available
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "json-input"))
    )
    browser.find_element_by_id("json-input").send_keys(data)
    browser.find_element_by_id("input-button").click()
    alert_message = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "alertMessage")))
        .text
    )
    assert "is already available" in alert_message

    # invalid license file
    browser.refresh()
    data = {"title": "Annotation Lab", "port": 8200, "debug": "false"}

    invalid_data = json.dumps(data)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "json-input"))
    )
    browser.find_element_by_id("json-input").send_keys(invalid_data)
    browser.find_element_by_id("input-button").click()
    alert_message = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "alertMessage")))
        .text
    )
    assert "Invalid" in alert_message

    # add floating license test case after merged
