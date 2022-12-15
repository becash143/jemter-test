from tests.utils.api_helper import *
from tests.utils.active_learning_helper import save_config
import json
from tests.utils.helpers import delete_existing_license
import os
import uuid
import requests
from math import ceil
from tests.api import API_URL, cookies


MODEL_NAME = "onto_electra_small_uncased"
EMBEDDINGS_NAME = "electra_small_uncased"

VALID_MODEL_FILE = f"{MODEL_NAME}_en_2.7.0_2.4_1607202932422.zip"
VALID_EMBEDDINGS_FILE = f"{EMBEDDINGS_NAME}_en_2.6.0_2.4_1598485458536.zip"
INVALID_MODEL_FILE = "dependency_typed_conllu_en_3.0.0_3.0_1616862441841.zip"

MODEL_PATH = f"/tmp/{VALID_MODEL_FILE}"
INVALID_MODEL_PATH = f"/tmp/{INVALID_MODEL_FILE}"
EMBEDDINGS_PATH = f"/tmp/{VALID_EMBEDDINGS_FILE}"


def test_download_free_embeddings():
    delete_existing_license()

    # test licensed embeddings without license
    download_model_embeddings(
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "clinical/models/"
        "sbert_jsl_mini_umls_uncased_en_3.1.0_2.4_1625050218116.zip",
        entities=[""],
        name="sbert_jsl_mini_umls_uncased",
        type="Embeddings",
    )
    embeddings_status = get_embeddings_status(
        name="sbert_jsl_mini_umls_uncased"
    )
    count = 0
    while embeddings_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        embeddings_status = get_embeddings_status(
            name="sbert_jsl_mini_umls_uncased"
        )

    assert embeddings_status == "failed"
    delete_model_embeddings(
        name="sbert_jsl_mini_umls_uncased", type="Embeddings"
    )

    download_model_embeddings(
        name="sent_electra_small_uncased",
        type="Embeddings",
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "public/models/"
        "sent_electra_small_uncased_en_2.6.0_2.4_1598489761661.zip",
        entities=[""],
    )
    count = 0
    embeddings_status = get_embeddings_status(
        name="sent_electra_small_uncased"
    )
    while embeddings_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        embeddings_status = get_embeddings_status(
            name="sent_electra_small_uncased"
        )

    assert embeddings_status == "downloaded"
    delete_model_embeddings(
        name="sent_electra_small_uncased", type="Embeddings"
    )


def test_download_licensed_embeddings():
    ensure_license()
    download_model_embeddings(
        name="sbert_jsl_mini_uncased",
        type="Embeddings",
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "clinical/models/"
        "sbert_jsl_mini_uncased_en_3.1.0_2.4_1625050221194.zip",
        entities=[],
    )
    count = 0
    embeddings_status = get_embeddings_status(name="sbert_jsl_mini_uncased")
    while embeddings_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        embeddings_status = get_embeddings_status(
            name="sbert_jsl_mini_uncased"
        )

    assert embeddings_status == "downloaded"
    delete_model_embeddings(name="sbert_jsl_mini_uncased", type="Embeddings")


def test_download_ner_free_model():
    delete_existing_license()

    # test licensed model without license
    download_model_embeddings(
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "clinical/models/"
        "ner_genetic_variants_en_3.1.0_3.0_1624607526370.zip",
        entities=["DNAMutation", "ProteinMutation", "SNP"],
        name="ner_genetic_variants",
        type="Named Entity Recognition",
    )
    model_status = get_model_status(name="ner_genetic_variants")
    count = 0
    while model_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        model_status = get_model_status(name="ner_genetic_variants")

    assert model_status == "failed"
    delete_model_embeddings(name="ner_genetic_variants", type="Models")

    download_model_embeddings(
        name="onto_electra_small_uncased",
        type="Named Entity Recognition",
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "public/models/"
        "onto_electra_small_uncased_en_2.7.0_2.4_1607202932422.zip",
        entities=["CARDINAL", "DATE", "EVENT"],
    )
    count = 0
    model_status = get_model_status(name="ner_onto_electra_small_uncased")
    while model_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        model_status = get_model_status(name="ner_onto_electra_small_uncased")

    assert model_status == "downloaded"
    delete_model_embeddings(
        name="ner_onto_electra_small_uncased", type="Models"
    )


