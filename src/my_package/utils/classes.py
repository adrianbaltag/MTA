"""This module contains utility class for the screenshots - selected parts of the initial screenshot."""

import argparse
import os
from datetime import datetime

import cv2
import easyocr
import numpy as np
import pyautogui


class ScreenshotUtility:
    """__Utility class for taking screenshots and processing them with OCR
    This class provides methods to take screenshots, find areas by text, and save images.
    """

    def __init__(self, output_folder=None, language="en"):
        """Initialize the screenshot utility with output folder and language"""
        # Set default output folder if none provided
        # If no output folder is provided, use the 'images' folder in the project
        if output_folder is None:
            # Get the current file's directory (utils folder)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the package root
            package_root = os.path.dirname(current_dir)
            # Set path to the images folder
            self.output_folder = os.path.join(package_root, "images")
        else:
            self.output_folder = output_folder

        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

        # Initialize OCR reader
        self.reader = easyocr.Reader([language])
        print(f"Initialized EasyOCR with language: {language}")

    def take_screenshot(self, region=None):
        """
        Take a screenshot of the entire screen or a specific region
        region: Optional tuple (left, top, width, height)
        """
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        # Convert to numpy array (for OpenCV compatibility)
        screenshot_np = np.array(screenshot)
        # Convert RGB to BGR (OpenCV format)
        # pylint: disable=E1101
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        return screenshot_bgr

    def find_area_by_text(
        self, image, target_text, confidence=0.5, area_expansion=(100, 50, 100, 50)
    ):
        """
        Locate an area containing specific text in a screenshot

        Args:
            image: The screenshot as a numpy array
            target_text: Text to search for (case insensitive)
            confidence: Minimum confidence threshold for OCR (0-1)
            area_expansion: Tuple (left, top, right, bottom) pixels to expand from the text

        Returns:
            Tuple (x_min, y_min, x_max, y_max) coordinates of the area
        """
        # Run OCR on the image
        results = self.reader.readtext(image)

        # Search for the target text in OCR results
        matches = []
        for bbox, text, prob in results:
            if target_text.lower() in text.lower() and prob > confidence:
                matches.append((bbox, text, prob))
                print(f"Found text '{text}' with confidence {prob:.2f}")

        if not matches:
            raise ValueError(f"Could not find text '{target_text}' in the screenshot")

        # Sort matches by confidence level (highest first)
        matches.sort(key=lambda x: x[2], reverse=True)
        best_match = matches[0]
        target_coordinates = best_match[0]

        # Calculate the area boundaries with expansion
        left_exp, top_exp, right_exp, bottom_exp = area_expansion

        x_min = max(0, int(target_coordinates[0][0]) - left_exp)
        y_min = max(0, int(target_coordinates[0][1]) - top_exp)
        x_max = min(image.shape[1], int(target_coordinates[2][0]) + right_exp)
        y_max = min(image.shape[0], int(target_coordinates[2][1]) + bottom_exp)

        return (x_min, y_min, x_max, y_max)

    def find_area_by_multiple_text(self, image, text_markers, confidence=0.5):
        """
        Find an area that encompasses multiple text markers

        Args:
            image: The screenshot as a numpy array
            text_markers: List of strings to search for
            confidence: Minimum confidence threshold for OCR

        Returns:
            Tuple (x_min, y_min, x_max, y_max) coordinates of the combined area
        """
        # Run OCR just once for efficiency
        results = self.reader.readtext(image)

        # Find all matching text markers
        all_matches = []
        for marker in text_markers:
            marker_matches = []
            for bbox, text, prob in results:
                if marker.lower() in text.lower() and prob > confidence:
                    marker_matches.append((bbox, text, prob))

            if marker_matches:
                # Get the best match for this marker
                best_match = max(marker_matches, key=lambda x: x[2])
                all_matches.append(best_match)
                print(
                    f"Found marker '{marker}' as '{best_match[1]}' with confidence {best_match[2]:.2f}"
                )
            else:
                print(f"Warning: Could not find marker '{marker}'")

        if not all_matches:
            raise ValueError(
                "Could not find any of the specified text markers in the screenshot"
            )

        # Calculate the combined bounding box that encompasses all matches
        all_coords = [match[0] for match in all_matches]
        all_points = [point for coords in all_coords for point in coords]

        # Find min/max coordinates
        x_values = [p[0] for p in all_points]
        y_values = [p[1] for p in all_points]

        x_min = max(0, int(min(x_values)) - 100)
        y_min = max(0, int(min(y_values)) - 50)
        x_max = min(image.shape[1], int(max(x_values)) + 100)
        y_max = min(image.shape[0], int(max(y_values)) + 100)

        return (x_min, y_min, x_max, y_max)

    def extract_area(self, image, coordinates):
        """Extract a portion of the image based on coordinates"""
        x_min, y_min, x_max, y_max = coordinates
        area_image = image[y_min:y_max, x_min:x_max]
        return area_image

    def save_image(self, image, prefix="area"):
        """Save an image to the output folder with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = os.path.join(self.output_folder, filename)
        # pylint: disable=E1101
        cv2.imwrite(filepath, image)
        print(f"Saved image to {filepath}")
        return filepath

    def capture_area_by_text(
        self,
        target_text,
        area_expansion=(100, 50, 100, 50),
        full_screen=True,
        region=None,
        save_full=False,
        confidence=0.5,
    ):
        """
        Capture a specific area identified by nearby text

        Args:
            target_text: Text to search for
            area_expansion: How much to expand around the text (left, top, right, bottom)
            full_screen: Whether to take a full screen screenshot
            region: Region to screenshot if not full screen (left, top, width, height)
            save_full: Whether to save the full screenshot
            confidence: Minimum OCR confidence

        Returns:
            Path to the saved area image
        """
        # Take initial screenshot
        print("Taking screenshot...")
        full_image = self.take_screenshot(region=region if not full_screen else None)

        # Save full screenshot if requested
        if save_full:
            self.save_image(full_image, prefix="full")

        # Find the area coordinates
        print(f"Looking for text '{target_text}'...")
        area_coords = self.find_area_by_text(
            full_image,
            target_text,
            confidence=confidence,
            area_expansion=area_expansion,
        )
        print(f"Found area at coordinates: {area_coords}")

        # Extract and save the area image
        area_image = self.extract_area(full_image, area_coords)
        saved_path = self.save_image(area_image)

        return saved_path, area_coords

    def capture_area_by_multiple_text(
        self, text_markers, save_full=False, confidence=0.7
    ):
        """
        Capture an area that encompasses multiple text markers

        Args:
            text_markers: List of text strings to search for
            save_full: Whether to save the full screenshot
            confidence: Minimum OCR confidence

        Returns:
            Path to the saved area image and the coordinates
        """
        # Take full screenshot
        print("Taking full screenshot...")
        full_image = self.take_screenshot()

        # Save full screenshot if requested
        if save_full:
            self.save_image(full_image, prefix="full")

        # Find area encompassing all text markers
        print(f"Looking for text markers: {text_markers}...")
        area_coords = self.find_area_by_multiple_text(
            full_image, text_markers, confidence
        )
        print(f"Found combined area at coordinates: {area_coords}")

        # Extract and save the area image
        area_image = self.extract_area(full_image, area_coords)
        saved_path = self.save_image(area_image, prefix="multi_area")

        return saved_path, area_coords


def main():
    """Example usage of the ScreenshotUtility class"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Dynamic Screenshot Utility")
    parser.add_argument("--text", type=str, help="Text to search for")
    parser.add_argument(
        "--multi", nargs="+", help="Multiple text markers to search for"
    )
    parser.add_argument("--output", type=str, help="Output folder path")
    parser.add_argument(
        "--save-full", action="store_true", help="Save the full screenshot"
    )
    parser.add_argument(
        "--expand",
        nargs=4,
        type=int,
        default=[100, 50, 100, 50],
        help="Area expansion (left top right bottom)",
    )
    args = parser.parse_args()

    # Create the utility
    util = ScreenshotUtility(output_folder=args.output)

    try:
        if args.multi:
            # Use multiple text markers
            saved_path, coords = util.capture_area_by_multiple_text(
                args.multi, save_full=args.save_full
            )
        elif args.text:
            # Use single text marker
            saved_path, coords = util.capture_area_by_text(
                args.text, area_expansion=tuple(args.expand), save_full=args.save_full
            )
        else:
            print("Error: Either --text or --multi argument is required")
            return

        print("Process completed successfully!")
        print(f"Area coordinates: {coords}")
        print(f"Saved to: {saved_path}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
