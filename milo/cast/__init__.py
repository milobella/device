import time
from typing import Dict, List

import pychromecast
from plexapi.server import PlexServer
from pychromecast.controllers.plex import PlexController
from pychromecast.controllers.media import MediaStatus, MEDIA_PLAYER_STATE_UNKNOWN


class Cast:
    def __init__(self, cast: pychromecast.Chromecast, plex_url: str, plex_token: str):
        self._cast = cast
        self._plex_ctrl = PlexController()
        self._state = MEDIA_PLAYER_STATE_UNKNOWN
        self._plex_url = plex_url
        self._plex_token = plex_token

    def connect(self):
        self._cast.register_handler(self._plex_ctrl)
        # add media controller listener
        self._cast.media_controller.register_status_listener(self)
        # timeout 0.001 just waits for status to be ready
        # but we just need the thread to start by calling wait()
        self._cast.wait(0.001)

    def play(self):
        self._cast.media_controller.play()

    def pause(self):
        self._cast.media_controller.pause()

    def play_media(self, url: str):
        self._plex_ctrl.block_until_playing(
            PlexServer(self._plex_url, self._plex_token).library.search(guid=url)[0]
        )

    def as_instrument(self) -> Dict:
        return {
            'kind': 'chromecast',
            'actions': ['play', 'pause', 'play_media'],
            'name': self._cast.name,
            'state': {'status': self._state}
        }

    def disconnect(self):
        self._cast.disconnect(blocking=False)

    def new_media_status(self, status: MediaStatus):
        self._state = status.player_state
        # Workaround to have the paused state https://github.com/home-assistant/core/pull/2222/files
        if status.player_is_playing:
            time.sleep(5)
            self._cast.media_controller.update_status()


class CastManager:
    def __init__(self, plex_url: str, plex_token: str):
        self._browser = None
        self._casts: Dict[str, Cast] = {}
        self._plex_url = plex_url
        self._plex_token = plex_token

    def play(self, name: str):
        if name in self._casts:
            self._casts[name].play()

    def pause(self, name: str):
        if name in self._casts:
            self._casts[name].pause()

    def play_media(self, name: str, url: str):
        if name in self._casts:
            self._casts[name].play_media(url)

    def start_discovery(self):
        def cast_found(chromecast: pychromecast.Chromecast):
            print("=> Discovered cast: " + chromecast.name)

            name = chromecast.name

            # with listeners and therefore receive 2 events instead of 1 on the listeners
            if name in self._casts:
                # disconnect existing cast device if there is any
                self._casts[name].disconnect()

            self._casts[name] = Cast(chromecast, plex_url=self._plex_url, plex_token=self._plex_token)
            self._casts[name].connect()

        print("Start discovery")
        self._browser = pychromecast.get_chromecasts(
            blocking=False, tries=None, retry_wait=5, timeout=5, callback=cast_found)

    def as_instruments(self) -> List[Dict]:
        return [cast.as_instrument() for cast in self._casts]
