# ============================================================
# MODULE 4: emotion_detection.py
# PURPOSE: Detect face from webcam and guess basic emotion
#          Uses OpenCV — no heavy model training needed!
# ============================================================

import cv2        # OpenCV for webcam and face detection
import time
import os

# -------------------------------------------------------
# Path to OpenCV's built-in face detector model file.
# This file comes with OpenCV — no download needed!
# -------------------------------------------------------
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def detect_emotion(capture_duration=5):
    """
    Opens the webcam, captures frames for `capture_duration` seconds,
    detects if a face is visible, and returns a basic emotion label.

    Emotion logic (simplified):
    - Face clearly visible + stable = "Confident / Neutral"
    - Face detected but small/far = "Nervous"
    - No face detected = "Not Visible"
    - Camera error = "Unknown"

    Returns:
        (str) Emotion label
        (int) Emotion score out of 20
    """

    print(f"\n📷 Opening webcam for {capture_duration} seconds...")
    print("   Please look at the camera naturally.\n")

    # Load OpenCV's face detector
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    if face_cascade.empty():
        print("⚠️  Face detector model not found. Using default emotion.")
        return "Neutral", 12

    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("⚠️  Webcam not accessible. Skipping emotion detection.")
        return "Unknown", 10  # Default score

    face_sizes = []        # Store detected face sizes
    frames_with_face = 0   # Count frames where a face was found
    total_frames = 0       # Count all frames processed

    start_time = time.time()

    while time.time() - start_time < capture_duration:
        ret, frame = cap.read()  # Read one frame from webcam

        if not ret:
            break  # Stop if camera fails

        total_frames += 1

        # Convert frame to grayscale (face detection works on grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        # scaleFactor: how much image is reduced per scale
        # minNeighbors: how many detections needed to confirm a face
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)  # Minimum face size in pixels
        )

        if len(faces) > 0:
            frames_with_face += 1
            # Store width of detected face (larger = closer/more confident)
            for (x, y, w, h) in faces:
                face_sizes.append(w)

            # Draw rectangle around face on screen
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Show the webcam window
        cv2.imshow("Emotion Detection - Press Q to quit early", frame)

        # Allow early exit with Q key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release webcam and close window
    cap.release()
    cv2.destroyAllWindows()

    # ---- Decide emotion based on face data ----
    emotion, score = _analyze_face_data(frames_with_face, total_frames, face_sizes)

    print(f"\n😊 Emotion Detection Result:")
    print(f"   Frames with face: {frames_with_face}/{total_frames}")
    print(f"   Detected Emotion: {emotion}")
    print(f"   Emotion Score:    {score}/20")

    return emotion, score


def _analyze_face_data(frames_with_face, total_frames, face_sizes):
    """
    Internal helper: Interprets face detection stats into emotion + score.
    """
    if total_frames == 0:
        return "Unknown", 10

    # Percentage of time face was visible
    presence_ratio = frames_with_face / total_frames

    # Average face size (bigger = closer to camera = more confident)
    avg_face_size = sum(face_sizes) / len(face_sizes) if face_sizes else 0

    if presence_ratio >= 0.7 and avg_face_size >= 150:
        return "Confident", 18
    elif presence_ratio >= 0.7 and avg_face_size >= 80:
        return "Neutral", 15
    elif presence_ratio >= 0.4:
        return "Nervous", 10
    elif presence_ratio > 0:
        return "Distracted", 7
    else:
        return "Not Visible", 5


# ---- Quick Test ----
if __name__ == "__main__":
    emotion, score = detect_emotion(capture_duration=5)
    print(f"\n[Test] Emotion: {emotion}, Score: {score}/20")
