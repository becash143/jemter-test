"""
Tests for labeling config related stuffs
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils.helpers import *


def test_visual_config_add_labels(browser):
    project_name = unique_project_name("test_visual_config_add_labels")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectConfiguration"
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "lsPreviewSuccess")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "4. Configuration")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "4. Configuration"))
    ).click()
    toggle_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Visual"))
    )
    browser.execute_script("arguments[0].click();", toggle_btn)
    # Add labels
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[@id='textarea_label_label']/form/textarea",
            )
        )
    ).send_keys("test_label")
    add_label = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "visual-add-btn"))
    )
    browser.execute_script("arguments[0].click();", add_label)
    label_list = browser.find_elements_by_xpath(
        "//div[contains(@class, 'current-labels')]/ul/li"
    )
    assert len(label_list) == 19
    # Remove label
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Visual"))
    )
    delete_label_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, '//li[@id="PERSON"]/button'))
    )
    browser.execute_script("arguments[0].click();", delete_label_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "FAC"))
    )
    label_list = browser.find_elements_by_xpath(
        "//div[contains(@class, 'current-labels')]/ul/li"
    )
    assert len(label_list) == 18
    # Add new Labels section
    add_config = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//details[@id="dropdownAddLabels"]/summary',
            )
        )
    )
    browser.execute_script("arguments[0].click();", add_config)
    add_label = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "labels",
            )
        )
    )
    browser.execute_script("arguments[0].click();", add_label)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "Test_Label"))
    )
    assert (
        len(
            browser.find_elements_by_xpath(
                "//div[contains(@class, 'visual-wrapper')]"
            )
        )
        == 2
    )
    # Delete Labels section
    browser.execute_script(
        "arguments[0].click();",
        browser.find_elements_by_class_name("delete-icon")[0],
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "Test_Label"))
    )
    assert (
        len(
            browser.find_elements_by_xpath(
                "//div[contains(@class, 'visual-wrapper')]"
            )
        )
        == 1
    )
    delete_project(browser, project_name)


def test_visual_config_add_choices(browser):
    project_name = unique_project_name("test_visual_config_add_choices")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectConfiguration"
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "lsPreviewSuccess")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "4. Configuration")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "4. Configuration"))
    ).click()
    toggle_visual = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Visual"))
    )
    browser.execute_script("arguments[0].scrollIntoView();", toggle_visual)
    browser.execute_script("arguments[0].click();", toggle_visual)

    # Add new Choices section
    add_choices = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//details[@id="dropdownAddLabels"]/summary',
            )
        )
    )
    browser.execute_script("arguments[0].click();", add_choices)
    choice_option = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "choices",
            )
        )
    )
    browser.execute_script("arguments[0].click();", choice_option)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "visual-wrapper",
            )
        )
    )
    assert (
        len(
            browser.find_elements_by_xpath(
                "//div[contains(@class, 'visual-wrapper')]"
            )
        )
        == 2
    )
    input_name = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(@placeholder, 'Add Choices')]")
        )
    )
    input_name.clear()
    input_name.send_keys("sentiment")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[@id='textarea_label_label']/form/textarea",
            )
        )
    ).click()

    # add choice
    add_choice = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(@placeholder, 'Add Choices')]")
        )
    )

    browser.execute_script("arguments[0].value='Sentiment'", add_choice)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "visual-add-btn",
            )
        )
    )
    add_choice_btn = browser.find_elements_by_class_name("visual-add-btn")[1]
    browser.execute_script("arguments[0].click();", add_choice_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "label_choice",
            )
        )
    )
    choice_list = browser.find_elements_by_class_name("label_choice")
    assert len(choice_list) == 3
    # Remove choice
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "Sentiment"))
    )
    browser.execute_script(
        "arguments[0].click();",
        browser.find_element_by_xpath('//li[@id="Sentiment"]/button'),
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, "Sentiment"))
    )
    choice_list = browser.find_elements_by_class_name("label_choice")
    assert len(choice_list) == 2
    # Delete Choices section
    browser.execute_script(
        "arguments[0].click();",
        browser.find_elements_by_class_name("delete-icon")[1],
    )
    assert (
        len(
            browser.find_elements_by_xpath(
                "//div[contains(@class, 'visual-wrapper')]"
            )
        )
        == 1
    )
    delete_project(browser, project_name)

def test_duplicate_label(browser):
    project_name = unique_project_name("test_duplicate_label")
    browser.get(f"{ANNOTATIONLAB_URL}/#/projects")
    create_project(browser, project_name)
    setup_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectConfiguration"
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "lsPreviewSuccess")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "4. Configuration")
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "4. Configuration"))
    ).click()
    config_textarea = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'CodeMirror-code')]")
        )
    )

    content = """<View>
        <Labels name="label" toName="text">
            <Label value="CARDINAL" model="ner_onto_100" background="#af906b"/>
            <Label value="CARDINAL" model="ner_onto_100" background="#af906b"/>
        </Labels>
        <Text name="text" value="$text"/>
        </View>      
    """
    actions = ActionChains(browser)
    actions.move_to_element(config_textarea)
    actions.click()
    if OS_BASE == "Darwin":
        actions.key_down(Keys.COMMAND).send_keys("a").key_up(
            Keys.COMMAND
        ).send_keys(content).perform()
    else:
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).send_keys(content).perform()

    custom_alert_message = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((
            By.XPATH, "//*[@id='lsPreviewError']/p"
        ))
    )
    assert (
        "Duplicate label"
        in custom_alert_message.text
    )
    delete_project(browser, project_name)

