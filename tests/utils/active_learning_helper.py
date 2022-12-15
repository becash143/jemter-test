import os
import json
import time
import requests
import random as rand
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from tests.utils.helpers import *
from tests.utils.api_helper import upload_license
from tests.utils.label_config import test_ner_training_config

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException


USERNAME = PASSWORD = TASK_CREATED_BY = "admin"
COMPLETION_CREATED_BY = "admin"
all_labels = set()
to_unique = set()
headers = {
    "Host": ANNOTATIONLAB_URL.replace("http://", ""),
    "Origin": ANNOTATIONLAB_URL,
    "Content-Type": "application/json",
}


def get_cookies():
    keycloak_url = os.environ.get(
        "KEYCLOAK_SERVER_URL", "http://keycloak-local:8080/auth/"
    )
    keycloak_realm = os.environ.get("KEYCLOAK_REALM_NAME", "master")
    url = (
        f"{keycloak_url}realms/{keycloak_realm}/protocol/openid-connect/token"
    )
    data = {
        "grant_type": "password",
        "username": os.environ.get("KEYCLOAK_SUPERUSER_USER", "admin"),
        "password": os.environ.get("KEYCLOAK_SUPERUSER_PASS", "admin"),
        "client_id": os.environ.get("KEYCLOAK_CLIENT_ID", "annotationlab"),
        "client_secret": os.environ.get(
            "KEYCLOAK_CLIENT_SECRET_KEY",
            "09a71c59-0351-4ce6-bc8f-8fd3feb9d2ff",
        ),
    }
    auth_info = requests.post(url, data=data).json()
    cookies = {
        "access_token": f"Bearer {auth_info['access_token']}",
        "refresh_token": auth_info["refresh_token"],
    }
    return cookies


def prepare_tasks(filename):
    tasks = []
    with open(os.path.join(f"/tests/utils/{filename}"), "r") as f:
        data = json.loads(f.read())

    for each in data.get("examples"):
        completions = get_completions(each.get("annotations"))
        tasks.append(
            {
                "completions": completions,
                "predictions": [],
                "created_at": str(datetime.now()).split(".")[0],
                "created_by": TASK_CREATED_BY,
                "data": {"text": each.get("content"), "title": ""},
            }
        )
    return tasks


def generate_hash(length=10):
    nums = list(range(48, 58))
    uppers = list(range(65, 91))
    lowers = list(range(97, 123))
    all_chars = nums + uppers + lowers
    return "".join(
        [
            chr(all_chars[rand.randint(0, len(all_chars) - 1)])
            for x in range(length)
        ]
    )


def build_label(chunk, start, end, label):
    # TO-TEST how to support multiple label?
    label_json = {
        "from_name": "label",
        "id": generate_hash(),
        #         "source": "$text",
        "to_name": "text",
        "type": "labels",
        "value": {
            "end": end,
            "labels": [label],
            "start": start,
            "text": chunk,
        },
    }
    return label_json


def get_completions(annotations):
    completions = []
    results = []
    for annotation in annotations:
        start = annotation.get("start")
        end = annotation.get("end")
        label = annotation.get("tag_name")
        all_labels.add(label)
        value = annotation.get("value")
        if len(str(value).strip()) == 0:
            continue
        result = build_label(value, start, end, label)
        check_str = f"{value}_{start}_{end}_{label}"
        if check_str in to_unique:
            continue
        to_unique.add(check_str)
        results.append(result)
    completions.append(
        {
            "created_username": COMPLETION_CREATED_BY,
            "created_ago": datetime.now().isoformat() + "Z",
            "lead_time": 2.476,
            "result": results,
            "honeypot": True,
            "submitted_at": datetime.now().isoformat() + "Z",
        }
    )
    return completions


def import_tasks(project_name, tasks=None, filename="al_import.json"):
    global to_unique
    to_unique = set()
    if not tasks:
        tasks = prepare_tasks(filename)
    cookies = get_cookies()
    import_url = f"{ANNOTATIONLAB_URL}/api/projects/{project_name}/import"
    r = requests.post(
        import_url, headers=headers, data=json.dumps(tasks), cookies=cookies
    )


def save_config(project_name, label_config=test_ner_training_config):
    cookies = get_cookies()
    config_url = f"{ANNOTATIONLAB_URL}/api/projects/{project_name}/save-config"
    r = requests.post(
        config_url, data={"label_config": label_config}, cookies=cookies
    )
    assert r.status_code != 200


