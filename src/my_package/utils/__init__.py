"""`__init__.py`__
This module initializes the utils package.
"""

from .capture_and_click import capture_and_click
from .capture_full_screenshot import capture_full_screenshot
from .classes import ScreenshotUtility
from .config import URL_FORMY, URL_GOOGLE, URL_YOUTUBE
from .create_txt_file import create_txt_file
from .gpu_checkup import gpu_checkup
from .open_app import open_app
from .read_image import read_image
from .user_input import user_input

__all__ = [
    "gpu_checkup",
    "capture_and_click",
    "URL_YOUTUBE",
    "URL_GOOGLE",
    "URL_FORMY",
    "open_app",
    "user_input",
    "capture_full_screenshot",
    "create_txt_file",
    "read_image",
    "ScreenshotUtility",
]
