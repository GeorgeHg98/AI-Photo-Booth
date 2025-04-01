from utils.template_loader import load_template
from utils.face_detector import detect_faces
from utils.image_merger import merge_faces_with_template
import cv2 # For image processing and webcam access
import os  # For image processing and webcam access
from datetime import datetime  # For timestamping filenames
import uuid  # For generating unique IDs


def wait_for_trigger():
    # Default implementation: wait for SPACE key
    # Replace this later with GPIO or another trigger for a real photo booth
    while True:
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to cancel
            return None
        elif key == 32:  # SPACE key to trigger
            return "TRIGGERED"
        

cap = cv2.VideoCapture(0)  # Initialize webcam
print("Press SPACE to take a photo, or ESC to cancel.")

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame from webcam")
        break  # Exit the loop if frame wasn't captured

    cv2.imshow("Live Feed", frame)  # Show live video feed to the user

    trigger = wait_for_trigger()
    if trigger == "TRIGGERED":
        # Countdown before taking photo
        for i in range(5, 0, -1):  # Countdown from 5 seconds
            countdown_frame = frame.copy()  # Clone current frame for overlay
            cv2.putText(countdown_frame, f"{i}", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 5)
            cv2.imshow("Live Feed", countdown_frame)
            cv2.waitKey(1000) 

        ret, frame = cap.read()  # Capture the final frame    
        image = frame.copy()  # Capture the current frame
        break
    elif trigger is None:
        cap.release()  # Release the webcam resource
        cv2.destroyAllWindows()  # Close all OpenCV windows
        exit()

cap.release()  # Release the webcam resource
cv2.destroyAllWindows()  # Close all OpenCV windows

all_faces = detect_faces(image)  # Detect all faces
num_faces = len(all_faces)
print(f"Detected {num_faces} face(s)")

config_path = f"config/template_{num_faces}.json"
template_path = f"templates/template_{num_faces}.png"

if not os.path.exists(config_path) or not os.path.exists(template_path):
    print("No matching template found for the number of faces detected.")
    exit()

template_image, face_slots = load_template(template_path, template_path)  # Load the template and metadata for the face slots

face_images = all_faces[:len(face_slots)]  # Truncate extra faces if any

final_image = merge_faces_with_template(template_image, face_images, face_slots)  # Merge detected faces with the template

#Save the final composite image
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
unique_id = uuid.uuid4().hex[:6]  # Short unique identifier
filename = f"photo_{timestamp}_{unique_id}.png"  # Construct unique filename
output_path = os.path.join("output", filename)  # Combine path and filename
os.makedirs("output", exist_ok=True)  # Ensure output directory exists
cv2.imwrite(output_path, final_image)  # Write the image to disk
print(f"Image saved to {output_path}")  # Notify the user