def test_download_ner_licensed_model():
    ensure_license()
    download_model_embeddings(
        name="ner_ade_healthcare",
        type="Named Entity Recognition",
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "clinical/models/"
        "ner_ade_healthcare_en_3.0.0_3.0_1617260836627.zip",
        entities=["DRUG", "ADE"],
    )
    count = 0
    model_status = get_model_status(name="ner_ade_healthcare")
    while model_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        model_status = get_model_status(name="ner_ade_healthcare")

    assert model_status == "downloaded"
    delete_model_embeddings(name="ner_ade_healthcare", type="Models")


def test_download_classification_free_model():
    delete_existing_license()
    download_model_embeddings(
        name="classifierdl_use_atis",
        type="Text Classification",
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "public/models/classifierdl_use_atis_en_2.7.1_2.4_1611572512585.zip",
        entities=[
            "atis_abbreviation",
            "atis_airfare",
            "atis_airline",
            "atis_flight",
            "atis_ground_service",
        ],
    )
    count = 0
    model_status = get_model_status(
        name="classification_classifierdl_use_atis"
    )
    while model_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        model_status = get_model_status(
            name="classification_classifierdl_use_atis"
        )

    assert model_status == "downloaded"
    delete_model_embeddings(
        name="classification_classifierdl_use_atis", type="Models"
    )


def test_download_classification_licensed_model():
    delete_existing_license()
    r = upload_license()
    if isinstance(r, str):
        raise Exception(r)
    download_model_embeddings(
        name="classifierdl_gender_biobert",
        type="Text Classification",
        download_link="https://s3.amazonaws.com/auxdata.johnsnowlabs.com/"
        "clinical/models/"
        "classifierdl_gender_biobert_en_2.7.1_2.4_1611247084544.zip",
        entities=["Female", "Male", "Unknown"],
    )

    count = 0
    model_status = ""
    while model_status not in ["failed", "downloaded"] and count < 10:
        count += 1
        time.sleep(3)
        model_status = get_model_status(
            name="classification_classifierdl_gender_biobert"
        )

    assert model_status == "downloaded"
    delete_model_embeddings(
        name="classification_classifierdl_gender_biobert", type="Models"
    )


def prepare_zips():
    download_info = {
        VALID_MODEL_FILE: MODEL_PATH,
        INVALID_MODEL_FILE: INVALID_MODEL_PATH,
        VALID_EMBEDDINGS_FILE: EMBEDDINGS_PATH,
    }
    for _file, download_path in download_info.items():
        link = (
            "https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/models/"
            f"{_file}"
        )
        download_public_file(link, download_path)


prepare_zips()


def test_upload_model_missing_param():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    with open(MODEL_PATH, "rb") as file:
        files = {"file": file}
        r = requests.post(
            upload_url,
            data={
                "upload_type": "models",
                "dztotalfilesize": "100",
                "dzuuid": str(uuid.uuid4()),
            },
            files=files,
            cookies=cookies,
        )
        assert r.status_code == 400
        assert r.json()["error"] == (
            "Missing required parameters "
            "['model_name', 'model_type', 'upload_type', 'labels']."
        )


def test_upload_model_invalid_upload_type():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    data = {
        "model_name": "BCD$#^@(",
        "model_type": "abc",
        "upload_type": "invalid",
        "description": "",
        "labels": json.dumps(["l1", "l2", "l3"]),
        "dztotalfilesize": "100",
        "dzuuid": str(uuid.uuid4()),
    }
    with open(MODEL_PATH, "rb") as file:
        files = {"file": file}
        r = requests.post(upload_url, data=data, files=files, cookies=cookies)
        assert r.status_code == 400
        assert r.json()["error"] == "Invalid upload type"


def test_upload_model_invalid_model_name():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    data = {
        "model_name": "BCD$#^@(",
        "model_type": "abc",
        "upload_type": "models",
        "description": "",
        "labels": json.dumps(["l1", "l2", "l3"]),
        "dztotalfilesize": "100",
        "dzuuid": str(uuid.uuid4()),
        "language": "en"
    }
    with open(MODEL_PATH, "rb") as file:
        files = {"file": file}
        r = requests.post(upload_url, data=data, files=files, cookies=cookies)
        assert r.status_code == 400
        assert r.json()["error"] == (
            "Name can only use alphanumeric, underscores(_), "
            "periods(.) and hyphens(-) with maximum 100 characters."
        )


