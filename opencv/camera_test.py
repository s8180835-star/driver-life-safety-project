
import cv2
import threading
from playsound import playsound

# ✅ Song paths (use absolute paths with raw strings)
happy_song = r"C:\Users\DELL\OneDrive\Desktop\opencv\funny.mp3"
sad_song   = r"C:\Users\DELL\OneDrive\Desktop\opencv\romantic.mp3"

# Load Haar cascades for face and smile detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

# Function to play songs in background
def play_song(song):
    threading.Thread(target=playsound, args=(song,), daemon=True).start()

last_mood = None  # To avoid restarting song every frame

if not cap.isOpened():
    print("Error: Cannot access camera")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]

            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

            if len(smiles) > 0:
                mood = "Happy"
                color = (0, 255, 0)  # Green box
                if last_mood != "Happy":  
                    play_song(happy_song)
                    last_mood = "Happy"
            else:
                mood = "Sad"
                color = (0, 0, 255)  # Red box
                if last_mood != "Sad":  
                    play_song(sad_song)
                    last_mood = "Sad"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
            cv2.putText(frame, mood, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Face Mood Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
