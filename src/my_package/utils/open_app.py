"""This script open a new tab in the browser, based on the url provided from config.py"""

import time
import webbrowser

# import the URLs from config.py
from my_package.utils.config import URL_YOUTUBE


def open_app(url):
    """__summary__:
    This function opens a new tab in the default web browser with the provided URL.
    """
    # Open the URL in the default web browser
    webbrowser.open(url)
    time.sleep(1)  # Wait for the browser to open


if __name__ == "__main__":
    open_app(URL_YOUTUBE)
