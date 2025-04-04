"""_summary_: This function will capture a screenshot of the ENTIRE browser window ONLY, search for a keyword using OCR and regex, and click on the detected text.
__note__: The function will ONLY work if the browser window IS THE MAIN SCREEN (for multiple monitors - select in your system the main screen)  is open and visible on the screen
Args:
    browser_title (str): Title of the browser window to capture.
    screenshot_name (str): Name of the screenshot file (without extension).
    keyword (str): The text to search for using OCR and regex.
"""

import os
import re

import easyocr
import pyautogui
import pygetwindow as gw


def capture_and_click(app_name, screenshot_name, keyword):
    """Captures a screenshot of the browser window, searches for a keyword, and clicks it.

    Args:
    app_name (str): Title of the browser window to capture.
        screenshot_name (str): Name of the screenshot file (without extension).
        keyword (str): The text to search for using OCR and regex.
    """
    # Step 1: Get browser window position and size
    browser_title = f"{app_name}"  # Change this if needed
    browser_window = None

    for window in gw.getWindowsWithTitle(browser_title):
        if browser_title in window.title:
            browser_window = window
            break

    if not browser_window:
        print("Browser window not found!")
        return

    x, y, width, height = (
        browser_window.left,
        browser_window.top,
        browser_window.width,
        browser_window.height,
    )

    # Step 2: Capture a screenshot and save it in the "test" folder on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    new_folder = os.path.join(desktop_path, "BROWSER_FULL_SCREENSHOT")

    # Ensure the directory exists
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print(f"Directory created: {new_folder}")

    # Use absolute path for the screenshot
    screenshot_path = os.path.join(new_folder, f"{screenshot_name}.png")
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(screenshot_path)
    print(f"Screenshot saved at: {screenshot_path}")

    # Step 3: Use OCR to extract text and positions - works - slower
    reader = easyocr.Reader(["en"], gpu=True)
    results = reader.readtext(screenshot_path)

    # Step 4: Apply regex to find a keyword
    keyword_pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for bbox, text, prob in results:
        if keyword_pattern.search(text):
            x_min, y_min = bbox[0]
            x_max, y_max = bbox[2]
            center_x = x + (x_min + x_max) // 2  # Adjust for window position
            center_y = y + (y_min + y_max) // 2

            # Step 5: Click on the detected text
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            pyautogui.click()
            print(f"Clicked on '{text}' at ({center_x}, {center_y})")
            return  # Stop after the first match

    print(f"Keyword '{keyword}' not found in screenshot.")


if __name__ == "__main__":
    capture_and_click("Formy", "screenshot", "Enter last name")
