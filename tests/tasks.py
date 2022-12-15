"""
Tests for tasks related stuffs
"""
import json
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from tests.utils.helpers import *
from tests.utils.dummy_tasks import * 


def test_import_task(browser):
    project_name = unique_project_name("test_import_task")
    create_project(browser, project_name)
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    task = {
        "created_at": "2020-05-19 12:15:42",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": "",
        },
        "id": 0,
    }

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "upload-dialog-msg"))
    )
    assert (
        "Tasks created:1"
        in browser.find_element_by_xpath(
            '//*[@id="upload-dialog-msg"]/h2'
        ).text
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "chk-1"))
    )
    chk_0_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "chk-1"))
    )
    browser.execute_script(
        "arguments[0].click();",
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "chk-1"))
        ),
    )
    if not chk_0_box.get_attribute("checked"):
        browser.execute_script(
            "arguments[0].click();",
            WebDriverWait(browser, DRIVER_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "chk-1"))
            ),
        )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.XPATH, '//button[contains(@value,"incomplete")]')
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "delete_task_s"))
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "confirmModalYes"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "confirmModalYes"))
    ).click()

    assert (
        "Task(s) successfully deleted!"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )
    delete_project(browser, project_name)


def test_is_task_title_exist(browser):
    project_name = unique_project_name("test_is_task_title_exist")
    create_project_with_task(browser, project_name)
    tasks_page_url = browser.current_url
    browser.find_element_by_xpath(
        '//*[@id="tasks"]/tbody/tr[1]/td[1]/div[1]/a'
    ).click()
    assert (
        len(browser.find_element_by_xpath('//*[@class="edit_title" ] ').text)
        != 0
    )
    browser.get(tasks_page_url)
    delete_project(browser, project_name)


def test_add_task_title(browser):
    project_name = unique_project_name("test_add_task_title")
    add_task_title(browser, project_name)
    delete_project(browser, project_name)


def test_update_task_title(browser):
    project_name = unique_project_name("test_update_task_title")
    add_task_title(browser, project_name)
    title = "Updated task title"
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
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "ls-skip-btn",
            )
        )
    )
    update_title(browser, title)
    tasks_page_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(tasks_page_url)
    wait_for_task_page_load(browser)
    task_1 = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    assert title in task_1.text
    delete_project(browser, project_name)


def test_delete_task(browser):
    project_name = unique_project_name("test_delete_task")
    create_project_with_task(browser, project_name)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
    ).click()
    browser.find_element_by_class_name("delete_task_s").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "confirmModalYes"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "confirmModalYes"))
    ).click()
    assert (
        "Task(s) successfully deleted!"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )
    delete_project(browser, project_name)


def test_delete_task_using_filter(browser):
    project_name = unique_project_name("test_task_delete_using_filter")
    create_project_with_task(browser, project_name)
    tasks_before = [
        task.text.strip().split("\n")[0].strip()
        for task in browser.find_elements_by_xpath('//*[@id="tasks"]/tbody/tr')
    ]

    browser.find_element_by_id("task_search").send_keys("2")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "tr"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "delete_task_s"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "delete_task_s"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.ID, "confirmModalYes")
        )
    ).click()

    table = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "table"))
    )
    WebDriverWait(table, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.TAG_NAME, "img"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "task-id"))
    )
    tasks_after = [
        task.text.strip().split("\n")[0].strip()
        for task in browser.find_elements_by_xpath('//*[@id="tasks"]/tbody/tr')
    ]
    assert set(tasks_before) - set(tasks_after) == set(["Task 2"])
    delete_project(browser, project_name)


