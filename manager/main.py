from typing import Any
import questionary
from os import system
from rich.pretty import pprint
from pydantic import ValidationError
from installer.config.loader import ConfigFile
from installer.config.schema.config import Config



def main():
    config = ConfigFile("config.yaml", Config)
    while True:
        system("clear")
        option = menu_choice()
        execute_action(option, config)

def menu_choice():
    option = select_by_number([
        "Display configuration",
        "Change configuration",
        "Check configuration",
        "Run server",
        "Exit"
    ])
    return option

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
    input("Enter any key to get back to menu...")

def show_config(config: ConfigFile):
    pprint(config.read_raw(), expand_all=True)


def change_config(config: ConfigFile):
    default_config = config.read_defaults()
    print("\nThis is the default config:")
    pprint(default_config, expand_all=True)
    print("")

    option = select_by_number([
        "Use the default config",
        "Use the default config with changes",
        "Make a new config from scrap"
    ])

    match option:
        case 1:
            config.write(default_config)
        case 2:
            _continue = True
            new_config = None

            while _continue:
                new_config = change_dict_value(default_config)
                _continue = questionary.confirm(
                    "Do you want to change another one? y/n: ",
                    default=False).ask()

            if new_config is not None:
                config.write(new_config)
        case 3:
            pass

def navigate_to_primitive(
            field: dict | Any,
            path: list | None = None
        ) -> tuple[Any, list]:
    if path is None:
        path = [] # New list for each call.
    print(type(field))
    if type(field) == dict:
        choices = list(field.keys())
        response = questionary.select(
            "Select a field:",
            choices=choices
        ).ask()
        path.append(response)
        return navigate_to_primitive(field[response], path)
    else:
        primitive = field
        return primitive, path

def change_dict_value(_dict: dict) -> dict:
    old_value, primitive_path = navigate_to_primitive(_dict)
    value_to_change = primitive_path[-1]
    new_value = questionary.text(
        f"Change {value_to_change} to [{old_value}]: "
    ).ask()
    if new_value.strip() == "":
        print("Didn't make any changes.")
    else:
        current_path = _dict
        print(value_to_change, primitive_path, new_value)
        for field in primitive_path[:-1]:
            print(field)
            current_path = current_path[field]
        current_path[value_to_change] = new_value
    return _dict

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

def get_int(msg, min: int, max: int):
    while True:
        try:
            n = int(input(msg))
            if min <= n <= max:
                return n
            print(f"Please enter a number between {min} and {max}")

        except ValueError:
            print("Enter a valid number.")

def select_by_number(choices: list, msg: str = "Select an option:"):
    choice = questionary.select(msg, choices).ask()
    return int(choices.index(choice))+1