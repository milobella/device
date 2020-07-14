# Milobella device Client

Run milobella in a device, using mic and speakers to communicate.

> Disclaimer : Only checked in a Raspberry PI 3B+ for now.

## Speech-To-Text
The translation of voice records into text is currently performed by the [Google Cloud Speech-To-Text API](https://cloud.google.com/speech-to-text).
The [mozilla/deepspeech](https://github.com/mozilla/DeepSpeech) project with Common Voice database is considered.

## Text-To-Speech
The translation of Milobella text answers into speech synthesis is ensured by [Google Cloud Text-To-Speech API](https://cloud.google.com/text-to-speech)
No replacement has been considered for now.

## Google cloud authentication configuration
Authentication process is detailed in this documentation [https://cloud.google.com/speech-to-text/docs/quickstart-protocol].
It is using basically a ``GOOGLE_APPLICATION_CREDENTIALS`` env variable pointing to a JSON private key file.
The JSON private key is generated when you create a Service Account.

Make sure you activated both of the APIs in your Google Cloud Project, and the same JSON file will be used.

## Milobella authentication configuration
The env variable ``MILOBELLA_AUTHORIZATION_TOKEN`` should contain the JWToken generated every time you authenticate.
A script ``authenticate.sh`` is here to show you how. (You need [jq](https://stedolan.github.io/jq/download/) if you want to use it)
```
source authenticate.sh
```

## Raspberry audio configuration
If you are using a Raspberry PI, an example of ``.asoundrc`` is located in this repository. We use plugin to
transform the sample rate to 16GHz. Somehow it works with this configuration.

The file ``.asoundrc`` needs to be copied in $HOME directory to be effective.
