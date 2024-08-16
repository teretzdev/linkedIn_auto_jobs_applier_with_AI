#!/usr/bin/env python
import os
import shutil
import zipfile
import sys

def create_archive(dir_path, archive_name):
    """
    Creates a zip archive of the given directory and its subdirectories.

    Args:
        dir_path (str): The path to the directory to archive.
        archive_name (str): The name of the archive file.
    """

    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dir_path)
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")

    print(f"Archive '{archive_name}' created successfully.")

# Example usage:
dir_to_archive = "d:\\linkedin-bot-ai\\"
archive_name = "linkedin-bot-ai.zip"
create_archive(dir_to_archive, archive_name)
