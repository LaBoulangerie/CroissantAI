# coding=utf-8

import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

port = getenv("PORT", 8000)
url = f"http://127.0.0.1:{port}/ask"
params = {"request": "Quelle est la capitale de Goast ?"}
headers = {"accept": "application/json"}

username = getenv("SECRET_KEY", "secret")
password = ""

response = requests.post(url, params=params, headers=headers, auth=(username, password))

if response.ok:
    response_data = response.json()
    assert "Tharass" in response_data["answer"]
    print("Test passed!", response_data["answer"])
else:
    print(
        f"Request failed with status code {response.status_code} and message {response.text}"
    )
