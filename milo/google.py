import os
import uuid

import subprocess
from gtts import gTTS
from playsound import playsound


def talk(text):
    tts = gTTS(text=text, lang='fr', lang_check=False)
    name = uuid.uuid4()
    tts.save(f"{name}.mp3")

    from platform import system
    system = system()

    if system == 'Windows':
        playsound(f"{name}.mp3")
    else:
        subprocess.Popen(
            ["mpg321", f"{name}.mp3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    os.remove(f"{name}.mp3")
