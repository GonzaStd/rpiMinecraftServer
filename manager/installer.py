from os import system
from manager.config.loader import ConfigFile
import manager.interface.interface as interface
import manager.config.config_manager as config_manager
import manager.mojang_api

class Installer:
    def __init__(self, config: ConfigFile):
        self.config = config
        self.configManager = config_manager.ConfigManager(config)

    def main(self):
        while True:
            system("clear")
            option = self._menu_choice()
            self._execute_action(option)

    def _install(self):
        pass


    def _menu_choice(self):
        option = interface.select_item([
            "Display configuration",
            "Change configuration",
            "Check configuration",
            "Install servers from current config",
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
                self._install()
            case 5:
                exit()
        input("Enter any key to get back to menu...")