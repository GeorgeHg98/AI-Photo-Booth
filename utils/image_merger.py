import cv2
import numpy as np

def merge_faces_with_template(template_image: np.ndarray, face_images: list, face_slots: list) -> np.ndarray:
        """
    Places cropped face images into the corresponding slots of a template image.

    Args:
        template_image (np.ndarray): The background image where faces are placed.
        face_images (list): List of face images (np.ndarray) to place into the template.
        face_slots (list): List of dicts defining where to place each face. Each dict must have 'x', 'y', 'w', 'h'.

    Returns:
        np.ndarray: The final composed image with all faces placed on the template.
    """
        
        final_image = template_image.copy()  #  Clone the template image to avoid modifying the original

        for i, (face_img, slot) in enumerate(zip(face_images, face_slots)):
            # Resize the face image to fit the slot dimensions
            resized_face = cv2.resize(face_img, (slot['w'], slot['h']))

            # Compute the region of interest (ROI) in the final image
            x, y = slot['x'], slot['y']
            h, w = slot['h'], slot['w']

            # Overlay the face on the ROI of the template image
            final_image[y:y+h, x:x+w] = resized_face

        return final_image  