def open_spark_nlp_config(browser, project_name):
    setup_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#projectConfiguration"
    )
    browser.get(setup_url)
    spark_nlp_tab = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//a[@data-bs-target="#predefinedLabels"]')
        )
    )
    spark_nlp_tab.click()


def trigger_deployment_from_tasks_page(browser, project_name):
    tasks_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(tasks_url)
    preannotation_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "btn_pre_annotation"))
    )
    browser.execute_script("arguments[0].click();", preannotation_btn)
    deploy_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "deploy_project_model"))
    )
    browser.execute_script("arguments[0].click();", deploy_btn)


def preannotate_task_by_id(browser, project_name, id, status):
    tasks_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(tasks_url)
    retry = 1
    while retry < 5:
        try:
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, f"chk-{id}"))
            )
            break
        except Exception:
            browser.refresh()
            retry += 1
    large_task = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, f"chk-{id}"))
    )
    browser.execute_script("arguments[0].click();", large_task)
    preannotation_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "btn_pre_annotation"))
    )
    browser.execute_script("arguments[0].click();", preannotation_btn)
    pre_annotate_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "confirm_pre_annotate"))
    )
    browser.execute_script("arguments[0].click();", pre_annotate_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "btn-outline-primary"), "Task(s) running"
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.ID, "btn_pre_annotation"), "Preannotate"
        )
    )
    status_info = browser.find_element_by_xpath(
        f"//tr[@class='record' and .//input[@id='chk-{id}']]"
        "//i[contains(@class, 'pre_annotation_status')]"
    )
    assert status in status_info.get_attribute("title")


def ensure_deployment(browser, project_name):
    WebDriverWait(browser, LONG_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.ID, "btn_pre_annotation"), "Server is busy"
        )
    )
    retry = 1
    while retry < 5:
        try:
            WebDriverWait(browser, LONG_TIMEOUT).until(
                EC.text_to_be_present_in_element(
                    (By.ID, "btn_pre_annotation"), "Preannotate"
                )
            )
            break
        except Exception:
            retry += 1
    browser.refresh()
    preannotation_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.ID, "btn_pre_annotation"),
        )
    )
    browser.execute_script("arguments[0].click();", preannotation_btn)
    WebDriverWait(browser, LONG_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.ID, "preannotate_msg"),
            "Do you want to preannotate all task(s)?",
        )
    )
    preannotation_info_box = browser.find_element_by_xpath(
        "//div[@id='show_pre_annotation_msg']"
    )

    assert (
        f'ago by admin from project "{project_name}"'
        in preannotation_info_box.text
    )


def download_embeddings_or_models(browser, name):
    modelshub_url = f"{ANNOTATIONLAB_URL}/#/models"
    browser.get(modelshub_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@id, 'model_')]")
        )
    )
    search_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_input_search_models"))
    )
    search_box.send_keys(name)
    found_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"model_{name}"))
    )
    downloaded = True if "Downloaded" in found_model.text else False
    if not downloaded:
        chk_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[@id='model_{name}']"
                    "//input[@class='chk_model_license']",
                )
            )
        )
        browser.execute_script("arguments[0].click();", chk_button)
        download_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "btn_download_model_embeddings")
            )
        )
        browser.execute_script("arguments[0].click();", download_button)
        # wait for download completion
        retry = 1
        while retry < 30:
            try:
                WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[@title='Refresh']")
                    )
                ).click()
                found_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located((By.ID, f"model_{name}"))
                )
                if "Downloaded" in found_model.text:
                    break
                retry += 1
                # Wait 5 secs and hit Refresh again
                time.sleep(5)
            except Exception:
                retry += 1


def prepare_training(browser, project_name, model_type, license_required=True):
    models_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//select[@placeholder='--Choose Training Type--']")
        )
    )
    Select(models_selection).select_by_visible_text(model_type)
    al_epoch = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "epoch"))
    )
    al_epoch.clear()
    al_epoch.send_keys("10")

    if not license_required:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "open-source-radio-button"))
        ).click()

    al_save = browser.find_element_by_xpath("//button[text()='Save']")
    browser.execute_script("arguments[0].click();", al_save)
    retry = 1
    while retry < 3:
        try:
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btn_train_model"))
            )
        except Exception:
            browser.refresh()
            retry += 1

    btn_train_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn_train_model"))
    )
    browser.execute_script("arguments[0].click();", btn_train_model)