def test_duplicate_tasks(browser):
    project_name = unique_project_name("test_duplicate_tasks")
    create_project(browser, project_name)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, project_name))
    ).click()

    # create duplicate tasks
    import_json_input_xpath = '//input[@id="url-input"]'
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, import_json_input_xpath))
    ).send_keys(json.dumps(DUMMY_TASKS))

    import_button = '//button[@id="url-button"]'
    browser.find_element_by_xpath(import_button).click()
    explore = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    )
    browser.execute_script("arguments[0].click();", explore)
    wait_for_task_page_load(browser)
    duplicates_filter = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "duplicates_filter"))
    )
    browser.execute_script("arguments[0].click();", duplicates_filter)

    box_content = browser.find_element_by_class_name("modal-content")
    WebDriverWait(box_content, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-body"))
    )
    WebDriverWait(box_content, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "li"))
    )
    lis = browser.find_elements_by_xpath('//div[@class="modal-body"]/ol/li')
    expected_list_text = [
        "Task 1 is duplicated to task(s) 5",
        "Task 2 is duplicated to task(s) 3, 4",
        "Task 6 is duplicated to task(s) 7",
    ]
    result = [li.text for li in lis]
    assert expected_list_text == result

    # Perform delete
    delete_button = '//button[@id="delete_btn"]'
    browser.find_element_by_xpath(delete_button).click()
    modal_confirm_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "confirmModalYes"))
    )
    browser.execute_script("arguments[0].click();", modal_confirm_btn)
    wait_for_task_page_load(browser)
    duplicates_filter = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "duplicates_filter"))
    )
    browser.execute_script("arguments[0].click();", duplicates_filter)

    box_content = browser.find_element_by_class_name("modal-content")
    WebDriverWait(box_content, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-body"))
    )
    content = WebDriverWait(box_content, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "span"))
    )
    assert "No duplicates found" in content.text

    delete_project(browser, project_name)


def test_assign_user_to_task(browser):
    assignee = "collaborate"
    project_name = unique_project_name("test_assign_user_to_task")
    create_project_with_task(browser, project_name)

    setup_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )

    # Add collaborate to team as annotator
    members_info = {assignee: ["Annotator"]}
    add_to_team(browser, members_info)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    # Assign user to task
    assign_task_to_user(browser, assignee, "2")

    login_as(assignee, assignee, browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Shared With Me"))
    )
    browser.find_element_by_partial_link_text("Shared With Me").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.PARTIAL_LINK_TEXT,
                project_name,
            )
        )
    ).click()
    wait_for_task_page_load(browser)

    assert len(browser.find_elements_by_tag_name("tr")) == 1
    assert "Assignee" not in browser.find_element_by_id("task_filter").text

    login_as("admin", "admin", browser)
    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(task_url)
    wait_for_task_page_load(browser)
    # Revoke user from task

    check_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()
    if not check_box.get_attribute("checked"):
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
        ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "assign_assignee"))
    ).click()

    revoke_user = browser.find_elements_by_class_name("dropdown_item")
    for user in revoke_user:
        if user.text == assignee:
            user.find_element_by_class_name("fa-times-circle").click()
            break

    assert (
        "Task(s) revoked from user 'collaborate'."
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )

    delete_project(browser, project_name)


def test_assign_reviewer_to_task(browser):
    reviewer = "collaborate"
    project_name = unique_project_name("test_assign_reviewer_to_task")
    create_project_with_task(browser, project_name)

    task_1 = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling?task_id=1"
    browser.get(task_1)
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "btn-save-completion"))
    )
    btn_save_completion = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-save-completion"))
    )
    browser.execute_script("arguments[0].click();", btn_save_completion)
    # Save Completion
    element = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-submit-completion"))
    )
    # Submit Completion
    browser.execute_script("arguments[0].click();", element)
    modal = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-modal-content"))
    )
    ok_btn = WebDriverWait(modal, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-btn-primary"))
    )
    browser.execute_script("arguments[0].click();", ok_btn)

    setup_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )

    # Add collaborate to team as reviewer
    members_info = {reviewer: ["Reviewer"]}
    add_to_team(browser, members_info)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    # Assign user to task
    assign_task_to_reviewer(browser, reviewer, "1")

    login_as(reviewer, reviewer, browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Shared With Me"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, project_name))
    ).click()
    wait_for_task_page_load(browser)
    assert len(browser.find_elements_by_tag_name("tr")) == 1
    assert "Reviewer" not in browser.find_element_by_id("task_filter").text
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()

    # Add your review
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Add your review']"))
    )

    add_your_review = browser.find_element_by_xpath(
        "//*[text()='Add your review']"
    )
    browser.execute_script("arguments[0].click();", add_your_review)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-popover"))
    )
    browser.find_element_by_id("txt_review_comment").send_keys("Good Work!")
    approve = browser.find_element_by_xpath("//*[text()='Approve']")
    browser.execute_script("arguments[0].click();", approve)
    submit_review = browser.find_element_by_id("btn-submit-review")
    browser.execute_script("arguments[0].click();", submit_review)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, "btn-submit-review"))
    )
    ant_collapse_item = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-collapse-header"))
    )
    browser.execute_script("arguments[0].click();", ant_collapse_item)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "ant-collapse-item-active")
        )
    )

    anticon_info_circle = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "anticon-info-circle")
        )
    )
    browser.execute_script("arguments[0].click();", anticon_info_circle)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-popover"))
    )
    assert (
        "Approve"
        in browser.find_element_by_class_name("ant-popover-title").text
    )

    login_as("admin", "admin", browser)
    # Checks Reviewed count on task page
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    delete_project(browser, project_name)


