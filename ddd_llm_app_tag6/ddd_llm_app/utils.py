import logging
import os
from datetime import datetime

# Create a module-specific logger
logger = logging.getLogger(__name__)

def read_file(filename: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    Args:
        filename (str): The name of the file to read.

    Returns:
        str: The content of the file.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Template file '{filename}' not found.")
    with open(filename, "r") as file:
        return file.read()


def save_text_with_timestamp(text: str, filename: str, directory: str = ".") -> str:
    """
    Saves the given text to a file, appending a timestamp to the filename.

    Args:
        text (str): The content to save.
        filename (str): The base filename (without timestamp).
        directory (str): The directory where the file will be saved. Defaults to the current directory.

    Returns:
        str: The full path to the saved file.
    """
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Append the timestamp to the filename before the extension
    name, ext = os.path.splitext(filename)
    timestamped_filename = f"{name}_{timestamp}{ext}"

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Construct the full file path
    filepath = os.path.join(directory, timestamped_filename)

    # Write the text to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)

    return filepath

def get_domain_descrription_fullpath(template_dir: str, filename: str) -> str:
    return os.path.expanduser(os.path.join(template_dir, 'templates', filename))

def get_template_fullpath(template_dir: str, filename: str) -> str:
    return os.path.expanduser(os.path.join(template_dir, 'templates', filename))