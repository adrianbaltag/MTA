"""working - issue for textarea - just 1st row is getting extracted"""

# import logging
# import os
# import re

# import cv2
# import easyocr
# import numpy as np
# from PIL import Image


# def read_image(img_index, *keys):
#     """Reads text from an image and extracts values corresponding to the provided keys using regex.

#     Args:
#         img_index (int): The index of the image to read from.
#         *keys (str): The keys/labels to search for in the image text.

#     Returns:
#         dict: A dictionary with the provided keys and their corresponding extracted values.

#     Raises:
#         ValueError: If the index is out of range or no keys are provided.
#     """
#     # Validate if keys are provided
#     if not keys:
#         raise ValueError("No keys provided for the dictionary.")

#     # Get the path to the images folder
#     app_dir = os.path.dirname(__file__)
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#     imgs_folder = os.path.join(base_dir, "images")

#     # Get a sorted list of image files in the folder
#     image_files = sorted(
#         [
#             f
#             for f in os.listdir(imgs_folder)
#             if f.lower().endswith((".png", ".jpg", ".jpeg"))
#         ]
#     )

#     # Check if there are any images in the folder
#     if not image_files:
#         logging.error("No images found in %s", imgs_folder)
#         return None

#     # Validate index range
#     if img_index < 0 or img_index >= len(image_files):
#         logging.error(
#             "Index %d is out of range. Found %d images.", img_index, len(image_files)
#         )
#         return None

#     # Get the filename based on the index
#     img_filename = image_files[img_index]
#     img_path = os.path.join(imgs_folder, img_filename)

#     # Log the exact path the script is trying to access
#     logging.debug("Attempting to read image at path: %s", img_path)

#     # Check if file actually exists
#     if not os.path.exists(img_path):
#         logging.error("File does not exist at %s", img_path)
#         return None

#     # Try reading the image using OpenCV
#     img = cv2.imread(img_path)

#     if img is None:
#         logging.warning(
#             "OpenCV couldn't read the image. Trying Pillow (PIL) instead..."
#         )
#         try:
#             img_pil = Image.open(img_path).convert("RGB")
#             img = np.array(img_pil)
#         except (IOError, OSError) as e:
#             logging.error(
#                 "Failed to read image using both OpenCV and PIL. Details: %s", e
#             )
#             return None

#     # Convert image to grayscale for better OCR accuracy
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(["en"], gpu=True, detector=True)

#     # Read text from the image
#     result = reader.readtext(gray)

#     # Extract all text with positions
#     text_blocks = []
#     for detection in result:
#         bbox, text, confidence = detection
#         # Calculate center point of the bounding box for positional analysis
#         center_x = sum(point[0] for point in bbox) / 4
#         center_y = sum(point[1] for point in bbox) / 4
#         text_blocks.append(
#             {
#                 "text": text,
#                 "confidence": confidence,
#                 "bbox": bbox,
#                 "center_x": center_x,
#                 "center_y": center_y,
#             }
#         )

#     # Log all extracted text
#     all_text = [block["text"] for block in text_blocks]
#     logging.info(f"All extracted text: {all_text}")

#     # Sort text blocks by y-position (top to bottom) and then x-position (left to right)
#     # This helps maintain the reading order
#     text_blocks.sort(key=lambda block: (block["center_y"], block["center_x"]))

#     # Prepare the result dictionary
#     extracted_text_dict = {key: "Not found" for key in keys}

#     # Create a single string with all text to use for regex searches
#     full_text = " ".join(all_text)

#     # For each key, try to find a matching pattern and extract the value
#     for key in keys:
#         # Create pattern to look for the key followed by a value
#         # This handles formats like "First Name: John" or "First Name John"
#         pattern = rf"{re.escape(key)}(?:\s*[:;-])?\s*([^:;]*?)(?=\s*(?:{'|'.join([re.escape(k) for k in keys if k != key])})|$)"

#         match = re.search(pattern, full_text, re.IGNORECASE)
#         if match:
#             value = match.group(1).strip()
#             if value:  # Only update if we found a non-empty value
#                 extracted_text_dict[key] = value
#                 continue

#         # If regex didn't work, try proximity-based approach
#         # Find the text block that contains the key
#         key_block = None
#         for i, block in enumerate(text_blocks):
#             if re.search(rf"\b{re.escape(key)}\b", block["text"], re.IGNORECASE):
#                 key_block = block
#                 key_block_index = i
#                 break

