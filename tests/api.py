import os
import json
import pytest
import requests
from datetime import datetime
from annotationlab.models.user_projects import UserProjects
from annotationlab.utils.keycloak_cookies import get_cookies
from tests.utils.api_helper import *
from tests.utils.helpers import delete_existing_license
from urllib.parse import urlencode
from tests.utils.label_config import (
    test_classfication_config,
    test_visual_ner_config_for_various_images
)

API_URL = 'http://annotationlab:8200'
cookies = get_cookies()
collaborate_cookie = get_cookies("collaborate", "collaborate")

headers = {
    'Host': API_URL.replace('http://', ''),
    'Origin': API_URL,
    'Content-Type': 'application/json'
}

CSV_COLS = TSV_COLS = [
    'task_id', 'text', 'title', 'completion_id', 'sentiment', 'label']
ZIP_CONTENT = {
    'csv': ['result.csv'],
    'tsv': ['result.csv'],
    'json': ['result.json'],
    'json_min': ['result.json'],
    'conll': ['result.conll'],
    'coco': ['images/', 'result.json', 'sample.jpg']
}


def test_create_project():
    PROJECT_NAME = "test_create_project"
    r = create_project(PROJECT_NAME)
    json_response = r.json()
    assert r.status_code == 201
    assert 'project_name' in json_response
    delete_project(PROJECT_NAME)


def test_create_project_with_reserved_names():
    names = ["permission", "name", "count"]
    for name in names:
        r = create_project(name)
        json_response = r.json()
        assert r.status_code == 400
        assert (
            'Cannot use reserved names. Please try another.'
            in json_response["error"]
        )


def test_orphaned_project():
    PROJECT_NAME = "test_orphaned_project"
    r = create_project(PROJECT_NAME)
    UserProjects.delete_user_project(PROJECT_NAME)
    r = create_project(PROJECT_NAME)
    json_response = r.json()
    assert r.status_code == 400
    assert 'Name not available, please try another.' in json_response.get(
        "error")
    delete_project(PROJECT_NAME)


def test_update_project():
    PROJECT_NAME = "test_demo_project"
    r = create_project(PROJECT_NAME)
    update_project_url = f'{API_URL}/api/projects/{PROJECT_NAME}'
    update_project(PROJECT_NAME, update_project_url)
    PROJECT_NAME = "test_update_project"
    update_project(PROJECT_NAME, update_project_url)
    delete_project(PROJECT_NAME)


def test_save_config():
    PROJECT_NAME = "test_save_config"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    delete_project(PROJECT_NAME)


def test_default_model_of_project():

    PROJECT_NAME = "default_model_test_project"
    create_project(PROJECT_NAME)

    # default model type should be ner
    assert get_model_type_of_project(PROJECT_NAME) == 'ner'

    # change project config to classification
    save_config(PROJECT_NAME, test_classfication_config.format("sentiment"))
    assert get_model_type_of_project(PROJECT_NAME) == 'classification'

    delete_project(PROJECT_NAME)


def test_save_suspicious_label_config():
    PROJECT_NAME = "test_save_suspicious_label_config"
    create_project(PROJECT_NAME)
    config_url = f'{API_URL}/api/projects/{PROJECT_NAME}/save-config'
    label_config = """
        <View>

            <script>alert(1)</script>

        </View>
    """
    r = requests.post(
        config_url,
        data={"label_config": label_config},
        cookies=cookies
    )

    assert r.status_code == 400
    assert 'Suspicious content detected' in r.text
    delete_project(PROJECT_NAME)


def test_import_task_from_json_input():
    project_name = "test_import_task_from_json_input"
    create_project_with_task(project_name)
    delete_project(project_name)


def test_import_task_from_file_input():
    project_name = "test_import_task_from_file_input"
    create_project(project_name)
    save_config(project_name)
    import_url = f'{API_URL}/api/projects/{project_name}/import'
    data = [
        {"text": "Test task 1 from file input"},  # dict
        [
            {"text": "Test task 2 from file input"},
            {"text": "Test task 3 from file input"},
        ],  # list
    ]
    for index, d in enumerate(data, 1):
        with open(f"/tmp/upload_{index}.json", "w+") as fp:
            json.dump(d, fp)
            fp.seek(0)
            files = {"filename": fp}
            r = requests.post(
                import_url,
                files=files,
                cookies=cookies
            )
        json_response = r.json()
        assert r.status_code == 201
        assert json_response["task_count"] == index
        assert json_response["task_ids"] == list(range(index, index + index))
    delete_project(project_name)


def test_import_completion():
    PROJECT_NAME = "test_import_completion"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    import_url = f'{API_URL}/api/projects/{PROJECT_NAME}/import'
    data = {
        "completions": [
            {
                "created_ago": "2020-07-18T06:17:12.545Z",
                "created_username": "admin",
                "honeypot": False,
                "id": 1,
                "lead_time": 3.491,
                "result": [
                            {
                                "from_name": "label",
                                "id": "w7PVuIWOwN",
                                "source": "$text",
                                "to_name": "text",
                                "type": "labels",
                                "value": {
                                    "end": 34,
                                    "labels": [
                                        "Money"
                                    ],
                                    "start": 26,
                                    "text": "yourself"
                                }
                            }
                ]
            },
            {
                "created_ago": "2020-07-18T06:17:16.951Z",
                "created_username": "admin",
                "honeypot": False,
                "id": 2,
                "lead_time": 2.666,
                "result": [
                            {
                                "from_name": "label",
                                "id": "Xu_IfgBaOS",
                                "source": "$text",
                                "to_name": "text",
                                "type": "labels",
                                "value": {
                                    "end": 13,
                                    "labels": [
                                        "Organization"
                                    ],
                                    "start": 8,
                                    "text": "faith"
                                }
                            }
                ]
            }
        ],
        "predictions": [],
        "created_at": "2020-11-24 04:55:33",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": "This is one big invalid Task title and it should get stored upto this chars."
        },
        "id": 1
    }
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert 'task_count' in json_response
    assert json_response['task_count'] == 1
    assert 'task_ids' in json_response
    assert len(json_response['task_ids']) == 1
    assert 'task_title_warning' in json_response
    assert json_response['task_title_warning'] == 1

    import_file_path = os.path.join("annotationlab/task_upload_test.json")
    with open(import_file_path, "rb") as file:
        files = {"filename": file}
        r = requests.post(
            import_url, 
            files=files,
            cookies=cookies
        )
    json_response = r.json()
    assert r.status_code == 201
    assert 'task_count' in json_response
    assert json_response['task_count'] == 1
    assert 'task_ids' in json_response
    assert len(json_response['task_ids']) == 1
    assert 'completion_count' in json_response
    assert json_response['completion_count'] == 1

    # Multiple file upload 
    with open(import_file_path, "rb") as file:
        r = requests.post(
            import_url,
            files=[
                ("filename", (file.name.split("/")[-1], file)),
                (
                    "filename",
                    (
                        "test_task_upload_test.json",
                        open(
                            os.path.join("annotationlab/task_upload_test.json"), "rb"
                        ),
                    ),
                ),
            ],
            cookies=cookies,
        )

    json_response = r.json()
    assert r.status_code == 201
    assert 'task_count' in json_response
    assert json_response['task_count'] == 2
    assert 'task_ids' in json_response
    assert len(json_response['task_ids']) == 2
    assert 'completion_count' in json_response
    assert json_response['completion_count'] == 2
    delete_project(PROJECT_NAME)


def test_license_upload():
    delete_existing_license()

    # uploading valid license by admin user
    r = upload_license(ocr=True)
    if isinstance(r, str):
        raise Exception(r)
    assert r.status_code == 200
    json_response = r.json()
    assert "message" in json_response
    assert "uploaded successfully" in json_response["message"]

    # Re upload same license
    r = upload_license(ocr=True)
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "Duplicate license key uploaded" in json_response["error"][0]

    # uploading valid license but not by admin user
    r = upload_license(ocr=True, user='collaborate')
    if isinstance(r, str):
        raise Exception(r)
    assert r.status_code == 403

    # Test case for json file with no license
    license_upload_url = f"{API_URL}/api/licenses"
    license_file_path = os.path.join("annotationlab/config.json")
    with open(license_file_path, "rb") as file:
        files = {"filename": file}
        r = requests.post(license_upload_url,
                          files=files,
                          cookies=cookies
                          )
        json_response = r.json()
        assert r.status_code == 400
        assert "error" in json_response
        assert "Invalid" in json_response["error"][0]

    # Test case for Non JSON file containing no license
    license_file_path = os.path.join("annotationlab/db.py")
    with open(license_file_path, "rb") as file:
        files = {"filename": file}
        r = requests.post(license_upload_url,
                          files=files,
                          cookies=cookies
                          )
        json_response = r.json()
        assert r.status_code == 400
        assert "error" in json_response
        assert "Invalid" in json_response["error"][0]

    # Test case for expired licenses
    license_file_path = os.path.join("/tests/utils/expired_license_test.json")
    with open(license_file_path, "rb") as file:
        files = {"filename": file}
        r = requests.post(license_upload_url,
                          files=files,
                          cookies=cookies
                          )
        json_response = r.json()
        assert r.status_code == 400
        assert "error" in json_response
        assert "The license key has expired." in json_response["error"][0]


