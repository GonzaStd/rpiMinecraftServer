from os import system
import manager.config.config_manager as ConfigManager
from manager.config.loader import ConfigFile
import manager.interface.interface as interface

class Installer:
    def __init__(self, config: ConfigFile):
        self.config = config
        self.configManager = ConfigManager.ConfigManager(config)

    def main(self):
        while True:
            system("clear")
            option = self._menu_choice()
            self._execute_action(option)


    def _menu_choice(self):
        option = interface.select_item([
            "Display configuration",
            "Change configuration",
            "Check configuration",
            "Exit"
        ])
        return option


    def _execute_action(self, option: int):
        match option:
            case 1:
                self.configManager.show_config()
            case 2:
                self.configManager.change_config()
            case 3:
                self.configManager.check_config()
            case 4:
                exit()
        input("Enter any key to get back to menu...")