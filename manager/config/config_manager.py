import questionary
import manager.interface.interface as interface
from manager.config.loader import ConfigFile
from pydantic import ValidationError
from rich.pretty import pprint


class ConfigManager:
    def __init__(self, config: ConfigFile):
        self.config = config

    def show_config(self):
        pprint(self.config.read_raw(), expand_all=True)


    def change_config(self):
        default_config = self.config.read_defaults()
        print("\nThis is the default config:")
        pprint(default_config, expand_all=True)
        print("")

        option = interface.select_item([
            "Use the default config",
            "Use the default config with changes",
            "Make a new config from scrap"
        ])

        match option:
            case 1:
                self.config.write(default_config)
            case 2:
                _continue = True
                new_config = None

                while _continue:
                    new_config = interface.change_dict_value(default_config)
                    _continue = questionary.confirm(
                        "Do you want to change another one? y/n: ",
                        default=False).ask()

                if new_config is not None:
                    self.config.write(new_config)
            case 3:
                pass


    def check_config(self):
        try:
           self.config.read()
        except ValidationError as e:
            print("Your configuration is invalid. "
                  f"More details in the message below:\n")

            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                field = f"[{field}]"
                msg = error['msg']
                print(f"❌ {field}: {msg}")