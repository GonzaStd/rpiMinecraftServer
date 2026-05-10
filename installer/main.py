from rich.pretty import pprint
from pydantic import ValidationError
from installer.config.loader import ConfigFile
from installer.config.schema.config import Config



def main():
    config = ConfigFile("config.yaml", Config)
    while True:
        option = menu_choice()
        execute_action(option, config)


def show_config(config: ConfigFile):
    pprint(config.read_raw(), expand_all=True)


def change_config(config: ConfigFile):
    print("\nThis is the default config:")
    pprint(config.read_defaults(), expand_all=True)
    pass


def check_config(config: ConfigFile):
    try:
        config.read()
    except ValidationError as e:
        print("Your configuration is invalid. "
              f"More details in the message below:\n")

        for error in e.errors():
            field = ".".join(str(x) for x in error["loc"])
            field = f"[{field}]"
            msg = error['msg']
            print(f"❌ {field}: {msg}")


def run(config: ConfigFile):
    pass


def execute_action(option: int, config: ConfigFile):
    match option:
        case 1:
            show_config(config)
        case 2:
            change_config(config)
        case 3:
            check_config(config)
        case 4: 
            run(config)
        case 5:
            exit()

def menu_choice():
    options = ["Display configuration", "Change configuration",
               "Check configuration", "Run server", "Exit"]
    i=1
    for option in options:
        print( f"{i}) " + option)
        i += 1

    choice = get_int("Enter your choice: ", 1, len(options))
    return choice

def get_int(msg, min, max):

    while True:
        try:
            n = int(input(msg))
            if min <= n <= max:
                return n
            print(f"Please enter a number between {min} and {max}")

        except ValueError:
            print("Enter a valid number.")