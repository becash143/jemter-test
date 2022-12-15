"""
Tests for setup related stuffs
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from tests.utils.helpers import *
import os
from sqlalchemy.sql import text
from datetime import datetime
import psycopg2
from tests.utils.active_learning_helper import import_tasks,save_config

CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
connection = psycopg2.connect(CONNECTION_STRING)
cursor = connection.cursor()

interface_preview_xpath = (
    "//div[@id='editor-wrap' and "
    ".//span[@class='ant-tag' and text()='Organization'] and "
    ".//span[@class='ant-tag' and text()='Fact'] and "
    ".//span[@class='ant-tag' and text()='Money'] and "
    ".//span[@class='ant-tag' and text()='Date']]"
)


def add_testing_assertion_model(project_name):
    update_query = (
        f"select project_id from user_projects where project_name = '{project_name}';"
    )
    cursor.execute(update_query)
    project_id = cursor.fetchone()[0]
    assertion_model_1 = f"""
            insert into trained_models values('assertion_testing_project_manual','2021-04-17 07:33:14.887443+00'
            ,'["Dummy_label1","Dummy_label2","Dummy_label3"]','{{}}','{{}}','{project_id}','glove_100d','/models/trained/assertion_testing_project_manual.model'); 
        """
    cursor.execute(assertion_model_1)
    assertion_model_2 = f"""
            insert into trained_models values('assertion_testing1_project_manual','2021-04-17 07:33:14.887443+00'
            ,'["Dummy_label4","Dummy_label5","Dummy_label6"]','{{}}','{{}}','{project_id}','glove_100d','/models/trained/assertion_testing1_project_manual.model'); 
        """
    cursor.execute(assertion_model_2)
    assertion_model_3 = f"""
            insert into trained_models values('assertion_testing2_project_manual','2021-04-17 07:33:14.887443+00'
            ,'["Dummy_label4","Dummy_label5","Dummy_label6"]','{{}}','{{}}','{project_id}','glove_100d','/models/trained/assertion_testing2_project_manual.model'); 
        """
    cursor.execute(assertion_model_3)
    ner_model_1 = f"""
            insert into trained_models values('ner_testing_project_manual','2021-04-17 07:33:14.887443+00'
            ,'["Dummy_label4","Dummy_label5","Dummy_label6"]','{{}}','{{}}','{project_id}','glove_100d','/models/trained/ner_testing_project_manual.model'); 
        """
    cursor.execute(ner_model_1)
    ner_model_2 = f"""
            insert into trained_models values('ner_testing1_project_manual','2021-04-17 07:33:14.887443+00'
            ,'["Dummy_label4","Dummy_label5","Dummy_label6"]','{{}}','{{}}','{project_id}','glove_100d','/models/trained/ner_testing1_project_manual.model'); 
        """
    cursor.execute(ner_model_2)
    connection.commit()


def delete_assertion_models():
    delete_assertion_model_1 = f"""delete from trained_models where model_name='assertion_testing_project_manual'"""
    cursor.execute(delete_assertion_model_1)
    delete_assertion_model_2 = f"""delete from trained_models where model_name='assertion_testing1_project_manual'"""
    cursor.execute(delete_assertion_model_2)
    delete_assertion_model_3 = f"""delete from trained_models where model_name='assertion_testing2_project_manual'"""
    cursor.execute(delete_assertion_model_3)
    delete_ner_model_1 = (
        f"""delete from trained_models where model_name='ner_testing_project_manual'"""
    )
    cursor.execute(delete_ner_model_1)
    delete_ner_model_2 = (
        f"""delete from trained_models where model_name='ner_testing1_project_manual'"""
    )
    cursor.execute(delete_ner_model_2)
    connection.commit()


def test_validate_assertion_model(browser):
    project = "test_validate_assertion_model"
    create_project(browser, project)
    add_testing_assertion_model(project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Organization" assertion = "true" model= "ner_testing_project_manual" background="darkorange"/>
            <Label value="Fact" background="orange" model="ner_testing_project_manual" />
            <Label value="Money" background="green" />
            <Label value="Date" background="darkblue"/>
            <Label value="Time" background="blue"/>
            <Label value="Ordinal" background="purple"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    text_danger_elements = browser.find_elements_by_class_name("text-danger")
    for validation_text_danger in text_danger_elements:
        text_danger = validation_text_danger.text
        if "(ner_testing_project_manual)" in text_danger:
            assert (
                "Invalid model(s) (ner_testing_project_manual) used for Assertion Status Label(s) (Organization)."
                in text_danger
            )
            break
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    assert submit_button.get_property("disabled") == True
    delete_project(browser, project)


def test_validate_assertion_if_atleast_single_ner_model(browser):
    project = "test_validate_assertion_if_atleast_single_ner_model"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Organization" assertion = "true" model= "assertion_testing_project_manual" background="darkorange"/>
            <Label value="Fact" background="orange" />
            <Label value="Money" background="green" />
            <Label value="Date" background="darkblue"/>
            <Label value="Time" background="blue"/>
            <Label value="Ordinal" background="purple"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    text_danger_elements = browser.find_elements_by_class_name("text-danger")
    for validation_text_danger in text_danger_elements:
        text_danger = validation_text_danger.text
        if "Assertion Status Model" in text_danger:
            assert (
                "To use an Assertion Status Model for preannotation, at least one NER Model should be used in a NER Label."
                in text_danger
            )
            break
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    assert submit_button.get_property("disabled") == True
    delete_project(browser, project)


def test_validate_single_assertion_model_in_config(browser):
    project = "test_validate_single_assertion_model_in_config"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Organization" assertion = "true" model= "assertion_testing_project_manual" background="darkorange"/>
            <Label value="Fact" background="orange" model="ner_testing_project_manual"/>
            <Label value="Money" background="green" assertion = "true" model="assertion_testing1_project_manual"/>
            <Label value="Date" background="darkblue"/>
            <Label value="Time" background="blue"/>
            <Label value="Ordinal" background="purple"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    text_danger_elements = browser.find_elements_by_class_name("text-danger")
    for validation_text_danger in text_danger_elements:
        text_danger = validation_text_danger.text
        if "Preannotation" in text_danger:
            assert (
                "Preannotation using multiple assertion models is not supported at the moment"
                in text_danger
            )
            assert all(
                key in text_danger
                for key in [
                    "assertion_testing1_project_manual",
                    "assertion_testing_project_manual",
                ]
            )
            break
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    assert submit_button.get_property("disabled") == True
    delete_project(browser, project)


def test_validate_hotkeys_in_config(browser):
    project = "test_validate_hotkeys_in_config"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Organization" assertion = "true" hotkey="/" background="darkorange"/>
            <Label value="Fact" background="orange" hotkey="."/>
            <Label value="Money" background="green" assertion = "true" hotkey=","/>
            <Label value="Date" background="darkblue" hotkey="'"/>
            <Label value="Time" background="blue" hotkey="m"/>
            <Label value="Ordinal" background="purple" hotkey="r"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    text_danger_elements = browser.find_elements_by_class_name("text-danger")
    for validation_text_danger in text_danger_elements:
        text_danger = validation_text_danger.text
        if "Fact" in text_danger:
            assert (
                "Fact" in text_danger
                and "Money" in text_danger
                and "Organization" in text_danger
                and "/" in text_danger
                and 'Time' in text_danger
                and 'Ordinal' in text_danger
            )
            break
            assert "Date" not in text_danger
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    assert submit_button.get_property("disabled") is True
    delete_project(browser, project)


def test_validate_model_in_config(browser):
    project = "test_validate_model_in_config"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Organization" background="darkorange"/>
            <Label value="Fact" background="orange" model="ner_testing_manual"/>
            <Label value="Money" background="green" model="ner1_testing_manual"/>
            <Label value="Date" background="darkblue"/>
            <Label value="Time" background="blue"/>
            <Label value="Ordinal" background="purple"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    text_danger_elements = browser.find_elements_by_class_name("text-danger")
    for validation_text_danger in text_danger_elements:
        text_danger = validation_text_danger.text
        if "Invalid" in text_danger:
            assert all(
                key in text_danger
                for key in ["ner1_testing_manual", "ner_testing_manual"]
            )
            assert "Invalid model names in config" in text_danger
            break
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    assert submit_button.get_property("disabled") == True
    delete_project(browser, project)


def test_validate_deployment_models(browser):
    project = "test_validate_deployment_models"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Person" background="red"/>
            <Label value="Organization" background="darkorange"/>
            <Label value="Organism_subdivision" model="ner_testing_project_manual" background="#1a8e43"/>
            <Label value="cell_line" model="ner_onto_100" background="#752f8c"/>
            <Label value="PROBLEM" model="assertion_testing_project_manual" background="#207604"/>
            <Label value="CONTACT" model="assertion_testing1_project_manual" background="#2161c8"/>
            <Label value="Section_Name" model="ner_testing1_project_manual" background="#003f5e"/>
            <Label value="FREQUENCY" model="assertion_testing2_project_manual" background="#f11784"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>"""
    validate_config_content(browser, project, content)
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and "
        ".//span[@class='ant-tag' and text()='Organization'] and "
        ".//span[@class='ant-tag' and text()='Person'] and "
        ".//span[@class='ant-tag' and text()='cell_line'] and "
        ".//span[@class='ant-tag' and text()='PROBLEM']]"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    text_danger_elements = browser.find_elements_by_class_name("text-danger")
    for validation_text_danger in text_danger_elements:
        text_danger = validation_text_danger.text
        if "preannotation" in text_danger:
            assert "Only up to 5 models can be used for preannotation" in text_danger
            break
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='submit_form' and @disabled='']")
        )
    )

    assert submit_button.get_property("disabled") == True
    delete_assertion_models()
    delete_project(browser, project)


