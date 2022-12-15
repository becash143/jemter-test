"""
These tests are for running against annotationlab frontend
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.utils.helpers import *
from tests.utils.active_learning_helper import *
from tests.utils.label_config import (
    ner_dl_label_config,
    assertion_jsl_labels,
    assertion_biobert_labels,
    ner_dl_interface_preview_xpath,
    test_relation_model_label_config,
    test_ner_and_classification_model_label_config,
    test_assertion_model_in_models_hub_label_config,
    test_ner_classification_and_assertion_model_label_config
)
from tests.utils.api_helper import upload_license
from tests.utils.dummy_tasks import * 

def test_deploy_from_setup_page(browser):
    project_name = unique_project_name("test_deploy_from_setup_page")
    delete_existing_license()
    create_project(browser, project_name)
    import_tasks(project_name, DUMMY_TASKS_FOR_AL)
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        ner_dl_label_config,
        ner_dl_interface_preview_xpath,
    )
    delete_project(browser, project_name)


def test_deploy_model_from_task_page(browser):
    project_name = unique_project_name("test_deploy_model_from_task_page")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name, ner_dl_label_config)
    import_tasks(project_name, DUMMY_TASKS_FOR_AL)

    trigger_deployment_from_tasks_page(browser, project_name)
    ensure_deployment(browser, project_name)
    delete_project(browser, project_name)


def test_preannotate_task(browser):
    project_name = unique_project_name("test_preannotate_task")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name, ner_dl_label_config)
    import_tasks(project_name, DUMMY_TASKS_FOR_AL)

    trigger_deployment_from_tasks_page(browser, project_name)
    ensure_deployment(browser, project_name)
    confirm_btn = browser.find_element_by_id("confirm_pre_annotate")
    browser.execute_script("arguments[0].click();", confirm_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//i[@title='Preannotation running']"))
    )
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
    assert "Preannotation Failed" in preannotation_statuses[0]
    assert "Preannotation completed" in preannotation_statuses[1]
    success_task = browser.find_element_by_xpath(
        "//a[contains(@href, 'task_id=1')]"
    )
    browser.execute_script("arguments[0].click();", success_task)
    preannotation_info = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'Completions_item')]")
        )
    )

    assert all(
        msg in preannotation_info.text for msg in
        ["Model (SparkNLP Pre-annotation)", "Created", "just now"]
    )

    delete_project(browser, project_name)


def test_active_learning_with_deploy(browser):
    project_name = unique_project_name("test_active_learning_with_deploy")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    enable_active_learning(browser, project_name, True)
    delete_project(browser, project_name)


def test_large_document_preannotation(browser):
    project_name = unique_project_name("test_large_document_preannotation")
    create_project(browser, project_name)
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        ner_dl_label_config,
        ner_dl_interface_preview_xpath,
    )
    import_tasks(project_name, filename="al_large_task_import.json")
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)
    predicted_labels_list = browser.find_elements_by_xpath(
        "//span[@class='ant-tree-title']/li"
    )
    assert len(predicted_labels_list) > 0
    next_page = browser.find_element_by_xpath("//ul/li[@title='Next Page']")
    browser.execute_script("arguments[0].click();", next_page)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "htx-text"))
    )
    predicted_labels_list = browser.find_elements_by_xpath(
        f"//span[@class='ant-tree-title']/li"
    )
    assert len(predicted_labels_list) > 0
    delete_project(browser, project_name)


def test_relation_model(browser):
    project_name = unique_project_name("test_relation_model")
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    create_project(browser, project_name)
    download_embeddings_or_models(browser, "embeddings_clinical")
    browser.refresh()
    download_embeddings_or_models(browser, "redl_bodypart_problem_biobert")
    browser.refresh()
    download_embeddings_or_models(browser, "ner_jsl")
    browser.refresh()
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='Injury_or_Poisoning']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        test_relation_model_label_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, filename="sample_task.json")
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)

    # Get relations
    relations_list = browser.find_elements_by_xpath(
        f"//span[@class='anticon anticon-swap']"
    )
    assert len(relations_list) > 0
    delete_project(browser, project_name)


def test_assertion_model_in_models_hub(browser):
    project_name = unique_project_name("test_assertion_model_in_models_hub")
    create_project(browser, project_name)
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    download_embeddings_or_models(browser, "embeddings_clinical")
    browser.refresh()
    download_embeddings_or_models(browser, "assertion_jsl")
    browser.refresh()
    download_embeddings_or_models(browser, "ner_jsl")
    browser.refresh()
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='Injury_or_Poisoning']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        test_assertion_model_in_models_hub_label_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, filename="sample_task.json")
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)

    assert any(
        len(browser.find_elements_by_xpath(f"//span[@data-labels='{label}']"))
        for label in assertion_jsl_labels
    ) > 0

    delete_project(browser, project_name)


def test_ner_and_classification_model(browser):
    project_name = unique_project_name("test_ner_and_classification_model")
    create_project(browser, project_name)
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    download_embeddings_or_models(browser, "biobert_pubmed_base_cased")
    browser.refresh()
    download_embeddings_or_models(browser, "classifierdl_gender_biobert")
    browser.refresh()
    download_embeddings_or_models(browser, "jsl_ner_wip_greedy_biobert")
    browser.refresh()
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='Test_Result']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        test_ner_and_classification_model_label_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, filename="sample_task.json")
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)
    assert any(
        prediction.get_attribute("checked")
        for prediction in browser.find_elements_by_xpath(
            "//input[@class='ant-checkbox-input']"
        )
    ) is True
    delete_project(browser, project_name)


def test_ner_classification_and_assertion_model(browser):
    project_name = unique_project_name("test_ner_classification_and_assertion_model")
    create_project(browser, project_name)
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    download_embeddings_or_models(browser, "biobert_pubmed_base_cased")
    browser.refresh()
    download_embeddings_or_models(browser, "classifierdl_gender_biobert")
    browser.refresh()
    download_embeddings_or_models(browser, "assertion_dl_biobert")
    browser.refresh()
    download_embeddings_or_models(browser, "jsl_ner_wip_greedy_biobert")
    browser.refresh()
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='Test_Result']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        test_ner_classification_and_assertion_model_label_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, filename="sample_task.json")
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)

    assert any(
        len(browser.find_elements_by_xpath(f"//span[@data-labels='{label}']"))
        for label in assertion_biobert_labels
    ) > 0

    assert any(
        prediction.get_attribute("checked")
        for prediction in browser.find_elements_by_xpath(
            "//input[@class='ant-checkbox-input']"
        )
    ) is True
    delete_project(browser, project_name)
