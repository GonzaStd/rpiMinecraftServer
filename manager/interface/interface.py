import questionary
from typing import Any


def select_item(items: list, msg: str = "Select an option:"):
    """
    Displays a list of items and prompts the user to select one.
    :param items:
    :param msg:
    :return:  Returns the index number + 1 so the options start from 1 instead of 0
    """
    choice = questionary.select(msg, items).ask()
    return int(items.index(choice)) + 1


def navigate_to_primitive(
        field: dict | Any,
        path: list | None = None
) -> tuple[Any, list]:
    if path is None:
        path = []  # New list for each call.
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