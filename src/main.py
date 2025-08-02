from configparser import ConfigParser

from utils.ModpackUpdater import ModpackUpdater
from utils.ConsoleInputHandler import ConsoleInputHandler

import os

def main():
    cfg = ConfigParser()
    cfg.read("config.ini")

    while True:
        selected_option = ConsoleInputHandler.selectFromOptions(
            "Select one of the options:",
            ["Update mods", "Create a Release Folder", "Create Modpack Folder"],
            False
        )
        match selected_option:
            case 0:
                update_mods_menu(cfg)
            case 1:
                create_release_folder_menu(cfg)
            case 2:
                create_modpack_folder_menu(cfg)

def update_mods_menu(cfg: ConfigParser):
    paths_to_update = {
        "server": cfg.get("PATHS", "ServerPath"),
        "client": cfg.get("PATHS", "ClientPath")
    }

    modpack_folder = cfg.get("PATHS", "ModpackPath")

    for name in paths_to_update:
        print(f"Mismatches for {name.capitalize()}\n")

        path = paths_to_update[name]
        if path == "":
            print(f"WARNING: No path was provided for {name} | Please edit the config.ini file")
            continue
        
        updater: ModpackUpdater = ModpackUpdater(
            [os.path.join(modpack_folder, "mods"), os.path.join(modpack_folder, f"{name}side")],
            os.path.join(path, "mods")
        )

        mismatch_str, no_mismatch = (updater.getMismatchesAsString())
        print(mismatch_str)

        if not no_mismatch:
            if ConsoleInputHandler.confirmChoice(f"Update {name.capitalize()} mods?"):
                updater.updateMods()
        
        mismatch_str, no_mismatch = (updater.getMismatchesAsString())
        print(f"Final mismatches for {name.capitalize()}")
        print(mismatch_str)


def create_release_folder_menu(cfg: ConfigParser):
    pass

def create_modpack_folder_menu(cfg: ConfigParser):
    pass    

main()