def test_upload_model_invalid_labels():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    data = {
        "model_name": MODEL_NAME,
        "model_type": "abc",
        "upload_type": "models",
        "description": "",
        "labels": json.dumps(["l1", "l#$"]),
        "dztotalfilesize": "100",
        "dzuuid": str(uuid.uuid4()),
        "language": "en"
    }
    with open(MODEL_PATH, "rb") as file:
        files = {"file": file}
        r = requests.post(upload_url, data=data, files=files, cookies=cookies)
        assert r.status_code == 400
        assert r.json()["error"] == (
            "Label can only use alphanumeric, "
            "underscores(_), periods(.), brackets((),[]) and hyphens(-) with "
            "maximum 100 characters"
        )


def test_upload_model_invalid_model_type():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    with open(MODEL_PATH, "rb") as file:
        files = {"file": file}
        data = {
            "model_name": MODEL_NAME,
            "model_type": "abc",
            "upload_type": "models",
            "description": "",
            "labels": json.dumps(["l1", "l2"]),
            "dztotalfilesize": "100",
            "dzuuid": str(uuid.uuid4()),
            "language": "en"
        }
        r = requests.post(upload_url, data=data, files=files, cookies=cookies)
        assert r.status_code == 400
        assert r.json()["error"] == "Invalid config type."


def test_upload_model_invalid_model_zip():
    total_size = os.stat(INVALID_MODEL_PATH).st_size
    chunk_size = 5000000
    total_chunks = ceil(total_size / chunk_size)
    data = {
        "dzuuid": str(uuid.uuid4()),
        "dzchunkindex": "0",
        "dztotalfilesize": str(total_size),
        "dzchunksize": str(chunk_size),
        "dztotalchunkcount": str(total_chunks),
        "dzchunkbyteoffset": "",
        "upload_type": "models",
        "model_name": "dependency_typed_conllu_en",
        "model_type": "ner",
        "description": "",
        "labels": json.dumps(["l1", "l2"]),
        "language": "en"
    }

    r = upload_models_embeddings(INVALID_MODEL_PATH, data)
    assert r.status_code == 400
    assert r.json()["error"] == "Can't upload. Invalid models file!"


def test_upload_model_valid_model_zip():
    filename = MODEL_PATH.split("/")[-1]
    total_size = os.stat(MODEL_PATH).st_size
    chunk_size = 5000000
    total_chunks = ceil(total_size / chunk_size)
    data = {
        "dzuuid": str(uuid.uuid4()),
        "dzchunkindex": "0",
        "dztotalfilesize": str(total_size),
        "dzchunksize": str(chunk_size),
        "dztotalchunkcount": str(total_chunks),
        "dzchunkbyteoffset": "",
        "upload_type": "models",
        "model_name": MODEL_NAME,
        "model_type": "ner",
        "description": "",
        "labels": json.dumps(["l1", "l2"]),
        "language": "en"
    }
    r = upload_models_embeddings(MODEL_PATH, data)
    assert r.status_code == 201
    assert r.json()["message"] == (f"models {filename} uploaded successfully")


def test_upload_model_already_exists():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    data = {
        "upload_type": "models",
        "model_name": MODEL_NAME,
        "model_type": "ner",
        "description": "",
        "labels": json.dumps(["l1", "l2"]),
        "dztotalfilesize": "100",
        "dzuuid": str(uuid.uuid4()),
        "language": "en"
    }
    with open(MODEL_PATH, "rb") as file:
        files = {"file": file}
        r = requests.post(upload_url, files=files, data=data, cookies=cookies)
        assert r.status_code == 400
        assert (
            "Uploaded model already exists; " f"name: 'ner_{MODEL_NAME}' "
        ) in r.json()["error"]


def test_upload_embeddings():
    total_size = os.stat(EMBEDDINGS_PATH).st_size
    chunk_size = 5000000
    total_chunks = ceil(total_size / chunk_size)
    data = {
        "dzuuid": str(uuid.uuid4()),
        "dzchunkindex": "0",
        "dztotalfilesize": str(total_size),
        "dzchunksize": str(chunk_size),
        "dztotalchunkcount": str(total_chunks),
        "dzchunkbyteoffset": "",
        "upload_type": "embeddings",
        "language": "en"
    }
    r = upload_models_embeddings(EMBEDDINGS_PATH, data)
    assert r.status_code == 201
    assert r.json()["message"] == (
        f"embeddings {VALID_EMBEDDINGS_FILE} uploaded successfully"
    )


