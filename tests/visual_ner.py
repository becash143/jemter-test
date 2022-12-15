"""
Tests for Visual NER related stuffs
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.utils.helpers import *
from tests.utils.api_helper import upload_license, delete_project_task
from tests.utils.visual_ner_helper import *

def test_zoom_for_visual_ner(browser):

    delete_existing_license()
    upload_license(ocr=True)

    project_name = unique_project_name('visual_ner_zoom')
    create_project(browser, project_name)
    select_visual_ner_labeling_config(browser, project_name)

    # Wait for canvas to load
    wait_for_element_by_xpath(browser, xpath="//canvas")

    initial_scale = get_image_scale(browser)

    for i in range(1, 10):
        zoom_in = wait_for_element_by_xpath(
            browser, xpath='//button[@id="zoom-in"]')
        browser.execute_script('arguments[0].click();', zoom_in)

    zoomed_in_scale = get_image_scale(browser)

    # Zoom in test
    assert any(
        [z_in > init for z_in, init in zip(zoomed_in_scale, initial_scale)]
    )

    for i in range(1, 10):
        zoom_out = wait_for_element_by_xpath(
            browser, xpath='//button[@id="zoom-out"]')
        browser.execute_script('arguments[0].click();', zoom_out)

    zoomed_out_scale = get_image_scale(browser)

    # Zoom out test
    assert any(
        [z_out < z_in for z_in, z_out
         in zip(zoomed_in_scale, zoomed_out_scale)]
    )

    delete_project(browser, project_name)


def test_import_visual_ner_task(browser):

    project_name = unique_project_name('test-import-task')
    create_visual_ner_project(browser, project_name)

    # # import task from local file
    create_visual_ner_task_with_local_file(
        browser,
        project_name,
        file_path=""
    )

    # check if task is created
    ensure_task_existence(browser, project_name)

    delete_project_task(project_name, task_id=1)

    # import task from URL
    create_visual_ner_task_with_url(
        browser,
        project_name
    )

    # check if task created
    ensure_task_existence(browser, project_name)

    delete_project(browser, project_name)


def test_pagination_for_visual_ner(browser):

    def get_current_pagination():
        return wait_for_element_by_xpath(
            browser,
            '//li[@class="ant-pagination-simple-pager"]'
        ).get_attribute("title")

    project_name = unique_project_name('pagination_test')
    create_visual_ner_project(browser, project_name)

    create_visual_ner_task_with_local_file(
        browser,
        project_name,
        file_path="",
        multipage=True
    )

    # wait until task has been created
    ensure_task_existence(browser, project_name)

    WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//tr[@class="record"]/td/div/a')
        )
    ).click()

    # check for paginations
    try:
        assert get_current_pagination() == '1/3'

        browser.find_element_by_xpath(
            '//li[@title="Next Page"]/button').click()

        assert get_current_pagination() == '2/3'

        browser.find_element_by_xpath(
            '//li[@title="Previous Page"]/button').click()

        assert get_current_pagination() == '1/3'

    except Exception:
        assert ("Pagination not detected!" and False)

    delete_project(browser, project_name)


def test_preannotate_button_disabled(browser):
    '''
        Preannotate button should be disabled at all times
        for image based projects
    '''

    project_name = unique_project_name('test_preannotation_button_disabled')
    create_visual_ner_project(browser, project_name)

    # # go to tasks page
    task_xpath = '//div[@id="left-panel"]/a[contains(@href,"tasks")]'
    WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, task_xpath)
        )
    ).click()
    wait_for_task_page_load(browser)

    preannotate_btn_xpath = "//button[@id='btn_pre_annotation' and "\
        "text()='Preannotate'][@disabled]"
    wait_for_element_by_xpath(browser, preannotate_btn_xpath)
    delete_project(browser, project_name)


def test_relation_for_visual_ner(browser):
    # project_name = "relations_in_visual_ner-261"
    project_name = unique_project_name('relations_in_visual_ner')
    create_visual_ner_project(browser, project_name)
    create_visual_ner_task_with_local_file(
        browser,
        project_name,
        "/tests/utils/visual_ner_relations_task.zip",
        multipage=False,
    )
    # check if task created
    ensure_task_existence(browser, project_name)

    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling?task_id=1")
    # Wait for canvas to load
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//canvas"))
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_all_elements_located(
            (
                By.CLASS_NAME,
                'ant-divider-inner-text',
            )
        )
    )
    has_relation = False
    for element in browser.find_elements_by_class_name("ant-divider-inner-text"):
        if "Relations (1)" in element.text:
            has_relation = True
            break

    assert has_relation == True

    delete_project(browser, project_name)


def test_deployment_confirmation_model_for_visual_ner(browser):
    '''
    Deployment confirmation message should be shown for visual NER.

    Make sure preannotator server is not deployed already before running this.
    '''

    stop_container("preannotator-server")

    delete_existing_license()
    upload_license(ocr=True)

    project_name = unique_project_name('visual_ner_zoom')
    create_project(browser, project_name)
    select_visual_ner_labeling_config(browser, project_name)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and not(@disabled)]")
        )
    )

    # click on save config
    WebDriverWait(
        browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[@id="submit_form"]')
        )
    ).click()

    dialogue_box_xpath = '//div[@id="confirm-box-message"]'
    message = WebDriverWait(
        browser, DRIVER_TIMEOUT
    ).until(
        EC.visibility_of_element_located(
            (By.XPATH, dialogue_box_xpath)
        )
    ).text

    'deploy OCR pipeline' in message
    delete_project(browser, project_name)


def test_deploy_preannotation_server_while_importing_task(browser):
    '''
    Preannotation server should be deployed while importing tasks for visual NER.

    Make sure preannotator server is not deployed already before running this.
    '''

    stop_container("preannotator-server")
    delete_existing_license()
    upload_license(ocr=True)
    project_name = unique_project_name('test_deploy_preannotation_server_while_importing_task')
    create_visual_ner_project(browser, project_name)
    create_sample_task_for_visual_ner(browser, project_name)

    error_msg = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "upload-row-error")
        )
    ).text

    assert (
        "Please try again in a while"
        in error_msg
    )

    browser.get(f'{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks')
    WebDriverWait(browser, LONG_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.ID, "btn_pre_annotation"), "Server is busy"
        )
    )
    retry = 1
    while retry < 5:
        try:
            WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
                EC.text_to_be_present_in_element(
                    (By.ID, "btn_pre_annotation"), "Preannotate"
                )
            )
            break
        except Exception:
            retry += 1

    create_sample_task_for_visual_ner(browser, project_name)

    # check if task created
    ensure_task_existence(browser, project_name)

    delete_project(browser, project_name)
