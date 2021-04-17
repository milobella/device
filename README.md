# Milobella device Client

Run milobella in a device, using mic and speakers to communicate.

## Requirements
<details>
  <summary>Check requirements before install</summary>

### #1 : Google cloud authentication configuration
Authentication process is detailed in this documentation https://cloud.google.com/speech-to-text/docs/quickstart-protocol.

It is using basically a ``GOOGLE_APPLICATION_CREDENTIALS`` env variable pointing to a JSON private key file.
The JSON private key is generated when you create a Service Account.

Make sure you activated both of the APIs in your Google Cloud Project, and the same JSON file will be used.

### #2 : Milobella authentication configuration
The env variable ``MILOBELLA_AUTHORIZATION_TOKEN`` should contain the JWToken generated every time you authenticate.
A script ``authenticate.sh`` is here to show you how. (You need [jq](https://stedolan.github.io/jq/download/) if you want to use it)
```
export MILOBELLA_USERNAME=myuser
export MILOBELLA_PASSWORD=mypass
source authenticate.sh
```

### #3 : Raspberry audio configuration
If you are using a Raspberry PI B+ with RASPIAUDIO Ultra +, check the
[RASPIAUDIO ultra+ configuation](docs/raspiaudio-ultra+-configuration.md) documentation.

</details>

## Install
```bash
pip install -r requirements.txt
pip install -U --upgrade-strategy=eager -e .
```

## Run
```
$ milobella --help
usage: milobella [-h] [--verbose] [--url URL]

optional arguments:
  -h, --help  show this help message and exit
  --verbose   increase output verbosity
  --url URL   Milobella URL
```

## Documentation
- [Technical choices](./docs/technical-choices.md)
- [**IN PROGRESS** Wake-up-word experimentation](./docs/wake-up-word-experimentation.md)
