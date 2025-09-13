# face_mood_pygame.py
import cv2
import pygame
import os

# ✅ Songs ka path (same folder me rakho)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
happy_song = os.path.join(BASE_DIR, "romantic.mp3.mp3")
sad_song   = os.path.join(BASE_DIR, "funny.mp3.mp3")

# ✅ Pygame init
pygame.mixer.init()

def play_song(path):
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)  # loop me play hoga
    else:
        print("⚠️ File not found:", path)

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

last_mood = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    mood = "Sad"  # default
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        if len(smiles) > 0:
            mood = "Happy"

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # ✅ Song play only on mood change
    if mood != last_mood:
        if mood == "Happy":
            play_song(happy_song)
        else:
            play_song(sad_song)
        last_mood = mood

    cv2.putText(frame, f"Mood: {mood}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Mood Detection (Happy/Sad)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
