# face_mood_song.py
import cv2
import threading
import os
from playsound import playsound

# Songs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
happy_song = os.path.join(BASE_DIR, "romantic.mp3")
sad_song   = os.path.join(BASE_DIR, "funny.mp3")

# Function to play song
def play_song(path):
    if os.path.exists(path):
        threading.Thread(target=playsound, args=(path,), daemon=True).start()
    else:
        print("⚠️ File not found:", path)

# Load Haarcascade files (OpenCV me built-in hote hain)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

cap = cv2.VideoCapture(0)
last_mood = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    mood = "Sad"  # default
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

        if len(smiles) > 0:
            mood = "Happy"
            cv2.putText(frame, "Smile Detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Song play logic
    if mood == "Happy" and last_mood != "Happy":
        play_song(happy_song)
        last_mood = "Happy"
    elif mood == "Sad" and last_mood != "Sad":
        play_song(sad_song)
        last_mood = "Sad"

    # Show result
    cv2.putText(frame, f"Mood: {mood}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("Face Mood Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
