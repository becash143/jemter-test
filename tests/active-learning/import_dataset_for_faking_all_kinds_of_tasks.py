import json
import os
import random as rand
from datetime import datetime

import requests
USERNAME = PASSWORD = TASK_CREATED_BY = "admin"
COMPLETION_CREATED_BY = "admin"
PROJECT_NAME = "sample_mixed_project"
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
            <Label value="Drug_Ingredient" background="gold" hotkey="T"/>
            <Label value="Drug_BrandName" background="green" hotkey="Y"/>
            <Label value="Dosage" background="chocolate" hotkey="U"/>
            <Label value="Route" background=" chocolate " hotkey="O"/>
            <Label value="Strength" background=" chocolate " hotkey="P"/>
            <Label value="Form" background=" chocolate " hotkey="I"/>
            <Label value="Duration" background="chocolate" hotkey="G"/>
            <Label value="Frequency" background=" chocolate " hotkey="H"/>
            <Label value="Date" background="blue" hotkey="_"/>
            <Label value="RelativeDate" background="blue" hotkey="F"/>
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
            <Label value="Test" background="green" hotkey="A"/>
            <Label value="Test_Result" background="orange" hotkey="S"/>
            <Label value="Total_Cholesterol" background="gold" hotkey="_"/>
            <Label value="LDL" background="gold" hotkey="_"/>
            <Label value="HDL" background="gold" hotkey="_"/>
            <Label value="Triglycerides" background="gold" hotkey="_"/>
            <Label value="ImagingFindings" background="orange" hotkey="_"/>
            <Label value="EKG_Findings" background="orange" hotkey="_"/>
            <Label value="Section_Header" background="gold" hotkey="_"/>
            <Label value="Medical_History_Header" background="green" hotkey="_"/>
            <Label value="Family_History_Header" background="green" hotkey="J"/>
            <Label value="Social_History_Header" background="green" hotkey="K"/>
            <Label value="Vital_Signs_Header" background="green" hotkey="L"/>
            <Label value="Absent" assertion="true" background="red" hotkey="Z"/>
            <Label value="Past" assertion="true" background="red" hotkey="X"/>
            <Label value="Hypothetical" assertion="true" background="red" hotkey="C"/>
            <Label value="Family" assertion="true" background="red" hotkey="V"/>
            <Label value="SomeoneElse" assertion="true" background="red" hotkey="M"/>
            <Label value="Possible" assertion="true" background="red" hotkey="N"/>
            <Label value="Planned" assertion="true" background="red" hotkey="B"/>
            <Label value="ManualFix" assertion="true" background="blue" hotkey="D"/>
            <Label value="Review" assertion="true" background="blue" hotkey="_"/>
            <Label value="NotInTaxonomy" assertion="true" background="blue" hotkey="_"/>
            <Label value="Anatomical_system" model="ner_anatomy" background="#cb4eb9"/>
            <Label value="Immaterial_anatomical_entity" model="ner_anatomy" background="#7745a7"/>
            <Label value="Tissue" model="ner_anatomy" background="#4e6d51"/>
            <Label value="Multi" model="ner_anatomy" background="#2163f2"/>
            <Label value="Pathological_formation" model="ner_anatomy" background="#a4a9f4"/>
            <Label value="Cellular_component" model="ner_anatomy" background="#ae5397"/>
            <Label value="Organ" model="ner_anatomy" background="#672fc2"/>
            <Label value="Cell" model="ner_anatomy" background="#202b7b"/>
            <Label value="Developing_anatomical_structure" model="ner_anatomy" background="#098d7a"/>
            <Label value="Organism_substance" model="ner_anatomy" background="#665fb8"/>
        </Labels>
        <Relations>
            <Relation value="is_generic_date_of" background="yellowgreen"/>
            <Relation value="is_start_date_of" background="yellowgreen"/>
            <Relation value="is_stop_date_of" background="yellowgreen"/>
            <Relation value="is_result_of" background="yellowgreen"/>
            <Relation value="is_symptom_of" background="yellowgreen"/>
            <Relation value="is_adverse_event_of" background="yellowgreen"/>
            <Relation value="is_caused_by" background="yellowgreen"/>
            <Relation value="is_finding_of" background="yellowgreen"/>
            <Relation value="is_before" background="yellowgreen"/>
            <Relation value="co_occurs_with" background="yellowgreen"/>
            <Relation value="is_evidence_of" background="yellowgreen"/>
        </Relations>
        <View style="height: 250px; overflow: auto;">
            <Text name="text" value="$text"/>
        </View>
        <Header value="Gender"/>
        <Choices name="Gender" toName="text" choice="single" showInLine="true">
            <Choice value="Female" hotkey="_"/>
            <Choice value="Male" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
        </Choices>
        <Header value="Age"/>
        <Choices name="Age" toName="text" choice="single" showInLine="true">
            <Choice value="Newborn (0-1m)" hotkey="_"/>
            <Choice value="Child (less than 18y)" hotkey="_"/>
            <Choice value="Adult (19-44y)" hotkey="_"/>
            <Choice value="Middle Aged (45-64y)" hotkey="_"/>
            <Choice value="Aged (65+y)" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
        </Choices>
        <Header value="Female Reproductive Status"/>
        <Choices name="Female Reproductive Status" toName="text" choice="single" showInLine="true">
            <Choice value="Pregnant" hotkey="_"/>
            <Choice value="Non-Pregnant" hotkey="_"/>
            <Choice value="Post-Menopausal" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
        </Choices>
        <Header value="Smoking Status"/>
        <Choices name="Smoking Status" toName="text" choice="single" showInLine="true">
            <Choice value="Current Smoker" hotkey="_"/>
            <Choice value="Past Smoker" hotkey="_"/>
            <Choice value="Nonsmoker" hotkey="_"/>
            <Choice value="Secondhand Smoke" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Alcohol"/>
        <Choices name="Alcohol" toName="text" choice="single" showInLine="true">
            <Choice value="Current Drinker" hotkey="_"/>
            <Choice value="Past Drinker" hotkey="_"/>
            <Choice value="Not Drinker" hotkey="_"/>
            <Choice value="Social Drinker" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Other Substance"/>
        <Choices name="Other Substance" toName="text" choice="single" showInLine="true">
            <Choice value="Current Consumer" hotkey="_"/>
            <Choice value="Past Consumer" hotkey="_"/>
            <Choice value="Not Consumer" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Diagnosis of Diabetes"/>
        <Choices name="Diagnosis of Diabetes" toName="text" choice="single" showInLine="true">
            <Choice value="Yes" hotkey="_"/>
            <Choice value="No" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Diagnosis of Hypertension"/>
        <Choices name="Diagnosis of Hypertension" toName="text" choice="single" showInLine="true">
            <Choice value="Yes" hotkey="_"/>
            <Choice value="No" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Diagnosis of Dyslipidemia"/>
        <Choices name="Diagnosis of Dyslipidemia" toName="text" choice="single" showInLine="true">
            <Choice value="Yes" hotkey="_"/>
            <Choice value="No" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Personal History of CVD (related to atherosclerosis)"/>
        <Choices name="Personal History of CVD" toName="text" choice="single" showInLine="true">
            <Choice value="Yes" hotkey="_"/>
            <Choice value="No" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Family History of CVD (related to atherosclerosis) "/>
        <Choices name="Family History of CVD" toName="text" choice="single" showInLine="true">
            <Choice value="Yes" hotkey="_"/>
            <Choice value="No" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Heart Rate"/>
        <Choices name="HR" toName="text" choice="single" showInLine="true">
            <Choice value="High" hotkey="_"/>
            <Choice value="Normal" hotkey="_"/>
            <Choice value="Low" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Respiratory Rate"/>
        <Choices name="RR" toName="text" choice="single" showInLine="true">
            <Choice value="High" hotkey="_"/>
            <Choice value="Normal" hotkey="_"/>
            <Choice value="Low" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Blood Pressure"/>
        <Choices name="BP" toName="text" choice="single" showInLine="true">
            <Choice value="High" hotkey="_"/>
            <Choice value="Normal" hotkey="_"/>
            <Choice value="Low" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Temperature"/>
        <Choices name="Temperature" toName="text" choice="single" showInLine="true">
            <Choice value="High" hotkey="_"/>
            <Choice value="Normal" hotkey="_"/>
            <Choice value="Low" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Oxygen Saturation"/>
        <Choices name="O2" toName="text" choice="single" showInLine="true">
            <Choice value="Normal" hotkey="_"/>
            <Choice value="Low" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
            <Choice value="Not Mentioned in Relevant Section" hotkey="_"/>
        </Choices>
        <Header value="Oxygen Therapy"/>
        <Choices name="O2_Therapy" toName="text" choice="single" showInLine="true">
            <Choice value="Yes" hotkey="_"/>
            <Choice value="No" hotkey="_"/>
            <Choice value="Unknown" hotkey="_"/>
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