def test_delete_license():
    # directly delete old imported from db
    delete_existing_license()

    # Not existing id
    license_id = 1111
    delete_url = list_url = f'{API_URL}/api/license/{license_id}'
    r = requests.delete(delete_url, headers=headers, cookies=cookies)
    assert r.status_code == 404
    assert r.json()["error"] == "No license found!"

    # Upload valid license
    r = upload_license(ocr=True)
    if isinstance(r, str):
        raise Exception(r)
    assert r.status_code == 200
    json_response = r.json()
    assert "message" in json_response
    assert "uploaded successfully" in json_response["message"]

    list_url = f'{API_URL}/api/licenses'
    r = requests.get(
        list_url,
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200
    assert 'items' in json_response
    license_id = [item["id"] for item in json_response["items"]][0]
    delete_url = list_url = f'{API_URL}/api/license/{license_id}'

    # Add dummy active server entry that uses this license
    created_id = create_dummy_active_server(license_id)

    # Delete the license
    r = requests.delete(delete_url, headers=headers, cookies=cookies)
    assert r.status_code == 400
    assert (
        r.json()["error"]
        == "Cannot delete license! It is currently being used "
        f"by server with ID: {created_id}"
    )

    # delete dummy active server entry that uses this license
    delete_dummy_active_server(license_id)

    # Delete the license
    delete_url = list_url = f'{API_URL}/api/license/{license_id}'
    r = requests.delete(delete_url, headers=headers, cookies=cookies)
    assert r.status_code == 200
    assert r.json()["message"] == "License deleted!"


def test_edit_task_title():
    PROJECT_NAME = "test_edit_task_title"
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 1
    edit_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}'
    data = {"title": "Test title"}
    r = requests.patch(
        edit_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert 'message' in json_response
    assert json_response['message'] == "Task title updated!"
    delete_project(PROJECT_NAME)


def test_get_project():
    PROJECT_NAME = "test_get_project"
    create_project(PROJECT_NAME)
    list_url = f'{API_URL}/api/projects'
    r = requests.get(
        list_url,
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200
    assert 'items' in json_response
    assert 'test_get_project' == json_response.get("items")[0].get("project_name")
    delete_project(PROJECT_NAME)


def create_tag(project_name, cookies=cookies):
    tag_url = f'{API_URL}/api/projects/{project_name}/tags'
    data = {
        "tag_name": "test",
        "tag_color": "#000000"
    }
    # check from collaborate
    r = requests.post(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def test_create_tag():
    PROJECT_NAME = "test_create_tag"
    create_project_with_task(PROJECT_NAME)
    # check from collaborate
    r = create_tag(PROJECT_NAME, collaborate_cookie)
    assert r.status_code == 403

    # check from admin
    r = create_tag(PROJECT_NAME)
    json_response = r.json()

    assert r.status_code == 201
    assert 'tag_id' in json_response
    delete_project(PROJECT_NAME)


def test_update_tag():
    PROJECT_NAME = "test_update_tag"
    create_project_with_task(PROJECT_NAME)
    r = create_tag(PROJECT_NAME)
    TAG_ID = r.json()['tag_id']

    tag_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tags/{TAG_ID}'
    data = {
        "tag_name": "test1",
        "tag_color": "#49cc90"
    }
    # check from collaborate
    r = requests.patch(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # check from admin
    r = requests.patch(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    print(json_response)
    assert r.status_code == 201
    assert 'message' in json_response
    assert json_response['message'] == "Tag updated"
    delete_project(PROJECT_NAME)


def test_create_completion():
    COMPLETION_ID = 0
    TASK_ID = 1
    PROJECT_NAME = "test_create_completion"
    create_project_with_task(PROJECT_NAME)
    # from admin
    r = create_completions(PROJECT_NAME, TASK_ID)
    assert r.status_code == 201

    # from collaborate (user not in project)
    r = create_completions(PROJECT_NAME, TASK_ID, cookies=collaborate_cookie)
    assert r.status_code == 403

    # collaborate in project as annotator but not assigned to task
    # add project team
    data = {
        "username": ["collaborate"],
        "scopes": ["Annotator"]
    }
    add_to_team(PROJECT_NAME, data)
    r = create_completions(PROJECT_NAME, TASK_ID, cookies=collaborate_cookie)
    assert r.status_code == 403

    # collaborate in project as reviewer but not assigned to task
    data = {
        "username": ["collaborate"],
        "scopes": ["Reviewer"]
    }
    add_to_team(PROJECT_NAME, data)
    r = create_completions(PROJECT_NAME, TASK_ID, cookies=collaborate_cookie)
    assert r.status_code == 403

    # assign collaborate to task
    user = 'collaborate'
    assign_user_to_task(PROJECT_NAME, user, task_ids=[TASK_ID])
    r = create_completions(PROJECT_NAME, TASK_ID, cookies=collaborate_cookie)
    assert r.status_code == 201

    # readonly as manager
    user = 'readonly'
    readonly_cookies = get_cookies(user, user)
    # collaborate in project as reviewer but not assigned to task
    data = {
        "username": ["readonly"],
        "scopes": ["Manager"]
    }
    add_to_team(PROJECT_NAME, data)
    r = create_completions(PROJECT_NAME, TASK_ID, cookies=readonly_cookies)
    assert r.status_code == 201

    delete_project(PROJECT_NAME)


def test_create_completion_for_whitespace_task():
    PROJECT_NAME = "test_create_completion_for_whitespace_task"
    create_project_with_task(PROJECT_NAME)
    create_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/2/completions'
    data = {
        "created_username": "admin",
        "created_ago": "2020-09-14T11:26:05.092Z",
        "result": [
            {
                "from_name": "label",
                "id": "n9oLJ1vNgD",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 13,
                    "labels": [
                        "Fact"
                    ],
                    "start": 6,
                    "text": "Patient"
                }
            }, {
                "from_name": "label",
                "id": "tKMo9ve8QW",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 40,
                    "labels": [
                        "Ordinal"
                    ],
                    "start": 37,
                    "text": "Doe"
                }
            }, {
                "from_name": "label",
                "id": "vhMwDQgg7A",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 33,
                    "labels": [
                        "Location"
                    ],
                    "start": 29,
                    "text": "John"
                }
            }, {
                "from_name": "label",
                "id": "vbWCJyO3TG",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 87,
                    "labels": [
                        "Percent"
                    ],
                    "start": 80,
                    "text": "patient"
                }
            }
        ]
    }

    r = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert 'id' in json_response
    assert r.status_code == 201
    delete_project(PROJECT_NAME)


def test_update_completion():
    PROJECT_NAME = "test_update_completion"
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 1
    create_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions'
    data = {
        "created_username": "admin",
        "created_ago": "2020-09-14T11:26:05.092Z",
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Organization"
                    ]
                }
            }
        ]
    }

    r = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    COMPLETION_ID = json_response['id']
    assert r.status_code == 201
    update_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions/{COMPLETION_ID}'
    data = {
        "created_username": "admin",
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Fact"
                    ]
                }
            }

        ]
    }

    r = requests.patch(
        update_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    assert r.status_code == 201
    json_response = r.json()
    assert 'message' in json_response
    assert 'Completion updated successfully' in json_response['message']
    delete_project(PROJECT_NAME)


def test_update_another_user_completion():
    PROJECT_NAME = "test_update_another_user_completion"
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 1
    data = {
        "username": ["collaborate"],
        "scopes": ["Manager"]
    }
    add_to_team(PROJECT_NAME, data)
    create_url = (
        f"{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions"
    )
    data = {
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Organization"
                    ]
                }
            }
        ]
    }

    r = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    json_response = r.json()
    COMPLETION_ID = json_response['id']
    assert r.status_code == 201
    update_url = (
        f"{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}"
        f"/completions/{COMPLETION_ID}"
    )
    data = {
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Fact"
                    ]
                }
            }

        ]
    }

    r = requests.patch(
        update_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 400
    assert 'error' in json_response
    assert (
        "user 'admin' is not allowed to update the completion."
        in json_response['error']
    )
    delete_project(PROJECT_NAME)


def test_export_as_csv(output_dir):
    PROJECT_NAME = "test_export_as_csv"
    create_task_with_completions(PROJECT_NAME)
    r = do_export_request(PROJECT_NAME, format='CSV')

    assert r.status_code == 200

    contents, columns = get_csv_info(output_dir, r.content, sep=',')
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["csv"]
    ])
    assert columns == CSV_COLS
    delete_project(PROJECT_NAME)


def test_export_as_tsv(output_dir):
    PROJECT_NAME = "test_export_as_tsv"
    create_task_with_completions(PROJECT_NAME)
    r = do_export_request(PROJECT_NAME, format='TSV')
    assert r.status_code == 200

    contents, columns = get_csv_info(output_dir, r.content, sep='\t')
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["tsv"]
    ])
    assert columns == TSV_COLS
    delete_project(PROJECT_NAME)


def test_export_as_json(output_dir):
    PROJECT_NAME = "test_export_as_json"
    create_task_with_completions(PROJECT_NAME)
    r = do_export_request(PROJECT_NAME, format='JSON')
    assert r.status_code == 200

    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json"]
    ])
    assert isinstance(json_data, list)

    data = json_data[0]
    assert 'completions' in data
    assert 'data' in data
    assert 'id' in data
    assert 'created_at' in data
    assert 'created_by' in data
    delete_project(PROJECT_NAME)


def test_export_as_coco(output_dir):
    PROJECT_NAME = "test_export_as_coco"
    # Image import
    create_visual_ner_task_with_completion(PROJECT_NAME)
    r = do_export_request(PROJECT_NAME, format='COCO')
    assert r.status_code == 200

    contents, json_data = get_coco_info(output_dir, r.content)

    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["coco"]
    ])
    assert isinstance(json_data, dict)

    assert json_data["images"] != []
    assert json_data["categories"] != []
    assert json_data["annotations"] != []
    assert json_data["info"] != {}
    assert "text" in json_data["annotations"][0]

    delete_project_task(PROJECT_NAME, task_id=1)

    # pdf import
    file_path = "/tests/utils/multipage_ocr_sample.pdf"
    create_visual_ner_task_with_completion(PROJECT_NAME, file_path=file_path)
    r = do_export_request(PROJECT_NAME, format='COCO')
    assert r.status_code == 200

    contents, json_data = get_coco_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["coco"][:1]
    ])
    exported_images = [f for f in contents if f.endswith(".png")]
    assert len(exported_images) == 3
    assert all(
        "multipage_ocr_sample" in img for img in exported_images
    )

    assert isinstance(json_data, dict)

    assert json_data["images"] != []
    assert json_data["categories"] != []
    assert json_data["annotations"] != []
    assert json_data["info"] != {}
    assert "text" in json_data["annotations"][0]
    assert "pageNumber" in json_data["annotations"][0]

    delete_project(PROJECT_NAME)


def test_exclude_deleted_completions_in_export(output_dir):
    PROJECT_NAME = "test_exclude_deleted_completions_in_export"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    import_url = f'{API_URL}/api/projects/{PROJECT_NAME}/import'
    data = {
        "completions": [
            {
                "created_ago": "2020-07-18T06:17:12.545Z",
                "created_username": "admin",
                "honeypot": False,
                "id": 1,
                "lead_time": 3.491,
                "result": [
                    {
                        "from_name": "label",
                        "id": "w7PVuIWOwN",
                        "source": "$text",
                        "to_name": "text",
                        "type": "labels",
                                "value": {
                                    "end": 34,
                                    "labels": [
                                        "Money"
                                    ],
                                    "start": 26,
                                    "text": "yourself"
                                }
                    }
                ]
            },
            {
                "created_ago": "2020-07-18T06:17:16.951Z",
                "created_username": "admin",
                "honeypot": False,
                "deleted_at": "2021-07-18T06:17:16.951Z",
                "id": 2,
                "lead_time": 2.666,
                "result": [
                    {
                        "from_name": "label",
                        "id": "Xu_IfgBaOS",
                        "source": "$text",
                        "to_name": "text",
                        "type": "labels",
                                "value": {
                                    "end": 13,
                                    "labels": [
                                        "Organization"
                                    ],
                                    "start": 8,
                                    "text": "faith"
                                }
                    }
                ]
            }
        ],
        "predictions": [],
        "created_at": "2020-11-24 04:55:33",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": ""
        },
        "id": 1
    }
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    r = do_export_request(PROJECT_NAME, format='JSON')
    assert r.status_code == 200

    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json"]
    ])
    assert isinstance(json_data, list)

    data = json_data[0]
    assert 'completions' in data
    assert 'data' in data
    assert 'id' in data
    assert 'created_at' in data
    assert 'created_by' in data
    verify_all_completion_without_deleted_at(data['completions'])
    delete_project(PROJECT_NAME)


