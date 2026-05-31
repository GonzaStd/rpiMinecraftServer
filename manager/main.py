from os import system
from manager import installer
from manager.config.loader import ConfigFile
import manager.interface.interface as interface
from manager.config.schema.config import Config

class Main:
    def __init__(self):
        self.config = ConfigFile("config.yaml", Config)
        self.installer = installer.Installer(self.config)


    def main(self):
        while True:
            system("clear")
            option = self._menu_choice()
            self._execute_action(option)


    def _menu_choice(self):
        option = interface.select_item([
            "Create or change configuration",
            "Manage running server",
            "Run server",
            "Exit"
        ])
        return option


    def _execute_action(self, option: int):
        match option:
            case 1:
                self.installer.main()
            case 2:
                pass
            case 3:
                self.run_server()
            case 4:
                exit()

    def run_server(self):
        pass
    input("Enter any key to get back to menu...")

