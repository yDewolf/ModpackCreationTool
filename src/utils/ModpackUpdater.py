from utils.FolderUtils import FolderUtils
from utils.FolderUtils import FileMismatch
from utils.FolderUtils import FileMismatchType

class ModpackUpdater:
    # Folders with the mods from the modpack
    super_mod_folders: list[str]
    # .minecraft or the server folder
    target_folder: str

    def __init__(self, super_mod_folders: list[str], target_folder: str) -> None:
        self.super_mod_folders = super_mod_folders
        self.target_folder = target_folder

    def getMismatches(self) -> list[FileMismatch]:
        mismatches = FolderUtils.getMultipleFolderMismatch(self.super_mod_folders, self.target_folder, [".jar"])
        return mismatches

    def getMismatchesAsString(self):
        mismatches = self.getMismatches()

        string = ""
        for mismatch in mismatches:
            message = ""
            match mismatch.mismatch_type:
                case FileMismatchType.ADD:
                    message = "➕ | Add mod to folder"

                case FileMismatchType.REMOVE:
                    message = "➖ | Remove mod from folder"
            
            string += f"{message} | {mismatch.filename} |\n"
        
        string += f"Mismatch count: {len(mismatches)}\n"

        return string, len(mismatches) == 0

    def updateMods(self):
        FolderUtils.updateFolderFiles(self.getMismatches(), self.target_folder)
