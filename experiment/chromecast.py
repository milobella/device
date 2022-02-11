import time
import pychromecast

# List chromecasts on the network, but don't connect
services, browser = pychromecast.discovery.discover_chromecasts()
print([service.friendly_name for service in services])


# Discover and connect to chromecasts named Living Room
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Salon"])
# print(chromecasts)
# [cc.device.friendly_name for cc in chromecasts]
# ['Living Room']

cast = chromecasts[0]
# Start worker thread and wait for cast device to be ready
cast.wait()
print(cast)

mc = cast.media_controller
# mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
# mc.block_until_active()
print(mc.status)
# MediaStatus(current_time=42.458322, content_id='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', content_type='video/mp4', duration=596.474195, stream_type='BUFFERED', idle_reason=None, media_session_id=1, playback_rate=1, player_state='PLAYING', supported_media_commands=15, volume_level=1, volume_muted=False)

mc.pause()
# time.sleep(5)
# mc.play()

# Shut down discovery
pychromecast.discovery.stop_discovery(browser)
