"""
These tests are for running against annotationlab frontend
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.utils import api_helper
from tests.utils.helpers import *
from tests.utils.active_learning_helper import *
from tests.utils.label_config import (
    test_image_classification_config,
    test_incompatible_config_with_spark_nlp_label_config,
    test_classfication_config
)

def test_incompatible_config_with_spark_nlp(browser):
    project_name = unique_project_name("test_incompatible_config_with_spark_nlp")
    create_project(browser, project_name)
    save_config(
        project_name,
        test_incompatible_config_with_spark_nlp_label_config
    )
    open_spark_nlp_config(browser, project_name)
    model_check = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//div[@id='ner_dl']//input[@type='checkbox']"))
    )
    browser.execute_script("arguments[0].click();", model_check)
    add_btn = browser.find_element_by_xpath("//button[text()='Add Label']")
    browser.execute_script("arguments[0].click();", add_btn)
    custom_alert_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//*[@id='lsPreviewError']/p"
        ))
    )
    assert (
        "toName=\"text\" not found in names"
        in custom_alert_message.text
    )
    delete_project(browser, project_name)


def test_empty_spark_nlp_label_in_config(browser):
    project_name = unique_project_name("test_empty_spark_nlp_label_in_config")
    create_project(browser, project_name)
    save_config(project_name)
    open_spark_nlp_config(browser, project_name)
    add_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//button[text()='Add Label']"))
    )
    browser.execute_script("arguments[0].click();", add_btn)
    custom_alert_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.ID, "alertModalBody"
        ))
    )
    assert (
        "Please select preannotation label(s)!"
        in custom_alert_message.text
    )

    create_sample_task(browser, project_name)
    preannotation = browser.find_element_by_id("btn_pre_annotation")
    browser.execute_script("arguments[0].click();", preannotation)
    preannotation_info_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "show_preannotated_labels"))
    )
    assert (
        "Select Preannotated Labels"
        in preannotation_info_box.text
    )
    assert bool(
        preannotation_info_box.find_element_by_xpath(
            ".//a[text()='Go to Setup Page']"
        )
    )
    delete_project(browser, project_name)


def test_update_advance_option(browser):
    project_name = unique_project_name("test_update_advance_option")
    create_project(browser, project_name)
    save_config(project_name)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    embeddings_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//select[@placeholder='--Select Embeddings--']"
        ))
    )
    Select(embeddings_selection).select_by_visible_text("bert_base_cased")

    al_val_split = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "valSplit"))
    )
    al_val_split.clear()
    al_val_split.send_keys("0.5")
    al_batch = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "batch"))
    )
    al_batch.clear()
    al_batch.send_keys("50")
    al_epoch = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "epoch"))
    )
    al_epoch.clear()
    al_epoch.send_keys("50")

    al_lr_rate = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "lr"))
    )
    al_lr_rate.clear()
    al_lr_rate.send_keys("0.005")

    al_lr_rate_decay = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "lrDecay"))
    )
    al_lr_rate_decay.clear()
    al_lr_rate_decay.send_keys("0.004")

    al_dropout = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "dropout"))
    )
    al_dropout.clear()
    al_dropout.send_keys("0.4")

    # To do
    # Set Tag
    # tag_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
    #     EC.element_to_be_clickable((By.ID, "txttag"))
    # )
    # tag_box.click()
    # WebDriverWait(browser, DRIVER_TIMEOUT).until(
    #     EC.visibility_of_element_located((By.ID, "export_tag"))
    # )
    # validated_tag = WebDriverWait(browser, DRIVER_TIMEOUT).until(
    #     EC.presence_of_element_located((
    #         By.XPATH, "//label[contains(., 'Validated')]"
    #     ))
    # )
    # browser.execute_script("arguments[0].click();", validated_tag)
    # tag_box.send_keys("Validated")

    save = browser.find_element_by_xpath("//button[text()='Save']")
    browser.execute_script("arguments[0].click();", save)
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    embeddings_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//select[@placeholder='--Select Embeddings--']"
        ))
    )
    assert (
        "bert_base_cased" in
        Select(embeddings_selection).first_selected_option.text
    )
    models_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//select[@placeholder='--Choose Training Type--']"
        ))
    )
    assert (
        "ner" in
        Select(models_selection).first_selected_option.text
    )
    assert "0.5" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "valSplit"))
    ).get_attribute("value")
    assert "50" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "batch"))
    ).get_attribute("value")
    assert "50" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "epoch"))
    ).get_attribute("value")
    assert "0.005" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "lr"))
    ).get_attribute("value")
    assert "0.004" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "lrDecay"))
    ).get_attribute("value")
    assert "0.4" == WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.NAME, "dropout"))
    ).get_attribute("value")

    # uncomment after tag is set above
    # assert (
    #     "Validated"
    #     in WebDriverWait(browser, DRIVER_TIMEOUT)
    #     .until(EC.visibility_of_element_located((By.ID, "tag_list")))
    #     .text
    # )
    delete_project(browser, project_name)


def test_active_learning_without_deploy(browser):
    project_name = unique_project_name("test_active_learning_without_deploy")
    delete_existing_license()
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    enable_active_learning(browser, project_name, False)
    delete_project(browser, project_name)


def test_default_model_selection(browser):
    project_name = unique_project_name("default_model_selection_test")
    create_project(browser, project_name)

    # default model after creating project should be ner
    assert get_model_type_of_project(browser, project_name) == 'ner'

    # change config type to classification
    choice_name = "moods"
    save_config(project_name, test_classfication_config.format("moods"))
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, project_name)
        )
    )
    assert get_model_type_of_project(browser, project_name) == choice_name
    delete_project(browser, project_name)


def test_transfer_learning_option(browser):
    delete_existing_license()
    project_name = unique_project_name("test_transfer_learning_option")
    create_project(browser, project_name)

    check_if_licensed_option_is_disabled(browser, project_name)
    is_transfer_learning_visible = check_for_transfer_learning(browser, project_name)
    assert is_transfer_learning_visible == False

    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    set_licensed_training(browser, project_name)
    is_transfer_learning_visible = check_for_transfer_learning(browser, project_name)
    assert is_transfer_learning_visible == False

    #transfer learning is only available for medical NER models 
    download_embeddings_or_models(browser, "ner_mit_movie_simple_distilbert_base_cased")
    is_transfer_learning_visible = check_for_transfer_learning(browser, project_name)
    assert is_transfer_learning_visible == False


    download_embeddings_or_models(browser, "ner_jsl")
    is_transfer_learning_visible = check_for_transfer_learning(browser, project_name)
    assert is_transfer_learning_visible == True
    api_helper.delete_model_embeddings(name="ner_jsl", type="Models")
    api_helper.delete_model_embeddings(name="ner_mit_movie_simple_distilbert_base_cased", type="Models")
    delete_project(browser, project_name)


def test_download_embeddings_alert(browser):
    delete_existing_license()
    project_name = unique_project_name("test_transfer_learning_option")
    create_project(browser, project_name)
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    set_licensed_training(browser, project_name)
    browser.get(ANNOTATIONLAB_URL)
    wait_for_projects_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Models Hub"))
    ).click()
    wait_for_modelshub_page_load(browser)
    download_embeddings_or_models(browser, 'ner_jsl')
    
    setup_training_tab_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#trainingActiveLearning"
    browser.get(setup_training_tab_url)
    transfer_learning_dropdown_xpath = "//input[@id='dropdownTransferLearning']"
    
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, transfer_learning_dropdown_xpath)
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//li[contains(@class, 'list-li')]//span[contains(text(), 'ner_jsl')]")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@id, 'confirmModalBody')]")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@id, 'confirmModalYes')]")
        )
    ).click()
    alert_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@id, 'alertMessage')]")
        )
    )

    assert "Please download embeddings: embeddings_clinical" in alert_message.text
    api_helper.delete_model_embeddings(name="ner_jsl", type="Models")
    delete_project(browser, project_name)


def test_transfer_learning_option_with_expired_license(browser):
    delete_existing_license()
    project_name = unique_project_name("test_transfer_learning_option_with_expired_license")
    create_project(browser, project_name)

    upload_expired_license()

    is_transfer_learning_visible = check_for_transfer_learning(browser, project_name)
    assert is_transfer_learning_visible == False
    delete_project(browser, project_name)

def test_hide_training_tab(browser):
    project_name = unique_project_name("test_hide_training_tab")
    create_project(browser, project_name)

    assert is_training_tab_visible(browser, project_name) == True
    save_config(project_name, test_image_classification_config)
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                project_name,
            )
        )
    )
    assert is_training_tab_visible(browser, project_name) == False
    delete_project(browser, project_name)


def test_show_either_error_or_warning_message(browser):
    project_name = unique_project_name("test_show_either_error_or_warning_message")
    create_project(browser, project_name)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    btn_train_model = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn_train_model"))
    )
    browser.execute_script("arguments[0].click();", btn_train_model)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, f"//div[@class='modal-content']"
        ))
    )
    mt_proceed_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'yesClick'))
    )
    browser.execute_script("arguments[0].click();", mt_proceed_dialog)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "error_message"))
    )
    assert len(browser.find_elements_by_id("error_message"))>0
    assert not len(browser.find_elements_by_class_name("text-warning"))
    embeddings_selection = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//select[@placeholder='--Select Embeddings--']"
        ))
    )
    Select(embeddings_selection).select_by_visible_text("bert_base_cased")
    assert len(browser.find_elements_by_class_name("text-warning"))>0
    assert not len(browser.find_elements_by_id("error_message"))
    delete_project(browser, project_name)


def test_check_split_dataset_disable_tags_and_validation_split(browser):
    project_name = unique_project_name("test_check_split_dataset_disable_tags_and_validation_split")
    create_project(browser, project_name)
    save_config(project_name)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_active_learning"))
    )
    tag_list = browser.find_element_by_id("txttag")
    validation_split = browser.find_element_by_name("valSplit")
    assert tag_list.get_property('disabled') == False
    assert validation_split.get_property('disabled') == False
    split_dataset_checkbox = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk_test_train_used"))
    )
    browser.execute_script("arguments[0].click();", split_dataset_checkbox)
    tag_list = browser.find_element_by_id("txttag")
    validation_split = browser.find_element_by_name("valSplit")
    assert tag_list.get_property('disabled') == True
    assert validation_split.get_property('disabled') == True
    delete_project(browser, project_name)

