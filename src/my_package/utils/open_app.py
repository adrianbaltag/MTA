# """This script open a new tab in the browser, based on the url provided from config.py"""

# import time
# import webbrowser

# # import the URLs from config.py
# from my_package.utils.config import URL_FORMY


# def open_app(url):
#     """__summary__:
#     This function opens a new tab in the default web browser with the provided URL.
#     """
#     # Open the URL in the default web browser
#     webbrowser.open(url)
#     time.sleep(1)  # Wait for the browser to open

"""below is working open browser on selected monitor, but not maximized"""

# if __name__ == "__main__":
# #     open_app(URL_FORMY)
# """This script opens a new browser window on a specific monitor based on the url and monitor index provided."""

# import os
# import subprocess
# import time
# import webbrowser
# from typing import Optional

# # import the URLs from config.py
# from my_package.utils.config import URL_FORMY


# def open_app(url: str, monitor_index: Optional[int] = None, maximize: bool = True):
#     """
#     Open a new browser window on a specific monitor with the provided URL.
#     Windows-only implementation.

#     Args:
#         url: The URL to open in the browser.
#         monitor_index: The index of the monitor to open the browser on (0-based).
#                       If None, opens on the default/primary monitor.
#         maximize: Whether to maximize the browser window.
#     """
#     if monitor_index is None:
#         # Fall back to default behavior if no monitor index is specified
#         webbrowser.open_new(url)
#         time.sleep(1)
#         return

#     try:
#         # Get monitor information using PowerShell
#         ps_command = """
#         Add-Type -AssemblyName System.Windows.Forms;
#         [System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
#             $_.Bounds.X.ToString() + "," + $_.Bounds.Y.ToString() + "," +
#             $_.Bounds.Width.ToString() + "," + $_.Bounds.Height.ToString()
#         }
#         """
#         result = subprocess.check_output(
#             ["powershell", "-Command", ps_command], text=True
#         )
#         monitor_info = [line.strip() for line in result.splitlines() if line.strip()]

#         print(f"Detected {len(monitor_info)} monitors.")
#         for i, monitor in enumerate(monitor_info):
#             print(f"Monitor {i}: {monitor}")

#         if monitor_index < 0 or monitor_index >= len(monitor_info):
#             raise ValueError(
#                 f"Monitor index {monitor_index} out of range. Available monitors: 0-{len(monitor_info) - 1}"
#             )

#         # Parse monitor positions
#         x, y, width, height = map(int, monitor_info[monitor_index].split(","))
#         print(
#             f"Using monitor {monitor_index} with position: x={x}, y={y}, width={width}, height={height}"
#         )

#         # Create a temporary PowerShell script that will open Chrome and position it
#         temp_script = os.path.join(
#             os.environ.get("TEMP", "."), "open_chrome_on_monitor.ps1"
#         )

#         with open(temp_script, "w") as f:
#             f.write(f"""
#             # Create a new Chrome process
#             Start-Process "chrome.exe" -ArgumentList "--new-window", "{url}" -PassThru | Out-Null

#             # Give it a moment to start
#             Start-Sleep -Seconds 1

#             # Get the newest Chrome window
#             $chromeWindows = Get-Process chrome | Where-Object {{$_.MainWindowHandle -ne 0}}

#             # Get the newest window (assuming it's the one we just opened)
#             $targetWindow = $chromeWindows | Sort-Object StartTime -Descending | Select-Object -First 1

#             if ($targetWindow) {{
#                 # Add the required Windows API functions
#                 Add-Type @"
#                 using System;
#                 using System.Runtime.InteropServices;

#                 public class Win32 {{
#                     [DllImport("user32.dll")]
#                     [return: MarshalAs(UnmanagedType.Bool)]
#                     public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);

#                     [DllImport("user32.dll")]
#                     public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

