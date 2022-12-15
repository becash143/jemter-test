from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tests.utils.helpers import *
from tests.utils.active_learning_helper import *
from tests.utils.api_helper import ensure_license
from tests.utils.label_config import (
    free_ner_model_config,
    license_ner_model_config,
    free_classification_model_config,
    license_classification_model_config,
)


def test_download_and_deploy_free_ner_model(browser):
    delete_existing_license()
    browser.get(ANNOTATIONLAB_URL)
    wait_for_projects_page_load(browser)
    project_name = unique_project_name("test_download_and_deploy_free_ner_model")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Models Hub"))
    ).click()
    wait_for_modelshub_page_load(browser)
    download_embeddings_or_models(browser, "nerdl_snips_100d")
    create_project(browser, project_name)
    task = {
        "text": "book a spot for nona gray  myrtle and alison"
                " at a top-rated brasserie that is distant from"
                " wilson av on nov  the 4th  2030 that serves ouzeri"
    }
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='cuisine']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        free_ner_model_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, task)
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)
    delete_project(browser, project_name)


def test_download_and_deploy_license_ner_model(browser):
    ensure_license()
    browser.get(ANNOTATIONLAB_URL)
    wait_for_projects_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Models Hub"))
    ).click()
    wait_for_modelshub_page_load(browser)
    download_embeddings_or_models(browser, "ner_deid_generic_glove")
    project_name = unique_project_name("test_download_and_deploy_license_ner_model")
    create_project(browser, project_name)
    task = {
        "text": "A. Record date : 2093-01-13, David Hale, M.D.,"
                " Name : Hendrickson, Ora MR. # 7194334 Date : 01/13/93"
                " PCP : Oliveira, 25 -year-old, Record date : 1-11-2000."
                " Cocke County Baptist Hospital. 0295 Keats Street. "
                "Phone +1 (302) 786-5227."
    }
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='NAME']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        license_ner_model_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, task)
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)
    delete_project(browser, project_name)


def test_download_embeddings(browser):
    delete_existing_license()
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    wait_for_modelshub_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Available Embeddings")
        )
    )
    download_embeddings_or_models(browser, "biobert_clinical_base_cased")
    delete_model_embeddings(
        browser, "biobert_clinical_base_cased", "embeddings"
    )


def test_download_and_deploy_free_classification_model(browser):
    delete_existing_license()
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    wait_for_modelshub_page_load(browser)

    project_name = unique_project_name("test_download_and_deploy_free_classification_model")
    download_embeddings_or_models(browser, "classifierdl_use_snips")
    create_project(browser, project_name)

    task = {
        "text": "I want to bring six of us to a bistro in town that serves "
                "hot chicken sandwich that is within the same area and show "
                "weather forcast for the stone memorial at st joseph "
                "peninsula state park on one hour from now"
    }
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//input[@class='ant-checkbox-input' and @name='BookRestaurant']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        free_classification_model_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, task)
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)
    assert any(
        prediction.get_attribute("checked")
        for prediction in browser.find_elements_by_xpath(
            "//input[@class='ant-checkbox-input']"
        )
    ) is True
    delete_project(browser, project_name)


def test_download_and_deploy_license_classification_model(browser):
    ensure_license()
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    wait_for_modelshub_page_load(browser)
    download_embeddings_or_models(browser, "biobert_pubmed_base_cased")
    download_embeddings_or_models(browser, "classifierdl_pico_biobert")

    project_name = unique_project_name("test_download_and_deploy_license_classification_model")
    create_project(browser, project_name)
    task = {
        "text": "A total of 10 adult daily smokers who reported at least one "
                "stressful event and coping episode and provided "
                "post-quit data."
    }
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//input[@class='ant-checkbox-input' and @name='PARTICIPANTS']]"
    )
    update_and_deploy_pretrained_model(
        browser,
        project_name,
        license_classification_model_config,
        interface_preview_xpath,
    )
    import_tasks(project_name, task)
    preannotate_task_by_id(browser, project_name, 1, "Preannotation completed")
    verify_prediction_inside_labeling_page(browser, project_name, 1)
    assert any(
        prediction.get_attribute("checked")
        for prediction in browser.find_elements_by_xpath(
            "//input[@class='ant-checkbox-input']"
        )
    ) is True
    delete_project(browser, project_name)


