import json
import os

import requests


class Milobella:
    def __init__(self, url):
        self._url = url
        self._token = os.environ['MILOBELLA_AUTHORIZATION_TOKEN']

    def milobella_request(self, question: str) -> str:
        milobella_response = requests.post(
            f"{self._url}/talk/text",
            data=json.dumps({'text': question}),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self._token
            }
        )
        print(milobella_response.json()["vocal"])
        return milobella_response.json()["vocal"]
