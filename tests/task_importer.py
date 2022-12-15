"""
The purpose of this script is to create huge number of projects
and each project having huge number of tasks (completed+incomplete)

Because of the fact that we reload (put into memory) tasks details
as soon as it is imported, the reponse of import API gradually slows down.
In future, we might need to update this load logic.

For now, to make the script execute at blazing speed, one needs to make small
change in server.py

in API: projects/<string:project_name>/import', methods=['POST'])
comment out/remove loading logic
ie.

# load new tasks and everything related
# user_project.load_tasks()
"""

import os
import json
import requests
import multiprocessing
from random import randint, uniform, choice
from datetime import datetime, timedelta

# base url of annotation lab
API_URL = 'http://annotationlab:8200'

# no of projects
PROJECTS_TO_IMPORT = 1000

# no of tasks in each project
COMPLETED_TASKS_TO_IMPORT = 100
INCOMPLETE_TASKS_TO_IMPORT = 100
SUBMITTED_TASKS_TO_IMPORT = 100
REVIEW_APPROVED_TASKS_TO_IMPORT = 100
REVIEW_REJECTED_TASKS_TO_IMPORT = 100

# Cookies expiry duration (in mins) []
COOKIES_EXPIRY = 15


headers = {
    'Host': API_URL.replace('http://', ''),
    'Origin': API_URL,
    'Content-Type': 'application/json'
}

labels = [
    {
        "value": {
            "start": 0,
            "end": 5,
            "text": "00001",
            "labels": ["Counter"]
        },
        "id": "dAt-dGNsRf",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 6,
            "end": 17,
            "text": "Performance",
            "labels": ["Person"]
        },
        "id": "rBCjMc9G19",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 18,
            "end": 25,
            "text": "Testing",
            "labels": ["Organization"],
        },
        "id": "2Gtm0Ih1iW",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 31,
            "end": 39,
            "text": "software",
            "labels": ["Fact"]
        },
        "id": "yjDaRvn-By",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 40,
            "end": 47,
            "text": "testing",
            "labels": ["Money"]
        },
        "id": "NEl0phghy1",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 48,
            "end": 55,
            "text": "process",
            "labels": ["Date"]
        },
        "id": "3cpvWp991Z",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 56,
            "end": 60,
            "text": "used",
            "labels": ["Time"]
        },
        "id": "uCd5v9GB-E",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 61,
            "end": 64,
            "text": "for",
            "labels": ["Ordinal"]
        },
        "id": "6gNAn-o2uG",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 65,
            "end": 72,
            "text": "testing",
            "labels": ["Percent"]
        },
        "id": "LVD8yga1Zu",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 73,
            "end": 82,
            "text": "the speed",
            "labels": ["Product"]
        },
        "id": "PJD_w2limR",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 84,
            "end": 92,
            "text": "response",
            "labels": ["Language"]
        },
        "id": "ot6w1QX_eh",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 93,
            "end": 108,
            "text": "time, stability",
            "labels": ["Location"],
        },
        "id": "e5hDmwhouX",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 110,
            "end": 121,
            "text": "reliability",
            "labels": ["ABC"]
        },
        "id": "E7wA-ZE_b2",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 123,
            "end": 134,
            "text": "scalability",
            "labels": ["DEF"]
        },
        "id": "NNrPMUA1wU",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 139,
            "end": 147,
            "text": "resource",
            "labels": ["GHI"]
        },
        "id": "dzxDMWq1wl",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 148,
            "end": 153,
            "text": "usage",
            "labels": ["JKL"]
        },
        "id": "SrAhcydDPy",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 159,
            "end": 179,
            "text": "software application",
            "labels": ["MNO"],
        },
        "id": "kaQhg0g1_B",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 186,
            "end": 196,
            "text": "particular",
            "labels": ["PQR"]
        },
        "id": "2HWbqFePRH",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 197,
            "end": 205,
            "text": "workload",
            "labels": ["STU"]
        },
        "id": "FJF37AeAT1",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 211,
            "end": 215,
            "text": "main",
            "labels": ["VWX"]
        },
        "id": "2J4KUo0Pr5",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 216,
            "end": 238,
            "text": "purpose of performance",
            "labels": ["Person"],
        },
        "id": "hHrGpr999n",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 239,
            "end": 246,
            "text": "testing",
            "labels": ["Organization"],
        },
        "id": "MsoOi2COHk",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 252,
            "end": 275,
            "text": " identify and eliminate",
            "labels": ["Fact"],
        },
        "id": "2WUX4wgto6",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 280,
            "end": 291,
            "text": "performance",
            "labels": ["Money"]
        },
        "id": "Dyoo8tAUCI",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 292,
            "end": 303,
            "text": "bottlenecks",
            "labels": ["Date"]
        },
        "id": "zB5cJ0uiu6",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 307,
            "end": 310,
            "text": "the",
            "labels": ["Time"]
        },
        "id": "xj7_HvGubG",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 311,
            "end": 319,
            "text": "software",
            "labels": ["Ordinal"]
        },
        "id": "nQ1Z6SiucG",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 320,
            "end": 331,
            "text": "application",
            "labels": ["Percent"],
        },
        "id": "eLEGdDyO-u",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 341,
            "end": 362,
            "text": "subset of performance",
            "labels": ["Product"],
        },
        "id": "mgmMeGy2fX",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 363,
            "end": 374,
            "text": "engineering",
            "labels": ["Language"],
        },
        "id": "haGwos8TSD",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 375,
            "end": 378,
            "text": "and",
            "labels": ["Location"]
        },
        "id": "qC_hCCSt4v",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 384,
            "end": 389,
            "text": "known",
            "labels": ["ABC"]
        },
        "id": "wAvdcWPAqR",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
    {
        "value": {
            "start": 394,
            "end": 406,
            "text":
            "Perf Testing",
            "labels": ["GHI"]},
        "id": "ZvX0jzawY8",
        "from_name": "label",
        "to_name": "text",
        "type": "labels",
    },
]

