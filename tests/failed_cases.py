import re
import os
import pandas as pd
import json
import pytest
import requests

from annotationlab.utils.keycloak_cookies import get_cookies

API_URL = 'http://annotationlab:8200'


def test_invalid_url():
    export_url = f'{API_URL}/wrong_url'
    headers = {
        'Host': API_URL.replace('http://', ''),
        'Origin': API_URL,
    }
    r = requests.get(
        export_url,
        cookies=get_cookies()
    )
    assert r.status_code == 404
    response = r.json()
    assert 'error' in response
    assert '404 Not Found' in response['error']


def test_inaccessible_project():
    export_url = f'{API_URL}/project/1111'
    headers = {
        'Host': API_URL.replace('http://', ''),
        'Origin': API_URL,
    }
    r = requests.get(
        export_url,
        cookies=get_cookies()
    )
    assert r.status_code == 404
    response = r.json()
    assert 'error' in response
    assert '404 Not Found' in response['error']


def test_invalid_cookies():
    export_url = f'{API_URL}/#/projects'
    headers = {
        'Host': API_URL.replace('http://', ''),
        'Origin': API_URL,
    }
    r = requests.get(
        export_url,
        cookies={'access_token': 'cookie'}
    )
    assert r.status_code == 401


if __name__ == '__main__':
    test_inaccessible_project()