def test_export_as_json_for_ground_truth(output_dir):
    PROJECT_NAME = "test_export_as_json_for_ground_truth"
    create_task_with_completions_and_honeypot(PROJECT_NAME)
    r = do_export_request(PROJECT_NAME, format='JSON', ground_truth=True)
    assert r.status_code == 200

    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json"]
    ])
    assert isinstance(json_data, list)

    data = json_data[0]
    assert 'completions' in data
    assert 'data' in data
    assert 'id' in data
    assert 'created_at' in data
    assert 'created_by' in data
    verify_all_completion_as_ground_truth(data['completions'])
    delete_project(PROJECT_NAME)


def test_export_as_json_min(output_dir):
    PROJECT_NAME = "test_export_as_json_min"
    create_task_with_completions(PROJECT_NAME)
    r = do_export_request(PROJECT_NAME, format='JSON_MIN')
    assert r.status_code == 200

    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json_min"]
    ])
    assert isinstance(json_data, list)

    data = json_data[0]
    assert 'task_id' in data
    assert 'text' in data
    assert 'completion_id' in data
    assert 'label' in data
    delete_project(PROJECT_NAME)


def test_export_as_conll(output_dir):
    PROJECT_NAME = "test_export_as_conll"
    create_task_with_completions(PROJECT_NAME)
    expected_output = (
        "-DOCSTART- -X- -X- O\n\n"
        "12345 -X- -X- O\n"
        "Patient -X- -X- B-Fact\n"
        "ID -X- -X- O\n"
        ": -X- -X- O\n"
        "31133496 -X- -X- O\n"
        "John,F -X- -X- O\n"
        ". -X- -X- O\n\n"
        "Doe -X- -X- B-Ordinal\n"
        "Birthday -X- -X- O\n"
        ": -X- -X- O\n"
        "04/11/2000 -X- -X- O\n"
        "6320 -X- -X- O\n"
        "[hello -X- -X- O\n"
        "? -X- -X- O\n\n"
        "{patient}(id)/(identity&name)] -X- -X- O\n".encode('utf-8')
    )
    contents, output = export_as_conll(PROJECT_NAME, output_dir)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["conll"]
    ])
    assert expected_output in output
    delete_project(PROJECT_NAME)


@pytest.mark.parametrize(
    "tag_ids, expected_result",
    [
        ({"tags": [1]}, {"count": 1, "ids": [1]}),
        ({"tags": []}, {"count": 2, "ids": [1, 2]}),
        ({}, {"count": 2, "ids": [1, 2]})
    ]
)
def test_tag_based_export(output_dir, tag_ids, expected_result):
    PROJECT_NAME = "test_tag_based_export"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)

    # Import two tasks with completions
    import_url = f'{API_URL}/api/projects/{PROJECT_NAME}/import'
    data = [
                {
                    "completions": [
                    {
                        "created_username": "admin",
                        "created_ago": "2020-11-24T04:55:51.276Z",
                        "lead_time": 7.026,
                        "result": [
                        {
                            "value": {
                            "start": 8,
                            "end": 13,
                            "text": "faith",
                            "labels": [
                                "Person"
                            ]
                            },
                            "id": "hfhsY870H5",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels"
                        }
                        ],
                        "honeypot": False,
                        "id": 1
                    }
                    ],
                    "predictions": [],
                    "created_at": "2020-11-24 04:55:17",
                    "created_by": "admin",
                    "data": {
                    "text": "To have faith is to trust yourself to the water",
                    "title": ""
                    },
                    "id": 1
                },
                {
                    "completions": [
                    {
                        "created_username": "admin",
                        "created_ago": "2020-11-24T04:55:33.470Z",
                        "lead_time": 12.076,
                        "result": [
                        {
                            "value": {
                            "start": 42,
                            "end": 47,
                            "text": "water",
                            "labels": [
                                "Fact"
                            ]
                            },
                            "id": "iMN37nDLCH",
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels"
                        }
                        ],
                        "honeypot": False,
                        "id": 1001
                    }
                    ],
                    "predictions": [],
                    "created_at": "2020-11-24 04:55:33",
                    "created_by": "admin",
                    "data": {
                    "text": "To have faith is to trust yourself to the water",
                    "title": ""
                    },
                    "id": 2
                }
            ]
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201

    # Assign tag to one task -> task-0
    TAG_ID = 1 # Validate Tag
    tag_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tags/{TAG_ID}'
    data = {"task_ids": [1]}
    r = requests.post(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 201

    # Export tasks with/without tag
    format='JSON'
    export_url = f'{API_URL}/api/projects/{PROJECT_NAME}/export?format={format}'

    r = requests.post(
        export_url,
        headers=headers,
        data = json.dumps(tag_ids),
        cookies=get_cookies()
    )
    assert r.status_code == 200
    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json"]
    ])
    assert isinstance(json_data, list)
    assert len(json_data) == expected_result["count"]
    ids = []
    for task in json_data:
        ids.append(task.get("id", None))
    assert ids.sort() == expected_result["ids"].sort()

    delete_project(PROJECT_NAME)


def test_asign_tag_to_task():
    PROJECT_NAME = "test_asign_tag_to_task"
    create_project_with_task(PROJECT_NAME)
    r = create_tag(PROJECT_NAME)
    TAG_ID = r.json()['tag_id']
    tag_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tags/{TAG_ID}'
    data = {
        "task_ids": [
            0,
            1
        ]
    }
    # check from collaborate
    r = requests.post(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # check from admin
    r = requests.post(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 201
    delete_project(PROJECT_NAME)


def test_delete_asign_tag_to_task():
    PROJECT_NAME = "test_delete_asign_tag_to_task"
    create_project_with_task(PROJECT_NAME)
    r = create_tag(PROJECT_NAME)
    TAG_ID = r.json()['tag_id']
    tag_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tag/{TAG_ID}'
    data = {
        "task_ids": [
            5, 6
        ]
    }
    # check from collaborate
    r = requests.delete(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # check from admin
    # invalid task ids
    r = requests.delete(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 400
    assert "Invalid task id(s): [5, 6]" in r.json()["error"]

    # check from admin
    # unassign from not tagged tasks
    data = {
        "task_ids": [
            1, 2
        ]
    }
    r = requests.delete(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 400
    assert "Task ID 1 is not tagged" in r.json()["error"]
    assert "Task ID 2 is not tagged" in r.json()["error"]

    # check from admin
    # assign tasks and try to unassign
    # check from admin
    assign_tag_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tags/{TAG_ID}'
    requests.post(
        assign_tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    r = requests.delete(
        tag_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    assert r.status_code == 200
    assert "Tag removed" in r.json()["message"]
    delete_project(PROJECT_NAME)


def test_delete_tag():
    PROJECT_NAME = "test_delete_tag"
    create_project_with_task(PROJECT_NAME)
    r = create_tag(PROJECT_NAME)
    TAG_ID = r.json()['tag_id']
    tag_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tags/{TAG_ID}'

    # check from collaborate
    r = requests.delete(
        tag_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # invalid tag id (from admin)
    invalid_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tags/1000'
    r = requests.delete(
        invalid_url,
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "Invalid Tag ID" in json_response["error"]

    # valid url (from admin)
    r = requests.delete(
        tag_url,
        headers=headers,
        cookies=cookies
    )
    assert r.status_code == 200
    json_response = r.json()
    assert json_response['message'] == "Tag deleted"
    delete_project(PROJECT_NAME)


def test_delete_completion():
    PROJECT_NAME = "test_delete_completion"
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 1
    create_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions'
    data = {
        "created_username": "admin",
        "created_ago": "2020-09-14T11:26:05.092Z",
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Organization"
                    ]
                }
            }
        ]
    }

    r = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    COMPLETION_ID = json_response['id']
    assert r.status_code == 201
    delete_completion_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions/{COMPLETION_ID}'
    r = requests.delete(
        delete_completion_url,
        headers=headers,
        cookies=cookies
    )

    assert r.status_code == 204
    delete_project(PROJECT_NAME)


def test_delete_another_user_completion():
    PROJECT_NAME = "test_delete_another_user_completion"
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 1
    data = {
        "username": ["collaborate"],
        "scopes": ["Manager"]
    }
    add_to_team(PROJECT_NAME, data)
    create_url = (
        f"{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions"
    )
    data = {
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Organization"
                    ]
                }
            }
        ]
    }

    r = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    json_response = r.json()
    COMPLETION_ID = json_response['id']
    assert r.status_code == 201
    delete_completion_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions/{COMPLETION_ID}'
    r = requests.delete(
        delete_completion_url,
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert 'error' in json_response
    assert "user 'admin' is not allowed to delete the completion." in json_response['error']
    delete_project(PROJECT_NAME)


def test_switch_ground_truth(output_dir):
    PROJECT_NAME = "test_switch_ground_truth"
    TASK_ID = 1
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    import_url = f'{API_URL}/api/projects/{PROJECT_NAME}/import'
    data = {
        "completions": [
            {
                "created_ago": "2020-07-18T06:17:12.545Z",
                "created_username": "admin",
                "honeypot": True,
                "id": 1,
                "lead_time": 3.491,
                "result": [
                            {
                                "from_name": "label",
                                "id": "w7PVuIWOwN",
                                "source": "$text",
                                "to_name": "text",
                                "type": "labels",
                                "value": {
                                    "end": 34,
                                    "labels": [
                                        "Money"
                                    ],
                                    "start": 26,
                                    "text": "yourself"
                                }
                            }
                ]
            },
            {
                "created_ago": "2020-07-18T06:17:16.951Z",
                "created_username": "admin",
                "id": 2,
                "lead_time": 2.666,
                "result": [
                    {
                        "from_name": "label",
                        "id": "Xu_IfgBaOS",
                        "source": "$text",
                        "to_name": "text",
                        "type": "labels",
                                "value": {
                                    "end": 13,
                                    "labels": [
                                        "Organization"
                                    ],
                                    "start": 8,
                                    "text": "faith"
                                }
                    }
                ]
            }
        ],
        "predictions": [],
        "created_at": "2020-11-24 04:55:33",
        "created_by": "admin",
        "data": {
            "text": "To have faith is to trust yourself to the water",
            "title": ""
        },
        "id": 1
    }
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    new_comp = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions'

    data = {
        "created_username": "admin",
        "created_ago": "2020-09-14T11:26:05.092Z",
        "id": 3,
        "honeypot": True,
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 21,
                    "end": 25,
                    "text": "task",
                    "labels": [
                        "Organization"
                    ]
                }
            }
        ]
    }
    r = requests.post(
        new_comp,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    r = do_export_request(PROJECT_NAME, format='JSON')
    assert r.status_code == 200

    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json"]
    ])
    assert isinstance(json_data, list)

    data = json_data[0]
    assert 'completions' in data
    for c in data['completions']:
        if c['id'] == 1:
            assert c['honeypot'] == False
        if c['id'] == 3:
            assert c['honeypot'] == True
    delete_project(PROJECT_NAME)


