from utils.template_loader import load_template
from utils.face_detector import detect_faces_default
from utils.image_merger import merge_faces_with_template
import cv2
import os
from datetime import datetime
import uuid


def wait_for_trigger():
    """
    Wait for a trigger event (e.g., SPACE key) while allowing the live feed to update.
    """
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to cancel
        return "EXIT"
    elif key == 32:  # SPACE key to trigger
        return "TRIGGERED"
    return None


cap = cv2.VideoCapture(0)  # Initialize webcam
print("Press SPACE to take a photo, or ESC to cancel.")

image = None  # Initialize the image variable

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame from webcam")
        break  # Exit the loop if frame wasn't captured

    cv2.imshow("Live Feed", frame)  # Show live video feed to the user

    trigger = wait_for_trigger()
    if trigger == "TRIGGERED":
        # Countdown before taking photo
        for i in range(5, 0, -1):
            start_time = datetime.now()
            while (datetime.now() - start_time).seconds < 1:  # Loop for 1 second
                ret, frame = cap.read()  # Continuously capture new frames
                if not ret:
                    print("Failed to grab frame during countdown")
                    break
                countdown_frame = frame.copy()  # Clone the current frame for overlay
                cv2.putText(countdown_frame, f"{i}", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 5)
                cv2.imshow("Live Feed", countdown_frame)
                cv2.waitKey(1)  # Allow the live feed to update

        ret, frame = cap.read()  # Capture the final frame
        if ret:
            image = frame.copy()  # Save the captured frame
        break
    elif trigger == "EXIT":
        print("Exiting...")
        image = None  # Ensure no image is processed
        break

cap.release()
cv2.destroyAllWindows()

if image is not None:
    all_faces = detect_faces_default(image)  # Detect all faces
    num_faces = len(all_faces)
    print(f"Detected {num_faces} face(s)")

    config_path = f"config/template_{num_faces}.json"
    template_path = f"templates/template_{num_faces}.png"

    if not os.path.exists(config_path) or not os.path.exists(template_path):
        print("No matching template found for the number of faces detected.")
        exit()

    template_image, face_slots = load_template(template_path, config_path)  # Load the template and metadata for the face slots

    face_images = all_faces[:len(face_slots)]  # Truncate extra faces if any

    final_image = merge_faces_with_template(template_image, face_images, face_slots)  # Merge detected faces with the template

    # Save the final composite image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    filename = f"photo_{timestamp}_{unique_id}.png"  # Construct unique filename
    output_path = os.path.join("output", filename)  # Combine path and filename
    os.makedirs("output", exist_ok=True)
    cv2.imwrite(output_path, final_image)  # Write the image to disk
    print(f"Image saved to {output_path}")
else:
    print("No photo was taken.")