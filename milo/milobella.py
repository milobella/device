import json
import os

import requests

MILOBELLA_TOKEN_ENV = 'MILOBELLA_AUTHORIZATION_TOKEN'


class Milobella:
    def __init__(self, url):
        self._url = url
        self._token = os.environ[MILOBELLA_TOKEN_ENV]

    def milobella_request(self, question: str) -> str:
        milobella_response = requests.post(
            f"{self._url}/talk/text",
            data=json.dumps({'text': question}),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self._token
            }
        )
        # print(milobella_response.json())
        return milobella_response.json()["vocal"]