def test_delete_task():
    PROJECT_NAME = "test_delete_task"
    create_project_with_task(PROJECT_NAME)
    delete_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks_delete'
    data = {
        "task_ids": [
            0,
            1
        ]
    }
    r = requests.delete(
        delete_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    assert r.status_code == 200
    json_response = r.json()
    assert "message" in json_response
    assert "Task(s) successfully deleted!" in json_response["message"]
    delete_project(PROJECT_NAME)


def test_add_project_members():
    PROJECT_NAME = "test_add_project_members"
    create_project_with_task(PROJECT_NAME)
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Annotator", "Reviewer", "Manager"]
    }
    # check from collaborate
    r = add_to_team(PROJECT_NAME, data, cookies=collaborate_cookie)
    assert r.status_code == 403

    # check from admin
    r = add_to_team(PROJECT_NAME, data)
    json_response = r.json()
    assert r.status_code == 200
    assert 'message' in json_response
    assert "Team member(s) updated successfully" in json_response['message']
    delete_project(PROJECT_NAME)


def test_remove_project_members():
    PROJECT_NAME = "test_remove_project_members"
    create_project_with_task(PROJECT_NAME)
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Annotator", "Reviewer", "Manager"]
    }
    delete_scope_url = f'{API_URL}/api/project/{PROJECT_NAME}/scope'
    # check from collaborate
    r = requests.delete(
        delete_scope_url,
        headers=headers,
        data=json.dumps({"requester": "readonly"}),
        cookies=collaborate_cookie
    )
    r.status_code == 403
    add_to_team(PROJECT_NAME, data)
    for user in data['username']:
        data = {
            'requester': user
        }
        r = requests.delete(
            delete_scope_url,
            headers=headers,
            data=json.dumps(data),
            cookies=cookies
        )
        json_response = r.json()
        assert r.status_code == 200
        assert 'message' in json_response
        assert (
            f"Removed user '{user}' from project '{PROJECT_NAME}"
            in json_response['message']
        )
    delete_project(PROJECT_NAME)


def test_get_project_members():
    PROJECT_NAME = "test_get_project_members"
    create_project_with_task(PROJECT_NAME)
    members_url = f'{API_URL}/api/projects/{PROJECT_NAME}/members_scopes'
    # check from collaborate
    r = requests.get(
        members_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403
    # check from admin
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Annotator", "Reviewer", "Manager"]
    }
    expected_output = {
        "collaborate": [
            "Annotator",
            "Reviewer",
            "Manager"
        ],
        "readonly": [
            "Annotator",
            "Reviewer",
            "Manager"
        ]
    }
    add_to_team(PROJECT_NAME, data)
    r = requests.get(
        members_url,
        headers=headers,
        cookies=cookies
    )
    assert "members" in r.json()
    json_response = r.json()
    assert json_response['members'] == expected_output
    assert r.status_code == 200

    delete_project(PROJECT_NAME)


def test_delete_project():
    PROJECT_NAME = "test_delete_project"
    create_project(PROJECT_NAME)
    delete_project(PROJECT_NAME)


