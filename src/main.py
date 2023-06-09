import shutil
import sys
from pathlib import Path
from typing import Union

from loguru import logger

from src.utils import read_json


class OraganizeFiles:
    """
    This class is used to organize files in a directory by
    moving files into directories based on extension.
    """
    def __init__(self):
        ext_dirs = read_json('data/extensions.json')

        # set keys as extensions and values as directory names
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name

    def __call__(self, directory_path: Union[str, Path]):
        """
        Organize files in a directory by moving them
        to sub directories based on extension.
        """
        directory_path = Path(directory_path)

        if not directory_path.exists():
            raise FileNotFoundError(f"{directory_path} does not exist")

        logger.info(f"Organizing files in {directory_path}...")

        file_extensions = []
        for file_path in directory_path.iterdir():
            # ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # move files
            file_extensions.append(file_path.suffix)
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = directory_path / 'other'
            else:
                DEST_DIR = directory_path / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == "__main__":
    org_files = OraganizeFiles()
    org_files(sys.argv[1])
    logger.info("Done!")
