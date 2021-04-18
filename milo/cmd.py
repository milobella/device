#!/usr/bin/env python3
import argparse
import os
import traceback

from milo.message import print_error
from milo.milobella import Milobella, MILOBELLA_TOKEN_ENV
from milo.run import run
from milo.stt.google import GoogleSTT
from milo.tts.google2 import GoogleTTS2
from milo.wuw.pocketsphinx import PocketSphinxWUW


class PocketSphinxArguments:
    threshold: float


class Arguments:
    verbose: bool
    milobella_url: str
    keyword: str
    pocketsphinx: PocketSphinxArguments


def validate_environment() -> None:
    if MILOBELLA_TOKEN_ENV not in os.environ:
        print_error(f"Missing env variable \"{MILOBELLA_TOKEN_ENV}\".")


def parse_arguments() -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--url", help="Milobella URL", default="https://milobella.com:10443")
    parser.add_argument("--keyword", help="Wake up word", default="bella")
    parser.add_argument("--pocket-sphinx-threshold", help="Milobella URL", default=1e-30, type=float)
    args = parser.parse_args()
    args_obj = Arguments()
    args_obj.verbose = not not args.verbose
    args_obj.milobella_url = args.url
    args_obj.keyword = args.keyword
    psphinx_args = PocketSphinxArguments()
    psphinx_args.threshold = args.pocket_sphinx_threshold
    args_obj.pocketsphinx = psphinx_args

    return args_obj


def main():
    args = parse_arguments()
    validate_environment()

    # Technologies selection.
    tts = GoogleTTS2()
    wuw = PocketSphinxWUW(keyword=args.keyword, kws_threshold=args.pocketsphinx.threshold)
    stt = GoogleSTT()

    # Initialize the milobella client
    milobella = Milobella(args.milobella_url)

    # noinspection PyBroadException
    try:
        run(milobella, tts, wuw, stt)
    except Exception:
        print_error(traceback.format_exc())


if __name__ == "__main__":
    main()
