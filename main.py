import manager.main as startMenu
try:
    menu = startMenu.Main()
    menu.main()
except KeyboardInterrupt:
    print("Cancel\n\n")
    exit()