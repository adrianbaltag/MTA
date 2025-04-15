"""This script holds the logic for the nsp application."""

from my_package.utils.classes import ScreenshotUtility

# Create the tool
screenshot_tool = ScreenshotUtility()

# Take a screenshot that includes both words
saved_picture, picture_location = screenshot_tool.capture_area_by_multiple_text(
    [
        "Top Most Used Carriers (4G)",
        "Last used (UTC)",
    ]
)

# The tool will tell you where it saved the picture
print(f"I saved your picture at: {saved_picture}")
