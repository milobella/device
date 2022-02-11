import json
import os

import requests

from milo.cast import Cast

MILOBELLA_TOKEN_ENV = 'MILOBELLA_AUTHORIZATION_TOKEN'


class Milobella:
    def __init__(self, url: str, cast: Cast):
        self._url = url
        self._token = os.environ[MILOBELLA_TOKEN_ENV]
        self._cast = cast
        self._current_context = None

    def milobella_request(self, question: str) -> (str, bool):
        request = {
            'text': question,
            'device': {
                'instruments': [
                    {'kind': 'chromecast', 'actions': ['play', 'pause'], 'name': name} for name in self._cast.names()
                ],
            },
            'context': self._current_context
        }
        print(request)
        milobella_response = requests.post(
            f"{self._url}/api/v1/talk/text",
            data=json.dumps(request),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self._token,
            }
        )
        response = milobella_response.json()
        self._current_context = response['context'] if 'context' in response else None
        if 'actions' in response:
            for action in response['actions']:
                for param in response['params']:
                    if param['key'] == 'instrument':
                        if action == 'play':
                            self._cast.play(param['value'])
                        if action == 'pause':
                            self._cast.pause(param['value'])

        print(response)
        return response["vocal"], response['auto_reprompt'] if 'auto_reprompt' in response else False
