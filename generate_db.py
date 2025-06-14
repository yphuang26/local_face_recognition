import os
import face_recognition
import pickle
from colorama import Fore, init

# Initialize colorama
init()

db = {"encodings": [], "names": []}

for filename in os.listdir("known_faces"):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        name = os.path.splitext(filename)[0]
        path = os.path.join("known_faces", filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            db["encodings"].append(encodings[0])
            db["names"].append(name)
            print(f"{Fore.GREEN}[INFO]{Fore.RESET} Added: {name}")
        else:
            print(f"{Fore.YELLOW}[WARN]{Fore.RESET} No face detected in: {filename}")

# Save as pickle
with open("database.pkl", "wb") as f:
    pickle.dump(db, f)

print(f"{Fore.BLUE}[SUCCESS]{Fore.RESET} Database creation completed!")