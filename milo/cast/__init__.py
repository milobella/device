from typing import Dict

import pychromecast


class Cast:
    def __init__(self):
        self.browser = None
        self.casts: Dict[str, pychromecast.Chromecast] = {}

    def play(self, name: str):
        if name in self.casts:
            self.casts[name].media_controller.play()

    def pause(self, name: str):
        if name in self.casts:
            self.casts[name].media_controller.play()

    def names(self):
        return self.casts.keys()

    def star_discovery(self):
        def cast_found(chromecast: pychromecast.Chromecast):
            print("=> Discovered cast: " + chromecast.name)

            name = chromecast.name

            # with listeners and therefore receive 2 events instead of 1 on the listeners
            if name in self.casts:
                # disconnect existing cast device if there is any
                self.casts[name].disconnect(blocking=False)
            self.casts[name] = chromecast
            # # add status listener
            # self.casts[name].register_connection_listener(self)
            # self.casts[name].register_status_listener(self)
            # # add media controller listener
            # self.casts[name].media_controller.register_status_listener(self)
            # # timeout 0.001 just waits for status to be ready
            # # but we just need the thread to start by calling wait()
            # self.casts[name].wait(0.001)

        print("Start discovery")
        self.browser = pychromecast.get_chromecasts(
            blocking=False, tries=None, retry_wait=5, timeout=5, callback=cast_found)
