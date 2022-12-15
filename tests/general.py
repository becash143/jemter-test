"""
Tests for general UI
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils.helpers import *


def test_close_sidebar(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "close_nav"))
    )
    browser.find_element_by_class_name("close_nav").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "open_nav"))
    )
    assert browser.find_element_by_class_name("open_nav").is_enabled()
    browser.find_element_by_class_name("open_nav").click()


def test_open_sidebar(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "close_nav"))
    )
    browser.find_element_by_class_name("close_nav").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "open_nav"))
    )
    browser.find_element_by_class_name("open_nav").click()
    assert browser.find_element_by_class_name("close_nav").is_enabled()


def test_ghost(browser):
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, "test_ghost")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "test_ghost"))
    )
    browser.find_element_by_partial_link_text("test_ghost").click()
    create_sample_task(browser, "test_ghost")
    create_task(browser, "test_ghost")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    browser.find_element_by_partial_link_text("Task 1").click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-btn-background-ghost"))
    )
    assert len(browser.find_elements_by_class_name(
        "ant-btn-background-ghost")) == 1
    browser.find_element_by_class_name(
        "ant-btn-background-ghost"
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-submit-btn"))
    )
    ls_submit_btn = browser.find_element_by_class_name("ls-submit-btn")
    browser.execute_script("arguments[0].click();", ls_submit_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-update-btn"))
    )
    ls_update_btn = browser.find_element_by_class_name('ls-update-btn')
    browser.execute_script("arguments[0].click();", ls_update_btn)
    assert len(browser.find_elements_by_class_name(
        "ant-btn-background-ghost")) == 0
    assert len(browser.find_elements_by_class_name(
        "ant-btn-background-ghost")) == 0
    delete_project(browser, "test_ghost")


def test_logout(browser):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "user_profile_icon"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Logout"))
    ).click()
    assert WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.ID, ("kc-page-title")), "Sign in to your account"
        )
    ) is True
    browser.get(f'{ANNOTATIONLAB_URL}/#/projects')
    assert WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.ID, ("kc-page-title")), "Sign in to your account"
        )
    ) is True
    login_as("admin", "admin", browser)