def test_upload_embeddings_already_exists():
    upload_url = f"{API_URL}/api/mt/modelshub/import"
    data = {
        "dzuuid": str(uuid.uuid4()),
        "dztotalfilesize": "100",
        "upload_type": "embeddings",
        "language": "en"
    }
    with open(EMBEDDINGS_PATH, "rb") as file:
        files = {"file": file}
        r = requests.post(upload_url, files=files, data=data, cookies=cookies)
        assert r.status_code == 400
        assert (
            "Embeddings already exists; " f"name: '{EMBEDDINGS_NAME}' "
        ) in r.json()["error"]


def test_delete_default_model_embeddings():
    default_models = {"Embeddings": "glove_100d", "Models": "ner_onto_100"}
    for _type, name in default_models.items():
        payload = {
            "name": name,
            "type": _type,
        }
        delete_url = f"{API_URL}/api/modelshub/delete"
        r = requests.delete(delete_url, json=payload, cookies=cookies)
        assert r.status_code == 400
        msg = "model" if _type == "Models" else "embeddings"
        assert r.json()["error"] == f"Deleting default {msg} is not allowed"


def test_delete_existing_model_in_use():
    model_name = f"ner_{MODEL_NAME}"
    label_config = f"""
    <View>
      <Labels name="label" toName="text">
        <Label value="l1" model="{model_name}"/>
        <Label value="l2" model="{model_name}"/>
      </Labels>
      <Text name="text" value="$text"/>
    </View>

    """
    project_name = "test_delete_existing_model_in_use"
    create_project(project_name)
    save_config(project_name, label_config)
    payload = {
        "name": model_name,
        "type": "Models",
    }
    delete_url = f"{API_URL}/api/modelshub/delete"
    r = requests.delete(delete_url, json=payload, cookies=cookies)
    assert r.status_code == 400
    assert r.json()["error"] == (
        f"The models '{model_name}' is used by following projects and "
        f"cannot be deleted {project_name} (owned by admin)"
    )

def test_delete_existing_embeddings_in_use():
    project_name = "test_delete_existing_model_in_use"
    save_url = f"{API_URL}/api/project/{project_name}/mt/training_params"
    r = requests.post(
        save_url,
        json={"embedding_name": EMBEDDINGS_NAME},
        cookies=cookies,
    )
    assert r.status_code == 200

    payload = {
        "name": EMBEDDINGS_NAME,
        "type": "Embeddings",
    }
    delete_url = f"{API_URL}/api/modelshub/delete"
    r = requests.delete(delete_url, json=payload, cookies=cookies)
    assert r.status_code == 400
    assert r.json()["error"] == (
        f"The embeddings '{EMBEDDINGS_NAME}' is used by following projects "
        f"and cannot be deleted {project_name} (owned by admin)"
    )
    delete_project(project_name)


def test_delete_existing_model_not_in_use():
    existing_model = f"ner_{MODEL_NAME}"
    payload = {
        "name": existing_model,
        "type": "Models",
    }
    delete_url = f"{API_URL}/api/modelshub/delete"
    r = requests.delete(delete_url, json=payload, cookies=cookies)
    assert r.status_code == 200
    assert r.json()["message"] == "Models deleted"


def test_delete_existing_embeddings_not_in_use():
    payload = {
        "name": EMBEDDINGS_NAME,
        "type": "Embeddings",
    }
    delete_url = f"{API_URL}/api/modelshub/delete"
    r = requests.delete(delete_url, json=payload, cookies=cookies)
    assert r.status_code == 200
    assert r.json()["message"] == "Embeddings deleted"


def test_delete_invalid_model_embeddings():
    invalid_data = {"Embeddings": "invalid_EM", "Models": "invalid_Model"}
    for _type, name in invalid_data.items():
        payload = {
            "name": name,
            "type": _type,
        }
        delete_url = f"{API_URL}/api/modelshub/delete"
        r = requests.delete(delete_url, json=payload, cookies=cookies)
        assert r.status_code == 400
        msg = "model" if _type == "Models" else "embeddings"
        assert r.json()["error"] == (
            f"Cannot find existing {msg} with name '{name}'"
        )
