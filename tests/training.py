"""
These tests are for running against annotationlab frontend
"""
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.utils.helpers import *
from tests.utils.active_learning_helper import *
from tests.utils import api_helper
from tests.utils.label_config import test_assertion_training_label_config


def test_assertion_training(browser):
    project_name = unique_project_name("test_assertion_training")
    delete_existing_license()
    r = api_helper.upload_license()
    if isinstance(r, str):
        raise Exception(r)
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    upload_custom_script(browser, project_name)
    browser.refresh()
    upload_custom_script(browser, project_name, filename="al_import.json")
    browser.refresh()
    btn_train_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn_train_model"))
    )
    browser.execute_script("arguments[0].click();", btn_train_model)
    confirmation_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, f"//div[@class='modal-content']"
        ))
    )
    assert (
        f"Custom Training Script found" in
        confirmation_dialog.text
    )
    mt_proceed_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'noClick'))
    )
    browser.execute_script("arguments[0].click();", mt_proceed_dialog)
    wait_for_training_completion(browser, project_name, False)
    delete_project(browser, project_name)


def test_trigger_training_with_deploy(browser):
    project_name = unique_project_name("test_trigger_training_with_deploy")
    delete_existing_license()
    r = api_helper.upload_license()
    if isinstance(r, str):
        raise Exception(r)
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    embedding_name = "embeddings_clinical"
    download_embeddings_or_models(browser, embedding_name)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    retry = 1
    while retry < 3:
        try:
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "chk_active_learning"))
            )
            embeddings_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.visibility_of_element_located((
                    By.XPATH, "//select[@placeholder='--Select Embeddings--']"
                ))
            )
            Select(embeddings_selection).select_by_visible_text(embedding_name)
            break
        except Exception:
            browser.get(
                f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
                "/setup#trainingActiveLearning"
            )
            retry += 1
    save = browser.find_element_by_xpath("//button[text()='Save']")
    browser.execute_script("arguments[0].click();", save)
    trigger_training(
        browser, project_name, license_required=True
    )
    browser.find_element_by_xpath(
        "//div[@id='left-panel']/a[contains(@href, '/tasks')]"
    ).click()
    preannotation_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "btn_pre_annotation"))
    )
    # select certain tasks
    for i in range(26, 31):
        task_id = browser.find_element_by_id(f"chk-{i}")
        browser.execute_script("arguments[0].click();", task_id)
    browser.execute_script("arguments[0].click();", preannotation_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.ID, "preannotate_msg"),
            "Do you want to preannotate all selected task(s)?"
        )
    )
    preannotation_info_box = browser.find_element_by_xpath(
        "//div[@id='show_pre_annotation_msg']")

    assert (
        f'ago by admin from project "{project_name}"' in
        preannotation_info_box.text
    )
    confirm_btn = browser.find_element_by_id("confirm_pre_annotate")
    browser.execute_script("arguments[0].click();", confirm_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "btn-outline-primary"),
            "Task(s) running"
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.ID, "btn_pre_annotation"),
            "Preannotate"
        )
    )
    preannotation_statuses = [
        em.get_attribute("title") for em in
        browser.find_elements_by_class_name("pre_annotation_status")
    ]
    assert any(
        "Preannotation completed" in status for status in
        preannotation_statuses
    )
    delete_project(browser, project_name)
    api_helper.delete_model_embeddings(
        name=embedding_name, type="Embeddings"
    )
    


def test_trigger_training_without_deploy(browser):
    project_name = unique_project_name("test_trigger_training_without_deploy")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name, test_assertion_training_label_config)
    tasks = []
    with open("/tests/active-learning/all_kinds_of_tasks.json") as f:
        data = json.load(f)
        for each in data.get("examples"):
            results = [
                result for result in each.get("completions")[0].get("result")
                if result.get("type") not in ["relation", "choices"]
            ]
            each["completions"][0]["result"] = results
            a_task = {
                "completions": each.get("completions"),
                "predictions": [],
                "created_at": str(datetime.now()).split(".")[0],
                "created_by": "admin",
                "data": each.get("data")
            }
            tasks.append(a_task)
    import_tasks(project_name, tasks)
    trigger_training(
        browser,
        project_name,
        deploy=False,
        license_required=True,
        model_type="assertion"
    )
    delete_project(browser, project_name)


def test_licensed_embedding(browser):
    project_name = unique_project_name("test_licensed_embedding")
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    trigger_training(browser, project_name)

    tasks_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(tasks_url)
    preannotation_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "btn_pre_annotation"))
    )

    # select certain tasks
    for i in range(26, 31):
        task_id = browser.find_element_by_id(f"chk-{i}")
        browser.execute_script("arguments[0].click();", task_id)

    browser.execute_script("arguments[0].click();", preannotation_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.ID, "preannotate_msg"),
            "Do you want to preannotate all selected task(s)?"
        )
    )
    preannotation_info_box = browser.find_element_by_xpath(
        "//div[@id='show_pre_annotation_msg']")

    assert (
        f"ago by admin from project \"{project_name}\"" in
        preannotation_info_box.text
    )

    confirm_btn = browser.find_element_by_id("confirm_pre_annotate")
    browser.execute_script("arguments[0].click();", confirm_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "btn-outline-primary"),
            "Task(s) running"
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT * 3).until(
        EC.text_to_be_present_in_element(
            (By.ID, "btn_pre_annotation"),
            "Preannotate"
        )
    )
    preannotation_statuses = [
        em.get_attribute("title") for em in
        browser.find_elements_by_class_name("pre_annotation_status")
    ]
    assert any(
        "Preannotation completed" in status for status in
        preannotation_statuses
    )
    delete_project(browser, project_name)


def test_custom_script_training(browser):
    project_name = unique_project_name("test_custom_script_training")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    trigger_training(browser, project_name, deploy=False)
    delete_project(browser, project_name)


def test_abort_training(browser):
    project_name = unique_project_name("test_abort_training")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    trigger_training(browser, project_name, wait_for_training=False)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    btn_abort_train_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "abort_train"))
    )
    browser.execute_script("arguments[0].click();", btn_abort_train_model)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, f"//div[@id='confirmAbortModal']"
        ))
    )
    mt_proceed_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'confirmModalYes'))
    )
    browser.execute_script("arguments[0].click();", mt_proceed_dialog)
    assert (
        "Training/Deploy model aborted."
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )
    delete_project(browser, project_name)
