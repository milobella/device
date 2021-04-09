# Milobella device Client

Run milobella in a device, using mic and speakers to communicate.

## Technical choices
### Audio device
For now, I'm using a Raspberry PI 3B+ combined with a [RASPIAUDIO Ultra +](https://raspiaudio.com/produit/ultra).
It's onboard mic and speaker which is convenient for my experimentation.

### Wake up word
To trigger the discussion a "wake-up-word" technology is necessary. There is a lot of these technologies in the opensource world.
Here is the list of technologies experimented : 
- [pocketsphinx](https://github.com/cmusphinx/pocketsphinx)
- [porcupine](https://github.com/Picovoice/porcupine)

[Wake up word experimentation](docs/wake-up-word-experimentation.md)

### Speech-To-Text
The translation of voice records into text is currently performed by the [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text).

The [mozilla/deepspeech](https://github.com/mozilla/DeepSpeech) project with Common Voice database is considered.

### Text-To-Speech
The translation of Milobella text answers into speech synthesis is ensured by [Google Cloud Text-To-Speech API](https://cloud.google.com/text-to-speech).

No replacement has been considered for now.

## Requirements
### Google cloud authentication configuration
Authentication process is detailed in this documentation https://cloud.google.com/speech-to-text/docs/quickstart-protocol.

It is using basically a ``GOOGLE_APPLICATION_CREDENTIALS`` env variable pointing to a JSON private key file.
The JSON private key is generated when you create a Service Account.

Make sure you activated both of the APIs in your Google Cloud Project, and the same JSON file will be used.

### Milobella authentication configuration
The env variable ``MILOBELLA_AUTHORIZATION_TOKEN`` should contain the JWToken generated every time you authenticate.
A script ``authenticate.sh`` is here to show you how. (You need [jq](https://stedolan.github.io/jq/download/) if you want to use it)
```
export MILOBELLA_USERNAME=myuser
export MILOBELLA_PASSWORD=mypass
source authenticate.sh
```

### Raspberry audio configuration
If you are using a Raspberry PI B+ with RASPIAUDIO Ultra +, check the 
[RASPIAUDIO ultra+ configuation](docs/raspiaudio-ultra+-configuration.md) documentation.

## Run the program
```
# [If not already in a venv] Not mandatory but it is always easier to have a virtualenv
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the app
python porcupine.py

# or python pocketsphinx.py
```
