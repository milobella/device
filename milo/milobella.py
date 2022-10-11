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
                    {'kind': 'chromecast', 'actions': ['play', 'pause', 'play_media'], 'name': name} for name in self._cast.names()
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
            # Execute all actions in the response
            # TODO: refactor
            for action in response['actions']:
                if action['identifier'] == "play":
                    instrument_name = next((p['value'] for p in action['params'] if p['key'] == 'instrument'), None)
                    instrument_kind = next((p['value'] for p in action['params'] if p['key'] == 'kind'), 'chromecast')
                    if instrument_name is None:
                        print('instrument name not provided')
                        continue
                    if instrument_kind != 'chromecast':
                        print(f'unsupported instrument kind {instrument_kind}')
                        continue
                    self._cast.play(instrument_name)

                elif action['identifier'] == "pause":
                    instrument_name = next((p['value'] for p in action['params'] if p['key'] == 'instrument'), None)
                    instrument_kind = next((p['value'] for p in action['params'] if p['key'] == 'kind'), 'chromecast')
                    if instrument_name is None:
                        print('instrument name not provided')
                        continue
                    if instrument_kind != 'chromecast':
                        print(f'unsupported instrument kind {instrument_kind}')
                        continue
                    self._cast.pause(instrument_name)

                elif action['identifier'] == "play_media":
                    instrument_name = next((p['value'] for p in action['params'] if p['key'] == 'instrument'), None)
                    instrument_kind = next((p['value'] for p in action['params'] if p['key'] == 'kind'), 'chromecast')
                    url = next((p['value'] for p in action['params'] if p['key'] == 'url'), None)
                    if instrument_name is None:
                        print('instrument name not provided')
                        continue
                    if instrument_kind != 'chromecast':
                        print(f'unsupported instrument kind {instrument_kind}')
                        continue
                    if url is None:
                        print('url not provided')
                        continue
                    self._cast.play_media(instrument_name, url)

        print(response)
        return response["vocal"], response['auto_reprompt'] if 'auto_reprompt' in response else False