def test_task_status_after_completion_delete(browser):
    project_name = unique_project_name("test_task_status_after_completion_delete")
    create_project_with_task(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    assert (
        "2 Incomplete"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[contains(@value,"incomplete")]')
            )
        )
        .text
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "1"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_changes("/labeling?task_id=1")
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    )
    # Save Completion
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "btn-save-completion"))
    )

    btn_save_completion = browser.find_element_by_id("btn-save-completion")
    browser.execute_script("arguments[0].click();", btn_save_completion)

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
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    assert (
        "2 Incomplete"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[contains(@value,"incomplete")]')
            )
        )
        .text
    )

    assert (
        "0 In Progress"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"inprogress")]'
        ).text
    )

    delete_project(browser, project_name)


def test_comments(browser):
    project_name = unique_project_name("test_comments")
    create_project_with_task(browser, project_name)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    )
    # Add a comment
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "comment"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "comment"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txt_comment"))
    )
    modal_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    browser.find_element_by_id("txt_comment").send_keys("This is comment!")

    WebDriverWait(modal_dialog, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
    ).click()

    assert (
        "Comment updated!"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )

    # Update a comment
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "comment"))
    )
    browser.find_elements_by_class_name("comment")[0].click()

    modal_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    browser.find_element_by_id("txt_comment").send_keys("This is comment!")
    WebDriverWait(modal_dialog, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "fa-comment-alt"))
    )

    assert (
        "Comment updated!"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )

    # View comment on annotator screen
    assignee = "collaborate"
    setup_url = (
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    browser.get(setup_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )
    # Add collaborate to team as annotator
    members_info = {assignee: ["Annotator"]}
    add_to_team(browser, members_info)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    # Assign user to task
    assign_task_to_user(browser, assignee, "2")
    login_as(assignee, assignee, browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "comment"))
    )
    browser.find_elements_by_class_name("comment")[0].click()

    modal_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    assert (
        "This is comment!This is comment!"
        in browser.find_element_by_id("txt_comment").text
    )

    login_as("admin", "admin", browser)

    # Delete a comment
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "comment"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "comment"))
    ).click()

    modal_dialog = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
    )
    WebDriverWait(modal_dialog, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-danger"))
    ).click()

    assert (
        "Comment removed!"
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )
    delete_project(browser, project_name)


def test_task_status_user_wise(browser):
    project_name = unique_project_name("test_task_status_user_wise")
    create_project(browser, project_name)
    members_info = {
        "collaborate": ["Annotator"],
        "readonly": ["Annotator"],
    }
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    add_to_team(browser, members_info)
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    wait_for_import_page_load(browser)
    task = USER_WISE_STATUS_COMPLETIONS

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()

    login_as("collaborate", "collaborate", browser)
    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(task_url)
    wait_for_task_page_load(browser)
    set_view_as(browser, "Annotator")
    assert (
        "1 In Progress"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"inprogress")]'
        ).text
    )
    assert (
        "1 Submitted"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"submitted")]'
        ).text
    )
    assert (
        "1 Reviewed"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"reviewed")]'
        ).text
    )

    login_as("readonly", "readonly", browser)
    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(task_url)

    wait_for_task_page_load(browser)
    set_view_as(browser, "Annotator")
    assert (
        "1 In Progress"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"inprogress")]'
        ).text
    )
    assert (
        "1 Submitted"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"submitted")]'
        ).text
    )
    assert (
        "1 Reviewed"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"reviewed")]'
        ).text
    )

    login_as("admin", "admin", browser)
    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(task_url)

    wait_for_task_page_load(browser)
    set_view_as(browser, "Manager")
    assert (
        "2 In Progress"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"inprogress")]'
        ).text
    )
    assert (
        "1 Submitted"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"submitted")]'
        ).text
    )

    delete_project(browser, project_name)


