import cv2
import screen_brightness_control as sbc
from playsound import playsound
import threading

# Haar cascade face & smile detection ke liye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Video capture start
cap = cv2.VideoCapture(0)

# Last mood track karne ke liye
last_mood = None

# Background me song bajane ke liye thread
def play_song(song_path):
    threading.Thread(target=playsound, args=(song_path,), daemon=True).start()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    mood = None

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]

        # Smile detect kar rahe hain
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

        if len(smiles) > 0:
            mood = "Happy"
            color = (0, 255, 0)  # Green box
            sbc.set_brightness(100)  # Brightness full
            if last_mood != "Happy":
                play_song(r"C:\Users\DELL\Music\happy_song.mp3")  # ✅ Happy song path
        else:
            mood = "Sad"
            color = (255, 0, 0)  # Blue box
            sbc.set_brightness(30)  # Brightness low
            if last_mood != "Sad":
                play_song(r"C:\Users\DELL\Music\sad_song.mp3")  # ✅ Sad song path

        # Last mood update
        last_mood = mood

        # Face box & mood text
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        cv2.putText(frame, mood, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Show video
    cv2.imshow("Mood Detector - Music & Brightness", frame)

    # 'q' dabao to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
