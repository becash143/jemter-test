import re
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.task_importer import get_cookies
from tests.utils.helpers import *
from tests.utils.api_helper import upload_license
from selenium.common.exceptions import TimeoutException
import docker

CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock')

def select_visual_ner_labeling_config(browser, project_name):

    configuration_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectConfiguration"
    browser.get(configuration_url)

    accordion_xpath = '//button[contains(@class,"accordion") and span[span[contains(text(), "Per region examples")]]]'

    accordion = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                accordion_xpath
            )
        )
    )

    browser.execute_script('arguments[0].click();', accordion)
    config_element_xpath = '//span[contains(text(), "Visual NER labeling")]'
    config_element = WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, config_element_xpath)
        )
    )
    browser.execute_script("arguments[0].click();", config_element)

    # click yes on dialog box
    dialogue_box_yes_xpath = '//div[@id="confirm_config_template_replace_dialog"]//div[text()="Yes"]'
    WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, dialogue_box_yes_xpath)
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "ant-tag")
        )
    )
    


def get_image_scale(browser):
    try:
        xpath = '//div[@id="image-container"]/img'
        image = wait_for_element_by_xpath(browser, xpath)
        style = image.get_attribute('style')
        return [float(x) for x in
                re.findall(r'scale\((.*), (.*)\)', style)[0]]
    except IndexError:
        try:
            scale = float(re.findall(r'scale\((.*)\)', style)[0])
            return [scale, 1]
        except Exception:
            return [1, 1]


def create_visual_ner_project(browser, project_name):
    '''
        creates visual NER project
        deploys model server
    '''
    delete_existing_license()
    upload_license(ocr=True)

    create_project(browser, project_name)
    select_visual_ner_labeling_config(browser, project_name)

    # click on save config
    save_config = WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[@id="submit_form"]')
        )
    )
    browser.execute_script("arguments[0].click()", save_config)

    if is_model_server_up():
        return

    try:
        confirm_deployment = WebDriverWait(
            browser, SHORT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@id="confirm-box-ok"]')
            )
        )

        browser.execute_script("arguments[0].click();", confirm_deployment)

    except TimeoutException:
        pass


def create_visual_ner_task_with_local_file(
        browser, project_name, file_path, multipage=False
):
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")

    wait_for_model_server()

    dir_path = os.path.join(file_path)
    if not file_path:
        dir_path = os.path.join("/tests/utils/multipage_ocr_sample.pdf") \
            if multipage else os.path.join("/tests/utils/ocr_sample.pdf")

    WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//div[@id="import_drag_drop"]')
        )
    )

    browser.find_element_by_id("file-input").send_keys(
        dir_path
    )
    message = "Tasks created" if file_path else "file(s) uploaded!"

    count = 0
    xpath = '//div[@id="upload-dialog-msg"]'
    while count < 20:
        try:
            WebDriverWait(
                browser, SHORT_TIMEOUT
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            break
        except TimeoutException:
            count += 1

    assert message in browser.find_element_by_id("upload-dialog-msg").text


def create_visual_ner_task_with_url(browser, project_name, url=''):
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import")

    wait_for_model_server()

    if not url:
        url = "http://jeroen.github.io/images/testocr.png"

    input_json = json.dumps({'image': url})

    WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//input[@id="url-input"]')
        )
    ).send_keys(input_json)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-button"))
    ).click()

    count = 0
    xpath = '//div[@id="upload-dialog-msg"]/p[1]'
    while count < 20:
        try:
            WebDriverWait(
                browser, SHORT_TIMEOUT
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            break
        except TimeoutException:
            count += 1

    element = browser.find_elements_by_xpath(xpath)
    assert len(element) > 0

    assert "file(s) uploaded!" in element[0].text

def ensure_task_existence(browser, project_name):

    browser.get(f'{ANNOTATIONLAB_URL}/#/project/{project_name}'
                 '/tasks')
    wait_for_element_by_xpath(browser, '//tr[@class="record"]', refresh=True)

def create_sample_task_for_visual_ner(browser, project_name):
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    sample_task_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "add_sample_task"))
    )
    browser.execute_script("arguments[0].click();", sample_task_btn)

def stop_container(container_name):
    try:
        CLIENT.containers.get(container_name).stop()
        time.sleep(5)
    except Exception as ex:
        print(f"no container {container_name} to delete; message={ex}")