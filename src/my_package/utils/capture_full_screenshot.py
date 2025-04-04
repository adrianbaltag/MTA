"""This script captures a full screenshot of a specified application window."""

import os
import re
import time

import pyautogui
import pygetwindow as gw


def capture_full_screenshot(app_name: str):
    """_summary__: This function captures a full screenshot of a specified application window.
    It finds the window by its title, activates it, and takes a screenshot of the visible area.

    Args:
        app_name (str): name of the application window to capture.

    Raises:
        Exception:no visible window found with the specified title.
    """
    # Find visible window matching the title
    windows = [w for w in gw.getWindowsWithTitle(app_name) if w.visible]
    if not windows:
        raise Exception(f"No visible window found with title containing '{app_name}'")

    window = windows[0]
    window.activate()
    time.sleep(1)  # Give time for the window to come to front

    # Get window bounds
    left, top, width, height = window.left, window.top, window.width, window.height

    # Take screenshot of the window region
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Go up to src/my_package/ from utils/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Clean filename just in case
    safe_name = re.sub(r'[<>:"/\\|?*]', "_", app_name)
    filename = f"{safe_name}.png"

    # Save path
    save_path = os.path.join(images_dir, filename)
    screenshot.save(save_path)

    print(f"Screenshot saved to: {save_path}")


if __name__ == "__main__":
    # Example usage
    capture_full_screenshot("Formy")  # Replace with your app name
