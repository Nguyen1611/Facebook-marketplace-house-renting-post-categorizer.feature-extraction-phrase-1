"""
Rename picture so that it can be uploaded to github and prevent error
"""
import os
import re


def rename_picture_files_in_subfolders(root_directory):
    picture_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}


    for subdir, _, files in os.walk(root_directory):
        # Filter files
        picture_files = [f for f in files if os.path.splitext(f)[1].lower() in picture_extensions]

        # Sort files to maintain the original order
        picture_files.sort(key=lambda f: int(re.sub('\D', '', f)) if re.sub('\D', '', f).isdigit() else float('inf'))

        # Rename files to a number based on their order in each subdir
        for i, file_name in enumerate(picture_files, start=1):
            new_name = f"{i}{os.path.splitext(file_name)[1]}"
            old_file_path = os.path.join(subdir, file_name)
            new_file_path = os.path.join(subdir, new_name)
            try:
                os.rename(old_file_path, new_file_path)
            except:
                continue # this will ignore error for manual fix
            print(f"Renamed '{old_file_path}' to '{new_file_path}'")


root_directory_path = 'dataset_model2'
rename_picture_files_in_subfolders(root_directory_path)
