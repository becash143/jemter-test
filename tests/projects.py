"""
Tests for project related stuffs
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from tests.utils.helpers import *


def test_create_project(browser):
    create_project(browser, "Create_Demo_Project")
    delete_project(browser, "Create_Demo_Project")


def test_update_project(browser):
    old_name = unique_project_name("Update_Project")
    new_name = f"{old_name}1"
    create_project(browser, old_name)
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{old_name}/setup"
    browser.get(setup_url)
    update = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "update_data"))
    )
    browser.execute_script("arguments[0].click();", update)
    project_name_field = browser.find_element_by_name("ProjectName")
    project_name_field.clear()
    project_name_field.send_keys(new_name)
    assert "" == browser.find_element_by_id("err_name").text
    project_desc_field = browser.find_element_by_name("ProjectDesc")
    project_desc_field.clear()
    project_desc_field.send_keys(
        "This is a Named Entity Recognition Development Project."
    )
    save_project = browser.find_element_by_id("save_project")
    browser.execute_script("arguments[0].click();", save_project)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(EC.url_contains(new_name))
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "breadcrumb-wrapper"), new_name
        )
    )
    assert (
        new_name
        in browser.find_element_by_class_name("breadcrumb-wrapper").text
    )
    delete_project(browser, new_name)


def test_project_switching(browser):
    project_name_1 = unique_project_name("test_project_switching_1")
    project_name_2 = unique_project_name("test_project_switching_2")
    create_project_with_task(browser, project_name_1)
    create_project(browser, project_name_2)
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name_2}/setup"
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//a[@title='{project_name_2}']/span")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "search_project_name")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@title,'{project_name_1}')]")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains(project_name_1)
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "search_project_name")
        )
    )
    assert (
        project_name_1 in WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"pagination-link")]')
            )
        ).text
    )
    delete_project(browser, project_name_2)
    delete_project(browser, project_name_1)


def test_manage_project_team(browser):
    project_name = unique_project_name("test_manage_project_team")
    create_project_with_task(browser, project_name)
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup"
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Project Team"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )
    # Add memmbers
    members_info = {
        "readonly": ["Annotator"],
        "collaborate": ["Annotator", "Reviewer"],
    }
    add_to_team(browser, members_info)
    browser.refresh()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Project Team"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "scopes"))
    )
    current_team = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "scope_tag"))
    )
    members = [c.text.replace("\nx", "") for c in current_team]

    expected = ["A readonly", "A R collaborate"]
    assert all(ex in members for ex in expected)

    # Remove collaborate from team
    remove_from_team(browser, "collaborate")

    current_team = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "scope_tag"))
    )
    members = [c.text.replace("\nx", "") for c in current_team]
    assert expected[1] not in members
    delete_project(browser, project_name)


def test_updating_config_with_existing_tasks(browser):
    project_name = unique_project_name(
        "test_updating_config_with_existing_tasks"
    )
    create_task_with_completion(browser, project_name)
    # Try switching to Classification
    content = """
        <View>
      <Text name="text" value="$text"/>
      <Choices name="surprise" toName="text" choice="single" model="classification_classifierdl_use_emotion">
        <Choice value="surprise"/>
        <Choice value="sadness"/>
        <Choice value="fear"/>
        <Choice value="joy"/>
      </Choices>
    </View>
    """

    validate_config_content(browser, project_name, content)
    "You've already completed some tasks" in WebDriverWait(
        browser, DRIVER_TIMEOUT
    ).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "validation",
            )
        )
    ).text
    submit_button = browser.find_element_by_xpath(
        "//button[@id='submit_form']"
    )
    assert submit_button.get_property("disabled") is True
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.ID,
                "chk-1",
            )
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "chk-1",
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    browser.find_element_by_class_name("delete_task_s").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "confirmModalYes")
        )
    ).click()
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and not(contains(@srcdoc, 'QUANTITY'))"
        " and not(contains(@srcdoc, 'LOC'))]"
    )
    validate_config_content(browser, project_name, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )

    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    assert submit_button.get_property("disabled") is False
    delete_project(browser, project_name)


def test_one_label_config_validation(browser):
    project_name = unique_project_name("test_one_label_config_validation")
    create_project(browser, project_name)
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="Fact" background="orange"/>
        </Labels>

        <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project_name, content)
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    assert submit_button.get_property("disabled") == False
    delete_project(browser, project_name)


def test_label_validation_from_config_after_deleting_task(browser):
    project_name = unique_project_name("test_label_validation_from_config_after_deleting_task")
    create_task_with_completion(browser, project_name)

    # Remove label QUANTITY and LOC from config
    content = """<View>
      <Labels name="label" toName="text">
        <Label value="CARDINAL" model="ner_onto_100"/>
        <Label value="EVENT" model="ner_onto_100"/>
        <Label value="WORK_OF_ART" model="ner_onto_100"/>
        <Label value="ORG" model="ner_onto_100"/>
        <Label value="DATE" model="ner_onto_100"/>
        <Label value="GPE" model="ner_onto_100"/>
        <Label value="PERSON" model="ner_onto_100"/>
        <Label value="PRODUCT" model="ner_onto_100"/>
        <Label value="NORP" model="ner_onto_100"/>
        <Label value="ORDINAL" model="ner_onto_100"/>
        <Label value="MONEY" model="ner_onto_100"/>
        <Label value="FAC" model="ner_onto_100"/>
        <Label value="LAW" model="ner_onto_100"/>
        <Label value="TIME" model="ner_onto_100"/>
        <Label value="PERCENT" model="ner_onto_100"/>
        <Label value="LANGUAGE" model="ner_onto_100"/>
      </Labels>

      <Text name="text" value="$text"/>
    </View>
    """

    validate_config_content(browser, project_name, content)
    config_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "validation",
            )
        )
    )
    assert "You've already completed some tasks" in config_message.text
    assert "LOC" in config_message.text
    assert "QUANTITY" in config_message.text
    submit_button = browser.find_element_by_xpath(
        "//button[@id='submit_form']"
    )
    assert submit_button.get_property("disabled") is True
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.ID,
                "chk-1",
            )
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "chk-1",
            )
        )
    ).click()
    delete_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    browser.execute_script("arguments[0].click();", delete_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "confirmModalYes")
        )
    ).click()

    interface_preview_xpath = (
        "//div[@id='editor-wrap' and not(contains(@srcdoc, 'QUANTITY'))"
        " and not(contains(@srcdoc, 'LOC'))]"
    )
    validate_config_content(browser, project_name, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )

    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    assert submit_button.get_property("disabled") is False

    delete_project(browser, project_name)


def test_label_validation_from_config_after_removing_completion_on_task(
    browser,
):
    project_name = unique_project_name("test_label_config_after_removing_completion_on_task")
    # completion that uses "QUANTITY" and "LOC" labels
    create_task_with_completion(browser, project_name)
    # Remove label QUANTITY and LOC from config
    content = """<View>
      <Labels name="label" toName="text">
        <Label value="CARDINAL" model="ner_onto_100"/>
        <Label value="EVENT" model="ner_onto_100"/>
        <Label value="WORK_OF_ART" model="ner_onto_100"/>
        <Label value="ORG" model="ner_onto_100"/>
        <Label value="DATE" model="ner_onto_100"/>
        <Label value="GPE" model="ner_onto_100"/>
        <Label value="PERSON" model="ner_onto_100"/>
        <Label value="PRODUCT" model="ner_onto_100"/>
        <Label value="NORP" model="ner_onto_100"/>
        <Label value="ORDINAL" model="ner_onto_100"/>
        <Label value="MONEY" model="ner_onto_100"/>
        <Label value="FAC" model="ner_onto_100"/>
        <Label value="LAW" model="ner_onto_100"/>
        <Label value="TIME" model="ner_onto_100"/>
        <Label value="PERCENT" model="ner_onto_100"/>
        <Label value="LANGUAGE" model="ner_onto_100"/>
      </Labels>

      <Text name="text" value="$text"/>
    </View>
    """
    interface_preview_xpath = (
        '//div[contains(text(), "") and '
        'contains(text(), "") and contains(text(), "")]'
    )
    validate_config_content(browser, project_name, content)
    validation_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "validation",
            )
        )
    )
    assert "You've already completed some tasks" in validation_message.text
    assert "LOC" in validation_message.text
    assert "QUANTITY" in validation_message.text
    submit_button = browser.find_element_by_xpath(
        "//button[@id='submit_form']"
    )
    assert submit_button.get_property("disabled") is True
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                "Tasks",
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                "Task 1",
            )
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.PARTIAL_LINK_TEXT,
                "Task 1",
            )
        )
    ).click()
    WebDriverWait(browser, 100).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "ls-skip-btn",
            )
        )
    )
    # Delete completion
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "ant-btn-dangerous",
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "ant-popover-buttons",
            )
        )
    )
    delete_button = browser.find_element_by_xpath(
        '//div[@class="ant-popover-buttons"]/button[2]'
    )
    browser.execute_script("arguments[0].click();", delete_button)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (
                By.XPATH,
                '//div[contains(@class,"Completions_deletedcompletioncard")]',
            )
        )
    )
    # verify that completion is deleted
    assert (
        len(
            browser.find_elements_by_xpath(
                '//div[contains(@class,"Completions_deletedcompletioncard")]'
            )
        )
        == 1
    )
    validate_config_content(browser, project_name, content)
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and not(contains(@srcdoc, 'QUANTITY'))"
        " and not(contains(@srcdoc, 'LOC'))]"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )
    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    assert submit_button.get_property("disabled") is False

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Tasks"))
    )
    # Remove label QUANTITY, LOC and CARDINAL from config
    content = """<View>
      <Labels name="label" toName="text">
        <Label value="EVENT" model="ner_onto_100"/>
        <Label value="WORK_OF_ART" model="ner_onto_100"/>
        <Label value="ORG" model="ner_onto_100"/>
        <Label value="DATE" model="ner_onto_100"/>
        <Label value="GPE" model="ner_onto_100"/>
        <Label value="PERSON" model="ner_onto_100"/>
        <Label value="PRODUCT" model="ner_onto_100"/>
        <Label value="NORP" model="ner_onto_100"/>
        <Label value="ORDINAL" model="ner_onto_100"/>
        <Label value="MONEY" model="ner_onto_100"/>
        <Label value="FAC" model="ner_onto_100"/>
        <Label value="LAW" model="ner_onto_100"/>
        <Label value="TIME" model="ner_onto_100"/>
        <Label value="PERCENT" model="ner_onto_100"/>
        <Label value="LANGUAGE" model="ner_onto_100"/>
      </Labels>

      <Text name="text" value="$text"/>
    </View>
    """
    validate_config_content(browser, project_name, content)

    validation_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "validation",
            )
        )
    )
    assert "CARDINAL" in validation_message.text
    assert "You've already completed some tasks" in validation_message.text
    submit_button = browser.find_element_by_xpath(
        "//button[@id='submit_form']"
    )
    assert submit_button.get_property("disabled") is True
    delete_result_btn_xpath = (
        "//h3[text()='Results']/following-sibling::button[1]"
        "[contains(@class, 'ant-btn-danger ')]"
    )
    # Delete result
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                "Tasks",
            )
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.PARTIAL_LINK_TEXT,
                "Task 1",
            )
        )
    ).click()

    delete_result_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                delete_result_btn_xpath,
            )
        )
    )
    browser.execute_script("arguments[0].click();", delete_result_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "ant-popover-buttons",
            )
        )
    )
    confirm_delete_button = browser.find_element_by_xpath(
        '//div[@class="ant-popover-buttons"]/button[2]'
    )
    browser.execute_script("arguments[0].click();", confirm_delete_button)
    assert (
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    delete_result_btn_xpath,
                )
            )
        )
        is True
    )
    element = browser.find_element_by_class_name("ls-update-btn")
    browser.execute_script("arguments[0].click();", element)

    # confirm result is deleted (ie invisibility location condition)
    assert (
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    delete_result_btn_xpath,
                )
            )
        )
        is True
    )
    interface_preview_xpath = (
        "//div[@id='editor-wrap' and not(contains(@srcdoc, 'QUANTITY'))"
        " and not(contains(@srcdoc, 'LOC')) "
        " and not(contains(@srcdoc, 'CARDINAL'))]"
    )
    validate_config_content(browser, project_name, content)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                interface_preview_xpath,
            )
        )
    )

    submit_button = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit_form"))
    )
    assert submit_button.get_property("disabled") is False

    delete_project(browser, project_name)


def test_group(browser):
    project_name = unique_project_name("test_group")
    create_project(browser, project_name)
    browser.get(ANNOTATIONLAB_URL)
    # Create/assign group
    project_tr = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"tr_{project_name}"))
    )
    project_chk_box = project_tr.find_element_by_class_name("checkBoxGroup")
    try:
        project_chk_box.click()
    except ElementClickInterceptedException:
        browser.execute_script("arguments[0].click();", project_chk_box)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownGroupsAssigner"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "addMoreButton"))
    ).click()
    txt_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_name"))
    )
    txt_box.send_keys("Group1")

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn_update_group"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.PARTIAL_LINK_TEXT, project_name), "Group1"
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "dropdownGroupsFilter"))
    ).click()
    labels_dropdown_list = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "dropdownGroupsFilterBody"))
    )
    assert "Group1" in labels_dropdown_list.text

    # Update group
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//li[@value='Group1']//button")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "edit_tag"))
    ).click()
    txt_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_name"))
    )
    txt_box.clear()
    txt_box.send_keys("Edited-Group")
    browser.find_element_by_class_name("btn_update_group").click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.PARTIAL_LINK_TEXT, project_name), "Edited-Group"
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownGroupsFilter"))
    ).click()
    labels_dropdown_list = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownGroupsFilterBody"))
    )
    assert "Edited-Group" in labels_dropdown_list.text

    # Unassign group
    project_tr = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"tr_{project_name}"))
    )
    project_chk_box = project_tr.find_element_by_class_name("checkBoxGroup")
    try:
        project_chk_box.click()
    except ElementClickInterceptedException:
        browser.execute_script("arguments[0].click();", project_chk_box)

    group_dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownGroupsAssigner"))
    )
    group_dropdown.click()
    WebDriverWait(group_dropdown, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "text-danger"))
    ).click()

    project_tr = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"tr_{project_name}"))
    )
    assert "Edited-Group" not in project_tr.text

    # Delete Group
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "dropdownGroupsFilter"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//li[@value='Edited-Group']//button")
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_tag"))
    ).click()
    info_msg = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "delete-group-message"))
    )
    assert (
        'Are you sure you want to delete "Edited-Group" Group?'
        in info_msg.text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn-delete-group"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, f"tr_{project_name}"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "dropdownGroupsFilter"))
    ).click()
    labels_dropdown_list = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "dropdownGroupsFilterBody"))
    )
    assert "Edited-Group" not in labels_dropdown_list.text
    delete_project(browser, project_name)
