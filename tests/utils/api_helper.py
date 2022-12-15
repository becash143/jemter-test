import re
import os
import time
import pandas as pd
import json
import pytest
import requests
from annotationlab.utils.keycloak_cookies import get_cookies
from tests.utils.label_config import (
    test_default_config,
    test_visual_ner_config
)
from tests.utils.helpers import *
from zipfile import ZipFile
from annotationlab.models.user_projects import UserProjects

from tests.utils.helpers import (
    restore_deleted_embeddings,
    delete_embeddings,
)


API_URL = "http://annotationlab:8200"

cookies = get_cookies()

headers = {
    "Host": API_URL.replace("http://", ""),
    "Origin": API_URL,
    "Content-Type": "application/json",
}

CSV_COLS = TSV_COLS = [
    "task_id",
    "text",
    "title",
    "completion_id",
    "sentiment",
    "label",
]
ZIP_CONTENT = {
    "csv": ["result.csv"],
    "tsv": ["result.csv"],
    "json": ["result.json"],
    "json_min": ["result.json"],
    "conll": ["result.conll"],
}


def upload_license(ocr=False, user="ADMIN"):
    JSL_LICENSE = os.environ.get("JSL_LICENSE")
    if not JSL_LICENSE:
        raise Exception("Set JSL_LICENSE in environment")
    _license = json.loads(JSL_LICENSE)
    if ocr and "SPARK_OCR_LICENSE" not in _license.keys():
        raise Exception("Set 'SPARK_OCR_LICENSE' in JSL_LICENSE")
    license_upload_url = f"{API_URL}/api/licenses"
    r = requests.post(
        license_upload_url,
        headers=headers,
        data=json.dumps(_license),
        cookies=cookies
        if user == "ADMIN"
        else get_cookies(username=user, password=user),
    )

    return r


def create_project(project_name: str):
    url = f"{API_URL}/api/projects/create"
    data = {
        "project_name": project_name,
        "project_description": "Demo project",
        "project_sampling": "uniform",
        "project_instruction": "<p><b>Named Entity Recognition</b> Development Project</p>",
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), cookies=cookies)
    return r


def update_project(project_name, update_project_url):
    data = {
        "project_name": project_name,
        "project_description": "test update",
        "project_sampling": "uniform",
        "project_instruction": "<p><b>Named Entity Recognition</b> Development Project</p>",
    }
    r = requests.put(update_project_url, data=json.dumps(data), cookies=cookies)
    assert r.status_code == 200


def save_config(PROJECT_NAME, label_config=test_default_config):
    config_url = f"{API_URL}/api/projects/{PROJECT_NAME}/save-config"
    r = requests.post(
        config_url,
        data={"label_config": label_config},
        cookies=cookies
    )

    assert r.status_code == 201


def get_model_type_of_project(PROJECT_NAME):
    url = f"{API_URL}/api/projects/{PROJECT_NAME}/mt/settings"
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200
    json_response = r.json()
    return json_response['settings']['model_type']['name']


def import_tasks(project_name, tasks):
    import_url = f"{API_URL}/api/projects/{project_name}/import"
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(tasks),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "task_count" in json_response
    assert json_response["task_count"] == len(tasks)


