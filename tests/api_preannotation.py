import time
from tests.utils.api_helper import *
from tests.utils.active_learning_helper import import_tasks, save_config
from tests.utils.helpers import (
    restore_deleted_embeddings,
    delete_embeddings,
    delete_existing_license,
)

collaborate_cookie = get_cookies("collaborate", "collaborate")


def test_preannotation():
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    PROJECT_NAME = "test_preannotation_project"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME)
    import_tasks(PROJECT_NAME)
    training_params_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_params"
    )
    data = {
        "training_params": {
            "val_split": "0.5",
            "epoch": "10",
            "lr": "0.002",
            "lr_decay": "0.006",
            "dropout": "0.7",
            "batch": "60",
        },
        "advance_option": {"tags": []},
    }
    r = requests.post(
        training_params_url,
        data=json.dumps(data),
        headers=headers,
        cookies=collaborate_cookie,
    )
    assert r.status_code == 403

    r = requests.post(
        training_params_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies,
    )
    training_url = f"{API_URL}/api/project/{PROJECT_NAME}/mt/train_model"
    training_status_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_status"
    )
    data = {"deploy": True}
    r = requests.post(
        training_url,
        data=json.dumps(data),
        headers=headers,
        cookies=collaborate_cookie,
    )
    assert r.status_code == 403
    r = requests.post(
        training_url, data=json.dumps(data), headers=headers, cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert json_response["message"] == "Training started!"
    r = requests.get(
        training_status_url, headers=headers, cookies=collaborate_cookie
    )
    assert r.status_code == 403

    r = requests.get(training_status_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    training_status_count = 0
    while (
        json_response.get("latest_training_status", "") != "success"
        and training_status_count < 12
    ):
        training_status_count += 1
        time.sleep(10)
        r = requests.get(training_status_url, headers=headers, cookies=cookies)
        json_response = r.json()
        assert r.status_code == 200
    assert "not_run_yet" in json_response["current_server_status"]
    assert "success" in json_response["latest_training_status"]

    preannotation_url = f"{API_URL}/api/projects/{PROJECT_NAME}/preannotate"
    data = {"task_ids": [30, 29]}
    r = requests.post(
        preannotation_url,
        headers=headers,
        data=json.dumps(data),
        cookies=collaborate_cookie,
    )
    assert r.status_code == 403

    deleted_embeddings = delete_embeddings("glove_100d")
    r = requests.post(
        preannotation_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies,
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert (
        json_response["error"]
        == "Preannotation Failed! Embeddings glove_100d not found"
    )
    restore_deleted_embeddings(deleted_embeddings)
    r = requests.post(
        preannotation_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies,
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert "Preannotation Started!" in json_response["message"]

    pre_annoatation_status_url = (
        f"{API_URL}/api/projects/{PROJECT_NAME}/preannotation_status"
    )
    r = requests.get(
        pre_annoatation_status_url, headers=headers, cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200
    assert all(
        (
            key in json_response
            for key in ["preannotation_task_status", "running"]
        )
    )
    assert 2 == json_response["running"]
    assert all(
        key in json_response["preannotation_task_status"]
        for key in ["29", "30"]
    )
    for task_id, status in json_response["preannotation_task_status"].items():
        assert task_id in ["29", "30"]
        assert status == {"message": "", "state": "running"}
    preannotation_status_count = 0
    while (
        0 != json_response.get("running", "")
        and preannotation_status_count < 12
    ):
        preannotation_status_count += 1
        time.sleep(5)
        r = requests.get(
            pre_annoatation_status_url, headers=headers, cookies=cookies
        )
        json_response = r.json()
        assert r.status_code == 200
    assert 0 == json_response["running"]
    for task_id, status in json_response["preannotation_task_status"].items():
        assert task_id in ["29", "30"]
        assert status == {"message": "", "state": "success"}
    delete_project(PROJECT_NAME)
