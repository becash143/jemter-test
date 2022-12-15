import json
import os
import random as rand
from datetime import datetime

import requests
USERNAME = PASSWORD = TASK_CREATED_BY = "admin"
COMPLETION_CREATED_BY = "admin"
PROJECT_NAME = "sample_classification_project"
all_labels = set()
to_unique = set()
tasks = []
API_URL = os.environ.get("ANNOTATIONLAB_URL", "http://annotationlab:8200")
headers = {
    'Host': API_URL.replace('http://', ''),
    'Origin': API_URL,
    'Content-Type': 'application/json'
}


def get_cookies():
    keycloak_url = os.environ.get("KEYCLOAK_SERVER_URL",
                                  "http://keycloak-local:8080/auth/")
    keycloak_realm = os.environ.get("KEYCLOAK_REALM_NAME", "master")
    url = f"{keycloak_url}realms/{keycloak_realm}/protocol" \
          "/openid-connect/token"
    data = {
        "grant_type": "password",
        "username": os.environ.get("KEYCLOAK_SUPERUSER_USER", USERNAME),
        "password": os.environ.get("KEYCLOAK_SUPERUSER_PASS", PASSWORD),
        "client_id": os.environ.get("KEYCLOAK_CLIENT_ID", "annotationlab"),
        "client_secret": os.environ.get("KEYCLOAK_CLIENT_SECRET_KEY",
                                        "09a71c59-0351-4ce6-bc8f-8fd3feb9d2ff")
    }
    auth_info = requests.post(url, data=data).json()
    cookies = {
        'access_token': f"Bearer {auth_info['access_token']}",
        'refresh_token': auth_info['refresh_token']
    }
    return cookies


cookies = get_cookies()

with open("tests/active-learning/classification.json", "r") as f:
    data = json.loads(f.read())


def generate_hash(length=10):
    nums = list(range(48, 58))
    uppers = list(range(65, 91))
    lowers = list(range(97, 123))
    all_chars = nums + uppers + lowers
    return "".join(
        [chr(all_chars[rand.randint(0, len(all_chars) - 1)]) for x in range(length)]
    )


def build_choices(choices):
    # TO-TEST how to support multiple label?
    classification_json = {
        "from_name": "sentiment",
        "id": generate_hash(),
        #         "source": "$text",
        "to_name": "text",
        "type": "choices",
        "value": {"choices": [choices]}
    }
    return classification_json


def get_completions(classification):
    completions = []
    results = []
    
    choices = classification.get('category')
    result = build_choices(choices)
    results.append(result)
    completions.append(
        {
            "created_username": COMPLETION_CREATED_BY,
            "created_ago": datetime.now().isoformat() + "Z",
            "lead_time": 2.476,
            "result": results,
            "honeypot": True,
            "submitted_at":datetime.now().isoformat() + "Z",
        }
    )
    return completions


for each in data.get("examples"):
    completions = get_completions(each)
    a_task = {
        "completions": completions,
        "predictions": [],
        "created_at": str(datetime.now()).split(".")[0],
        "created_by": TASK_CREATED_BY,
        "data": {"text": each.get("description"), "title": ""},
    }
    tasks.append(a_task)

print(all_labels)


def get_cookies():
    keycloak_url = os.environ.get(
        "KEYCLOAK_SERVER_URL", "http://keycloak-local:8080/auth/"
    )
    keycloak_realm = os.environ.get("KEYCLOAK_REALM_NAME", "master")
    url = f"{keycloak_url}realms/{keycloak_realm}/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "username": os.environ.get("KEYCLOAK_SUPERUSER_USER", "admin"),
        "password": os.environ.get("KEYCLOAK_SUPERUSER_PASS", "admin"),
        "client_id": os.environ.get("KEYCLOAK_CLIENT_ID", "annotationlab"),
        "client_secret": os.environ.get(
            "KEYCLOAK_CLIENT_SECRET_KEY", "09a71c59-0351-4ce6-bc8f-8fd3feb9d2ff"
        ),
    }
    auth_info = requests.post(url, data=data).json()
    cookies = {
        "access_token": f"Bearer {auth_info['access_token']}",
        "refresh_token": auth_info["refresh_token"],
    }
    return cookies


def import_tasks(tasks, project_name):
    import_url = f"{API_URL}/api/projects/{project_name}/import"
    r = requests.post(
        import_url,
        headers=headers,
        data=json.dumps(tasks),
        cookies=cookies
    )
    print("Response from Annotation Lab")
    print(r.text)


def create_project():
    url = f'{API_URL}/api/projects/create'
    data = {"project_name": PROJECT_NAME, "project_description": "Demo project", "project_sampling": "uniform",
            "project_instruction": "<p><b>Named Entity Recognition</b> Development Project</p>"}
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        cookies=cookies
    )
    return r


def save_config():
    config_url = f'{API_URL}/api/projects/{PROJECT_NAME}/save-config'
    label_config = """
        <View>
            <Text name="text" value="$text" />
            <Choices name="sentiment" toName="text" choice="multiple">

                <Header value="Select Topics" />
                <Choice value="Politics"/>
                <Choice value="Business"/>
                <Choice value="Sport"/>
                <Choice value="Sci/Tech"/>

                <Header value="Select Moods" />
                <Choice value="Cheerful"/>
                <Choice value="Melancholy"/>
                <Choice value="Romantic"/>

        </Choices>
        </View>
                    """
    r = requests.post(
        config_url,
        data={"label_config": label_config},
        cookies=cookies
    )


access_token = get_cookies().get("access_token")
create_project()
save_config()
import_tasks(tasks, PROJECT_NAME)