def create_project_with_task(PROJECT_NAME: str):
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    import_url = f"{API_URL}/api/projects/{PROJECT_NAME}/import"
    data = [
        {"text": "hello this is first task", "title": "First"},
        {"text": "hello this is second task", "title": "Second"},
        {
            "text": "12345\tPatient ID: 31133496\t\n John,F. Doe\tBirthday:   "
            "04/11/2000\t\n 6320 [hello? {patient}(id)/(identity&name)]",
            "title": "Third"
        },
    ]
    r = requests.post(
        import_url, headers=headers, data=json.dumps(data), cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 201
    assert "task_count" in json_response
    assert json_response["task_count"] == len(data)
    assert "task_ids" in json_response
    assert len(json_response["task_ids"]) == 3


def create_task_with_completions(PROJECT_NAME):
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 3
    create_url = f"{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions"
    data = {
        "created_username": "admin",
        "created_ago": "2020-09-14T11:26:05.092Z",
        "result": [
            {
                "value": {"choices": ["Discharge", "Assessment"]},
                "id": "po4_Vew0Oy",
                "from_name": "sentiment",
                "to_name": "text",
                "type": "choices",
            },
            {
                "from_name": "label",
                "id": "n9oLJ1vNgD",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {"end": 13, "labels": ["Fact"], "start": 6, "text": "Patient"},
            },
            {
                "from_name": "label",
                "id": "tKMo9ve8QW",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {"end": 40, "labels": ["Ordinal"], "start": 37, "text": "Doe"},
            },
            {
                "from_name": "label",
                "id": "vhMwDQgg7A",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 33,
                    "labels": ["Location"],
                    "start": 29,
                    "text": "John",
                },
            },
            {
                "from_name": "label",
                "id": "vbWCJyO3TG",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 87,
                    "labels": ["Percent"],
                    "start": 80,
                    "text": "patient",
                },
            },
        ],
    }

    r = requests.post(
        create_url, headers=headers, data=json.dumps(data), cookies=cookies
    )
    json_response = r.json()
    COMPLETION_ID = json_response["id"]
    assert r.status_code == 201
    return TASK_ID, COMPLETION_ID


def get_existing_licenses():
    license_url = f"{API_URL}/api/jsl/license"
    r = requests.get(
        license_url,
        headers=headers,
        cookies=cookies
    )
    return r.json()


def ensure_license(ocr=False):
    license_type = "Spark NLP for Healthcare" if not ocr else "Spark OCR"
    existing_licenses = get_existing_licenses()
    # If no license or has expired, upload license
    if (
        license_type not in existing_licenses
        or int(existing_licenses[license_type].split("days")[0].strip()) < 1
    ):
        delete_existing_license()
        # uploading valid license by admin user
        r = upload_license(ocr=ocr)
        assert r.status_code == 200


def create_visual_ner_task_with_completion(PROJECT_NAME, file_path=False):
    import_url = f"{API_URL}/api/projects/{PROJECT_NAME}/import"
    ensure_license(ocr=True)
    if not file_path:
        create_project(PROJECT_NAME)
        save_config(PROJECT_NAME, test_visual_ner_config)
        project_id = UserProjects.get_project_by_project_name(
            PROJECT_NAME, fields=["project_id"]
        ).project_id
        wait_for_server_deployment(PROJECT_NAME, project_id)
        data = {"image": "/static/samples/sample.jpg"}
        completions_path = "/tests/utils/visual_ner_completions.json"
        r = requests.post(
            import_url,
            headers=headers,
            data=json.dumps(data),
            cookies=cookies
        )
    else:
        completions_path = "/tests/utils/multi-page-pdf-completions.json"
        data = {
            "overwrite": False,
            "ocr_enable": False
        }
        with open(file_path, "rb") as file:
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
    assert json_response["total_file_count"] == 1

    wait_for_ocr_process(PROJECT_NAME)

    with open(os.path.join(completions_path), "r") as f:
        data = json.loads(f.read())
        r = create_completions(PROJECT_NAME, 1, data)
        json_response = r.json()
        assert r.status_code == 201


def create_task_with_multiple_completions_and_honeypot(PROJECT_NAME):
    create_project_with_task(PROJECT_NAME)
    TASK_ID = 2
    create_url = f"{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions"
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
                "value": {"end": 13, "labels": ["Fact"], "start": 6, "text": "Patient"},
            },
            {
                "from_name": "label",
                "id": "tKMo9ve8QW",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {"end": 40, "labels": ["Ordinal"], "start": 37, "text": "Doe"},
            },
            {
                "from_name": "label",
                "id": "vhMwDQgg7A",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 33,
                    "labels": ["Location"],
                    "start": 29,
                    "text": "John",
                },
            },
            {
                "from_name": "label",
                "id": "vbWCJyO3TG",
                "source": "$text",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "end": 87,
                    "labels": ["Percent"],
                    "start": 80,
                    "text": "patient",
                },
            },
        ],
    }

    requests.post(create_url, headers=headers, data=json.dumps(data), cookies=cookies)

    r = requests.post(
        create_url, headers=headers, data=json.dumps(data), cookies=cookies
    )

    json_response = r.json()
    COMPLETION_ID = json_response["id"]
    assert r.status_code == 201
    return TASK_ID, COMPLETION_ID


