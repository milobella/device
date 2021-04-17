import bcolors


def print_error(message: str) -> None:
    print(f"{bcolors.ERRMSG} Milobella error : {message}{bcolors.ENDC}")
    exit(1)


def print_warn(message: str) -> None:
    print(f"{bcolors.WARN} Milobella warning : {message}{bcolors.ENDC}")


def print_info(message: str) -> None:
    print(f"{bcolors.OKMSG}{message}{bcolors.ENDC}")
