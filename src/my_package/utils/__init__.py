"""`__init__.py`__
This module initializes the utils package.
"""

from .capture_and_click import capture_and_click
from .config import URL_FORMY, URL_GOOGLE, URL_YOUTUBE
from .gpu_checkup import gpu_checkup
from .open_app import open_app

__all__ = [
    "gpu_checkup",
    "capture_and_click",
    "URL_YOUTUBE",
    "URL_GOOGLE",
    "URL_FORMY",
    "open_app",
]
