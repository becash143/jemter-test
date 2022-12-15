import json
import os
import random as rand
from datetime import datetime

import requests
USERNAME = PASSWORD = TASK_CREATED_BY = "admin"
COMPLETION_CREATED_BY = "admin"
PROJECT_NAME = "sample_assertion_project"
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

with open("tests/active-learning/all_kinds_of_tasks.json", "r") as f:
    data = json.loads(f.read())


for each in data.get("examples"):
    results = [result for result in each.get("completions")[0].get("result") if result.get("type") not in ["relation", "choices"]]
    each["completions"][0]["result"] = results
    a_task = {
        "completions": each.get("completions"),
        "predictions": [],
        "created_at": str(datetime.now()).split(".")[0],
        "created_by": TASK_CREATED_BY,
        "data": each.get("data")
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
            <Labels name="ner" toName="text">
            <Label value="Imaging_Technique" background="red"/>
            <Label value="Vaccine" background="green" hotkey="_"/>
            <Label value="Allergen" background=" green " hotkey="_"/>
            <Label value="Treatment" background="green" hotkey="_"/>
            <Label value="Diet" background="green" hotkey="_"/>
            <Label value="Clinical_Dept" background="green" hotkey="_"/>
            <Label value="Medical_Device" background="green" hotkey="_"/>
            <Label value="Admission_Discharge" background="green" hotkey="_"/>
            <Label value="Pregnancy_Delivery_Puerperium" background="pink" hotkey="_"/>
            <Label value="Pregnancy" background="pink" hotkey="_"/>
            <Label value="Labour_Delivery" background="pink" hotkey="_"/>
            <Label value="Puerperium" background="pink" hotkey="_"/>
            <Label value="Fetus_NewBorn" background="pink" hotkey="_"/>
            <Label value="Oncological" background="pink" hotkey="_"/>
            <Label value="Communicable_Disease" background="pink" hotkey="_"/>
            <Label value="Psychological_Condition" background="pink" hotkey="_"/>
            <Label value="Injury_or_Poisoning" background="pink" hotkey="_"/>
            <Label value="Disease_Syndrome_Disorder" background="pink" hotkey="4"/>
            <Label value="Symptom" background="blue" hotkey="3"/>
            <Label value="Assertion_DOBirth" background="red" hotkey="_"/>
            <Label value="Assertion_DODeath" background="red" hotkey="_"/>
            <Label value="Birth_Entity" background="brown" hotkey="0"/>
            <Label value="Death_Entity" background="brown" hotkey="9"/>
            <Label value="Age" background="brown" hotkey="1"/>
            <Label value="Gender" background="gray" hotkey="2"/>
            <Label value="Female_Reproductive_Status" background="gray" hotkey="_"/>
            <Label value="Race_Ethnicity" background="gray" hotkey="_"/>
            <Label value="Employment" background="brown" hotkey="_"/>
            <Label value="Relationship_Status" background="brown" hotkey="_"/>
            <Label value="Sexually_Active_or_Sexual_Orientation" background="brown" hotkey="_"/>
            <Label value="Temperature" background="olive" hotkey="_"/>
            <Label value="Pulse" background="gold" hotkey="_"/>
            <Label value="Respiration" background="tan" hotkey="_"/>
            <Label value="Blood_Pressure" background="brown" hotkey="_"/>
            <Label value="O2_Saturation" background="orange" hotkey="_"/>
            <Label value="VS_Finding" background="orange" hotkey="_"/>
            <Label value="Oxygen_Therapy" background="orange" hotkey="_"/>
            <Label value="Weight" background="tan" hotkey="_"/>
            <Label value="Height" background="tan" hotkey="_"/>
            <Label value="BMI" background="tan" hotkey="_"/>
            <Label value="External_body_part_or_region" background="orange" hotkey="Q"/>
            <Label value="Internal_organ_or_component" background="orange" hotkey="W"/>
            <Label value="Direction" background="orange" hotkey="E"/>
            <Label value="Smoking" background="gray" hotkey="6"/>
            <Label value="Assertion_SecondHand" background="red" hotkey="_"/>
            <Label value="Alcohol" background="gray" hotkey="7"/>
            <Label value="Assertion_SocialDrinking" background="red" hotkey="_"/>
            <Label value="Substance" background="gray" hotkey="_"/>
            <Label value="Substance_Quantity" background="gray" hotkey="_"/>
            <Label value="Drug_Ingredient" background="gold" />
            <Label value="Drug_BrandName" background="green" />
            <Label value="Dosage" background="chocolate" />
            <Label value="Route" background=" chocolate " />
            <Label value="Strength" background=" chocolate " />
            <Label value="Form" background=" chocolate "/>
            <Label value="Duration" background="chocolate"/>
            <Label value="Frequency" background=" chocolate "/>
            <Label value="Date" background="blue" hotkey="_"/>
            <Label value="RelativeDate" background="blue" />
            <Label value="Time" background="blue" hotkey="_"/>
            <Label value="RelativeTime" background="blue" hotkey="_"/>
            <Label value="Diabetes" background="orange" hotkey="_"/>
            <Label value="Hypertension" background="orange" hotkey="_"/>
            <Label value="Hyperlipidemia" background="orange" hotkey="_"/>
            <Label value="Overweight" background="orange" hotkey="_"/>
            <Label value="Obesity" background="orange" hotkey="_"/>
            <Label value="Kidney_Disease" background="orange" hotkey="_"/>
            <Label value="Heart_Disease" background="orange" hotkey="_"/>
            <Label value="Cerebrovascular_Disease" background="orange" hotkey="_"/>
            <Label value="Modifier" background="olive" hotkey="5"/>
            <Label value="Procedure" background="green" hotkey="8"/>
            <Label value="Test" background="green" />
            <Label value="Test_Result" background="orange" />
            <Label value="Total_Cholesterol" background="gold" hotkey="_"/>
            <Label value="LDL" background="gold" hotkey="_"/>
            <Label value="HDL" background="gold" hotkey="_"/>
            <Label value="Triglycerides" background="gold" hotkey="_"/>
            <Label value="ImagingFindings" background="orange" hotkey="_"/>
            <Label value="EKG_Findings" background="orange" hotkey="_"/>
            <Label value="Section_Header" background="gold" hotkey="_"/>
            <Label value="Medical_History_Header" background="green" hotkey="_"/>
            <Label value="Family_History_Header" background="green" />
            <Label value="Social_History_Header" background="green" />
            <Label value="Vital_Signs_Header" background="green" />
            <Label value="Absent" assertion="true" background="red" />
            <Label value="Past" assertion="true" background="red" />
            <Label value="Hypothetical" assertion="true" background="red" />
            <Label value="Family" assertion="true" background="red" />
            <Label value="SomeoneElse" assertion="true" background="red" />
            <Label value="Possible" assertion="true" background="red" />
            <Label value="Planned" assertion="true" background="red" />
            <Label value="ManualFix" assertion="true" background="blue" />
            <Label value="Review" assertion="true" background="blue" hotkey="_"/>
            <Label value="NotInTaxonomy" assertion="true" background="blue" hotkey="_"/>
        </Labels>
        <View style="height: 250px; overflow: auto;">
            <Text name="text" value="$text"/>
        </View>
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