@pytest.mark.parametrize("user_data", [
    {
        "firstName": "User@123",
        "lastName": "User_last_name",
        "status_code": 400,
        "response": {"error"},
    },
    {
        "firstName": "Üsér",
        "lastName": "TèSt",
        "status_code": 201,
        "response": {"user_id"},
    },
])
def test_validate_user_detail(user_data):
    user_url = f'{API_URL}/api/users'
    data = {
        "username": "test_api_validate_user_detail",
        "firstName": user_data["firstName"],
        "lastName": user_data["lastName"],
        "email": "",
        "enabled": True
    }
    r = requests.post(
        user_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == user_data["status_code"]
    assert user_data["response"].issubset(json_response)
    if user_data["status_code"] == 201:
        delete_users(
            json_response["user_id"], "test_api_validate_user_detail", "admin")


def test_create_user():
    # check from collaborate user
    r = create_user(
        "create_user",
        cookies=collaborate_cookie,
        dont_assert=True)
    assert r.status_code == 403

    # check from admin
    USER_ID = create_user("create_user")
    delete_users(USER_ID, "create_user", "admin")


def test_set_password():
    USER_ID = create_user("test_set_password")
    set_password_url = f'{API_URL}/api/users/{USER_ID}/reset_password'

    data = {
        "password": "new_user",
        "temporary": True
    }

    # check from collaborate
    r = requests.put(
        set_password_url,
        json=data,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # check from admin
    r = requests.put(
        set_password_url,
        json=data,
        headers=headers,
        cookies=cookies
    )

    assert r.status_code == 204
    delete_users(USER_ID, "test_set_password", "admin")


def test_update_user():
    USER_ID = create_user("test_update_user")
    user_url = f'{API_URL}/api/users/{USER_ID}'
    data = {
        "firstName": "Name",
        "lastName": "Changed",
        "email": "name@jsl.com",
        "enabled": True
    }
    # check from collaborate
    r = requests.put(
        user_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # check from admin
    r = requests.put(
        user_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    assert r.status_code == 204
    delete_users(USER_ID, "test_update_user", "admin")


def test_get_users():
    user_url = f'{API_URL}/api/users'
    # check from collaborate
    r = requests.get(
        user_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # check from admin
    r = requests.get(
        user_url,
        headers=headers,
        cookies=cookies
    )
    users = r.json()
    assert "users" in users
    assert r.status_code == 200


def test_get_user_groups():
    group_url = f'{API_URL}/api/user_groups'
    # check from collaborate
    r = requests.get(
        group_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403
    r = requests.get(
        group_url,
        headers=headers,
        cookies=cookies
    )
    assert "groups" in r.json()
    assert r.status_code == 200


def test_delete_user():
    USER_ID = create_user("test_delete_user")
    # check from collaborate
    r = delete_users(
        USER_ID,
        "test_delete_user",
        "admin",
        cookies=collaborate_cookie
    )
    assert r.status_code == 403
    # check from admin
    r = delete_users(USER_ID, "test_delete_user", "admin")
    assert r.status_code == 204


def test_assign_user_to_task():
    PROJECT_NAME = "test_assign_user_to_task"
    create_project_with_task(PROJECT_NAME)

    # add project team
    data = {
        "username": ["collaborate"],
        "scopes": ["Annotator"]
    }
    add_to_team(PROJECT_NAME, data)

    # assign user (by resource owner)
    r = assign_user_to_task(PROJECT_NAME, 'collaborate')
    assert r.status_code == 201
    assert "message" in r.json()
    assert "Task(s) assigned to user" in r.json().get("message")

    # assign user (by unauthorised user)
    r = assign_user_to_task(
        PROJECT_NAME, 'readonly', cookies=collaborate_cookie)
    assert r.status_code == 403
    assert "error" in r.json()
    assert (
        "not allowed to assign/revoke assignee from task(s)!"
        in r.json().get("error")
    )
    delete_project(PROJECT_NAME)


def test_revoke_user_from_task():
    PROJECT_NAME = "test_revoke_user_from_task"
    create_project_with_task(PROJECT_NAME)
    username = "collaborate"
    assignee_url = f'{API_URL}/api/projects/{PROJECT_NAME}/user/'\
                   f'{username}/assignee'
    task_data = {
        "task_ids": [0, 1]
    }
    r = requests.delete(
        assignee_url,
        headers=headers,
        data=json.dumps(task_data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert f"User '{username}' has no assignee role" in\
        json_response.get("error")

    team_data = {
        "username": [username],
        "scopes": ["Annotator"]
    }
    add_to_team(PROJECT_NAME, team_data)

    r = requests.delete(
        assignee_url,
        headers=headers,
        data=json.dumps(task_data),
        cookies=cookies
    )
    json_response = r.json()

    assert r.status_code == 201
    assert "message" in json_response
    assert "Task(s) revoked from user" in json_response.get("message")
    delete_project(PROJECT_NAME)


def assign_reviewer_to_task(
        project_name: str,
        assign_to: str,
        cookies: dict = cookies,
        task_ids: list = [0, 1]):

    reviewer_url = f'{API_URL}/api/projects/{project_name}/user/'\
                   f'{assign_to}/reviewer'
    data = {
        "task_ids": task_ids
    }
    r = requests.patch(
        reviewer_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def test_assign_reviewer_to_task():
    PROJECT_NAME = "test_assign_reviewer_to_task"
    create_project_with_task(PROJECT_NAME)

    # add project team
    data = {
        "username": ["collaborate"],
        "scopes": ["Reviewer"]
    }
    add_to_team(PROJECT_NAME, data)
    # assign user (by resource owner)
    r = assign_reviewer_to_task(PROJECT_NAME, 'collaborate')
    assert r.status_code == 201
    assert "message" in r.json()
    assert "Task(s) assigned to user" in r.json().get("message")

    # assign user (by unauthorised user)
    r = assign_reviewer_to_task(
        PROJECT_NAME, 'readonly', cookies=collaborate_cookie)
    assert r.status_code == 403
    assert "error" in r.json()
    assert (
        "not allowed to assign/revoke reviewer from task(s)!"
        in r.json().get("error")
    )

    delete_project(PROJECT_NAME)


def test_revoke_reviewer_from_task():
    PROJECT_NAME = "test_revoke_reviewer_from_task"
    create_project_with_task(PROJECT_NAME)
    username = "collaborate"
    assignee_url = f'{API_URL}/api/projects/{PROJECT_NAME}/user/'\
                   f'{username}/reviewer'
    task_data = {
        "task_ids": [0, 1]
    }
    r = requests.delete(
        assignee_url,
        headers=headers,
        data=json.dumps(task_data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert f"User '{username}' has no reviewer role" in\
        json_response.get("error")

    team_data = {
        "username": [username],
        "scopes": ["Reviewer"]
    }
    add_to_team(PROJECT_NAME, team_data)
    r = requests.delete(
        assignee_url,
        headers=headers,
        data=json.dumps(task_data),
        cookies=cookies
    )
    json_response = r.json()

    assert r.status_code == 201
    assert "message" in json_response
    assert "Task(s) revoked from user" in json_response.get("message")
    delete_project(PROJECT_NAME)


def test_give_review():
    PROJECT_NAME = "test_give_review"
    TASK_ID = 1
    create_project_with_task(PROJECT_NAME)

    # create completions (one submitted, other not submitted)
    r = create_completions(
        PROJECT_NAME,
        TASK_ID
    )
    assert r.status_code == 201
    not_submitted_completion = r.json()['id']
    # submit completions and try reviewing
    r = create_completions(
        PROJECT_NAME,
        TASK_ID,
        {"submitted_at": "2021-02-04T11:26:05.092Z"}
    )
    submitted_completion = r.json()['id']
    assert r.status_code == 201

    # try reviewing from collaborate without adding to team
    r = give_review(
        PROJECT_NAME, TASK_ID, not_submitted_completion, collaborate_cookie)
    assert r.status_code == 403

    # add collaborate to team
    username = 'collaborate'
    data = {
        "username": [username],
        "scopes": ["Reviewer"]
    }
    add_to_team(PROJECT_NAME, data)

    # try reviewing from collaborate without assigning as reviewer
    r = give_review(
        PROJECT_NAME, TASK_ID, not_submitted_completion, collaborate_cookie)
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert f"User '{username}' is not allowed to review" in\
        json_response.get("error")

    # assign collaborate as reviewer
    r = assign_reviewer_to_task(PROJECT_NAME, username)
    assert r.status_code == 201

    # try reviewing from collaborate
    r = give_review(
        PROJECT_NAME, TASK_ID, not_submitted_completion, collaborate_cookie)
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert (
        f"Cannot review unsubmitted completions!"
        in json_response.get("error")
    )

    # try reviewing from collaborate (SUBMITTED COMPLETION)
    r = give_review(
        PROJECT_NAME, TASK_ID, submitted_completion, collaborate_cookie)
    json_response = r.json()
    assert r.status_code == 201
    assert "message" in json_response
    assert "Completion review successfully submitted" in\
        json_response.get("message")

    # Review already reviewed completion
    r = give_review(
        PROJECT_NAME, TASK_ID, submitted_completion, collaborate_cookie)
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "Completion is already reviewed by user" in\
        json_response.get("error")

    delete_project(PROJECT_NAME)


def test_submit_completion():
    PROJECT_NAME = "test_submit_completion"
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 1
    create_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions'
    data = {
        "created_username": "admin",
        "created_ago": "2020-09-14T11:26:05.092Z",
        "result": [
            {
                "id": "uNOfk3JtcC",
                "from_name": "label",
                "to_name": "text",
                "source": "$text",
                "type": "labels",
                "value": {
                    "start": 0,
                    "end": 5,
                    "text": "task",
                    "labels": [
                        "Organization"
                    ]
                }
            }
        ]
    }

    r = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    COMPLETION_ID = json_response['id']
    assert r.status_code == 201
    url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions/{COMPLETION_ID}'
    data["submitted_at"] = "2020-09-14T11:26:05.092Z"
    requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    # Updating submitted completion
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    assert r.status_code == 400
    json_response = r.json()
    assert 'error' in json_response
    assert 'Completion is already submitted.' in json_response['error']

    # Deleting submitted completion
    r = requests.delete(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    assert r.status_code == 400
    json_response = r.json()
    assert 'error' in json_response
    assert 'Completion is already submitted.' in json_response['error']
    delete_project(PROJECT_NAME)


def test_single_ground_truth_per_task_while_import(output_dir):
    PROJECT_NAME = "test_single_ground_truth_per_task_while_import"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    import_url = f'{API_URL}/api/projects/{PROJECT_NAME}/import'
    data =  {
    "completions": [
      {
        "created_username": "admin",
        "created_ago": "2021-02-06T09:56:00.072Z",
        "lead_time": 7,
        "result": [
          {
            "value": {
              "start": 20,
              "end": 25,
              "text": "trust",
              "labels": [
                "Organization"
              ]
            },
            "id": "373dfwjoWd",
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
          }
        ],
        "honeypot": True,
        "updated_at": "2021-02-06T09:56:32.678104Z",
        "updated_by": "admin"
      },
      {
        "created_username": "admin",
        "created_ago": "2021-02-02T09:56:13.185Z",
        "lead_time": 9,
        "result": [
          {
            "value": {
              "start": 42,
              "end": 47,
              "text": "water",
              "labels": [
                "Money"
              ]
            },
            "id": "qhZUzVopHg",
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
          }
        ],
        "honeypot": True
      },
      {
        "created_username": "admin",
        "created_ago": "2021-02-02T09:56:26.117Z",
        "lead_time": 7,
        "result": [
          {
            "value": {
              "start": 3,
              "end": 7,
              "text": "have",
              "labels": [
                "Person"
              ]
            },
            "id": "BZ_wdRDWVH",
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
          }
        ],
        "honeypot": True
      },
      {
        "created_username": "collaborate",
        "created_ago": "2021-02-05T10:36:08.862Z",
        "lead_time": 13,
        "result": [
          {
            "value": {
              "start": 42,
              "end": 47,
              "text": "water",
              "labels": [
                "Time"
              ]
            },
            "id": "d3FFH9z772",
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
          }
        ],
        "honeypot": True,
        "updated_at": "2021-02-05T10:37:46.908828Z",
        "updated_by": "collaborate",
        "submitted_at": None
      },
      {
        "created_username": "collaborate",
        "created_ago": "2021-02-03T10:36:13.487Z",
        "lead_time": 11,
        "result": [
          {
            "value": {
              "start": 26,
              "end": 34,
              "text": "yourself",
              "labels": [
                "Person"
              ]
            },
            "id": "AVEUNO2U9r",
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
          }
        ],
        "honeypot": True,
        "id": 5,
        "updated_at": "2021-02-03T10:37:39.590810Z",
        "updated_by": "collaborate",
        "submitted_at": None
      }
    ],
    "predictions": [],
    "created_at": "2021-02-03 10:32:58",
    "created_by": "admin",
    "data": {
      "text": "To have faith is to trust yourself to the water",
      "title": ""
    },
    "id": 1
  }
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    r = do_export_request(PROJECT_NAME, format='JSON')
    assert r.status_code == 200

    contents, json_data = get_json_info(output_dir, r.content)
    assert all([
        any(zip_content in content for content in contents)
        for zip_content in ZIP_CONTENT["json"]
    ])
    assert isinstance(json_data, list)

    data = json_data[0]
    assert 'completions' in data
    assert 'data' in data
    assert 'id' in data
    assert 'created_at' in data
    assert 'created_by' in data
    verify_ground_truth_per_user(data['completions'])
    delete_project(PROJECT_NAME)


def test_get_tasks():
    PROJECT_NAME = "test_get_tasks"
    create_project_with_task(PROJECT_NAME)
    list_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks'
    r = requests.get(
        list_url,
        headers=headers,
        cookies=cookies
    )
    assert r.status_code == 200
    json_response = r.json()
    expected_keys = [
        "count",
        "items",
        "has_next",
        "has_prev",
        "iter_pages",
        "next_num",
        "prev_num"
    ]
    assert all(key in json_response for key in expected_keys)
    assert all('id' in t for t in json_response["items"])
    assert 3 == len(json_response["items"])
    delete_project(PROJECT_NAME)


def test_comment_permissions():
    project_name = "test_comment"
    create_project_with_task(project_name)
    url = f'{API_URL}/api/projects/{project_name}/tasks/1/comment'
    data = {"comment": "This is comment!"}    # Add a comment

    # Comment from collaborate (no owner or no task assigned)
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403
    assert "User not allowed to comment" in r.json()["error"]

    # Add collaborate in project team but do not assign
    team_data = {
        "username": ["collaborate"],
        "scopes": ["Annotator"]
    }
    add_to_team(project_name, team_data)
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403
    assert "User not allowed to comment" in r.json()["error"]

    # assign collaborate to task 1
    assign_user_to_task(project_name, "collaborate", task_ids=[1])
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 201


def test_add_comment():
    project_name = "test_comment"
    url = f'{API_URL}/api/projects/{project_name}/tasks/2/comment'
    data = {"comment": "This is comment!"}    # Add a comment
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert json_response["task_id"] == 2
    assert "commented_by" in json_response["comment"][0]
    assert json_response["comment"][0]["cid"] == 1
    assert json_response["comment"][0]["comment"] == "This is comment!"
    assert json_response["comment"][0]["commented_by"] == "admin"


def test_edit_comment():
    project_name = "test_comment"
    data = {"comment": "This is updated comment!"}
    # Invalid comment Id
    url = f'{API_URL}/api/projects/{project_name}/tasks/2/comment/22'
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 404
    assert "Invalid comment id" in r.json()["error"]

    # Comment in other users' comment
    url = f'{API_URL}/api/projects/{project_name}/tasks/1/comment/1'
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 403
    assert "Cannot modify/delete other's comment" in r.json()["error"]

    # Valid comment Id
    url = f'{API_URL}/api/projects/{project_name}/tasks/2/comment/1'
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    assert r.status_code == 201
    assert r.json()["comment"][0]["comment"] == "This is updated comment!"


def test_delete_comment():
    project_name = "test_comment"
    # Invalid comment Id
    url = f'{API_URL}/api/projects/{project_name}/tasks/2/comment/22'
    r = requests.delete(
        url,
        headers=headers,
        cookies=cookies
    )
    assert r.status_code == 404
    assert "Invalid comment id" in r.json()["error"]

    # Comment in other users' comment
    url = f'{API_URL}/api/projects/{project_name}/tasks/1/comment/1'
    r = requests.delete(
        url,
        headers=headers,
        cookies=cookies
    )
    assert r.status_code == 403
    assert "Cannot modify/delete other's comment" in r.json()["error"]

    # Valid comment delete
    url = f'{API_URL}/api/projects/{project_name}/tasks/2/comment/1'
    r = requests.delete(
        url,
        headers=headers,
        cookies=cookies
    )
    assert r.status_code == 201
    assert r.json()["comment"] == []
    delete_project(project_name)


def test_task_status_user_wise():
    """
    Project Members
    -----------------
    bikash -> annotator, reviewer
    nabin -> annotator
    umesh -> manager, reviewer

    Task assignment
    -----------------
    All tasks (0 to 10) assigned to nabin, bikash
    task 6, 7, 8,9, 10 assigned as reviewer to umesh

    Various task completions
    ------------------------
    task 0
        completion  by nabin: created

    task 1
        completion by nabin: created
        completion by bikash: created

    task 2
        completion by nabin:  submitted(not starred)

    task 3
        completion by nabin: submitted(starred)

    task 4
        completion  by nabin: created
        completion  by bikash: submitted(starred)
        completion by admin: created

    task 5
        completion  by nabin: submitted (starred)
        completion  by bikash: submitted(starred)
        completion by admin: created

    task 6
        completion  by nabin: submitted (starred) and review rejected by umesh
        completion  by bikash: submitted(starred)

    task 7
        completion  by nabin: submitted (starred)
        completion  by bikash: submitted(starred) and review approved by umesh
        completion by admin: submitted (starred)

    task 8
        completion  by nabin: submitted (starred) and review approved by umesh
        completion  by bikash: submitted(starred) and review approved by umesh

    task 9
        completion  by nabin: submitted(starred) and review approved by umesh
        completion  by bikash: created

    task 10
        completion  by nabin: submitted(starred) and review rejected by umesh
        completion  by bikash: created

    task 11 (not assigned to anyone)
        completion created by admin

    task 12 (not assigned to anyone)
        completion submitted (starred) by admin

    task 13 (not assigned to anyone)
        completion created by umesh

    task 14 (not assigned to anyone)
        completion submitted (starred) by umesh
    """

    PROJECT_NAME = "test_task_status_user_wise"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    users = {
        "bikash": ["Annotator", "Reviewer"],
        "nabin": ["Annotator"],
        "umesh": ["Reviewer", "Manager"],

    }

    # Create users
    created_user_ids = dict()
    for user_name in users.keys():
        USER_ID = create_user(user_name)
        created_user_ids.update({
            user_name: USER_ID
        })
        set_password_url = f'{API_URL}/api/users/{USER_ID}/reset_password'

        data = {
            "password": user_name,
            "temporary": False
        }

        r = requests.put(
            set_password_url,
            json=data,
            headers=headers,
            cookies=cookies
        )
        assert r.status_code == 204

    # Add to team
    for user_name, roles in users.items():
        data = {
            'username': [user_name],
            'scopes': roles
        }
        r = add_to_team(PROJECT_NAME, data)
        json_response = r.json()
        assert r.status_code == 200
        assert 'message' in json_response
        assert (
            "Team member(s) updated successfully"
            in json_response['message']
        )
    # Import data
    import_url = f'{API_URL}/api/projects/{PROJECT_NAME}/import'
    with open(os.path.join(
            "/tests/utils/various_user_completions.json"), "r") as f:
        data = json.loads(f.read())

    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )

    # Assign annotators to tasks
    r = assign_user_to_task(PROJECT_NAME, 'bikash', task_ids=[1, 3, 4])
    assert r.status_code == 201
    assert "message" in r.json()
    assert "Task(s) assigned to user" in r.json().get("message")

    # Assign reviewers to tasks
    r = assign_reviewer_to_task(
        PROJECT_NAME, 'umesh', task_ids=[7, 8, 9, 10, 11])
    assert r.status_code == 201
    assert "message" in r.json()
    assert "Task(s) assigned to user" in r.json().get("message")

    expected_statues = {
        "admin": {
            "Annotator": {
                1: "incomplete",
                2: "incomplete",
                3: "incomplete",
                4: "incomplete",
                5: "inprogress",
                6: "inprogress",
                7: "incomplete",
                8: "submitted",
                9: "incomplete",
                10: "incomplete",
                11: "incomplete",
                12: "inprogress",
                13: "submitted",
                14: "incomplete",
                15: "incomplete",
            },
            "Manager": {
                1: "inprogress",
                2: "inprogress",
                3: "inprogress",
                4: "inprogress",
                5: "inprogress",
                6: "inprogress",
                7: "inprogress",
                8: "submitted",
                9: "reviewed",
                10: "inprogress",
                11: "inprogress",
                12: "inprogress",
                13: "submitted",
                14: "incomplete",
                15: "incomplete",
            },
        },
        "umesh": {
            "Reviewer": {
                7: "inprogress",
                8: "submitted",
                9: "reviewed",
                10: "inprogress",
                11: "inprogress",
            },
            "Manager": {
                1: "inprogress",
                2: "inprogress",
                3: "inprogress",
                4: "inprogress",
                5: "inprogress",
                6: "inprogress",
                7: "inprogress",
                8: "submitted",
                9: "reviewed",
                10: "inprogress",
                11: "inprogress",
                12: "inprogress",
                13: "submitted",
                14: "incomplete",
                15: "incomplete",
            },
        },
        "nabin": {
            "Annotator": {
                1: "inprogress",
                2: "inprogress",
                3: "inprogress",
                4: "submitted",
                5: "inprogress",
                6: "submitted",
                7: "rejected",
                8: "submitted",
                9: "reviewed",
                10: "reviewed",
                11: "rejected",
            }
        },
        "bikash": {
            "Annotator": {
                1: "incomplete",
                2: "inprogress",
                3: "incomplete",
                4: "incomplete",
                5: "submitted",
                6: "submitted",
                7: "submitted",
                8: "reviewed",
                9: "reviewed",
                10: "inprogress",
                11: "inprogress",
            },
            "Reviewer": {}
        }
    }
    # Assert statuses
    for user_name, status in expected_statues.items():
        verfiy_task_status(PROJECT_NAME, status, user_name)

    # Delete users
    for user_name, user_id in created_user_ids.items():
        delete_users(user_id, user_name, "admin")

    delete_project(PROJECT_NAME)


def test_group():
    url = f'{API_URL}/api/project_groups'
    data = {"group_name": "Group1", "group_color": "red"}    # Add a group
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "group_id" in json_response
    GROUP_ID = json_response['group_id']

    # Update Group details
    data = {"group_id": GROUP_ID, "group_name": "GroupOne", "group_color": "red"}
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "message" in json_response
    assert json_response['message'] == "Group updated!"

    r = requests.delete(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()

    assert r.status_code == 201
    assert "message" in json_response
    assert json_response['message'] == "Group Deleted!"


def test_group_assignment():
    group_url = f'{API_URL}/api/project_groups'
    data = {"group_name": "Group1", "group_color": "red"} # Create Group
    r = requests.post(
        group_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "group_id" in json_response
    GROUP_ID = json_response['group_id']

    # Assign group to project
    url = f'{API_URL}/api/project_groups/{GROUP_ID}'
    project_name = "test_group_assignment"
    create_project(project_name)
    data = {"project_names": [project_name]}
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "message" in json_response
    assert json_response['message'] == "Group Assigned!"

    # add project team
    other_user = "collaborate"
    user_data = {
        "username": [other_user],
        "scopes": ["Reviewer"]
    }
    add_to_team(project_name, user_data)

    # assign group (by unauthorised user)
    collaborate_cookie = get_cookies(other_user, other_user)
    r = requests.patch(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # unassign group (by unauthorised user)
    r = requests.delete(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # Unassign group to project
    r = requests.delete(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "message" in json_response
    assert json_response['message'] == "Group Unassigned!"

    # delete group
    data = {"group_id": GROUP_ID}
    requests.delete(
        group_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    delete_project(project_name)


def test_search_by_label_in_tasks_page():
    project_name = "test_search_by_label_in_tasks_page"
    create_project(project_name)
    with open(os.path.join(
        "/tests/utils/data_for_labels_search/config_for_search_project.txt"
    )) as f:
        label_config = f.read()
    with open(os.path.join(
        "/tests/utils/data_for_labels_search/result_for_search_project.json"
    )) as f:
        tasks_json = json.load(f)
    save_config(project_name, label_config)
    import_tasks(project_name, tasks_json)
    search_keywords = [
        "Task6and1and7",
        "Task8and9and2",
        "Task3and2and7",
        "Task2and4and6",
        "Task1and3and5",
        "Task11and3and6",
        "Task7and3and4",
        "Task4and7and8",
        "Task9and11and6",
        "Task10and1and5",
        "Task5and10and11",
    ]
    list_url = f'{API_URL}/api/projects/{project_name}/tasks'
    for label in search_keywords:
        query_string_params = {
            "search": f"label:{label}"
        }
        r = requests.get(
            f"{list_url}?{urlencode(query_string_params)}",
            headers=headers,
            cookies=cookies
        )
        expected_task_ids = sorted(re.findall(r"\d+", label))
        assert r.status_code == 200
        json_response = r.json()
        assert "items" in json_response
        obtained_ids = sorted([
            str(task["id"] - 1) for task in json_response["items"]
        ])
        assert obtained_ids == expected_task_ids
    delete_project(project_name)


def test_search_by_label_and_extraction_in_tasks_page():
    project_name = "test_search_by_label_and_extraction_in_tasks_page"
    create_project(project_name)
    with open(os.path.join(
        "/tests/utils/data_for_labels_search/config_for_search_project.txt"
    )) as f:
        label_config = f.read()
    with open(os.path.join(
        "/tests/utils/data_for_labels_search/result_for_search_project.json"
    )) as f:
        tasks_json = json.load(f)
    save_config(project_name, label_config)
    import_tasks(project_name, tasks_json)
    search_keywords = {
        "Task6and1and7": "diaphragm",
        "Task8and9and2": "Transcription Sample Report",
        "Task3and2and7": "ER",
        "Task2and4and6": "oppositionality",
        "Task1and3and5": "myocardial",
        "Task11and3and6": "PHYSICAL",
        "Task7and3and4": "proximal LAD with",
        "Task4and7and8": "received first set of shot",
        "Task9and11and6": "ULTRASOUND ABDOMEN",
        "Task10and1and5": "chlorhexidine based prep",
        "Task5and10and11": "human KCNJ9",
    }
    list_url = f'{API_URL}/api/projects/{project_name}/tasks'
    for task_id, (label, extracted_text) in enumerate(
        search_keywords.items(), 2
    ):

        query_string_params = {
            "search": f"label:{label}={extracted_text}"
        }
        r = requests.get(
            f"{list_url}?{urlencode(query_string_params)}",
            headers=headers,
            cookies=cookies
        )
        assert r.status_code == 200
        json_response = r.json()
        assert "items" in json_response
        assert json_response["items"][0]["id"] == task_id
    delete_project(project_name)


def test_search_by_choice_in_tasks_page():
    project_name = "test_search_by_choice_in_tasks_page"
    create_project(project_name)
    with open(os.path.join(
        "/tests/utils/data_for_labels_search/config_for_search_project.txt"
    )) as f:
        label_config = f.read()
    with open(os.path.join(
        "/tests/utils/data_for_labels_search/result_for_search_project.json"
    )) as f:
        tasks_json = json.load(f)
    save_config(project_name, label_config)
    import_tasks(project_name, tasks_json)
    search_keywords = {
        "yes": [2, 3, 5, 6, 7, 9, 10, 11, 12],
        "no": [2, 3, 4, 5, 6, 7, 8, 9],
        "unknown": [2, 3, 4, 5, 7, 8, 9],
    }
    list_url = f'{API_URL}/api/projects/{project_name}/tasks'
    for choice, task_ids in search_keywords.items():

        query_string_params = {
            "search": f"choice:{choice}"
        }
        r = requests.get(
            f"{list_url}?{urlencode(query_string_params)}",
            headers=headers,
            cookies=cookies
        )
        assert r.status_code == 200
        json_response = r.json()
        assert "items" in json_response
        obtained_ids = sorted(task["id"] for task in json_response["items"])
        assert obtained_ids == task_ids
    delete_project(project_name)


def test_task_title_visual_ner_image_url_import():
    project_name = "test_task_title_visual_ner_image_url_import"
    ensure_license(ocr=True)
    create_project(project_name)
    save_config(project_name, test_visual_ner_config_for_various_images)
    project_id = UserProjects.get_project_by_project_name(
        project_name, fields=["project_id"]
    ).project_id
    wait_for_server_deployment(project_name, project_id)
    import_url = f"{API_URL}/api/projects/{project_name}/import"
    data = [
        {
            "image": "https://images.template.net/wp-content/uploads/2017/06/Employee-Medical-Report1.jpg"
        },
        {
            "image": "https://p.calameoassets.com/120704083202-b66973c62fa0ec61a061b8394f14695b/p1.jpg",
            "title": "MyTitle1"
        },
        {
            "image": "https://i.pinimg.com/736x/da/2e/db/da2edbf7c34fd73ed79784235e27aa29.jpg",
            "title": "MyTitle2"
        },
        {
            "image": "https://www.philippinemedicalassociation.org/wp-content/uploads/2020/04/Memorandum-Circular-No-2020-04-14-061_001-791x1024.png"
        }
    ]
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "total_file_count" in json_response
    assert json_response["total_file_count"] == 4
    wait_for_ocr_process(project_name)

    # Get task_ids and titles for created tasks
    task_url = f"{API_URL}/api/projects/{project_name}/tasks"
    r = requests.get(
        task_url,
        headers=headers,
        cookies=cookies
    )
    obtained_titles = set(
        each_task["title"] for each_task in r.json()["items"]
    )
    assert obtained_titles == {
        "Employee-Medical-Report1.jpg",
        "Memorandum-Circular-No-2020-04-14-061_001-791x1024.png",
        "MyTitle1.jpg",
        "MyTitle2.jpg"
    }
    delete_project(project_name)


def test_task_search_visual_ner():
    project_name = "test_task_search_visual_ner"
    ensure_license(ocr=True)
    create_project(project_name)
    save_config(project_name, test_visual_ner_config_for_various_images)
    project_id = UserProjects.get_project_by_project_name(
        project_name, fields=["project_id"]
    ).project_id
    wait_for_server_deployment(project_name, project_id)
    images_path = "/tests/utils/images_for_visual_ner_import.zip"
    data = {
        "overwrite": False,
        "ocr_enable": False
    }
    import_url = f"{API_URL}/api/projects/{project_name}/import"
    with open(images_path, "rb") as file:
        files = {"filename": file}
        r = requests.post(
            import_url,
            files=files,
            data=data,
            cookies=cookies
        )
        json_response = r.json()
        assert r.status_code == 201
        assert "total_file_count" in json_response
        assert json_response["total_file_count"] == 7
    wait_for_ocr_process(project_name)

    completions_path = "/tests/utils/various_images_completions.json"
    with open(os.path.join(completions_path), "r") as f:
        images_completions = json.loads(f.read())

    # Get task_ids and titles for created tasks
    task_url = f"{API_URL}/api/projects/{project_name}/tasks"
    r = requests.get(
        task_url,
        headers=headers,
        cookies=cookies
    )

    # Create completions for all images
    for each_task in r.json()["items"]:
        task_title = each_task["title"]
        task_id = each_task["id"]
        completion_data = images_completions[task_title]
        r = create_completions(project_name, task_id, completion_data)
        json_response = r.json()
        assert r.status_code == 201

    existing_titles = [
        "followup-on-asthma.png",
        "kawasaki-disease.png",
        "asthma.png",
        "chronic-sinusitis.png",
        "allergy-evaluation-consult.png",
        "allergic-rhinitis.png",
        "evaluation-of-allergies.png"
    ]
    expected_results = {
        "label:Medicine": {
            existing_titles[0],
            existing_titles[1],
            existing_titles[5]
        },
        "label:Medicine=Aspirin": {
            existing_titles[1]
        },
        "label:Disease": {
            existing_titles[0],
            existing_titles[1],
            existing_titles[6]
        },
        "label:Disease=Hematuria": {
            existing_titles[0]
        },
        "label:Disease=Kawasaki disease": {
            existing_titles[1]
        },
        "label:Age": {
            existing_titles[2],
            existing_titles[3],
            existing_titles[6]
        },
        "label:Age=55-year-old": {
            existing_titles[6]
        },
        "label:Organ": {
            existing_titles[0],
            existing_titles[3],
            existing_titles[5]
        },
        "label:Result": {
            existing_titles[0],
            existing_titles[1],
            existing_titles[2],
            existing_titles[4]
        },
        "label:Pulse": {
            existing_titles[2],
            existing_titles[4]
        },
        "label:Temperature": {
            existing_titles[0],
            existing_titles[2],
            existing_titles[4]
        },
        "label:Pressure": {
            existing_titles[0],
            existing_titles[2],
            existing_titles[4],
            existing_titles[5]
        },
        "label:Weight": {
            existing_titles[0],
            existing_titles[5]
        },
        "text:redness of mucous membranes": {
            existing_titles[1]
        },
        "text:allergic rhinitis": {
            existing_titles[0],
            existing_titles[3],
            existing_titles[5]
        },
        "text:significant bruising": {
            existing_titles[2]
        },
        "text:possible food allergies": {
            existing_titles[3],
            existing_titles[6]
        },
        "text:Heparin causing thrombocytopenia": {
            existing_titles[4]
        },
        "choice:positive": {
            existing_titles[2]
        },
        "choice:negative": {
            existing_titles[0],
            existing_titles[5]
        },
        "choice:unknown": {
            existing_titles[6]
        }
    }
    list_url = f'{API_URL}/api/projects/{project_name}/tasks'
    for keyword, expected_titles in expected_results.items():

        query_string_params = {
            "search": keyword
        }
        r = requests.get(
            f"{list_url}?{urlencode(query_string_params)}",
            headers=headers,
            cookies=cookies
        )
        assert r.status_code == 200
        json_response = r.json()
        assert "items" in json_response
        obtained_titles = {task["title"] for task in json_response["items"]}
        assert obtained_titles == expected_titles
    delete_project(project_name)


def test_upload_training_script():
    PROJECT_NAME = "test_upload_training_script"
    create_project(PROJECT_NAME)
    upload_script_url = f"{API_URL}/api/project/{PROJECT_NAME}/mt/script"

    # Uploading NER Training Script
    training_file_path = os.path.join("annotationlab/utils/db.py")
    with open(training_file_path, "rb") as file:
        files = {"filename": file}
        data = {"upload_type": "ner"}
        r = requests.post(
            upload_script_url,
            files=files,
            data=data,
            cookies=cookies
        )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert "Upload successful" == json_response.get("message")

    # # Uploading Assertion Status Training Script
    # training_file_path = os.path.join("annotationlab/utils/functions.py")
    # with open(training_file_path, "rb") as file:
    #     files = {"filename": file}
    #     data = {"upload_type": "assertion_status"}
    #     r = requests.post(
    #         upload_script_url, 
    #         files=files, 
    #         data=data, 
    #         cookies=cookies
    #     )
    # json_response = r.json()
    # assert r.status_code == 200
    # assert "message" in json_response
    # assert "Upload successful" == json_response.get("message")

    # Uploding Invalid File type
    training_file_path = os.path.join("annotationlab/config.json")
    with open(training_file_path, "rb") as file:
        files = {"filename": file}
        data = {"upload_type": "classification"}
        r = requests.post(
            upload_script_url, 
            files=files, 
            data=data, 
            cookies=cookies
        )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "Invalid training script type" == json_response.get("error")

    # Uploding Invalid Script type
    training_file_path = os.path.join("annotationlab/utils/io.py")
    with open(training_file_path, "rb") as file:
        files = {"filename": file}
        data = {"upload_type": "ner_assertion"}
        r = requests.post(
            upload_script_url, 
            files=files, 
            data=data, 
            cookies=cookies
        )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "Invalid training script type" == json_response.get("error")

    # Uploading training script from collaborate user
    data = {
        "username": ["collaborate"],
        "scopes": ["Reviewer"]
    }
    add_to_team(PROJECT_NAME, data)
    training_file_path = os.path.join("annotationlab/utils/misc.py")
    with open(training_file_path, "rb") as file:
        files = {"filename": file}
        data = {"upload_type": "classification"}
        r = requests.post(
            upload_script_url, 
            files=files, 
            data=data, 
            cookies=get_cookies("collaborate", "collaborate")
        )
    assert r.status_code == 403


def test_get_training_scripts():
    PROJECT_NAME = "test_upload_training_script"
    list_training_scripts_url = f"{API_URL}/api/project/{PROJECT_NAME}/mt/script"
    r = requests.get(
        list_training_scripts_url, 
        headers=headers, 
        cookies=cookies
    )
    json_response = r.json()
    assert "custom_scripts" in json_response
    custom_scripts = json_response["custom_scripts"]
    assert "ner" in custom_scripts
    assert "db.py" in custom_scripts["ner"]["file_path"]
    assert r.status_code == 200


def test_delete_custom_scripts():
    PROJECT_NAME = "test_upload_training_script"
    delete_script_url = f"{API_URL}/api/project/{PROJECT_NAME}/mt/script"

    # Deleting Assertion Status Training Script
    # data = {"project_name": PROJECT_NAME, "upload_type": "assertion_status"}
    # r = requests.delete(
    #     delete_script_url, 
    #     headers=headers, 
    #     data=json.dumps(data), 
    #     cookies=cookies
    # )
    # assert r.status_code == 204

    # Deleting Assertion Status from Collaborate user (Not allowed)
    data = {"project_name": PROJECT_NAME, "upload_type": "assertion_status"}
    r = requests.delete(
        delete_script_url, 
        headers=headers, 
        data=json.dumps(data), 
        cookies=get_cookies("collaborate", "collaborate")
    )
    assert r.status_code == 403

    # Deleting Invalid Script Type
    data = {"project_name": PROJECT_NAME, "upload_type": "ner_assertion"}
    r = requests.delete(
        delete_script_url, 
        headers=headers, 
        data=json.dumps(data), 
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "ner_assertion script not found" == json_response.get("error")

    # Deleting ner Status Training Script
    data = {"project_name": PROJECT_NAME, "upload_type": "ner"}
    r = requests.delete(
        delete_script_url, headers=headers, data=json.dumps(data), cookies=cookies
    )
    assert r.status_code == 204
    delete_project(PROJECT_NAME)


def test_logout():
    r = requests.get(f'{API_URL}/logout')
    assert any(history.status_code == 302 for history in r.history)
    assert '/auth/realms/master/protocol/openid-connect/auth' in r.url
    r = requests.get(f'{API_URL}/#/projects', allow_redirects=False)
    assert r.status_code == 302


def test_delete_admin_user():
    admin_user_id = requests.get(
        f'{API_URL}/api/users?search=admin',
        headers=headers,
        cookies=cookies
    ).json()["users"]['items'][0]['id']

    r = requests.delete(
        f'{API_URL}/api/users/{admin_user_id}',
        headers=headers,
        cookies=cookies
    )
    assert r.status_code != 204


def test_remove_user_from_admin_group():
    admin_user_id = requests.get(
        f'{API_URL}/api/users?search=admin',
        headers=headers,
        cookies=cookies
    ).json()['users']["items"][0]['id']

    user_groups = requests.get(
        f"{API_URL}/api/user_groups",
        headers=headers,
        cookies=cookies
    ).json()["groups"]
    admin_group_id = [
        x['id'] for x in user_groups if x['name'] == 'UserAdmins'
    ][0]

    r = requests.delete(
        f"{API_URL}/api/users/{admin_user_id}/groups/{admin_group_id}",
        headers=headers,
        cookies=cookies
    )

    assert r.status_code != 201

    # # Make readonly user use an admin
    readonly_user_id = requests.get(
        f'{API_URL}/api/users?search=readonly',
        headers=headers,
        cookies=cookies
    ).json()['users']["items"][0]['id']
    r = requests.put(
        f"{API_URL}/api/users/{readonly_user_id}/groups/{admin_group_id}",
        headers=headers,
        cookies=cookies
    )

    assert r.status_code == 201

    # Remove readonly user from userAdmin group.
    r = requests.delete(
        f"{API_URL}/api/users/{readonly_user_id}/groups/{admin_group_id}",
        headers=headers,
        cookies=cookies
    )

    assert r.status_code == 201


def test_get_all_analytics_permissions():
    r = get_all_analytics_permissions(collaborate_cookie)
    assert r.status_code == 403
    r = get_all_analytics_permissions()
    assert r.status_code == 200
    assert "projects" in r.json()
    assert len(r.json()["projects"]) == 0
    project_name = "test_get_all_analytics_permissions"
    create_project(project_name)
    request_analytics_permission(project_name)
    r = get_all_analytics_permissions()
    assert len(r.json()["projects"]) == 1
    project = r.json()["projects"][0]
    expected_keys = [
        "name",
        "analytics_permission"
    ]
    assert all(key in project for key in expected_keys)
    delete_project(project_name)


def test_get_analytics_permission():
    project_name = "test_get_analytics_permission"
    create_project(project_name)
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    assert r.status_code == 403
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Manager"]
    }
    add_to_team(project_name, data)
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    assert r.status_code == 200
    json_response = r.json()
    assert json_response["analytics_permission"] == {}
    readonly_cookies = get_cookies("readonly", "readonly")
    request_analytics_permission(project_name, readonly_cookies)
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    assert r.status_code == 200
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert json_response["analytics_permission"]["requested_by"] == "readonly"
    assert json_response["analytics_permission"]["status"] == "requested"

    approve_analytics_permission(project_name)
    r = get_analytics_permission_for_project(project_name, collaborate_cookie)
    assert r.status_code == 200
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert "approved_at" in json_response["analytics_permission"]
    assert json_response["analytics_permission"]["requested_by"] == "readonly"
    assert json_response["analytics_permission"]["approved_by"] == "admin"
    assert json_response["analytics_permission"]["status"] == "approved"
    delete_project(project_name)


def test_request_analytics_permission():
    project_name = "test_get_analytics_permission"
    create_project(project_name)
    r = request_analytics_permission(
        project_name, collaborate_cookie
    )
    assert r.status_code == 403
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Manager"]
    }
    add_to_team(project_name, data)
    r = request_analytics_permission(
        project_name, collaborate_cookie
    )
    assert r.status_code == 201
    assert r.json()["message"] == "Analytics request made successfully"
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert (
        json_response["analytics_permission"]["requested_by"] == "collaborate"
    )
    assert json_response["analytics_permission"]["status"] == "requested"
    r = request_analytics_permission(
        project_name, collaborate_cookie
    )
    assert r.status_code == 400
    assert (
        r.json()["error"]
        == "Request already exists. Please contact admin to take action on it."
    )
    approve_analytics_permission(project_name)
    r = request_analytics_permission(
        project_name, collaborate_cookie
    )
    assert r.status_code == 400
    assert r.json()["error"] == "Analytics request is already approved."
    delete_project(project_name)


def test_approve_analytics_permission():
    project_name = "test_approve_analytics_permission"
    create_project(project_name)
    r = approve_analytics_permission(project_name, collaborate_cookie)
    assert r.status_code == 403
    r = approve_analytics_permission(project_name)
    assert r.status_code == 400
    assert r.json()["error"] == "Cannot take action on non-requested project"
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Manager"]
    }
    add_to_team(project_name, data)
    request_analytics_permission(project_name, collaborate_cookie)
    r = approve_analytics_permission(project_name)
    assert r.status_code == 201
    assert r.json()["message"] == "Analytics request updated"
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert "approved_at" in json_response["analytics_permission"]
    assert (
        json_response["analytics_permission"]["requested_by"] == "collaborate"
    )
    assert json_response["analytics_permission"]["approved_by"] == "admin"
    assert json_response["analytics_permission"]["status"] == "approved"
    delete_project(project_name)


def test_reject_analytics_permission():
    project_name = "test_reject_analytics_permission"
    create_project(project_name)
    r = reject_analytics_permission(project_name, collaborate_cookie)
    assert r.status_code == 403
    r = reject_analytics_permission(project_name)
    assert r.status_code == 400
    assert r.json()["error"] == "Cannot take action on non-requested project"
    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Manager"]
    }
    add_to_team(project_name, data)
    request_analytics_permission(project_name, collaborate_cookie)
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert (
        json_response["analytics_permission"]["requested_by"] == "collaborate"
    )
    assert json_response["analytics_permission"]["status"] == "requested"
    r = reject_analytics_permission(project_name)
    assert r.status_code == 201
    assert r.json()["message"] == "Analytics request updated"
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert "denied_at" in json_response["analytics_permission"]
    assert (
        json_response["analytics_permission"]["requested_by"] == "collaborate"
    )
    assert json_response["analytics_permission"]["denied_by"] == "admin"
    assert json_response["analytics_permission"]["status"] == "denied"
    delete_project(project_name)


def test_revoke_analytics_permission():
    project_name = "test_revoke_analytics_permission"
    create_project(project_name)
    r = revoke_analytics_permission(project_name, collaborate_cookie)
    assert r.status_code == 403

    data = {
        "username": ["collaborate", "readonly"],
        "scopes": ["Manager"]
    }
    add_to_team(project_name, data)
    request_analytics_permission(project_name, collaborate_cookie)
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    json_response = r.json()
    assert "requested_at" in json_response["analytics_permission"]
    assert (
        json_response["analytics_permission"]["requested_by"] == "collaborate"
    )
    assert json_response["analytics_permission"]["status"] == "requested"
    r = revoke_analytics_permission(project_name)
    assert r.status_code == 201
    assert r.json()["message"] == "Analytics request updated"
    r = get_analytics_permission_for_project(
        project_name, collaborate_cookie
    )
    assert r.json()["analytics_permission"] == {}
    delete_project(project_name)


def test_get_project_charts():
    project_name = "test_get_project_charts"
    create_project(project_name)
    r = get_project_charts(project_name)
    assert r.status_code == 400
    assert r.json()["error"] == "Analytics is not available for this project."
    request_analytics_permission(project_name)
    approve_analytics_permission(project_name)
    r = get_project_charts(project_name)
    assert r.status_code == 200
    data = r.json()["iaa"][0]
    assert set(data.keys()) == {"name", "data"}
    delete_project(project_name)


def test_refresh_project_charts():
    project_name = "test_refresh_project_charts"
    create_project(project_name)
    r = refresh_project_charts(project_name)
    assert r.status_code == 400
    assert r.json()["error"] == "Analytics is not available for this project."
    request_analytics_permission(project_name)
    approve_analytics_permission(project_name)
    r = refresh_project_charts(project_name)
    assert r.status_code == 201
    assert r.json()["message"] == "Chart is being refreshed"
    r = check_refresh_status(project_name)
    refresh_status = r.json()["status"]
    assert refresh_status == "refreshing"
    while refresh_status == "refreshing":
        r = check_refresh_status(project_name)
        refresh_status = r.json()["status"]

    r = get_project_charts(project_name)
    assert r.status_code == 200
    data = r.json()["iaa"][0]
    assert set(data.keys()) == {"name", "data", "updated_by", "updated_at"}

    delete_project(project_name)


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = f'{current_path}/../exports'
    test_export_as_csv(output_dir)
