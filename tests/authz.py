"""
If a project owner shares a project with another user
then the user should be able to access the project
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils.helpers import *


def assert_no_permission(browser, project_name, option):
    # No side menu
    menu = browser.find_elements_by_xpath(
        "//a[contains(@class, 'left-menu-item') and "
        f"contains(text(), '{option}')]")
    assert len(menu) == 0

    # No permission
    url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/{option.lower()}"
    browser.get(url)
    info = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "text-danger"))
    )
    assert (
        "You don't have the permission to access the requested resource"
        in info.text
    )
    url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(url)
    wait_for_task_page_load(browser)


def test_no_project_access(browser):
    login_as("admin", "admin", browser)
    project_name = unique_project_name("test_no_project_access")
    create_project(browser, project_name)
    login_as("collaborate", "collaborate", browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Shared With Me"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "project_tbl"))
    )
    assert (
        project_name not in browser.find_element_by_xpath(
            "//*[@id='project_tbl']/tbody"
        ).text
    )
    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_access_for_annotator_reviewer(browser):
    project_name = unique_project_name("test_access_for_annotator_reviewer")
    create_project_with_task(browser, project_name)
    manage_team_url = (
        f"{ANNOTATIONLAB_URL}/#project/{project_name}/setup#projectTeam"
    )
    browser.get(manage_team_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )

    members_info = {
        "collaborate": ["Annotator"],
        "readonly": ["Reviewer"],
    }
    add_to_team(browser, members_info)
    for user in members_info.keys():
        login_as(user, user, browser)
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((
                By.PARTIAL_LINK_TEXT, "Shared With Me"
            ))
        ).click()
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.presence_of_element_located((
                By.PARTIAL_LINK_TEXT, project_name
            ))
        ).click()
        assert_no_permission(browser, project_name, "Import")
        assert_no_permission(browser, project_name, "Export")
        assert_no_permission(browser, project_name, "Setup")

        # ---------no option to assign/review------------
        assignee = browser.find_elements_by_id("dropdownAssigneeFilter")
        assert len(assignee) == 0
        reviewer = browser.find_elements_by_id("dropdownReviewerFilter")
        assert len(reviewer) == 0

        # -------no access to tasks by default----------
        tasks = browser.find_elements_by_xpath(
            "tr[@class='record']")
        assert len(tasks) == 0

    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_access_for_manager(browser):
    project_name = unique_project_name("test_access_for_manager")
    create_project_with_task(browser, project_name)
    manage_team_url = (
        f"{ANNOTATIONLAB_URL}/#project/{project_name}/setup#projectTeam"
    )
    browser.get(manage_team_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )

    members_info = {
        'collaborate': ['Manager'],
    }
    add_to_team(browser, members_info)

    login_as("collaborate", "collaborate", browser)
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Shared With Me"))
    ).click()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, project_name))
    ).click()

    # can access setup page
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Setup"))
    )
    setup_link = browser.find_element_by_xpath(
        f"//a[contains(@class, 'left-menu-item') and "
        "contains(@href, 'setup')]"
    )
    setup_link.click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "project_detail"))
    )
    # has access to all 4 tabs in setup page
    tab_ids = [
        "tabprojectDescription",
        "tabprojectTeam",
        "tabprojectConfiguration",
        "tabtrainingActiveLearning"
    ]
    for tab_id in tab_ids:
        assert len(browser.find_elements_by_id(tab_id)) == 1

    # has no access to delete project
    delete_btn = browser.find_elements_by_xpath(
        "//button[@text()='Delete Project']")
    assert len(delete_btn) == 0

    # -------- has access to assign/review-----------
    url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(url)
    wait_for_task_page_load(browser)
    assignee = browser.find_elements_by_id("dropdownAssigneeFilter")
    assert len(assignee) == 1
    reviewer = browser.find_elements_by_id("dropdownReviewerFilter")
    assert len(reviewer) == 1

    # -----------can see all tasks---------------
    tasks = browser.find_elements_by_xpath(
        "//tr[@class='record']")
    assert len(tasks) == 2

    # ----------can access labeling page----------
    tasks[0].find_element_by_xpath(
        '//span[contains(@class,"task-id")]'
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//li[contains(@class,"Completions_completion")]'
            )
        )
    )

    # -----------can import tasks---------------
    import_link = browser.find_element_by_xpath(
        "//a[contains(@class, 'left-menu-item') and "
        "contains(@href, 'import')]"
    )
    import_link.click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Add Sample Task"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "tasks"))
    )
    tasks = browser.find_elements_by_xpath(
        "//tr[@class='record']")
    assert len(tasks) == 3

    # ---------assert export--------------
    export_link = browser.find_element_by_xpath(
        "//a[contains(@class, 'left-menu-item') and "
        "contains(@href, 'export')]"
    )
    export_link.click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.ID, "export_block"
            )
        )
    )

    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_non_admin_can_not_access_modelhub(browser):
    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/models")
    div = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "container"))
    )
    assert "You don't have the permission to access" in div.text
    login_as("admin", "admin", browser)


def test_non_admin_can_not_access_settings(browser):
    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/settings")
    div = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "text-danger"))
    )
    assert "You don't have the permission to access" in div.text
    login_as("admin", "admin", browser)


def test_non_admin_can_not_access_users(browser):
    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/users")
    div = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "container"))
    )
    assert "You don't have the permission to access" in div.text
    login_as("admin", "admin", browser)


def test_non_admin_can_not_access_license(browser):
    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/license")
    div = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "container"))
    )
    assert "You don't have the permission to access" in div.text
    login_as("admin", "admin", browser)
