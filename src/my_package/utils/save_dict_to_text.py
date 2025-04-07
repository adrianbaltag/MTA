# import logging
# import os
# from datetime import datetime


# def save_dict_to_text(extracted_dict, filename=None):
#     """
#     Saves the extracted dictionary data to a text file in the txt_data folder on desktop.

#     Args:
#         extracted_dict (dict): Dictionary containing extracted data from read_image function
#         filename (str, optional): Name for the text file. If None, uses timestamp.

#     Returns:
#         str: Path to the created text file or None if operation failed
#     """
#     # Define the keys to extract in the correct order
#     keys = ["First name", "Last name", "Job title"]

#     # Check if the dictionary has the required keys
#     if not all(key in extracted_dict for key in keys):
#         missing_keys = [key for key in keys if key not in extracted_dict]
#         logging.error(f"Dictionary is missing required keys: {missing_keys}")
#         return None

#     # Create the txt_data folder on desktop if it doesn't exist
#     desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#     txt_data_path = os.path.join(desktop_path, "txt_data")

#     try:
#         if not os.path.exists(txt_data_path):
#             os.makedirs(txt_data_path)
#             logging.info(f"Created directory: {txt_data_path}")
#     except OSError as e:
#         logging.error(f"Failed to create directory {txt_data_path}. Error: {e}")
#         return None

#     # Generate filename if not provided
#     if filename is None:
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"extracted_data_{timestamp}.txt"

#     # Ensure filename has .txt extension
#     if not filename.lower().endswith(".txt"):
#         filename += ".txt"

#     file_path = os.path.join(txt_data_path, filename)

#     # Write the data to the text file
#     try:
#         with open(file_path, "w", encoding="utf-8") as f:
#             # Write each key's value on a new line
#             for key in keys:
#                 f.write(f"{extracted_dict[key]}\n")

#             # Add the separator pattern after job title
#             f.write("============= ===========\n")

#         logging.info(f"Successfully saved data to {file_path}")
#         return file_path

#     except Exception as e:
#         logging.error(f"Failed to write data to file {file_path}. Error: {e}")
#         return None


# if __name__ == "__main__":
#     # Set up logging
#     logging.basicConfig(level=logging.INFO)

#     # save_dict_to_text(res=read_image(0, "First name", "Last name", "Job title"))
#     # Example usage

import logging
import os
from datetime import datetime


def save_dict_to_text(extracted_dict):
    """
    Saves only the values from the extracted dictionary to a text file in the txt_data folder on desktop.
    Uses the 'First name' value from the dictionary as the filename.

    Args:
        extracted_dict (dict): Dictionary containing extracted data from read_image function

    Returns:
        str: Path to the created text file or None if operation failed
    """
    # Define the keys to extract in the correct order
    keys = ["First name", "Last name", "Job title"]

    # Check if the dictionary has the required keys
    if not all(key in extracted_dict for key in keys):
        missing_keys = [key for key in keys if key not in extracted_dict]
        logging.error(f"Dictionary is missing required keys: {missing_keys}")
        return None

    # Create the txt_data folder on desktop if it doesn't exist
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    txt_data_path = os.path.join(desktop_path, "txt_data")

    try:
        if not os.path.exists(txt_data_path):
            os.makedirs(txt_data_path)
            logging.info(f"Created directory: {txt_data_path}")
    except OSError as e:
        logging.error(f"Failed to create directory {txt_data_path}. Error: {e}")
        return None

    # Use the "First name" value as the filename
    filename = extracted_dict["First name"].strip()

    # Handle empty or invalid filenames
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"extracted_data_{timestamp}"
        logging.warning("First name is empty, using timestamp instead")

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

            # Add the separator pattern after job title
            f.write("========= ============================\n")

        # Print notification
        print(f"Text file has been created successfully: {file_path}")

        logging.info(f"Successfully saved data to {file_path}")
        return file_path

    except Exception as e:
        logging.error(f"Failed to write data to file {file_path}. Error: {e}")
        return None


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