def test_delete_downloaded_models(browser):
    delete_existing_license()
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    wait_for_modelshub_page_load(browser)
    download_embeddings_or_models(browser, "onto_300")
    download_embeddings_or_models(browser, "sent_electra_small_uncased")
    delete_model_embeddings(browser, "ner_onto_300", "model")
    delete_model_embeddings(
        browser, "sent_electra_small_uncased", "embeddings"
    )


def test_rename_trained_model(browser):
    project_name = unique_project_name("test_rename_trained_model")
    create_project(browser, project_name)
    save_config(project_name)
    import_tasks(project_name)
    trigger_training(browser, project_name, deploy=False)
    model_name = f"ner_{project_name}.model"
    new_model_name = "ner_updated_name"
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Available Models')]")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_input_search_models"))
    ).send_keys(model_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//span[contains(@id, '{model_name}')]")
        )
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'tag_more_option_block')]")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//li[contains(@class, 'tag_more_option_li')]"
                "//span[contains(text(), 'Rename')]",
            )
        )
    ).click()

    # Special chars in name
    text_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//label[@title='{model_name}']//input")
        )
    )
    actions = ActionChains(browser)
    actions.move_to_element(text_box)
    actions.click()
    actions.key_down(
        Keys.CONTROL
    ).send_keys("a").key_up(Keys.CONTROL).perform()
    actions.send_keys("@").perform()
    actions.send_keys(Keys.ENTER).perform()

    alert_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(@id, 'alertMessage' )]")
        )
    )
    assert (
        "Name can only use alphanumeric, underscores(_), periods(.) and "
        "hyphens(-) with maximum 100 characters."
        in alert_message.text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@id, 'alertModalOk')]")
        )
    ).click()

    # Reserved prefix in name
    text_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//label[@title='{model_name}']//input")
        )
    )
    actions = ActionChains(browser)
    actions.move_to_element(text_box)
    actions.click()
    actions.key_down(
        Keys.CONTROL
    ).send_keys("a").key_up(Keys.CONTROL).perform()
    actions.send_keys("ner").perform()
    actions.send_keys(Keys.ENTER).perform()

    alert_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(@id, 'alertMessage' )]")
        )
    )
    assert (
        "Invalid name: Models cannot be renamed with prefixes ner, "
        "classification and assertion"
        in alert_message.text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@id, 'alertModalOk')]")
        )
    ).click()

    # Valid rename
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//div[contains(@id, 'available_model_{model_name}')]"
                "//div[contains(@class, 'tag_more_option_block')]"
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//li[contains(@class, 'tag_more_option_li')]"
                "//span[contains(text(), 'Rename')]",
            )
        )
    ).click()
    text_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//label[@title='{model_name}']//input")
        )
    )
    actions = ActionChains(browser)
    actions.move_to_element(text_box)
    actions.click()
    actions.key_down(
        Keys.CONTROL
    ).send_keys("a").key_up(Keys.CONTROL).perform()
    actions.send_keys("updated_name").perform()
    actions.send_keys(Keys.ENTER).perform()

    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Available Models')]")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//span[contains(@id, '{model_name}')]")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "txt_input_search_models"))
    ).send_keys(new_model_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//span[contains(@id, '{new_model_name}' )]")
        )
    )

    # validate updated name on project configuration page
    open_spark_nlp_config(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(@id, '{new_model_name}')]")
        )
    )
    delete_project(browser, project_name)


def test_delete_trained_model(browser):
    browser.get(ANNOTATIONLAB_URL)
    model_name = "ner_updated_name"
    delete_model_embeddings(browser, model_name, "model")


def test_language_filter(browser):
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "card-body")
        )
    )
    assert "English" in browser.find_elements_by_class_name("card-body")[0].text

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.ID, "dropdownLanguageFilter")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.ID, "dropdownLanguageFilterBody")
        )
    )

    filter_body_element = browser.find_element_by_id("dropdownLanguageFilterBody")
    all_filter_item = filter_body_element.find_elements_by_class_name("list-li")
    for li in all_filter_item:
        if "German" in li.text:
            li.click()
            break

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "card-body")
        )
    )

    for card_body in browser.find_elements_by_class_name("card-body"):
        assert "English" not in card_body.text
        assert "German" in card_body.text
