#!/usr/bin/env python3
import argparse
import os
import traceback

import bcolors as bcolors

from milo.run import run
from milo.stt.google import GoogleSTT
from milo.tts.google2 import GoogleTTS2
from milo.wuw.porcupine import PorcupineWUW


class Arguments:
    verbose: bool
    milobella_url: str


def print_error(message: str) -> None:
    print(f"{bcolors.ERRMSG} Milobella error : {message}{bcolors.ENDC}")
    exit(1)


def validate_environment() -> None:
    if "MILOBELLA_AUTHORIZATION_TOKEN" not in os.environ:
        print_error("Missing env variable \"MILOBELLA_AUTHORIZATION_TOKEN\".")


def parse_arguments() -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--url", help="Milobella URL", default="https://milobella.com:10443")
    args = parser.parse_args()
    args_obj = Arguments()
    args_obj.verbose = not not args.verbose
    args_obj.milobella_url = args.url

    return args_obj


# noinspection PyBroadException
def main():
    args = parse_arguments()
    validate_environment()

    # Technologies selection. For now we don't have choice but it is meant to simplify the comparison of
    # different technologies
    tts = GoogleTTS2()
    wuw = PorcupineWUW()
    stt = GoogleSTT()

    try:
        run(args.milobella_url, tts, wuw, stt)
    except Exception:
        print_error(traceback.format_exc())


if __name__ == "__main__":
    main()
