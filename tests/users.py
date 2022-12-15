"""
Tests for keycloak user related stuffs
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils.helpers import *


def test_create_user(browser):
    create_user(browser, "demo_user")
    delete_user(browser, "demo_user")


def test_update_user(browser):
    create_user(browser, "update_user")
    user_email = "new@jsl.com"
    browser.find_element_by_id("txt_email").send_keys(user_email)
    browser.find_element_by_id("save_details").click()
    delete_user(browser, "update_user")


def test_assign_group(browser):
    create_user(browser, "test_assign_group")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Groups"))
    )
    browser.find_element_by_partial_link_text("Groups").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@data-bs-target='#groups']"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "txt_user_group"))
    ).click()
    browser.refresh()
    browser.find_element_by_partial_link_text("Groups").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@data-bs-target='#groups']"))
    )
    user_admin_checkbox = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, "txt_user_group"))
    )
    assert user_admin_checkbox.get_attribute("checked") == 'true'
    delete_user(browser, "test_assign_group")


def test_set_password(browser):
    create_user(browser, "set_password")
    browser.find_element_by_partial_link_text("Credentials").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@data-bs-target='#credential']"))
    )
    txt_password = browser.find_element_by_id("txt_password")
    time.sleep(2)
    txt_password.send_keys("newuser")
    txt_cnf_password = browser.find_element_by_id(
        "txt_password_confirmation")
    txt_cnf_password.send_keys("newuser")
    browser.find_element_by_id("change_password").click()
    browser.get(f'{ANNOTATIONLAB_URL}/#/users')
    delete_user(browser, "set_password")


def test_validate_user_detail(browser):
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
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Add User'))
    )
    assert browser.current_url.endswith("/users")
    add_user_btn.click()
    save_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "save_details"))
    )
    assert browser.current_url.endswith("/user")

    browser.find_element_by_id("txt_username").send_keys(
        "test_validate_user_detail")
    browser.find_element_by_id("txt_first_name").send_keys("User@123")
    browser.find_element_by_id("txt_last_name").send_keys("User_last_name")
    save_btn.click()
    err_first_name = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "err_first_name")))
        .text
    )
    err_last_name = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "err_last_name")))
        .text
    )
    assert (
        err_first_name
        == "First name can only use alphabet, unicode, space with maximum 30 characters"
    )
    assert (
        err_last_name
        == "Last name can only use alphabet, unicode, space with maximum 30 characters"
    )
    first_name_field = browser.find_element_by_id("txt_first_name")
    first_name_field.clear()
    first_name_field.send_keys("Üsér")
    last_name_field = browser.find_element_by_id("txt_last_name")
    last_name_field.clear()
    last_name_field.send_keys("TèSt")
    browser.find_element_by_id("save_details").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains("/user/"))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Groups"))
    )
    assert (
        "test_validate_user_detail"
        in browser.find_element_by_class_name("pagination-link").text
    )
    delete_user(browser, "test_validate_user_detail")


def test_search_and_delete_user(browser):
    create_user(browser, "test_delete_user")
    delete_user(browser, "test_delete_user")


def test_delete_user_and_share_project_resources(browser):
    create_user(browser, "test_delete_with_resources")
    browser.get(f'{ANNOTATIONLAB_URL}/#/users')
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("/users")
    )
    browser.find_element_by_id("txt_search_user").send_keys(
        "test_delete_with_resources")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, "admin"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "test_delete_with_resources"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_delete_user"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    assert browser.find_elements_by_id("input_username") != 0
    delete_user = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "share_delete_user"))
    )
    browser.execute_script("arguments[0].click();", delete_user)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    assert len(browser.find_elements_by_link_text(
        "test_delete_with_resources")) == 0

    create_user(browser, "test_delete_with_resources")
    browser.find_element_by_partial_link_text("Credentials").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@data-bs-target='#credential']"))
    )
    txt_password = browser.find_element_by_id("txt_password")
    time.sleep(2)
    txt_password.send_keys("newuser")
    browser.find_element_by_id(
        "txt_password_confirmation").send_keys("newuser")
    browser.find_element_by_id("chk_temporary").click()
    browser.find_element_by_id("change_password").click()

    time.sleep(1)

    browser.get(f'{ANNOTATIONLAB_URL}/#/users')

    login_as("test_delete_with_resources", "newuser", browser)
    project_name = "test_delete_user_and_share_project_resources"
    create_project(browser, project_name)
    login_as("admin", "admin", browser)
    browser.get(f'{ANNOTATIONLAB_URL}/#/users')
    browser.find_element_by_id("txt_search_user").send_keys(
        "test_delete_with_resources")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, "admin"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_delete_user"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    assert len(browser.find_elements_by_id("input_username")) == 1
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "input_username"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "input_username"))
    ).send_keys("test_delete_with_resources")
    delete_user = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "share_delete_user"))
    )
    browser.execute_script("arguments[0].click();", delete_user)
    error_msg = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "err_search_username"))
    )
    assert error_msg.text == "User not allowed to exchange project"
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "input_username"))
    ).clear()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "input_username"))
    ).send_keys("admin")
    delete_user = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "share_delete_user"))
    )
    browser.execute_script("arguments[0].click();", delete_user)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "admin"))
    )
    assert "test_delete_with_resources" not in browser.find_element_by_class_name(
        "table"
    ).text
    browser.get(f'{ANNOTATIONLAB_URL}/#/projects')
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("projects")
    )
    browser.refresh()
    table = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "tr_test_delete_user_and_share_project_resources"))
    )

    assert (
        project_name
        == table.find_element_by_partial_link_text(project_name).text
    )
    delete_project(browser, project_name)