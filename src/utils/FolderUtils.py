import os
import shutil
from enum import Enum


class FileMismatchType(Enum):
    ADD = 1
    REMOVE = 2

class FileMismatch:
    filename: str
    super_folder: str
    mismatch_type: FileMismatchType

    def __init__(self, filename: str, super_folder: str, mismatch_type: FileMismatchType) -> None:
        self.filename = filename
        self.super_folder = super_folder
        self.mismatch_type = mismatch_type

class FolderUtils:
    @staticmethod
    def getFolderFiles(folder_path: str, target_extensions: list[str] = []) -> list[str]:
        files: list[str] = []
    
        for file in os.listdir(folder_path):
            if not os.path.isfile(os.path.join(folder_path, file)):
                continue
            
            file_path = os.path.join(folder_path, file)
            filename, extension = os.path.splitext(file_path)
            if len(target_extensions) > 0 and not target_extensions.__contains__(extension):
                continue

            files.append(file)
        
        return files

    @staticmethod
    def getFolderFileMismatch(super_folder: str, folder_path: str, target_extensions: list[str] = []) -> list[FileMismatch]:
        files_to_add: list[str] = FolderUtils.getMissingFiles(super_folder, folder_path, target_extensions)
        files_to_remove: list[str] = FolderUtils.getMissingFiles(folder_path, super_folder, target_extensions)

        mismatches: list[FileMismatch] = []
        for filename in files_to_add:
            mismatches.append(FileMismatch(filename, super_folder, FileMismatchType.ADD))
        
        for filename in files_to_remove:
            mismatches.append(FileMismatch(filename, super_folder, FileMismatchType.REMOVE))

        return mismatches


    # Returns the mismatchs found using the super folders as references
    @staticmethod
    def getMultipleFolderMismatch(super_folders: list[str], folder_path: str, target_extensions: list[str] = []) -> list[FileMismatch]:
        file_cache = {}
        
        files_in_super: list[str] = []
        for super_folder in super_folders:
            folder_files = FolderUtils.getFolderFiles(super_folder, target_extensions)
            for filename in folder_files:
                file_cache[filename] = super_folder

            files_in_super += folder_files

        files_to_add = FolderUtils.getMissingFiles("", folder_path, files_in_super=files_in_super, target_extensions=target_extensions)
        files_to_remove = FolderUtils.getMissingFiles(folder_path, "", files_in_folder=files_in_super, target_extensions=target_extensions)

        mismatches: list[FileMismatch] = []
        for filename in files_to_add:
            mismatches.append(FileMismatch(filename, file_cache[filename], FileMismatchType.ADD))
        
        for filename in files_to_remove:
            mismatches.append(FileMismatch(filename, folder_path, FileMismatchType.REMOVE))

        return mismatches

    @staticmethod
    def getMissingFiles(super_folder: str, folder_path: str, target_extensions: list[str] = [], files_in_super = [], files_in_folder = []) -> list[str]:
        missing_files: list[str] = []

        if files_in_super == []:
            files_in_super = FolderUtils.getFolderFiles(super_folder, target_extensions)
        
        if files_in_folder == []:
            files_in_folder = FolderUtils.getFolderFiles(folder_path, target_extensions)

        for filename in files_in_super:
            if files_in_folder.__contains__(filename):
                continue

            missing_files.append(filename)
        
        return missing_files
    
    @staticmethod
    def updateFolderFiles(mismatches: list[FileMismatch], folder_path: str):
        for mismatch in mismatches:
            match mismatch.mismatch_type:
                case FileMismatchType.ADD:
                    shutil.copy(
                        os.path.join(mismatch.super_folder, mismatch.filename),
                        folder_path
                    )
                
                case FileMismatchType.REMOVE:
                    os.remove(os.path.join(folder_path, mismatch.filename))