def trigger_training(
    browser,
    project_name,
    deploy=True,
    license_required=False,
    model_type="ner",
    wait_for_training=True
):
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    deploy_id = "yesClick" if deploy else "noClick"
    prepare_training(browser, project_name, model_type, license_required)

    # Delete existing license
    delete_existing_license()

    license_states = {
        "no-license": (
            "//div[@id='error_message' and text()="
            "'Training failed! License not found']"
        ),
        "expired": (
            "//div[@id='error_message' and text()="
            "'Training failed! Spark NLP for Healthcare expired']"
        ),
        "valid": None,
    }
    if license_required:
        for state, xpath in license_states.items():
            if state == "expired":
                upload_expired_license()
            elif state == "valid":
                r = upload_license()
                if isinstance(r, str):
                    raise Exception(r)

            mt_proceed_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, deploy_id))
            )
            browser.execute_script("arguments[0].click();", mt_proceed_dialog)
            if xpath:
                WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )

                btn_train_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "btn_train_model"))
                )
                browser.execute_script(
                    "arguments[0].click();", btn_train_model
                )

    else:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, deploy_id))
        )
        mt_proceed_dialog = (
            WebDriverWait(browser, DRIVER_TIMEOUT)
            .until(EC.element_to_be_clickable((By.ID, deploy_id)))
            .click()
        )
    if wait_for_training:
        wait_for_training_completion(browser, project_name, deploy)


def update_and_deploy_pretrained_model(
    browser, project_name, label_config, interface_preview_xpath
):
    validate_config_content(browser, project_name, label_config)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    # hack to wait for the validation api to be called
    time.sleep(2)
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and not(@disabled)]")
        )
    )
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    browser.execute_script("arguments[0].click();", submit_button)
    dialogue_box = WebDriverWait(browser, LONG_TIMEOUT * 2).until(
        EC.visibility_of_element_located(
            (By.ID, "confirm_deployement_dialogs")
        )
    )

    assert (
        "Do you want to deploy the preannotation server after saving config?"
        in dialogue_box.text
    )
    confirm_btn = dialogue_box.find_element_by_xpath(".//div[text()='Yes']")
    browser.execute_script("arguments[0].click();", confirm_btn)

    message = (
        WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )

    assert "Project config saved" in message

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='left-panel']/a[contains(@href, '/tasks')]")
        )
    )
    tasks_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(tasks_url)
    ensure_deployment(browser, project_name)


def wait_for_training_completion(browser, project_name, deploy):
    retry = 1
    running_xpath = f'//div[contains(text(), "Training (step 1 of 3)" )]'
    while retry < 3:
        try:
            WebDriverWait(browser, LONG_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, running_xpath))
            )
            break
        except Exception:
            browser.refresh()
            retry += 1

    completed_class = "bg_status_success"
    failed_class = "bg_status_danger"
    iteration = 1
    element_found = False
    training_success = False
    while iteration < 30:
        for xpath in [completed_class, failed_class]:
            try:
                WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, xpath))
                )
                element_found = True
                break
            except Exception:
                pass
        if element_found:
            training_success = xpath == completed_class
            break
        iteration += 1
    if not training_success:
        raise Exception("Training failed!")
    browser.refresh()
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#projectConfiguration"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form']")
        )
    )
    WebDriverWait(browser, LONG_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "lsPreviewSuccess"))
    )
    config_tab = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//a[@data-bs-target='#configuration']")
        )
    )
    config_tab.click()
    xml_config = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror-code"))
    )
    if deploy:
        assert project_name in xml_config.text
    else:
        assert project_name not in xml_config.text


