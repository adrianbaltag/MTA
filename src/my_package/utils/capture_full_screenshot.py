# """This script captures a full screenshot of a specified application window."""

# import os
# import re
# import time

# import pyautogui
# import pygetwindow as gw


# def capture_full_screenshot(app_name: str):
#     """_summary__: This function captures a full screenshot of a specified application window.
#     It finds the window by its title, activates it, and takes a screenshot of the visible area.

#     Args:
#         app_name (str): name of the application window to capture.

#     Raises:
#         Exception:no visible window found with the specified title.
#     """
#     # Find visible window matching the title
#     windows = [w for w in gw.getWindowsWithTitle(app_name) if w.visible]
#     if not windows:
#         raise ValueError(f"No visible window found with title containing '{app_name}'")

#     window = windows[0]
#     window.activate()
#     time.sleep(1)  # Give time for the window to come to front

#     # Get window bounds
#     left, top, width, height = window.left, window.top, window.width, window.height

#     # Take screenshot of the window region
#     screenshot = pyautogui.screenshot(region=(left, top, width, height))

#     # Go up to src/my_package/ from utils/
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#     images_dir = os.path.join(base_dir, "images")
#     os.makedirs(images_dir, exist_ok=True)

#     # Clean filename just in case
#     safe_name = re.sub(r'[<>:"/\\|?*]', "_", app_name)
#     filename = f"{safe_name}.png"

#     # Save path
#     save_path = os.path.join(images_dir, filename)
#     screenshot.save(save_path)

#     print(f"Screenshot saved to: {save_path}")


# if __name__ == "__main__":
#     # Example usage
#     capture_full_screenshot("Formy")  # Replace with your app name

"""newer version"""

# # """This script captures a full screenshot of a specified application window."""
# import os
# import re
# import time

# import pyautogui
# import pygetwindow as gw


# def capture_full_screenshot(app_name: str):
#     windows = [w for w in gw.getWindowsWithTitle(app_name) if w.visible]
#     if not windows:
#         raise ValueError(f"No visible window found with title containing '{app_name}'")

#     window = windows[0]
#     window.restore()
#     window.activate()
#     time.sleep(1)

#     left, top, width, height = window.left, window.top, window.width, window.height
#     print(
#         f"[INFO] Window position: left={left}, top={top}, width={width}, height={height}"
#     )

#     # Take full screenshot
#     full_screenshot = pyautogui.screenshot().convert("RGB")
#     print(f"[INFO] Full screenshot size: {full_screenshot.size}")

#     # Diagnostic check for invalid region
#     if width <= 0 or height <= 0:
#         raise ValueError("❌ Invalid window size: Cannot take screenshot.")

#     crop_box = (left, top, left + width, top + height)
#     print(f"[INFO] Crop box: {crop_box}")

#     # Make sure the crop region is valid
#     try:
#         cropped = full_screenshot.crop(crop_box)
#     except Exception as e:
#         print(f"❌ Failed to crop the image: {e}")
#         full_screenshot.save(
#             "debug_fullscreen.png"
#         )  # save full screenshot for troubleshooting
#         raise

#     # Build path to src/my_package/images
#     current_file_dir = os.path.dirname(os.path.abspath(__file__))
#     package_root_dir = os.path.abspath(os.path.join(current_file_dir, ".."))
#     images_dir = os.path.join(package_root_dir, "images")
#     os.makedirs(images_dir, exist_ok=True)

#     # Clean name & save
#     safe_name = re.sub(r'[<>:"/\\|?*]', "_", app_name)
#     filename = f"{safe_name}.png"
#     save_path = os.path.join(images_dir, filename)

#     cropped.save(save_path)
#     print(f"✅ Screenshot saved to: {save_path}")


# if __name__ == "__main__":
#     capture_full_screenshot("Canva")  # replace with actual window title

# """This script captures a full screenshot of a specified application window tab."""
# import os
# import re
# import time
# from typing import List, Optional

# import pyautogui
# import pygetwindow as gw


# def list_visible_windows() -> List[str]:
#     """List all visible windows on the system.

#     Returns:
#         List of window titles that are currently visible
#     """
#     return [window.title for window in gw.getAllWindows() if window.visible]


# def capture_full_screenshot(tab_index: int, app_title_pattern: Optional[str] = None):
#     """Captures a screenshot of a window at the specified tab index.

#     Args:
#         tab_index: The index of the window in the list of visible windows, 0-based
#         app_title_pattern: Optional pattern to filter windows by title

#     Raises:
#         ValueError: If no visible windows match the criteria or the index is out of range
#     """
#     # Get all visible windows
#     all_windows = [w for w in gw.getAllWindows() if w.visible]

#     # Filter by title pattern if provided
#     if app_title_pattern:
#         filtered_windows = [
#             w for w in all_windows if app_title_pattern.lower() in w.title.lower()
#         ]
#     else:
#         filtered_windows = all_windows

#     # Display available windows for debugging
#     print(f"[INFO] Found {len(filtered_windows)} visible window(s):")
#     for i, win in enumerate(filtered_windows):
#         print(f"  [{i}] {win.title} ({win.width}x{win.height})")

#     # Check if the index is valid
#     if not filtered_windows:
#         raise ValueError(
#             "No visible windows found"
#             + (
#                 f" with title containing '{app_title_pattern}'"
#                 if app_title_pattern
#                 else ""
#             )
#         )

