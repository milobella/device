# Milobella device Client

Run milobella in a device, using mic and speakers to communicate.

> Disclaimer : Only checked in a Raspberry PI 3B+ for now.

# Technical choices
#### Speech-To-Text
The translation of voice records into text is currently performed by the [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text).

The [mozilla/deepspeech](https://github.com/mozilla/DeepSpeech) project with Common Voice database is considered.

#### Text-To-Speech
The translation of Milobella text answers into speech synthesis is ensured by [Google Cloud Text-To-Speech API](https://cloud.google.com/text-to-speech).

No replacement has been considered for now.

# Requirements
#### Google cloud authentication configuration
Authentication process is detailed in this documentation https://cloud.google.com/speech-to-text/docs/quickstart-protocol.

It is using basically a ``GOOGLE_APPLICATION_CREDENTIALS`` env variable pointing to a JSON private key file.
The JSON private key is generated when you create a Service Account.

Make sure you activated both of the APIs in your Google Cloud Project, and the same JSON file will be used.

#### Milobella authentication configuration
The env variable ``MILOBELLA_AUTHORIZATION_TOKEN`` should contain the JWToken generated every time you authenticate.
A script ``authenticate.sh`` is here to show you how. (You need [jq](https://stedolan.github.io/jq/download/) if you want to use it)
```
export MILOBELLA_USERNAME=myuser
export MILOBELLA_PASSWORD=mypass
source authenticate.sh
```

#### Raspberry audio configuration
If you are using a Raspberry PI, an example of ``.asoundrc`` is located in this repository. It is using a plugin to
transform the default sample rate to 16GHz, which is necessary to make work the google cloud speech-to-text. Somehow it works with this configuration ...

The file ``.asoundrc`` needs to be copied in $HOME directory to be effective, and probably some adjustments are necessary to match the proper card and devices.

# Run the program
```
# [If not already in a venv] Not mandatory but it is always easier to have a virtualenv
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the app
python milobella.py
```