#         # If we found the key, look for the value in the next block or nearby
#         if key_block:
#             # First check if the value is in the same text block after the key
#             value_in_same = re.search(
#                 rf"\b{re.escape(key)}\b(?:\s*[:;-])?\s*(.*)",
#                 key_block["text"],
#                 re.IGNORECASE,
#             )
#             if value_in_same and value_in_same.group(1).strip():
#                 extracted_text_dict[key] = value_in_same.group(1).strip()
#             # Otherwise check next block if it exists
#             elif key_block_index + 1 < len(text_blocks):
#                 next_block = text_blocks[key_block_index + 1]
#                 # Check if the next block is close to the key block horizontally or below it
#                 x_distance = abs(next_block["center_x"] - key_block["center_x"])
#                 y_distance = next_block["center_y"] - key_block["center_y"]

#                 if (y_distance > 0 and y_distance < 50) or (
#                     y_distance < 20 and x_distance < 150
#                 ):
#                     # This block is likely associated with the key
#                     extracted_text_dict[key] = next_block["text"].strip()

#     # Log the extracted dictionary and the filename for debugging
#     logging.info(f"Reading from: {img_filename}")
#     logging.debug(f"Extracted Text: {extracted_text_dict}")

#     return extracted_text_dict


# if __name__ == "__main__":
#     # Example usage: Reads 'text from the first image in the images folder
#     result = read_image(0, "Text area")
#     print(result)


# =======================================

import logging
import os
import re

import cv2
import easyocr
import numpy as np
from PIL import Image


