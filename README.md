# AI Photo Booth

An AI-powered photo booth application that captures photos using a webcam, detects faces, and merges them into predefined templates for fun and creative outputs.

---

## Features
- **Live Webcam Feed**: Displays a live video feed and allows users to capture photos.
- **Face Detection**: Detects faces in the captured photo using MediaPipe.
- **Template-Based Merging**: Places detected faces into predefined templates based on the number of faces.
- **Output Generation**: Saves the final composite image to an output directory with a unique filename.

---

## How It Works
1. **Start the Application**:
   - Run the main script: `photo-main.py`.
   - The webcam feed will open, and you can press:
     - **SPACE** to capture a photo.
     - **ESC** to exit the application.

2. **Face Detection**:
   - The application detects faces in the captured photo using MediaPipe.
   - The number of detected faces determines the template to use.

3. **Template Selection**:
   - Templates (`template_X.png`) and their configurations (`template_X.json`) are loaded based on the number of faces detected.

4. **Face Merging**:
   - Detected faces are resized and placed into the corresponding slots in the template.

5. **Save Output**:
   - The final composite image is saved in the `output/` directory with a unique filename.

---

## Project Structure

AI-Photo-Booth/
├── config/
│   ├── template_1.json       # Configuration for 1-face template
│   ├── template_2.json       # Configuration for 2-face template
├── templates/
│   ├── template_1.png        # Template image for 1 face
│   ├── template_2.png        # Template image for 2 faces
├── output/                   # Directory for saving final images
├── utils/
│   ├── face_detector.py      # Face detection logic using MediaPipe
│   ├── template_loader.py    # Loads templates and configurations
│   ├── image_merger.py       # Merges faces into templates
├── photo-main.py             # Main script for the application
└── README.md                 # Project documentation

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Photo-Booth
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
```
### 3. Activate the Virtual Environment
- On Windows:
```bash
.venv\Scripts\activate
```
- On macOS/Linux:
```bash
source .venv/bin/activate
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Run the app
Run it from bash or from the IDE

## Adding new templates

### 1. Create a template image:
- Add a new template image (e.g., template_3.png) to the templates/ directory.
### 2. Define face slots:
- Create a corresponding JSON file (e.g., template_3.json) in the config/ directory.
- Define the face slot positions and sizes:
```json
[
    { "x": 100, "y": 150, "w": 200, "h": 200 },
    { "x": 400, "y": 150, "w": 200, "h": 200 }
]
```
### 3. Test the template:
- run the app and ensure the new template works as expected

## Known issues
- If no matching template is found for the number of detected faces, the program will exit with a message.
- Ensure that the templates/ and config/ directories contain valid files for the expected number of faces.

## Contributing

- Fork the repository.
- Create a new branch for your feature or bug fix:
    - from the IDE or from bash
- Commit your changes after you thoroughly checked and push the branch to your local branch and after to the origin branch

## License
This project is licensed under the MIT License. See the LICENSE file for details.

