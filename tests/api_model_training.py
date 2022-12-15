import time
from tests.utils.api_helper import *
from tests.utils.active_learning_helper import import_tasks, save_config
import json
from tests.utils.helpers import (
    restore_deleted_embeddings,
    delete_embeddings,
    delete_existing_license,
)
from tests.utils.label_config import test_assertion_training_label_config

data = {"username": ["collaborate"], "scopes": ["Annotator"]}
add_to_team("test_model_training_project", data)
collaborate_cookie = get_cookies("collaborate", "collaborate")


def test_set_training_params():
    PROJECT_NAME = "test_model_training_project"
    create_project(PROJECT_NAME)
    training_params_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_params"
    )

    param_data = {
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
        data=json.dumps(param_data),
        headers=headers,
        cookies=collaborate_cookie,
    )
    assert r.status_code == 403

    data = {"advance_option": {"tags": ["Tag1", "Tag2"]}}
    r = requests.post(
        training_params_url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert (
        "Invalid tags: Tag1, Tag2" in json_response["error"]
        or "Invalid tags: Tag2, Tag1" in json_response["error"]
    )

    r = requests.post(
        training_params_url,
        headers=headers,
        data=json.dumps(param_data),
        cookies=cookies,
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert (
        "Training parameters updated successfully!"
        in json_response["message"]
    )


def test_trigger_model_training():
    ensure_license()
    PROJECT_NAME = "test_model_training_project"
    save_config(PROJECT_NAME)
    import_tasks(PROJECT_NAME)
    training_url = f"{API_URL}/api/project/{PROJECT_NAME}/mt/train_model"
    data = {"deploy": True}
    r = requests.post(
        training_url,
        data=json.dumps(data),
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403
    r = requests.post(
        training_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert json_response["message"] == "Training started!"
    training_status_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_status"
    )
    r = requests.get(
        training_status_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    r = requests.get(training_status_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    server_status_count = 0
    while (
        json_response.get("current_server_status", "")
        != "Training (step 1 of 3)" and server_status_count < 30
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


def test_download_model_log_from_models_hub():
    get_model_log_url = (
        f"{API_URL}/api/mt/modelshub/ner_test_model_training_project.model"
        "/training_log"
    )
    r = requests.get(get_model_log_url, headers=headers, cookies=cookies)
    assert r.status_code == 200
    assert (
        "ner_test_model_training_project.model_training.log"
        in r.headers["filename"]
    )


def test_get_latest_training_logs():
    PROJECT_NAME = "test_get_latest_training_logs"
    create_project(PROJECT_NAME)
    get_latest_training_logs_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_log"
    )
    r = requests.get(
        get_latest_training_logs_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    # get logs when no trained model available
    r = requests.get(
        get_latest_training_logs_url,
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "No trained model available!" in json_response["error"]

    # logs of trained model
    get_latest_training_logs_url = (
        f"{API_URL}/api/project/test_model_training_project/mt/training_log"
    )
    r = requests.get(
        get_latest_training_logs_url,
        headers=headers,
        cookies=cookies
    )

    assert r.status_code == 200
    assert r.headers["filename"] == "test_model_training_project_logs.zip"
    delete_project(PROJECT_NAME)


def test_model_training_settings():
    PROJECT_NAME = "test_model_training_project"
    get_settings_url = f"{API_URL}/api/projects/{PROJECT_NAME}/mt/settings"

    r = requests.get(
        get_settings_url,
        headers=headers,
        cookies=collaborate_cookie
    )
    assert r.status_code == 403

    r = requests.get(get_settings_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    assert "settings" in json_response
    assert all(
        key in json_response["settings"]["last_train_stats"]
        for key in ["completion_count", "training_type"]
    )
    assert (
        json_response["settings"]["last_train_stats"]["completion_count"]
        == 31
    )
    assert (
        "manual"
        in json_response["settings"]["last_train_stats"]["training_type"]
    )


def test_get_embeddings():
    user_url = f"{API_URL}/api/modelshub/available_embeddings"
    r = requests.get(user_url, headers=headers, cookies=collaborate_cookie)
    r.status_code == 403

    r = requests.get(user_url, headers=headers, cookies=cookies)
    expected_fields = [
        "embedding_name", "source", "status", "uploaded_at", "version"
    ]
    assert all(
        field in embedding for field in expected_fields
        for embedding in r.json()
    )
    assert r.status_code == 200


def test_select_embeddings():
    PROJECT_NAME = "test_select_embeddings"
    create_project(PROJECT_NAME)
    select_embeddings_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_params"
    )
    # invalid embedding name
    data = {
        "embedding_name": "embedding_name"
    }
    r = requests.post(
        select_embeddings_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "Embeddings not available" in json_response["error"]

    # valid embedding name
    data = {
        "embedding_name": "bert_base_cased"
    }
    r = requests.post(
        select_embeddings_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert (
        "Training parameters updated successfully!"
        in json_response["message"]
    )

    # select transfer learning model 
    data = {
        "transfer_learning_model": {
            "embedding_name": "embeddings_clinical",
            "model_name": "ner_jsl",
            "path": "/models/pretrained/ner_jsl_en_3.1.0_2.4_1624566960534"
        }
    }
    r = requests.post(
        select_embeddings_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert (
        "Training parameters updated successfully!"
        in json_response["message"]
    )

    # select incompatible embedding
    data = {
        "embedding_name": "tfhub_use"
    }
    r = requests.post(
        select_embeddings_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert (
        "tfhub_use embeddings cannot be used in ner model training"
        in json_response["error"]
    )

    delete_project(PROJECT_NAME)


def test_select_model_type():
    PROJECT_NAME = "test_select_model_type"
    create_project(PROJECT_NAME)
    save_config(PROJECT_NAME, test_assertion_training_label_config)
    select_model_type_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_params"
    )
    data = {"model_type": {"name": "hello"}}
    r = requests.post(
        select_model_type_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert (
        "Model type hello not available. "
        "Available types: ['ner', 'assertion']"
        in json_response["error"]
    )

    select_model_type(
        PROJECT_NAME,
        model_type={"model_type": {"name": "assertion"}}
    )
    delete_project(PROJECT_NAME)


def test_update_active_learning_frequency():
    PROJECT_NAME = "test_update_active_learning_frequency"
    create_project(PROJECT_NAME)
    update_active_learning_frequency_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/al/completions_frequency"
    )
    data = {"completions_frequency": "100"}
    r = requests.post(
        update_active_learning_frequency_url,
        headers=headers,
        cookies=collaborate_cookie,
        data=json.dumps(data),
    )
    assert r.status_code == 403

    r = requests.post(
        update_active_learning_frequency_url,
        headers=headers,
        cookies=cookies,
        data=json.dumps(data),
    )
    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert "Active Learning completions frequency updated." in json_response["message"]

    data = {}
    r = requests.post(
        update_active_learning_frequency_url,
        headers=headers,
        cookies=cookies,
        data=json.dumps(data),
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert "Missing completions frequency" in json_response["error"]
    delete_project(PROJECT_NAME)


def test_deploy_model():
    PROJECT_NAME = "test_model_training_project"
    config_url = f"{API_URL}/api/projects/{PROJECT_NAME}/save-config"
    label_config = """
               <View>
            <Labels name="label" toName="text">
                <Label value="Medicine" background="red" model="ner_test_model_training_project.model"/>
                <Label value="MedicalCondition" background="darkorange" model="ner_test_model_training_project.model"/>
                <Label value="Pathogen" background="orange" model="ner_test_model_training_project.model"/>
                <Label value="ORG" background="blue" model="ner_dl"/>
            </Labels>
            <Text name="text" value="$text"/>
        </View>
    """
    r = requests.post(
        config_url,
        data={"label_config": label_config},
        cookies=cookies,
    )
    assert r.status_code == 201
    deploy_model_url = f"{API_URL}/api/project/{PROJECT_NAME}/mt/deploy"
    r = requests.post(deploy_model_url, headers=headers, cookies=collaborate_cookie)
    assert r.status_code == 403

    deleted_embeddings = delete_embeddings("glove_100d")
    r = requests.post(deploy_model_url, headers=headers, cookies=cookies)
    assert r.status_code == 400
    json_response = r.json()
    assert "error" in json_response
    assert (
        json_response["error"] ==
        "Model deployment failed! Embeddings glove_100d not found"
    )
    restore_deleted_embeddings(deleted_embeddings)
    r = requests.post(deploy_model_url, headers=headers, cookies=cookies)
    json_response = r.json()
    r.status_code == 200
    assert "message" in json_response
    assert "Model deployment has started!" in json_response["message"]


def test_get_deployed_model():
    get_deployed_models_info_url = f"{API_URL}/api/mt/deployment_info"
    r = requests.get(get_deployed_models_info_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    deploy_count = 0
    while (
        "ner_dl"
        not in json_response.get("deployment_info", "").get("models_info", "")
        and deploy_count < 30
    ):
        deploy_count += 1
        time.sleep(10)
        r = requests.get(get_deployed_models_info_url, headers=headers, cookies=cookies)
        json_response = r.json()
        assert r.status_code == 200
    assert "embeddings_name" in json_response["deployment_info"]
    assert "glove_100d_en_2" in json_response["deployment_info"]["embeddings_name"]
    assert "models_info" in json_response["deployment_info"]
    assert all(
        models in json_response["deployment_info"]["models_info"]
        for models in [
            "ner_test_model_training_project.model",
            "ner_dl",
        ]
    )


def test_configured_models():
    PROJECT_NAME = "test_model_training_project"
    configured_models_url = f"{API_URL}/api/projects/{PROJECT_NAME}/mt/models_configured"
    r = requests.get(configured_models_url, headers=headers, cookies=collaborate_cookie)
    assert r.status_code == 403

    r = requests.get(configured_models_url, headers=headers, cookies=cookies)
    json_response = r.json()
    assert r.status_code == 200
    assert "models_configured" in json_response
    assert all(
        models in json_response["models_configured"]["ner_labels"]
        for models in ["ner_test_model_training_project.model", "ner_dl"]
    )


def test_enable_disable_active_learning():
    PROJECT_NAME = "test_model_training_project"
    enable_disable_al_url = f"{API_URL}/api/project/{PROJECT_NAME}/al"
    data = {"deploy": False}
    r = requests.post(
        enable_disable_al_url,
        data=json.dumps(data),
        headers=headers,
        cookies=collaborate_cookie,
    )
    assert r.status_code == 403
    r = requests.post(
        enable_disable_al_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 400
    assert "error" in json_response
    assert 'Missing "enabled" parameter' in json_response["error"]

    data = {"enabled": True, "deploy": False}
    r = requests.post(
        enable_disable_al_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 400
    assert "Please select embeddings to train" in json_response["error"]

    # Set embeddings
    select_embeddings_url = (
        f"{API_URL}/api/project/{PROJECT_NAME}/mt/training_params"
    )
    r = requests.post(
        select_embeddings_url,
        data=json.dumps({"embedding_name": "glove_100d"}),
        headers=headers,
        cookies=cookies
    )
    json_response = r.json()
    assert r.status_code == 200

    r = requests.post(
        enable_disable_al_url,
        data=json.dumps(data),
        headers=headers,
        cookies=cookies
    )

    json_response = r.json()
    assert r.status_code == 200
    assert "message" in json_response
    assert (
        "Active Learning setting saved successfully!"
        in json_response["message"]
    )
    delete_project(PROJECT_NAME)


def test_validate_models_with_different_embeddings():
    PROJECT_NAME = "test_validate_models_with_different_embeddings"
    create_project(PROJECT_NAME)
    config_url = f"{API_URL}/api/projects/{PROJECT_NAME}/save-config"
    label_config = """<View>
        <Labels name="label" toName="text">
            <Label value="PER" model="ner_dl"/>
            <Label value="LOC" model="ner_onto_bert_base_cased"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>"""
    r = requests.post(
        config_url,
        data={"label_config": label_config},
        cookies=cookies,
    )
    json_response = r.json()
    r.status_code == 400
    assert (
        "Following models are not using same embeddings."
        in json_response["label_config"][0]["error"]
    )
    expected_result = {
        'ner_dl': 'glove_100d',
        'ner_onto_bert_base_cased': 'bert_base_cased'
    }
    assert (
        json_response["label_config"][0]["incompatible_models_embeddings"]
        == expected_result
    )
    delete_project(PROJECT_NAME)


def test_validate_models_with_missing_embeddings():
    PROJECT_NAME = "test_validate_models_with_missing_embeddings"
    create_project(PROJECT_NAME)
    embedding_name = "bert_base_cased"
    deleted_embeddings = delete_embeddings(embedding_name)
    config_url = f"{API_URL}/api/projects/{PROJECT_NAME}/save-config"
    content = """<View>
        <Labels name="label" toName="text">
            <Label value="DATE" model="ner_onto_bert_base_cased"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>"""
    r = requests.post(
        config_url,
        data={"label_config": content},
        cookies=cookies,
    )
    json_response = r.json()
    assert r.status_code == 400
    assert (
        "Following embeddings not found. "
        "Upload it or download from Models Hub."
        in json_response["label_config"][0]["error"]
    )
    assert (
        json_response["label_config"][0]["embeddings_not_found"]
        == {
            "bert_base_cased": ["ner_onto_bert_base_cased"]
        }
    )
    restore_deleted_embeddings(deleted_embeddings)
    delete_project(PROJECT_NAME)