def create_task_with_completions_and_honeypot(PROJECT_NAME):
    TASK_ID, COMPLETION_ID = create_task_with_multiple_completions_and_honeypot(
        PROJECT_NAME
    )
    upate_honeypot_url = f"{API_URL}/api/projects/{PROJECT_NAME}/tasks/{TASK_ID}/completions/{COMPLETION_ID}"
    data = {"honeypot": True}
    r = requests.patch(
        upate_honeypot_url, headers=headers, data=json.dumps(data), cookies=cookies
    )
    assert r.status_code == 201


@pytest.fixture(scope="session")
def output_dir():
    output_dir = "/tmp/exports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def do_export_request(PROJECT_NAME, format, ground_truth=False):
    export_url = f"{API_URL}/api/projects/{PROJECT_NAME}/export?format={format}"

    print(export_url)
    headers = {
        "Host": API_URL.replace("http://", ""),
        "Origin": API_URL,
        "Content-Type": "application/json",
    }
    data = {"groundTruth": ground_truth}
    r = requests.post(
        export_url, data=json.dumps(data), headers=headers, cookies=get_cookies()
    )
    return r


def do_conll_export_request(PROJECT_NAME, format):
    export_url = f"{API_URL}/api/projects/{PROJECT_NAME}/export?format={format}"
    print(export_url)
    headers = {
        "Host": API_URL.replace("http://", ""),
        "Origin": API_URL,
    }
    r = requests.post(
        export_url, headers=headers, cookies=get_cookies()
    )
    print(r)
    return r


def get_csv_info(output_dir, content, sep):
    zip_file = f"{output_dir}/file.zip"
    with open(zip_file, "wb+") as f:
        f.write(content)
        z = ZipFile(f)
        zip_contents = z.namelist()

        with z.open(zip_contents[0], "r") as csv_file:
            df = pd.read_csv(csv_file, sep=sep)
            columns = list(df)
    return zip_contents, columns


def get_json_info(output_dir, content):
    zip_file = f"{output_dir}/file.zip"
    with open(zip_file, "wb+") as f:
        f.write(content)
        z = ZipFile(f)
        zip_contents = z.namelist()
        with z.open(zip_contents[0], "r") as json_file:
            json_data = json.load(json_file)
    return zip_contents, json_data


def get_coco_info(output_dir, content):
    zip_file = f"{output_dir}/file.zip"
    with open(zip_file, "wb+") as f:
        f.write(content)
        z = ZipFile(f)
        zip_contents = z.namelist()
        json_file = next(
            (f for f in zip_contents if f.endswith(".json")),
            None
        )
        if not json_file:
            raise Exception("No JSON file in coco export")
        with z.open(json_file, "r") as fp:
            json_data = json.load(fp)
    return zip_contents, json_data


def verify_all_completion_without_deleted_at(completions):
    for c in completions:
        assert not "deleted_at" in c

    return


def verify_all_completion_as_ground_truth(completions):
    for c in completions:
        assert c["honeypot"] is True

    return


def export_as_conll(PROJECT_NAME, output_dir):
    r = do_conll_export_request(PROJECT_NAME, format="CONLL2003")

    assert r.status_code == 200

    with open(f"{output_dir}/file.zip", "wb+") as f:
        f.write(r.content)
        z = ZipFile(f)
        zip_contents = z.namelist()
        with z.open(zip_contents[0], "r") as fp:
            data = fp.read()
    return zip_contents, data