def test_next_task(browser):
    tasks = [
        {
            "completions": [
                {
                    "created_username": "collaborate",
                    "created_ago": "2021-09-09T12:17:27.391Z",
                    "lead_time": 7,
                    "result": [
                        {
                            "value": {
                                "start": 8,
                                "end": 11,
                                "text": "DEF",
                                "labels": ["CARDINAL"],
                            },
                            "id": "AXYDwBtWma",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        }
                    ],
                    "honeypot": True,
                    "id": 1001,
                    "updated_at": "2021-09-09T12:18:36.167514Z",
                    "updated_by": "collaborate",
                    "submitted_at": "2021-09-09T18:03:35.713",
                }
            ],
            "predictions": [],
            "created_at": "2021-09-09 12:17:27",
            "created_by": "collaborate",
            "data": {"text": "This is DEF task", "title": ""},
            "id": 1,
        },
        {
            "completions": [
                {
                    "created_username": "collaborate",
                    "created_ago": "2021-09-09T12:17:49.989Z",
                    "lead_time": 10,
                    "result": [
                        {
                            "value": {
                                "start": 8,
                                "end": 11,
                                "text": "JKL",
                                "labels": ["CARDINAL"],
                            },
                            "id": "GjvjL58fvD",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        }
                    ],
                    "honeypot": True,
                    "id": 3001,
                    "updated_at": "2021-09-09T12:19:19.181066Z",
                    "updated_by": "collaborate",
                    "submitted_at": "2021-09-09T18:04:18.635",
                }
            ],
            "predictions": [],
            "created_at": "2021-09-09 12:17:50",
            "created_by": "collaborate",
            "data": {"text": "This is JKL task", "title": ""},
            "id": 3,
        },
        {
            "completions": [
                {
                    "created_username": "collaborate",
                    "created_ago": "2021-09-09T12:17:35.815Z",
                    "lead_time": 31,
                    "result": [
                        {
                            "value": {
                                "start": 8,
                                "end": 11,
                                "text": "GHI",
                                "labels": ["CARDINAL"],
                            },
                            "id": "bBx4BOoajs",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                        }
                    ],
                    "honeypot": True,
                    "id": 2001,
                    "updated_at": "2021-09-09T12:19:09.115353Z",
                    "updated_by": "collaborate",
                    "submitted_at": "2021-09-09T18:04:08.660",
                }
            ],
            "predictions": [],
            "created_at": "2021-09-09 12:17:36",
            "created_by": "collaborate",
            "data": {"text": "This is GHI task", "title": ""},
            "id": 2,
        },
        {"text": "This is ABC task"},
        {"text": "This is MNO task"},
        {"text": "This is PQR task"},
        {"text": "This is STU task"},
    ]

    project_name = unique_project_name("test_next_task_annotator1")
    create_project(browser, project_name, "sequential")
    members_info = {
        "collaborate": ["Annotator"],
        "readonly": ["Reviewer"],
    }
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("/setup#projectTeam")
    )
    add_to_team(browser, members_info)
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(tasks))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()

    # Assign reviewer to task
    assign_reviewer = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_reviewer"))
    )
    browser.execute_script("arguments[0].click();", assign_reviewer)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//details[@class='assign_reviewer']"
                "//label[contains(@class, 'dropdown_item')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", dropdown)
    check_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()
    if not check_box.get_attribute("checked"):
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
        ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, '//button[contains(@value,"inprogress")]')
        )
    )
    # Assign assignee to task
    assign_assignee = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_assignee"))
    )
    browser.execute_script("arguments[0].click();", assign_assignee)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//details[@class='assign_assignee']"
                "//label[contains(@class, 'dropdown_item')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", dropdown)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )

    # Skip for annotator
    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    set_view_as(browser, "Annotator")
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling")
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    )
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    before_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "4" in before_skip_task_id
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "5"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "5" in after_skip_task_id
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "6"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "6" in after_skip_task_id

    # Skip for reviewer
    login_as("readonly", "readonly", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    set_view_as(browser, "Reviewer")
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling")
    wait_for_labeling_page_load(browser)
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    before_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "1" in before_skip_task_id
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "2"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "2" in after_skip_task_id
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "3"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "3" in after_skip_task_id

    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_view_as_role(browser):
    login_as("admin", "admin", browser)
    project_name = unique_project_name("test_view_as_role")
    task_page_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    user = "collaborate"
    create_project_with_task(browser, project_name)
    members_info = {
        user: ["Annotator", "Reviewer", "Manager"],
    }
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("/setup#projectTeam")
    )
    add_to_team(browser, members_info)

    browser.get(task_page_url)
    wait_for_task_page_load(browser)
    # Assign user to task
    assign_task_to_user(browser, user, "2")

    login_as(user, user, browser)
    browser.get(task_page_url)
    wait_for_task_page_load(browser)
    set_view_as(browser, "Manager")
    assert (
        "2 Incomplete"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"incomplete")]'
        ).text
    )

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[contains(text(), "View as" )]')
        )
    ).click()

    # Open Annotator View
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[contains(text(), "Annotator" )]')
        )
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[contains(text(), "Annotator" )]')
        )
    ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "record"))
    )

    assert (
        "1 Incomplete"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"incomplete")]'
        ).text
    )
    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_consistence_view_as(browser):
    project_name = unique_project_name("test_consistence_view_as")
    create_project_with_task(browser, project_name)
    set_view_as(browser, "Annotator")
    browser.refresh()
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownViewasFilter"))
    )
    assert "A" in dropdown.text
    set_view_as(browser, "Manager")
    browser.refresh()
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownViewasFilter"))
    )
    assert "M" in dropdown.text
    set_view_as(browser, "Annotator")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()
    wait_for_labeling_page_load(browser)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "dropdownViewasFilter"))
    )
    assert "A" in dropdown.text
    delete_project(browser, project_name)


