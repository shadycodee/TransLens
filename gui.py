import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
from capture import capture_frame
from text_extraction import extract_text
from translate_text import translate_text

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Extraction and Translation")

        self.label = Label(root)
        self.label.pack()

        self.capture_button = tk.Button(root, text="Capture", command=self.capture_and_process)
        self.capture_button.pack()

        self.extracted_text = tk.StringVar()
        self.extracted_text_label = Label(root, textvariable=self.extracted_text)
        self.extracted_text_label.pack()

        self.translated_text = tk.StringVar()
        self.translated_text_label = Label(root, textvariable=self.translated_text)
        self.translated_text_label.pack()

    def capture_and_process(self):
        frame = capture_frame()
        if frame is not None:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            text = extract_text(frame)
            self.extracted_text.set(text)

            translated = translate_text(text)
            self.translated_text.set(translated)

    def on_close(self):
        self.root.destroy()

root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.on_close)
root.mainloop()
