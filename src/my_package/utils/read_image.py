# pylint:disable=W0012
# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name, too-many-branches, too-many-locals, too-many-statements, broad-except
import os

import cv2
import easyocr


def read_image(img_index: int) -> dict:
    """
    Read an image by its index and return the extracted text as a dictionary.

    Args:
        img_index: The index of the image to read

    Returns:
        A dictionary with paragraph numbers as keys and extracted text as values
    """
    # Get the current script directory
    current_dir = os.path.dirname(__file__)

    # Go up one level to the parent directory where the img_to_read folder is located
    parent_dir = os.path.dirname(current_dir)

    # Define the image folder path
    img_folder = os.path.join(parent_dir, "img_to_read")

    # Get all image files from the folder
    image_files = [
        f for f in os.listdir(img_folder) if f.endswith((".png", ".jpg", ".jpeg"))
    ]

    # Sort the images to ensure consistent indexing
    image_files.sort()

    # Get the image path based on the index
    if img_index < 0 or img_index >= len(image_files):
        raise ValueError(
            f"Image index out of range. Valid range: 0-{len(image_files) - 1}"
        )

    img_path = os.path.join(img_folder, image_files[img_index])

    # Create an EasyOCR reader instance with English language support and GPU acceleration
    reader = easyocr.Reader(["en"], gpu=True)

    # Read the image using OpenCV
    # pylint: disable=E1101   --> # ignore the warning about the image not being in RGB format
    img = cv2.imread(img_path)

    # Use EasyOCR to read the text from the image
    result = reader.readtext(img, detail=0, paragraph=True)

    # Create a dictionary with paragraph numbers as keys and text as values
    result_dict = {f"paragraph_{i + 1}": text for i, text in enumerate(result)}
    print(result_dict)
    return result_dict


if __name__ == "__main__":
    read_image(3)