def test_view_as_next_task(browser):
    tasks = DUMMY_TASK_FOR_NEXT_COMPLETION

    project_name = unique_project_name("test_view_as_next_task")
    create_project(browser, project_name, "sequential")
    members_info = {
        "collaborate": ["Annotator", "Reviewer"],
    }
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.url_contains("/setup#projectTeam")
    )
    add_to_team(browser, members_info)
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    wait_for_import_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(tasks))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()

    # Assign reviewer to task
    assign_reviewer = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_reviewer"))
    )
    browser.execute_script("arguments[0].click();", assign_reviewer)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//details[@class='assign_reviewer']"
                "//label[contains(@class, 'dropdown_item')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", dropdown)
    check_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()
    if not check_box.get_attribute("checked"):
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
        ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, '//button[contains(@value,"inprogress")]')
        )
    )
    # Assign assignee to task
    assign_assignee = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "assign_assignee"))
    )
    browser.execute_script("arguments[0].click();", assign_assignee)
    dropdown = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//details[@class='assign_assignee']"
                "//label[contains(@class, 'dropdown_item')]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", dropdown)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )

    # Skip for annotator
    login_as("collaborate", "collaborate", browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    set_view_as(browser, "Annotator")
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling")
    wait_for_labeling_page_load(browser)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ls-skip-btn"))
    )
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    before_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "4" in before_skip_task_id
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "5"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "5" in after_skip_task_id
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "6"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "6" in after_skip_task_id

    # Skip for reviewer
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks")
    wait_for_task_page_load(browser)
    set_view_as(browser, "Reviewer")
    wait_for_task_page_load(browser)
    browser.get(f"{ANNOTATIONLAB_URL}/#/project/{project_name}/labeling")
    wait_for_labeling_page_load(browser)
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    before_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "1" in before_skip_task_id
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "2"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "2" in after_skip_task_id
    skip_btn = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ls-skip-btn"))
    )
    browser.execute_script("arguments[0].click();", skip_btn)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, ("//span[contains(@class, 'labeling_heading')]")), "3"
        )
    )
    after_skip_task_id = browser.find_element_by_class_name(
        "labeling_heading"
    ).text
    assert "3" in after_skip_task_id

    login_as("admin", "admin", browser)
    delete_project(browser, project_name)