#     if tab_index < 0 or tab_index >= len(filtered_windows):
#         raise ValueError(
#             f"Tab index {tab_index} is out of range. Valid range: 0-{len(filtered_windows) - 1}"
#         )

#     # Get the window at the specified index
#     window = filtered_windows[tab_index]
#     print(f"[INFO] Selected window: [{tab_index}] {window.title}")

#     # Restore and activate the window
#     window.restore()
#     window.activate()
#     time.sleep(1)  # Give the window time to fully activate

#     left, top, width, height = window.left, window.top, window.width, window.height
#     print(
#         f"[INFO] Window position: left={left}, top={top}, width={width}, height={height}"
#     )

#     # Take full screenshot
#     full_screenshot = pyautogui.screenshot().convert("RGB")
#     print(f"[INFO] Full screenshot size: {full_screenshot.size}")

#     # Diagnostic check for invalid region
#     if width <= 0 or height <= 0:
#         raise ValueError("❌ Invalid window size: Cannot take screenshot.")

#     crop_box = (left, top, left + width, top + height)
#     print(f"[INFO] Crop box: {crop_box}")

#     # Make sure the crop region is valid
#     try:
#         cropped = full_screenshot.crop(crop_box)
#     except Exception as e:
#         print(f"❌ Failed to crop the image: {e}")
#         full_screenshot.save(
#             "debug_fullscreen.png"
#         )  # Save full screenshot for troubleshooting
#         raise

#     # Build path to src/my_package/images
#     current_file_dir = os.path.dirname(os.path.abspath(__file__))
#     package_root_dir = os.path.abspath(os.path.join(current_file_dir, ".."))
#     images_dir = os.path.join(package_root_dir, "images")
#     os.makedirs(images_dir, exist_ok=True)

#     # Use window title for the filename
#     safe_name = re.sub(r'[<>:"/\\|?*]', "_", window.title)
#     filename = f"tab_{tab_index}_{safe_name}.png"
#     save_path = os.path.join(images_dir, filename)

#     cropped.save(save_path)
#     print(f"✅ Screenshot saved to: {save_path}")

#     return save_path


# def interactive_window_selection():
#     """Interactive function to help users select the right window by index."""
#     all_windows = [w for w in gw.getAllWindows() if w.visible]

#     print("\n===== Available Windows =====")
#     for i, win in enumerate(all_windows):
#         print(f"[{i}] {win.title}")

#     try:
#         selection = int(input("\nEnter the index of the window to capture: "))
#         if 0 <= selection < len(all_windows):
#             return capture_full_screenshot(selection)
#         else:
#             print("Invalid selection.")
#     except ValueError:
#         print("Please enter a valid number.")


# if __name__ == "__main__":
#     # Option 1: Capture by tab index (first visible window)
#     capture_full_screenshot(7)

#     # Option 2: Capture by tab index with filtering (first Chrome window)
#     # capture_window_by_tab_index(0, "Chrome")

#     # Option 3: Interactive selection
#     # interactive_window_selection()

import os

import mss
import mss.tools
from PIL import Image


def capture_full_screenshot(monitor_index: int = 0):
    """Captures a screenshot of a specific monitor.
    Screenshots are saved in the 'img_to_read' directory.
    The directory is created if it doesn't exist.

    Args:
        monitor_index (int): Index of the monitor to use (0-based).
    """
    # Build path to src/my_package/images
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    package_root_dir = os.path.abspath(os.path.join(current_file_dir, ".."))
    images_dir = os.path.join(package_root_dir, "img_to_read")
    os.makedirs(images_dir, exist_ok=True)

    # Use MSS to get monitor information and take screenshot
    with mss.mss() as sct:
        # Get monitor information
        monitors = sct.monitors

        # Print all monitors for debugging
        print(f"[INFO] Detected {len(monitors) - 1} monitors:")
        for i, m in enumerate(monitors):
            if i == 0:
                print(f"  All monitors combined: {m}")
            else:
                print(f"  Monitor {i - 1}: {m}")

        # Check if monitor_index is valid
        if monitor_index + 1 >= len(monitors):
            raise ValueError(
                f"Error: Monitor index {monitor_index} is out of range. Only {len(monitors) - 1} monitors detected."
            )

        # Get the requested monitor (add 1 because mss uses 1-based indexing, with 0 being "all monitors")
        target_monitor = monitors[monitor_index + 1]
        print(f"[INFO] Using monitor {monitor_index}: {target_monitor}")

        # Capture screenshot of the entire monitor
        print(f"[INFO] Capturing monitor {monitor_index}...")
        screenshot = sct.grab(target_monitor)

        # Convert to PIL Image for processing and saving
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Check if the image is empty or black
        if img.getbbox() is None:
            raise ValueError(
                "[ERROR] Screenshot appears to be empty or completely black"
            )

    # Save the screenshot
    filename = f"monitor{monitor_index}.png"
    save_path = os.path.join(images_dir, filename)

    img.save(save_path)
    print(f"✅ Screenshot saved to: {save_path}")
    return save_path


if __name__ == "__main__":
    # Capture the first monitor (index 0)
    capture_full_screenshot(monitor_index=2)

    # To capture another monitor, change the index:
    # capture_full_screenshot(monitor_index=1)  # Second monitor
