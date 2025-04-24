import cv2
import face_recognition
import numpy as np
import os
import json

def capture_face_data():
    base_path = "/Users/pratham/Documents/Tess/HELIXKEY/data"
    os.makedirs(base_path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    print("📸 Webcam opened. Press 'c' to capture, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        cv2.imshow("Face Capture (c = capture, q = quit)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            print("🔍 Processing frame...")
            rgb = frame[:, :, ::-1]

            # Detect face locations first (and use that!)
            face_locations = face_recognition.face_locations(rgb)
            if not face_locations:
                print("⚠️ No face detected. Try again.")
                continue

            top, right, bottom, left = face_locations[0]
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(os.path.join(base_path, "face_snapshot.jpg"), face_image)
            cv2.imwrite(os.path.join(base_path, "captured.jpg"), frame)

            try:
                encodings = face_recognition.face_encodings(rgb, face_locations)
                if encodings:
                    encoding = encodings[0]
                    np.save(os.path.join(base_path, "encoding.npy"), encoding)
                    np.savetxt(os.path.join(base_path, "encoding.txt"), encoding, delimiter=",")
                    print("✅ Saved face encoding.")
                else:
                    print("⚠️ No encoding returned.")
            except Exception as e:
                print(f"❌ Encoding error: {e}")

            try:
                landmarks_list = face_recognition.face_landmarks(rgb)
                if landmarks_list:
                    with open(os.path.join(base_path, "landmarks.json"), 'w') as f:
                        json.dump(landmarks_list[0], f, indent=2)
                    print("✅ Saved landmarks.")
                else:
                    print("⚠️ No landmarks found.")
            except Exception as e:
                print(f"❌ Landmark error: {e}")

            break

        elif key == ord('q'):
            print("❌ Capture cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_face_data()