def test_task_status_after_new_annotator_assigned(browser):
    project_name = unique_project_name(
        "test_task_status_after_new_annotator_assigned")
    create_project(browser, project_name)
    members_info = {
        "collaborate": ["Annotator"],
        "readonly": ["Annotator"],
    }
    browser.get(
        f"{ANNOTATIONLAB_URL}/#/project/{project_name}/setup#projectTeam"
    )
    add_to_team(browser, members_info)
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    wait_for_import_page_load(browser)
    task = DUMMY_SUBMITTED_TASK

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()

    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(task_url)
    wait_for_task_page_load(browser)

    assert (
        "0"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"inprogress")]//span[contains(@class, "badge")]'
        ).text
    )
    assert (
        "1"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"submitted")]//span[contains(@class, "badge")]'
        ).text
    )

    # Revoke user from task
    assignee = "collaborate"
    check_box = WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    )
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "ckbCheckAll"))
    ).click()
    if not check_box.get_attribute("checked"):
        WebDriverWait(browser, DRIVER_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "ckbCheckAll"))
        ).click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "assign_assignee"))
    ).click()

    revoke_user = browser.find_elements_by_class_name("dropdown_item")
    for user in revoke_user:
        if user.text == assignee:
            user.find_element_by_class_name("fa-times-circle").click()
            break

    assert (
        "Task(s) revoked from user 'collaborate'."
        in WebDriverWait(browser, DRIVER_TIMEOUT)
        .until(EC.visibility_of_element_located((By.ID, "toastModalMessage")))
        .text
    )

    # Assign new user to task
    assignee = "readonly"
    assign_task_to_user(browser, assignee, "1")
    wait_for_task_page_load(browser)

    assert (
        "1"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"inprogress")]//span[contains(@class, "badge")]'
        ).text
    )
    assert (
        "0"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"submitted")]//span[contains(@class, "badge")]'
        ).text
    )

    delete_project(browser, project_name)


def test_owner_have_reviewer_permission(browser):
    project_name = unique_project_name("test_owner_have_reviewer_permission")
    create_project(browser, project_name)

    # add project team
    manage_team_url = (
        f"{ANNOTATIONLAB_URL}/#project/{project_name}/setup#projectTeam"
    )
    browser.get(manage_team_url)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "txtuser"))
    )
    members_info = {
        "collaborate": ["Annotator"]
    }
    add_to_team(browser, members_info)

    # Import submitted task by collaborate user
    import_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/import"
    browser.get(import_url)
    wait_for_import_page_load(browser)
    task = DUMMY_SUBMITTED_TASK
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "url-input"))
    ).send_keys(json.dumps(task))
    browser.find_element_by_id("url-button").click()
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Explore Tasks")
        )
    ).click()

    task_url = f"{ANNOTATIONLAB_URL}/#/project/{project_name}/tasks"
    browser.get(task_url)
    wait_for_task_page_load(browser)
    
    # set view as to Reviewer
    set_view_as(browser, "Reviewer")
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Task 1"))
    ).click()

    wait_for_labeling_page_load(browser)

    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Add your review']"))
    )

    # Perform Review
    add_your_review = browser.find_element_by_xpath(
        "//*[text()='Add your review']"
    )
    browser.execute_script("arguments[0].click();", add_your_review)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-popover"))
    )
    browser.find_element_by_id("txt_review_comment").send_keys("Good Work!")
    approve = browser.find_element_by_xpath("//*[text()='Approve']")
    browser.execute_script("arguments[0].click();", approve)
    submit_review = browser.find_element_by_id("btn-submit-review")
    browser.execute_script("arguments[0].click();", submit_review)
    WebDriverWait(browser, DRIVER_TIMEOUT).until(
        EC.invisibility_of_element_located((By.ID, "btn-submit-review"))
    )
    browser.get(task_url)
    wait_for_task_page_load(browser)
    # Check Reviewed status count
    assert (
        "1 Reviewed"
        in browser.find_element_by_xpath(
            '//button[contains(@value,"reviewed")]'
        ).text
    )

    delete_project(browser, project_name)