def add_to_team(project_name, data, cookies=cookies):
    add_to_team_url = f'{API_URL}/api/projects/{project_name}/add_to_team'
    r = requests.post(
        add_to_team_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def delete_project(PROJECT_NAME):
    delete_url = f"{API_URL}/api/projects/{PROJECT_NAME}/delete"

    r = requests.delete(delete_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert json_response["message"] == "Project successfully Deleted!"


def create_user(username, cookies=cookies, dont_assert=False):

    USER_ID = "1"
    user_url = f'{API_URL}/api/users'
    data = {
        "username": username,
        "firstName": "New",
        "lastName": "User",
        "email": "",
        "enabled": True
    }
    r = requests.post(
        user_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    if dont_assert:
        return r
    json_response = r.json()

    USER_ID = json_response['user_id']
    assert r.status_code == 201
    assert 'user_id' in json_response
    return USER_ID



def delete_users(USER_ID, USER_NAME, NEW_USER_NAME, cookies=cookies):
    user_url = f'{API_URL}/api/users/{USER_ID}'
    data = {
        'new_username': NEW_USER_NAME,
        'username': USER_NAME
    }
    r = requests.delete(
        user_url,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def assign_user_to_task(
    project_name: str, assign_to: str, cookies: dict = cookies, task_ids: list = [0, 1]
):

    assignee_url = f"{API_URL}/api/projects/{project_name}/user" f"/{assign_to}/assignee"
    data = {"task_ids": task_ids}
    r = requests.patch(
        assignee_url, headers=headers, data=json.dumps(data), cookies=cookies
    )
    return r


def assign_reviewer_to_task(
    project_name: str, assign_to: str, cookies: dict = cookies, task_ids: list = [0, 1]
):

    reviewer_url = f"{API_URL}/api/projects/{project_name}/user/" f"{assign_to}/reviewer"
    data = {"task_ids": task_ids}
    r = requests.patch(
        reviewer_url, headers=headers, data=json.dumps(data), cookies=cookies
    )
    return r


# Test cases related to review completions
def create_completions(project_name, task_id, completion_data={}, cookies=cookies):
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
                    "labels": ["Organization"],
                },
            }
        ],
    }
    data.update(completion_data)
    r = requests.post(
        f"{API_URL}/api/projects/{project_name}/tasks/{task_id}/completions",
        headers=headers,
        data=json.dumps(data),
        cookies=cookies,
    )
    return r


def give_review(project_name, task_id, completion_id, cookies=cookies):
    data = {
        "review_status": {
            "comment": "good to go",
            "approved": True,
        }
    }
    # give review
    r = requests.patch(
        f"{API_URL}/api/projects/{project_name}/tasks/{task_id}/completions/"
        f"{completion_id}/review",
        headers=headers,
        data=json.dumps(data),
        cookies=cookies,
    )
    return r


def verify_ground_truth_per_user(completions):

    for c in completions:

        if c["id"] in [1002, 1003, 5]:
            assert c["honeypot"] is False
        else:
            assert c["honeypot"] is True
    return


def verfiy_task_status(project_name, expected_status, username):
    list_url = f"{API_URL}/api/projects/{project_name}/tasks"
    for view_as, statuses in expected_status.items():
        url = f"{list_url}?view_as={view_as}"
        r = requests.get(
            url,
            headers=headers,
            cookies=get_cookies(username, username)
        )
        tasks = r.json()["items"]
        expected_ids = set(statuses.keys())
        obtained_ids = set(t["id"] for t in tasks)
        assert expected_ids == obtained_ids
        for task in tasks:
            assert task.get("status") == expected_status[view_as][task["id"]]

