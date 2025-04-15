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
    print(result)

    ticket_number = "Trouble-ID"
    try:
        # Find the index of the element in the result list
        index = result.index(ticket_number)
        # print(f"Element '{ticket_number}' found at index: {index}")
    except ValueError:
        print(f"Element '{ticket_number}' not found in the result list.")
    ticket = result[index + 1]
    print(f"Ticket number: {ticket}")

    cx_mdn = "MDN"
    try:
        # Find the index of the element in the result list
        index = result.index(cx_mdn)
        # print(f"Element '{cx_mdn}' found at index: {index}")
    except ValueError:
        print(f"Element '{cx_mdn}' not found in the result list.")
    mdn = result[index + 1]
    print(f"MDN: {mdn}")

    prob_desc = "Problem Description"
    try:
        # Find the index of the element in the result list
        index = result.index(prob_desc)
        # print(f"Element '{prob_desc}' found at index: {index}")
    except ValueError:
        print(f"Element '{prob_desc}' not found in the result list.")
    issue = result[index + 1]
    print(f"Problem description: {issue}")
    # # Create a dictionary with paragraph numbers as keys and text as values

    return ticket, mdn, issue


if __name__ == "__main__":
    read_image(1)
