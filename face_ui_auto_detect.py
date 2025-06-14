import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import pickle
import numpy as np
import os
import uuid
import sys

class FaceRecognitionAPP:
    def __init__(self):
        # Database initialization
        self.DB_FILE = "database.pkl"
        self.KNOWN_FOLDER = "known_faces"

        if not os.path.exists(self.KNOWN_FOLDER):
            os.makedirs(self.KNOWN_FOLDER)

        self.load_database()

        # UI initialization
        self.window = tk.Tk()
        self.window.title("Face Recognition")
        self.window.geometry("960x720")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Main display
        self.label = tk.Label(self.window)
        self.label.pack()

        # Recognition result display
        self.result_label = tk.Label(self.window, text="", font=("Helvetica", 20))
        self.result_label.pack()

        # Button frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        # Register button (initially disabled)
        self.register_button = tk.Button(
            button_frame,
            text="Add New Face",
            command=self.register_face,
            font=("Helvetica", 16),
            bg="lightgreen",
            state="disabled",
            width=15,
            height=2
        )
        self.register_button.pack(side=tk.LEFT, padx=10)

        # Status display
        self.status_label = tk.Label(
            button_frame,
            text="Please face the camera",
            font=("Helvetica", 14),
            fg="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Camera initialization
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot open the camera")
            self.window.destroy()
            sys.exit(1)

        self.current_unknown_face = None
        self.current_face_encoding = None
        self.current_identity = ""

        # Start updating
        self.update()

    def load_database(self):
        if os.path.exists(self.DB_FILE):
            try:
                with open(self.DB_FILE, "rb") as f:
                    db = pickle.load(f)
                self.known_encodings = db.get("encodings", [])
                self.known_names = db.get("names", [])
            except Exception as e:
                print(f"Error loading database: {e}")
                self.known_encodings = []
                self.known_names = []
        else:
            self.known_encodings = []
            self.known_names = []

    def save_database(self):
        try:
            db = {"encodings": self.known_encodings, "names": self.known_names}
            with open(self.DB_FILE, "wb") as f:
                pickle.dump(db, f)
        except Exception as e:
            print(f"Error saving database: {e}")
            messagebox.showerror("Error", f"Failed to save database: {e}")

    def save_new_face(self, name, face_img, encoding):
        try:
            # Save image
            filename = f"{name}_{uuid.uuid4().hex[:8]}.jpg"
            filepath = os.path.join(self.KNOWN_FOLDER, filename)
            cv2.imwrite(filepath, face_img)

            # Update database
            self.known_encodings.append(encoding)
            self.known_names.append(name)
            self.save_database()

            messagebox.showinfo("Success", f"Face registered successfully as {name}")

            # Clear current unknown face
            self.current_unknown_face = None
            self.current_face_encoding = None
        except Exception as e:
            print(f"Error saving new face: {e}")
            messagebox.showerror("Error", f"Failed to save face: {e}")

    def register_face(self):
        if self.current_unknown_face is None:
            messagebox.showerror("Error", "No face detected")
            return

        name = simpledialog.askstring("Register", "Enter the name: ")
        if name and name.strip():
            self.save_new_face(name.strip(), self.current_unknown_face, self.current_face_encoding)

    def update_ui_status(self, identity):
        self.current_identity = identity

        if identity == "Unknown":
            self.result_label.config(text="Recognition result: Unknown", fg="red")
            self.register_button.config(state="normal", bg="lightgreen")
            self.status_label.config(text="Face registration available", fg="gray")
        elif identity == "No face detected":
            self.result_label.config(text="Recognition result: No face detected", fg="gray")
            self.register_button.config(state="disabled", bg="lightgray")
            self.status_label.config(text="Please face the camera", fg="gray")
        else:
            self.result_label.config(text=f"Recognition result: {identity}", fg="green")
            self.register_button.config(state="disabled", bg="lightgray")
            self.status_label.config(text="Identity recognized", fg="gray")
    
    def update(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                self.result_label.config(text="Error: Cannot read frame")
                self.window.after(100, self.update)
                return
            
            # Face recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            identity = "No face detected"

            # Process detected face
            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.45)
                name = "Unknown"

                if True in matches:
                    face_distances = face_recognition.face_distance(self.known_encodings, encoding)
                    best_idx = np.argmin(face_distances)
                    name = self.known_names[best_idx]

                identity = name

                # Draw rectangle and label
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)  # Green for known, Red for unknown
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                # Store unknown face
                if name == "Unknown":
                    self.current_unknown_face = frame[top:bottom, left:right].copy()
                    self.current_face_encoding = encoding.copy()
                else:
                    # If not unknown, clear stored unknown face
                    self.current_unknown_face = None
                    self.current_face_encoding = None

                break # Only process first face

            # If no face detected, clear unknown face
            if identity == "No face detected":
                self.current_unknown_face = None
                self.current_face_encoding = None

            # Update UI status
            self.update_ui_status(identity)

            # Update camera view
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = img.resize((960, 600), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        except Exception as e:
            print("Error occurred during update")
            self.result_label.config(text=f"Error: {str(e)}")

        # Continue next update
        self.window.after(30, self.update)

    def on_closing(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    try:
        app = FaceRecognitionAPP()
        app.run()
    except Exception as e:
        print(f"Program execution failed: {e}")
        messagebox.showerror("Serious Error", f"Program execution failed: {e}")