def test_validate_models_with_different_embeddings(browser):
    project = "test_validate_models_with_different_embeddings"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="PER" model="ner_dl" background="#fadca2"/>
            <Label value="LOC" model="ner_onto_bert_base_cased"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>"""
    validate_config_content(browser, project, content)
    error_msg_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.ID,
                "lsPreviewError",
            )
        )
    )
    assert (
        "Following models are not using same embeddings. "
        "Select models which are trained using only one embeddings."
        in error_msg_box.text
    )
    # Uncomment this when PR #1597 has been merged
    # assert (
    #     "ner_dl (glove_100d)" in error_msg_box.text
    # )
    # assert (
    #     "ner_onto_bert_base_cased (bert_base_cased)" in error_msg_box.text
    # )
    delete_project(browser, project)


def test_validate_models_with_missing_embeddings(browser):
    # delete embeddings 'bert_base_cased' temporarily
    embedding_name = "bert_base_cased"
    deleted_embeddings = delete_embeddings(embedding_name)

    project = "test_validate_models_with_missing_embeddings"
    create_project(browser, project)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="DATE" model="ner_onto_bert_base_cased"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>"""
    validate_config_content(browser, project, content)
    error_msg_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.ID,
                "lsPreviewError",
            )
        )
    )
    assert (
        "Following embeddings not found. "
        "Upload it or download from Models Hub."
        in error_msg_box.text
    )
    assert (
        "bert_base_cased (Used by ner_onto_bert_base_cased)"
        in error_msg_box.text
    )
    delete_project(browser, project)
    restore_deleted_embeddings(deleted_embeddings)


def test_training_with_no_completion(browser):
    project_name = "test_training_with_no_completion"
    create_project(browser, project_name)
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}"
        "/setup#trainingActiveLearning"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn_train_model"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "yesClick"))
    ).click()
    err = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "error_message"))
    )
    assert "No completions found. Incorrect filter criteria?" in err.text
    delete_project(browser, project_name)