def trigger_model_training(project_name: str, deploy: bool = False):
    collaborate_cookie = get_cookies("collaborate", "collaborate")
    training_url = f"{API_URL}/api/project/{project_name}/mt/train_model"
    data = {"deploy": deploy}
    r = requests.post(
        training_url, data=json.dumps(data), headers=headers, cookies=collaborate_cookie
    )
    assert r.status_code == 403

    r = requests.post(
        training_url, data=json.dumps(data), headers=headers, cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert json_response["error"] == "Training failed! Please select model to train"
    select_model_type(project_name)

    deleted_embeddings = delete_embeddings("glove_100d")
    r = requests.post(
        training_url, data=json.dumps(data), headers=headers, cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert json_response["error"] == "Training failed! Please select embeddings"
    restore_deleted_embeddings(deleted_embeddings)
    select_embeddings_url = f"{API_URL}/api/project/{project_name}/mt/embeddings"
    data = {"embedding_name": "glove_100d"}
    r = requests.post(
        select_embeddings_url, data=json.dumps(data), headers=headers, cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 200
    start_training(project_name)


def start_training(project_name: str, deploy: bool = False):
    collaborate_cookie = get_cookies("collaborate", "collaborate")
    data = {"deploy": deploy}
    training_url = f"{API_URL}/api/project/{project_name}/mt/train_model"
    r = requests.post(
        training_url, data=json.dumps(data), headers=headers, cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert json_response["message"] == "Training started!"
    training_status_url = f"{API_URL}/api/project/{project_name}/mt/training_status"
    r = requests.get(training_status_url, headers=headers, cookies=collaborate_cookie)
    assert r.status_code == 403

    r = requests.get(training_status_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    server_status_count = 0
    while (
        json_response.get("current_server_status", "") != "Training (step 1 of 3)"
        and server_status_count < 30
    ):
        server_status_count += 1
        time.sleep(2)
        r = requests.get(training_status_url, headers=headers, cookies=cookies)
        json_response = r.json()
        assert r.status_code == 200
    assert all(
        key in json_response
        for key in ["latest_training_status", "current_server_status"]
    )
    assert "running" in json_response["latest_training_status"]
    training_status_count = 0
    while (
        json_response.get("latest_training_status", "") != "success"
        and training_status_count < 30
    ):
        training_status_count += 1
        time.sleep(10)
        r = requests.get(training_status_url, headers=headers, cookies=cookies)
        json_response = r.json()
        assert r.status_code == 200
    assert "not_run_yet" in json_response["current_server_status"]


def download_model_embeddings(name: str, type: str, download_link: str, entities: list):
    download_url = f"{API_URL}/api/modelshub/download"
    data = [
        {
            "name": name,
            "type": type,
            "download_link": download_link,
            "entities": entities,
        }
    ]
    r = requests.post(
        download_url, data=json.dumps(data), headers=headers, cookies=cookies
    )
    assert r.status_code == 201

def delete_model_embeddings(name: str, type: str):
    delete_url = f"{API_URL}/api/modelshub/delete"
    data = {
        "name": name,
        "type": type,
    }
    r = requests.delete(
        delete_url, data=json.dumps(data), headers=headers, cookies=cookies
    )
    assert r.status_code == 200

def select_model_type(PROJECT_NAME, model_type={}):
    if not model_type:
        model_type = {"model_type": {"name": "ner"}}
    select_model_type_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_params"
    )
    r = requests.post(
        select_model_type_url,
        json=model_type,
        headers=headers,
        cookies=cookies,
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response

    assert (
        "Training parameters updated successfully"
        in json_response["message"]
    )


def download_public_file(link, path):
    with requests.get(link, stream=True) as r:
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def upload_models_embeddings(file_path, data):
    total_chunks = int(data["dztotalchunkcount"])
    chunk_size = 5000000
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    filename = file_path.split("/")[-1]

    with open(file_path, "rb") as file:
        files = {"file": file}
        for current_chunk in range(1, total_chunks + 1):
            data.update({
                "dzchunkindex": str(current_chunk - 1),
                "dzchunkbyteoffset": str(chunk_size * (current_chunk - 1))
            })
            r = requests.post(
                upload_url,
                files=files,
                data=data,
                cookies=cookies
            )

            if current_chunk != total_chunks:
                assert r.status_code == 200
                assert r.json()["message"] == (
                    f"Chunk {current_chunk} of {total_chunks} "
                    f"for file {filename} uploaded successfully"
                )
    return r


def delete_project_task(PROJECT_NAME, task_id):
    delete_url = f'{API_URL}/api/projects/{PROJECT_NAME}/tasks_delete'
    data = {
        "task_ids": [
            task_id
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


def wait_for_server_deployment(project_name, project_id):
    deployment_check_url = (
        f"{API_URL}/api/projects/{project_name}/mt/deployment_info"
        f"?server_project_id={project_id}"
    )
    r = requests.get(
        deployment_check_url,
        headers=headers,
        cookies=cookies
    )
    try:
        if "models_info" in r.json()["deployment_info"]:
            return
    except Exception:
        pass
    deployment_url = (
        f"{API_URL}/api/projects/{project_name}/mt/deploy_default_model"
    )
    # Wait 20 secs for the error "Model server is busy" to go away
    # (It appears because of project deletion from previous test)
    start = time.time()
    while (time.time() - start) < 20:
        r = requests.get(
            deployment_url,
            headers=headers,
            cookies=cookies
        )
        if r.json().get("error"):
            time.sleep(2)
            continue
        assert r.status_code == 200
        assert r.json()["message"] == "Default model deployment started!"
        break

    while True:
        try:
            r = requests.get(
                deployment_check_url,
                headers=headers,
                cookies=cookies
            )
            assert "models_info" in r.json()["deployment_info"]
            break
        except Exception:
            # Check after 2 seconds
            time.sleep(2)


def wait_for_ocr_process(PROJECT_NAME):
    ocr_status_url = f"{API_URL}/api/projects/{PROJECT_NAME}/ocr_status"
    while True:
        r = requests.get(
            ocr_status_url,
            headers=headers,
            cookies=cookies
        )
        json_response = r.json()
        assert r.status_code == 200
        if not json_response["is_ocr_running"]:
            break
        # Wait 5 secs and check again
        time.sleep(5)


def get_embeddings_status(name):
    get_embbedings_url = f"{API_URL}/api/modelshub/available_embeddings"
    r = requests.get(
        get_embbedings_url,
        headers=headers,
        cookies=cookies,
    )
    json_response = r.json()
    data = [
        data for data in json_response if data.get("embedding_name") == name
    ]
    assert len(data)
    return data[0].get("status")


def get_model_status(name):
    get_embbedings_url = f"{API_URL}/api/modelshub/available_models"
    r = requests.get(
        get_embbedings_url,
        headers=headers,
        cookies=cookies,
    )
    json_response = r.json()
    data = [data for data in json_response if data.get("model_name") == name]
    assert len(data)
    return data[0].get("status")


def get_all_analytics_permissions(cookies=cookies):
    analytics_url = f"{API_URL}/api/analytics_permission"
    r = requests.get(
        analytics_url,
        headers=headers,
        cookies=cookies
    )
    return r


def get_analytics_permission_for_project(project_name, cookies=cookies):
    url = f"{API_URL}/api/projects/{project_name}/analytics_permission"
    r = requests.get(
        url,
        headers=headers,
        cookies=cookies
    )
    return r


def request_analytics_permission(project_name, cookies=cookies):
    request_url = f"{API_URL}/api/projects/{project_name}/request_analytics"
    r = requests.post(
        request_url,
        headers=headers,
        cookies=cookies
    )
    return r


def approve_analytics_permission(project_name, cookies=cookies):
    approve_url = f'{API_URL}/api/analytics_permission'
    data = {
        "allowed": True,
        "project_name": project_name
    }
    r = requests.patch(
        approve_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def reject_analytics_permission(project_name, cookies=cookies):
    reject_url = f'{API_URL}/api/analytics_permission'
    data = {
        "allowed": False,
        "project_name": project_name
    }
    r = requests.patch(
        reject_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def revoke_analytics_permission(project_name, cookies=cookies):
    revoke_url = f'{API_URL}/api/analytics_permission'
    data = {
        "project_name": project_name
    }
    r = requests.delete(
        revoke_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def get_project_charts(project_name):
    charts_url = f"{API_URL}/api/projects/{project_name}/charts"
    r = requests.get(
        charts_url,
        headers=headers,
        cookies=cookies
    )
    return r


def refresh_project_charts(project_name):
    charts_url = f"{API_URL}/api/projects/{project_name}/charts/refresh"
    r = requests.get(
        charts_url,
        headers=headers,
        cookies=cookies
    )
    return r


def check_refresh_status(project_name):
    url = f"{API_URL}/api/projects/{project_name}/charts/check_refresh_status"
    r = requests.get(
        url,
        headers=headers,
        cookies=cookies
    )
    return r
