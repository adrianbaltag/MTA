# pylint: disable=C0301,C0116,C0114, W0613, W0611, C0413, E0401, W0614, W0718
"""This module provides a function to extract and save certain strings from a returned dict created by 'read_image' to a text file."""

import os
from datetime import datetime
from typing import List, Optional

from my_package.utils.read_image import read_image


def save_dict_to_text(
    img_index: int = 0, keys: List[str] = None, filename_key: Optional[str] = None
) -> str:
    """
    Extracts specified keys from read_image results and saves values to a text file.

    Args:
        img_index (int): Index of the image to read from.
        keys (List[str]): List of keys to extract from the image data.
        filename_key (str, optional): Key whose value will be used as the filename.
                                     If None, uses the first key in keys list.

    Returns:
        str: Path to the created text file or None if operation failed
    """
    # Set default keys if none provided
    if keys is None:
        keys = ["paragraph_18", "paragraph_25", "paragraph_26"]

    # Read image data once using the existing read_image function
    extracted_dict = read_image(img_index)

    if not extracted_dict:
        print(f"Failed to extract data from image {img_index}")
        return None

    # Check if all requested keys exist in the extracted dictionary
    missing_keys = [key for key in keys if key not in extracted_dict]
    if missing_keys:
        print(f"Dictionary is missing required keys: {missing_keys}")
        return None

    # Determine which key's value to use for the filename
    if filename_key is None:
        filename_key = keys[0]  # Use first key if none specified

    if filename_key not in extracted_dict:
        print(f"Filename key '{filename_key}' not found in extracted data")
        return None

    # Create the txt_data folder on desktop if it doesn't exist
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    txt_data_path = os.path.join(desktop_path, "txt_data")

    try:
        if not os.path.exists(txt_data_path):
            os.makedirs(txt_data_path)
            print(f"Created directory: {txt_data_path}")
    except OSError as e:
        print(f"Failed to create directory {txt_data_path}. Error: {e}")
        return None

    # Use the specified key's value as the filename
    filename = extracted_dict[filename_key].strip()

    # Handle empty or invalid filenames
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"extracted_data_{timestamp}"
        print(f"The value for '{filename_key}' is empty, using timestamp instead")

    # Remove any characters that might be invalid in a filename
    filename = "".join(c for c in filename if c.isalnum() or c in " _-")

    # Ensure filename has .txt extension
    if not filename.lower().endswith(".txt"):
        filename += ".txt"

    file_path = os.path.join(txt_data_path, filename)

    # Write the data to the text file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            # Write only the values, each on a new line
            for key in keys:
                f.write(f"{extracted_dict[key]}\n")

            # Add the separator pattern after the last key
            f.write("========= ============================\n")

        # Print notification
        print(f"Text file has been created successfully: {file_path}")

        return file_path

    except Exception as e:
        print(f"Failed to write data to file {file_path}. Error: {e}")
        return None


if __name__ == "__main__":
    # Exaample o --> no args passed
    # save_dict_to_text()

    # Example 1: Using default parameters
    save_dict_to_text(
        img_index=0,
        keys=["paragraph_19", "paragraph_25", "paragraph_26"],
        filename_key="paragraph_19",
    )

    # Example 2: Specifying custom keys and filename key
    # save_dict_to_text(
    #     img_index=0,
    #     keys=["paragraph_19", "paragraph_25", "paragraph_26"],
    #     filename_key="paragraph_19"
    # )