users = [
    'admin',
    'collaborate',
    'readonly',
    'ghanshyam',
    'ali',
    'umesh',
    'nabin',
    'shubhanshi',
    'bikash',
    'tejas',
    'narendra'
]

text = "{index} Performance Testing is a software testing process used for "\
       "testing the speed, response time, stability, reliability, scalability"\
       " and resource usage of a software application under particular "\
       "workload. The main purpose of performance testing is to identify "\
       "and eliminate the performance bottlenecks in the software "\
       "application. It is a subset of performance engineering and "\
       "also known as 'Perf Testing'."


def get_cookies():
    keycloak_url = os.environ.get("KEYCLOAK_SERVER_URL",
                                  "http://keycloak-local:8080/auth/")
    keycloak_realm = os.environ.get("KEYCLOAK_REALM_NAME", "master")
    url = f"{keycloak_url}realms/{keycloak_realm}/protocol" \
          "/openid-connect/token"
    data = {
        "grant_type": "password",
        "username": os.environ.get("KEYCLOAK_SUPERUSER_USER", "admin"),
        "password": os.environ.get("KEYCLOAK_SUPERUSER_PASS", "admin"),
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


class Worker(multiprocessing.Process):

    def __init__(self, job_queue):
        super().__init__()
        self._job_queue = job_queue

    def run(self):
        while True:
            project_name = self._job_queue.get()
            if project_name is None:
                break
            self.cookies = get_cookies()
            self.cookies_ts = datetime.now()
            self.create_project(project_name)
            self.save_config(project_name)
            self.import_tasks(project_name)

    def create_project(self, project_name):
        data = {
            "project_name": project_name,
            "project_description": f"Performance project {project_name}",
            "project_sampling": "uniform",
            "project_instruction": "Performance"
        }
        requests.post(
            f'{API_URL}/api/projects/create',
            headers=headers,
            data=json.dumps(data),
            cookies=self.cookies
        )

    def save_config(self, project_name):
        label_config = """
        <View>
          <Labels name="label" toName="text">
            <Label value="Counter" background="cyan"/>
            <Label value="Person" background="red"/>
            <Label value="Organization" background="darkorange"/>
            <Label value="Fact" background="orange"/>
            <Label value="Money" background="green"/>
            <Label value="Date" background="darkblue"/>
            <Label value="Time" background="blue"/>
            <Label value="Ordinal" background="purple"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
            <Label value="ABC" background="#428"/>
            <Label value="DEF" background="#428"/>
            <Label value="GHI" background="#428"/>
            <Label value="JKL" background="#428"/>
            <Label value="MNO" background="#428"/>
            <Label value="PQR" background="#428"/>
            <Label value="STU" background="#428"/>
            <Label value="VWX" background="#428"/>
          </Labels>
          <Text name="text" value="$text"/>
        </View>
        """
        requests.post(
            f'{API_URL}/api/projects/{project_name}/save-config',
            data={"label_config": label_config},
            cookies=self.cookies
        )

    def import_task_api(self, project_name, start, end, task_status=None):
        import_url = f'{API_URL}/api/projects/{project_name}/import'
        for index in range(start, end):
            data = prepare_data(text.format(index=f'{index:05}'), index, task_status)
            if datetime.now() >\
               self.cookies_ts + timedelta(minutes=COOKIES_EXPIRY - 2):
                self.cookies = get_cookies()
                self.cookies_ts = datetime.now()
            requests.post(
                import_url,
                headers=headers,
                data=json.dumps(data),
                cookies=self.cookies
            )
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{ts} "Task_{index}" imported for project "{project_name}"')

    def import_tasks(self, project_name):
        last_task = COMPLETED_TASKS_TO_IMPORT + 1
        self.import_task_api(project_name, 1, last_task)

        start = last_task
        last_task = start + SUBMITTED_TASKS_TO_IMPORT
        self.import_task_api(project_name, start, last_task, "submitted")

        start = last_task
        last_task = start + REVIEW_APPROVED_TASKS_TO_IMPORT
        self.import_task_api(project_name, start, last_task, "reviewed-approved")

        start = last_task
        last_task = start + REVIEW_REJECTED_TASKS_TO_IMPORT
        self.import_task_api(project_name, start, last_task, "reviewed-rejected")

        start = last_task
        last_task = start + INCOMPLETE_TASKS_TO_IMPORT
        for index in range(start, last_task):
            data = {
                'text': text.format(index=f'{index:05}'),
                'title': f'Task_{index}'
            }
            if datetime.now() >\
               self.cookies_ts + timedelta(minutes=COOKIES_EXPIRY - 2):
                self.cookies = get_cookies()
                self.cookies_ts = datetime.now()
            requests.post(
                f'{API_URL}/api/projects/{project_name}/import',
                headers=headers,
                data=json.dumps(data),
                cookies=self.cookies
            )
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{ts} "Task_{index}" imported for project "{project_name}"')


def prepare_data(text, index, task_status=None):
    labels_for_this_completion = []
    for i in range(1, randint(10, 20)):
        label = labels[randint(0, len(labels) - 1)]
        labels_for_this_completion.append(label)
    time_stamp = datetime.now() - timedelta(days=randint(1, 40))
    completions = {
        "created_username": choice(users),
        "created_ago": time_stamp.isoformat(),
        "lead_time": float(f'{uniform(100, 150):.3f}'),
        "result": labels_for_this_completion,
        "honeypot": 'false',
        "id": index * 1000 + 1
    }

    if task_status in ["submitted", "reviewed-approved", "reviewed-rejected"]:
        completions["submitted_at"] = time_stamp.isoformat()
    if task_status == "reviewed-approved":
        completions["review_status"] = {
            "comment": "Good Work",
            "approved": True,
            "reviewer": choice(users),
            "reviewed_at": time_stamp.isoformat()
        }
    if task_status == "reviewed-rejected":
        completions["review_status"] = {
            "comment": "Need to change!",
            "approved": False,
            "reviewer": choice(users),
            "reviewed_at": time_stamp.isoformat()
        }

    return {
        'completions': [completions],
        'predictions': [],
        'created_at': time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
        'data': {
            'text': text,
            'title': f'Task_{index}'
        },
        'id': index
    }


if __name__ == '__main__':
    jobs = []
    job_queue = multiprocessing.Queue()
    start = datetime.now()

    for i in range(multiprocessing.cpu_count()):
        p = Worker(job_queue)
        jobs.append(p)
        p.start()

    for i in range(PROJECTS_TO_IMPORT):
        job_queue.put(f'Performance_Project_{i:04}')

    # Send None for each worker to check and quit.
    for j in jobs:
        job_queue.put(None)

    for j in jobs:
        j.join()
    seconds = (datetime.now() - start).seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print(f'Time taken: {hours} hrs {minutes} mins {seconds} secs')
