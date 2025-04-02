import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Face Detection module
mp_face_detection = mp.solutions.face_detection

class FaceDetector:
    def _init_(self, method: str ="mediapipe"):
        self.method = method.lower() # Store the detectopm method as a lowercase string
        if self.method == "mediapipe":
            # Initialize MediaPipe Face Detection module
            self.detector = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        else:
            raise NotImplementedError(f"Face detection method '{self.method}' is not implemented.")
        

    def detect_faces(self, image: np.ndarray) -> list:
        # Dispatch to the appropiate internal method based on selected detection backend

        if self.method == "mediapipe":
             return self.detect_faces_mediapipe(image)
        else:
            raise NotImplementedError(f"Face detection method '{self.method}' is not implemented.")
        
    def _detect_faces_mediapipe(self, image: np.ndarray) -> list:
        face_images = []  # List to store detected face images

        # Convert BGR to RGB as required by MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.detector.process(rgb_image)

        if results.detections:
            h, w, _ = image.shape  # Get the height and width of the image
            for detection in results.detections:
                # Get relative bounding box from detection result
                bbox = detection.location_data.relative_bounding_box
                # Calculate absolute bounding box coordinates
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                # Add margin around the bounding box   
                margin = 0.1  # Adjust this value to increase/decrease the margin
                x1 = max(0, x1 - int(margin * width))
                y1 = max(0, y1 - int(margin * height))
                x2 = min(w, x1 + int((1 + 2 * margin) * width))
                y2 = min(h, y1 + int(( 1 + 2 * margin) * height))

                # Extract the face image using the bounding box coordinates
                face_crop = image[y1:y2, x1:x2]
                face_images.append(face_crop)

        return face_images  # Return the list of detected face images

    def detect_faces(image: np.ndarray) -> list: 
        """
    Abstracted detection interface. This function can be called directly from outside
    the module to detect faces using the default method.
    """
        detector = FaceDetector(method="mediapipe")
        return detector.detect_faces(image)
        