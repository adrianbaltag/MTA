"""This script creates a text file on the desktop with the ticket number, MDN, and issue."""

import os

from my_package.utils.read_image import read_image


def create_txt_file():
    """__summary__:
    This function creates a text file on the desktop with the ticket number, MDN, and issue.
    It first checks if the folder txt_data exists on the desktop, and if not, it creates it. Then, it creates a text file with the ticket number as the filename
      and writes the ticket number, MDN, and issue to the file.
    """
    my_ticket, my_mdn, my_issue = read_image(0)

    # check if the folder txt_data exists on the desktop, and if not then create it
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    txt_data_path = os.path.join(desktop_path, "txt_data")
    if not os.path.exists(txt_data_path):
        os.makedirs(txt_data_path)
        print(f"Created directory: {txt_data_path}")
    else:
        print(f"Directory already exists: {txt_data_path}")
    # Create a text file on txt_data folder on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    txt_data_path = os.path.join(desktop_path, "txt_data")
    file_path = os.path.join(txt_data_path, f"{my_ticket}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{my_ticket}\n")
        f.write(f"{my_mdn}\n")
        f.write(f"{my_issue}\n")
        f.write("========= ============================\n")
    print(f"Text file has been created successfully: {file_path}")


if __name__ == "__main__":
    create_txt_file()
