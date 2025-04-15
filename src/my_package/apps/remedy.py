"""This script holds the logic for the remedy application."""

import time

import keyboard

# pylint: disable=E0401, W0105,W0012,W0612, F841
# ruff:  noqa: E0401, W0105,W0012,W0612, F841
from my_package.utils.capture_and_click import capture_and_click
from my_package.utils.capture_full_screenshot import capture_full_screenshot
from my_package.utils.config import URL_REMEDY
from my_package.utils.create_txt_file import create_txt_file
from my_package.utils.open_app import open_app
from my_package.utils.user_input import user_input


def remedy():
    """__summary__:Main function to execute the remedy logic.
    It opens a specific URL, captures a screenshot, and processes the image to extract text.
    """
    nrb_ticket = (
        user_input()
    )  # Call the user_input function to get the NRB ticket number
    time.sleep(1)  # Wait for the user input to be processed

    open_app(
        URL_REMEDY, index=2
    )  # Open the form URL in the default web browser, on selected monitor index based
    time.sleep(1)  # Wait for the form to load

    capture_and_click("SCREENSHOT", "Trouble-ID", 2)  # select same index as open_app

    time.sleep(1)  # Wait for the screenshot to be taken
    keyboard.write(nrb_ticket)
    keyboard.press_and_release("enter")
    time.sleep(3)  # Wait for loading the page
    capture_full_screenshot(
        monitor_index=2
    )  # Capture the full screenshot of the selected monitor
    time.sleep(1)  # Wait for the screenshot to be taken

    """Create a text file with the extracted text from the screenshot."""
    create_txt_file()


if __name__ == "__main__":
    remedy()
