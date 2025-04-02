import cv2  
import json  


def load_template(template_path: str, config_path: str):
    """
    Loads a template image and corresponding face slot configuration.

    Args:
        template_path (str): Path to the template image.
        config_path (str): Path to the JSON config file with face slot definitions.

    Returns:
        tuple: (template_image, face_slots), where:
            - template_image is a np.ndarray (BGR image)
            - face_slots is a list of dicts, each with keys like 'x', 'y', 'w', 'h'
    """

    # Load the image template from the given file path
    # OpenCV loads images as BGR by default
    template_image = cv2.imread(template_path)
    if template_image is None:
        # If the image failed to load, raise a clear error
        raise FileNotFoundError(f"Template image not found at {template_path}")

    # Open the JSON configuration file that defines face slot positions
    with open(config_path, 'r') as f:
        face_slots = json.load(f)  # Parse JSON content into a Python object (list of dicts)

    # Ensure that the JSON file is a list (each element representing a face slot)
    if not isinstance(face_slots, list):
        raise ValueError("Template config must be a list of face slot dictionaries")

    # Validate that each face slot contains the expected keys: x, y, w, h
    for slot in face_slots:
        if not all(k in slot for k in ('x', 'y', 'w', 'h')):
            raise ValueError("Each face slot must contain 'x', 'y', 'w', and 'h' keys")

    # Return the loaded image and the validated slot definitions
    return template_image, face_slots