#                     // Constants for ShowWindow
#                     public const int SW_MAXIMIZE = 3;
#                 }}
# "@
#                 # Calculate position - center on target monitor
#                 $x = {x} + 50
#                 $y = {y} + 50
#                 $w = {width} - 100
#                 $h = {height} - 100

#                 # Constants
#                 $HWND_TOP = New-Object IntPtr 0
#                 $SWP_SHOWWINDOW = 0x0040

#                 # Move and resize the window
#                 [Win32]::SetWindowPos($targetWindow.MainWindowHandle, $HWND_TOP, $x, $y, $w, $h, $SWP_SHOWWINDOW)

#                 # If maximize is requested, maximize the window
#                 {"# " if not maximize else ""}[Win32]::ShowWindow($targetWindow.MainWindowHandle, [Win32]::SW_MAXIMIZE)

#                 Write-Host "Successfully positioned Chrome window on monitor {monitor_index}"
#             }} else {{
#                 Write-Host "Could not find Chrome window to position"
#             }}
#             """)

#         # Execute the PowerShell script
#         print("Executing PowerShell script to position Chrome window...")
#         ps_process = subprocess.Popen(
#             ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_script],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#         )
#         stdout, stderr = ps_process.communicate()

#         print(f"PowerShell output: {stdout}")
#         if stderr:
#             print(f"PowerShell errors: {stderr}")

#         # Clean up the temporary script
#         try:
#             os.remove(temp_script)
#         except:
#             pass

#     except Exception as e:
#         print(f"Error positioning browser: {e}")
#         # Fallback to default browser with new window
#         webbrowser.open_new(url)

#     time.sleep(1)  # Wait for the browser to open


# if __name__ == "__main__":
#     # Example: Open on the first monitor (index 0) and maximize the window
#     open_app(URL_FORMY, monitor_index=1, maximize=True)

#     # To open on the second monitor without maximizing:
#     # open_app(URL_FORMY, monitor_index=1, maximize=False)

import subprocess
import time

import screeninfo
from pywinauto import findwindows
from pywinauto.application import Application

from my_package.utils.config import URL_FORMY


def open_app(url, index=None):
    """__summary__:
    This function opens a new browser window on a specific monitor with the provided URL.
    Windows-only implementation.
    args:
        url: The URL to open in the browser.
        index: The index of the monitor to open the browser on (0-based).
    """
    monitors = screeninfo.get_monitors()

    for i, monitor in enumerate(monitors):
        print(
            f"Monitor {i}: X={monitor.x}, Y={monitor.y}, Width={monitor.width}, Height={monitor.height}"
        )

    # Adjust based on setup (2 = left monitor - home setup)
    target_monitor_index = index
    target_monitor = monitors[target_monitor_index]

    # Open Chrome in a new window
    try:
        subprocess.Popen(
            [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                url,
                "--new-window",
            ]
        )
    except FileNotFoundError:
        print("Chrome not found, trying default browser.")
        subprocess.Popen(["start", "chrome", url, "--new-window"], shell=True)

    time.sleep(5)  # Wait for the browser to appear (increased sleep time)

    try:
        # Wait for the Chrome window to appear
        chrome_window = None
        for _ in range(10):  # Try up to 10 times (with 1-second intervals)
            # Look for windows with "Chrome" in the title
            windows = findwindows.find_windows(title_re=".*Chrome.*")
            if windows:
                chrome_window = windows[0]
                break
            time.sleep(1)

        if chrome_window:
            # Connect to the Chrome window using its handle
            app = Application().connect(handle=chrome_window)
            window = app.top_window()  # Get the top window (first Chrome window)

            if window:
                # Restore window in case it is minimized !!!!
                window.restore()

                # Move the browser window to the left monitor
                window.move_window(
                    target_monitor.x,
                    target_monitor.y,
                    width=target_monitor.width,
                    height=target_monitor.height,
                )

                #  bring the window to the foreground
                window.set_focus()

            time.sleep(1)  # Give it a second
        else:
            print("No Chrome window found after several attempts.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    open_app(URL_FORMY, index=2)