def read_image(img_index, *keys):
    """Reads text from an image and extracts values corresponding to the provided keys using regex.
    Enhanced to handle multi-line text areas and form fields.

    Args:
        img_index (int): The index of the image to read from.
        *keys (str): The keys/labels to search for in the image text.

    Returns:
        dict: A dictionary with the provided keys and their corresponding extracted values.

    Raises:
        ValueError: If the index is out of range or no keys are provided.
    """
    # Validate if keys are provided
    if not keys:
        raise ValueError("No keys provided for the dictionary.")

    # Get the path to the images folder
    app_dir = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    imgs_folder = os.path.join(base_dir, "images")

    # Get a sorted list of image files in the folder
    image_files = sorted(
        [
            f
            for f in os.listdir(imgs_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )

    # Check if there are any images in the folder
    if not image_files:
        logging.error("No images found in %s", imgs_folder)
        return None

    # Validate index range
    if img_index < 0 or img_index >= len(image_files):
        logging.error(
            "Index %d is out of range. Found %d images.", img_index, len(image_files)
        )
        return None

    # Get the filename based on the index
    img_filename = image_files[img_index]
    img_path = os.path.join(imgs_folder, img_filename)

    # Log the exact path the script is trying to access
    logging.debug("Attempting to read image at path: %s", img_path)

    # Check if file actually exists
    if not os.path.exists(img_path):
        logging.error("File does not exist at %s", img_path)
        return None

    # Try reading the image using OpenCV
    # pylint: disable=no-member
    img = cv2.imread(img_path)

    if img is None:
        logging.warning(
            "OpenCV couldn't read the image. Trying Pillow (PIL) instead..."
        )
        try:
            img_pil = Image.open(img_path).convert("RGB")
            img = np.array(img_pil)
        except (IOError, OSError) as e:
            logging.error(
                "Failed to read image using both OpenCV and PIL. Details: %s", e
            )
            return None

    # Convert image to grayscale for better OCR accuracy
    # pylint: disable=no-member
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize EasyOCR reader with better text detection parameters
    reader = easyocr.Reader(["en"], gpu=True)

    # Read text from the image
    # Using standard readtext without paragraph=True to avoid structure issues
    result = reader.readtext(gray)

    # Extract all text with positions
    text_blocks = []
    for detection in result:
        # Handle different return formats safely
        if len(detection) == 3:
            bbox, text, confidence = detection
        elif len(detection) == 2:
            bbox, text = detection
            confidence = 0.9  # Default confidence if not provided
        else:
            logging.warning(f"Unexpected detection format: {detection}")
            continue

        # Calculate center point and dimensions of the bounding box
        center_x = sum(point[0] for point in bbox) / 4
        center_y = sum(point[1] for point in bbox) / 4

        # Calculate width and height of bounding box for better text area detection
        width = max(point[0] for point in bbox) - min(point[0] for point in bbox)
        height = max(point[1] for point in bbox) - min(point[1] for point in bbox)

        text_blocks.append(
            {
                "text": text,
                "confidence": confidence,
                "bbox": bbox,
                "center_x": center_x,
                "center_y": center_y,
                "width": width,
                "height": height,
            }
        )

    # Log all extracted text
    all_text = [block["text"] for block in text_blocks]
    logging.info(f"All extracted text: {all_text}")

    # Sort text blocks by y-position (top to bottom) and then x-position (left to right)
    text_blocks.sort(key=lambda block: (block["center_y"], block["center_x"]))

    # Debug log the sorted blocks with their positions
    for i, block in enumerate(text_blocks):
        logging.debug(
            f"Block {i}: {block['text']} at x={block['center_x']:.1f}, y={block['center_y']:.1f}, w={block['width']:.1f}, h={block['height']:.1f}"
        )

    # Prepare the result dictionary
    extracted_text_dict = {key: "Not found" for key in keys}

    # Try to identify text areas based on layout
    # For text areas, we want to find multi-line blocks or group of blocks that appear to be a form field

    # Attempt to manually group blocks by their spatial relationship
    grouped_blocks = []
    current_group = []
    last_y = -1
    y_threshold = 30  # Maximum vertical gap to consider blocks part of the same group

    # Group text blocks that are closely positioned vertically
    for block in text_blocks:
        if last_y == -1 or (block["center_y"] - last_y) <= y_threshold:
            current_group.append(block)
        else:
            if current_group:
                grouped_blocks.append(current_group)
            current_group = [block]
        last_y = block["center_y"]

    # Add the last group if it exists
    if current_group:
        grouped_blocks.append(current_group)

    # Create a full text string that preserves some layout information
    layout_text = ""
    for group in grouped_blocks:
        group_text = " ".join(block["text"] for block in group)
        layout_text += group_text + "\n"

    # Log the layout-preserved text
    logging.debug(f"Layout-preserved text:\n{layout_text}")

    # For each key, try to find a matching pattern and extract the value
    for key in keys:
        # Create the key pattern, allowing for variations in spacing
        key_pattern = re.escape(key).replace("\\ ", "\\s+")

        # First try: look for the key in the layout text
        layout_pattern = rf"{key_pattern}(?:\s*[:;-])?\s*(.*?)(?:\n\n|\n(?:{'|'.join([re.escape(k).replace('\\ ', '\\s+') for k in keys if k != key])})|$)"
        layout_match = re.search(layout_pattern, layout_text, re.IGNORECASE | re.DOTALL)

        if layout_match:
            value = layout_match.group(1).strip()
            if value:
                extracted_text_dict[key] = value
                continue

        # Second try: find the key block and then locate related value blocks
        key_block_idx = -1
        for i, block in enumerate(text_blocks):
            if re.search(rf"\b{key_pattern}\b", block["text"], re.IGNORECASE):
                key_block_idx = i
                break

        if key_block_idx >= 0:
            key_block = text_blocks[key_block_idx]

            # Try to extract value from the same block
            value_in_same = re.search(
                rf"\b{key_pattern}\b(?:\s*[:;-])?\s*(.*)",
                key_block["text"],
                re.IGNORECASE,
            )
            if value_in_same and value_in_same.group(1).strip():
                extracted_text_dict[key] = value_in_same.group(1).strip()
                continue

            # Look for value blocks below and slightly to the right of the key block
            value_blocks = []

            # Define the region where we expect to find the value
            # For a text area, we expect it to be below the label and within a reasonable horizontal range
            x_min = key_block["center_x"] - 50
            x_max = key_block["center_x"] + 200
            y_min = key_block["center_y"] + 5
            y_max = y_min + 200  # Look up to 200 pixels down

            for i in range(key_block_idx + 1, len(text_blocks)):
                block = text_blocks[i]

                # Skip blocks that contain other keys
                if any(
                    re.search(rf"\b{re.escape(k)}\b", block["text"], re.IGNORECASE)
                    for k in keys
                ):
                    continue

                # Check if this block is positioned in our expected value region
                if (
                    y_min <= block["center_y"] <= y_max
                    and x_min <= block["center_x"] <= x_max
                ):
                    value_blocks.append(block)

            # Sort value blocks by vertical position to preserve order
            value_blocks.sort(key=lambda b: b["center_y"])

            # Combine all value blocks into a single string
            if value_blocks:
                combined_value = "\n".join(block["text"] for block in value_blocks)
                extracted_text_dict[key] = combined_value.strip()
                continue

            # If still no value found, just try the next block as a fallback
            if key_block_idx + 1 < len(text_blocks):
                next_block = text_blocks[key_block_idx + 1]
                extracted_text_dict[key] = next_block["text"].strip()

    # Log the extracted dictionary and the filename for debugging
    logging.info(f"Reading from: {img_filename}")
    logging.debug(f"Extracted Text: {extracted_text_dict}")

    return extracted_text_dict


if __name__ == "__main__":
    # Example usage: Reads text from the first image in the images folder
    result = read_image(3, "First name", "Last name", "Job title")
    print(result)
