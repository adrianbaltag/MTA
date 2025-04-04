"""This script holds the logic for the remedy application."""

import time

import keyboard

from my_package.utils.capture_and_click import capture_and_click
from my_package.utils.config import URL_FORMY
from my_package.utils.open_app import open_app
from my_package.utils.user_input import user_input


def remedy():
    nrb_ticket = (
        user_input()
    )  # Call the user_input function to get the NRB ticket number
    time.sleep(1)  # Wait for the user input to be processed

    open_app(URL_FORMY)  # Open the form URL in the default web browser
    time.sleep(1)  # Wait for the form to load

    capture_and_click(
        "Formy", "screenshot", "Enter last name"
    )  # Capture the screenshot and click on the form

    time.sleep(1)  # Wait for the screenshot to be taken
    keyboard.write(nrb_ticket)
    keyboard.press_and_release("enter")


if __name__ == "__main__":
    remedy()
