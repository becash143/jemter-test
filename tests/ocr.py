"""
Tests for OCR related stuffs
"""
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.task_importer import get_cookies
from tests.utils.helpers import *
from tests.utils.api_helper import upload_license
from selenium.common.exceptions import TimeoutException


def check_model_server(browser, project_name):
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "chk_ocr"))
    ).click()
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "confirm-box-message"))
        )
        is_confirm_present = True
    except TimeoutException:
        is_confirm_present = False
    if is_confirm_present:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "confirm-box-ok"))
        ).click()
        count = 0
        while not is_model_server_up():
            time.sleep(3)
            count += 1
            if count == 5:
                raise Exception("Model server is not up!")


def check_file_upload_ocr(browser, project_name):
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "upload-dialog-msg"))
    )
    assert (
        "1 file(s) uploaded!"
        in browser.find_element_by_xpath('//*[@id="upload-dialog-msg"]/p[1]').text
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "upload-done-button"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='chk_ocr' and @disabled='']"))
    )
    WebDriverWait(browser, 500).until(
        EC.visibility_of_element_located((By.ID, "successful_ocr"))
    )
    assert "Last OCR state: " in browser.find_element_by_id(
        "successful_ocr"
    ).get_attribute("innerText")


def test_ocr_without_license(browser):
    delete_existing_license()
    project_name = unique_project_name("test_ocr_without_license")
    create_project(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "chk_ocr"))
    ).click()
    assert "No valid Spark OCR license available!" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "toastModalMessage"))
    ).text
    delete_project(browser, project_name)


def test_ocr(browser):
    delete_existing_license()
    r = upload_license(ocr=True)
    if isinstance(r, str):
        raise Exception(r)
    project_name = unique_project_name("test_ocr")
    create_project(browser, project_name)
    check_model_server(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "url-input"))
    ).send_keys(
        "http://www.africau.edu/images/default/sample.pdf"
    )
    browser.find_element_by_id("url-button").click()
    check_file_upload_ocr(browser, project_name)
    delete_project(browser, project_name)


def test_ocr_with_local_file(browser):
    delete_existing_license()
    r = upload_license(ocr=True)
    if isinstance(r, str):
        raise Exception(r)
    project_name = unique_project_name("test_ocr_with_local_file")
    create_project(browser, project_name)
    check_model_server(browser, project_name)
    dir_path = os.path.join("/tests/utils/ocr_sample.pdf")
    browser.find_element_by_id("file-input").send_keys(
        dir_path
    )
    check_file_upload_ocr(browser, project_name)
    delete_project(browser, project_name)
