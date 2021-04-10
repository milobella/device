import argparse
import os
import traceback

import bcolors as bcolors

from milo.porcupine import run_porcupine


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
    try:
        run_porcupine(args.milobella_url)
    except Exception as e:
        print_error(traceback.format_exc())


if __name__ == "__main__":
    main()