def enable_active_learning(browser, project_name, deploy):
    mt_id = 1 if deploy else 2
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )

    al_epoch = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "epoch"))
    )
    al_epoch.clear()
    al_epoch.send_keys("10")
    al_save = browser.find_element_by_xpath("//button[text()='Save']")
    browser.execute_script("arguments[0].click();", al_save)
    chk_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "chk_active_learning"))
    )
    browser.execute_script("arguments[0].click();", chk_button)
    al_confirm_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[@class='modal-content']")
        )
    )
    assert (
        "Do you want to deploy the model after successful training?"
        in al_confirm_box.text
    )
    assert (
        "The trained model can also be deployed later "
        "by updating the project configuration" in al_confirm_box.text
    )
    deploy_id = "yesClick" if deploy else "noClick"
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, deploy_id))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, deploy_id))
    ).click()
    chk_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "chk_active_learning"))
    )
    assert chk_button.get_property("checked") is True
    if deploy:
        assert (
            "(Auto deployment enabled)"
            in browser.find_element_by_xpath(
                "//label[@for='flexSwitchCheckChecked']"
            ).text
        )
    else:
        assert (
            "(Auto deployment disabled)"
            in browser.find_element_by_xpath(
                "//label[@for='flexSwitchCheckChecked']"
            ).text
        )

    import_tasks(project_name)
    browser.refresh()
    wait_for_training_completion(browser, project_name, deploy)


def verify_prediction_inside_labeling_page(browser, project_name, _id):
    labeling_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling?task_id={_id}"
    )
    browser.get(labeling_url)
    wait_for_labeling_page_load(browser)
    prediction = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-container"))
    )
    assert "Model (SparkNLP Pre-annotation)" in prediction.text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-container"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "htx-text"))
    )


def get_model_type_of_project(browser, project_name):
    setup_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    browser.get(setup_url)
    training_type_dropdown_xpath = (
        '//select[@placeholder="--' 'Choose Training Type--"]'
    )
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, training_type_dropdown_xpath)
        )
    )

    select_training_type = Select(dropdown)
    return select_training_type.first_selected_option.text


def set_licensed_training(browser, project_name):
    setup_training_tab_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#trainingActiveLearning"
    browser.get(setup_training_tab_url)
    retry = 1
    while retry < 3:
        try:
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "chk_active_learning"))
            )
            licensed_radio_xpath = "//input[@id='licensed-radio-button']"
            licensed_radio = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.XPATH, licensed_radio_xpath)
                )
            )
            licensed_radio.click()
            break
        except Exception:
            browser.refresh()
            retry += 1
    save = browser.find_element_by_xpath("//button[contains(@class, 'saveTrainingActiveLearning')]")
    browser.execute_script("arguments[0].click();", save)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='toastModalId']")
        )
    )


def check_if_licensed_option_is_disabled(browser, project_name):
    setup_training_tab_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#trainingActiveLearning"
    browser.get(setup_training_tab_url)
    licensed_radio_xpath = "//input[@id='licensed-radio-button']"
    licensed_radio = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, licensed_radio_xpath)
        )
    )
    assert licensed_radio.get_property("disabled") == True


def check_for_transfer_learning(browser, project_name):
    setup_training_tab_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#trainingActiveLearning"
    browser.get(setup_training_tab_url)
    transfer_learning_dropdown_xpath = "//input[@id='dropdownTransferLearning']"
    
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.XPATH, transfer_learning_dropdown_xpath)
            )
        )
    except:
        return False
    return True


def is_training_tab_visible(browser, project_name):
    setup_page_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup"
    browser.get(setup_page_url)

    training_tab_xpath = "//li[@id='tabtrainingActiveLearning']"
    try:
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, training_tab_xpath))
        )
        browser.find_element_by_xpath(training_tab_xpath)
    except:
        return False
    return True


def upload_custom_script(browser, project_name, filename="custom_script.py"):
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='modal_upload_script']/span")
        )
    ).click()
    script_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//select[@name='scriptType']")
        )
    )
    Select(script_selection).select_by_visible_text("NER Script")
    file_upload = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='file-input']"))
    )
    file_upload.send_keys(f"/tests/utils/{filename}")
    if filename != "custom_script.py":
        retry = 1
        while retry < 4:
            try:
                error_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "err_message")
                    )
                )
                assert f"Invalid file" in error_message.text
                break
            except Exception:
                retry += 1
    else:
        retry = 1
        browser.refresh()
        while retry < 2:
            try:
                WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//button[@id='modal_upload_script']/span")
                    )
                ).click()
                uploaded_file = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                    EC.visibility_of_element_located((By.ID, "available_files"))
                )
                if f"{filename}" in error_message.text:
                    break
                retry += 1
            except Exception:
                retry += 1
        uploaded_file = WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "available_files"))
        )
        assert f"{filename}" in uploaded_file.text

