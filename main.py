import cv2
import pytesseract
from googletrans import Translator, LANGUAGES
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit, QVBoxLayout, 
    QFileDialog, QMessageBox, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QTimer, Qt
from PIL import Image

# Set up Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Update this path if necessary

class ImageTextExtractor(QWidget):
    def __init__(self):
        super().__init__()

        self.cap = None
        self.camera_running = False
        self.extracted_text = ""

        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("TransLens")
        self.showFullScreen()
        self.setStyleSheet("background-color: #f0f0f0;")

        title_label = QLabel("TransLens", self)
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #4b0082;")

        self.open_camera_button = QPushButton("Open Camera", self)
        self.open_camera_button.setFont(QFont("Arial", 14))
        self.open_camera_button.setStyleSheet("background-color: #4b0082; color: white; padding: 10px;")
        self.open_camera_button.clicked.connect(self.open_camera)

        self.capture_button = QPushButton("Capture Image", self)
        self.capture_button.setFont(QFont("Arial", 14))
        self.capture_button.setStyleSheet("background-color: #4b0082; color: white; padding: 10px;")
        self.capture_button.clicked.connect(self.capture_image)

        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.setFont(QFont("Arial", 14))
        self.upload_button.setStyleSheet("background-color: #4b0082; color: white; padding: 10px;")
        self.upload_button.clicked.connect(self.upload_image)

        self.extract_button = QPushButton("Extract Text", self)
        self.extract_button.setFont(QFont("Arial", 14))
        self.extract_button.setStyleSheet("background-color: #4b0082; color: white; padding: 10px;")
        self.extract_button.clicked.connect(self.extract_text)

        self.lang_combobox = QComboBox(self)
        self.lang_combobox.addItems(list(LANGUAGES.values()))
        self.lang_combobox.setFont(QFont("Arial", 14))
        self.lang_combobox.setStyleSheet("padding: 10px;")

        self.translate_button = QPushButton("Translate Text", self)
        self.translate_button.setFont(QFont("Arial", 14))
        self.translate_button.setStyleSheet("background-color: #4b0082; color: white; padding: 10px;")
        self.translate_button.clicked.connect(self.translate_text)

        self.panel = QLabel(self)
        self.panel.setFixedSize(640, 480)
        self.panel.setAlignment(Qt.AlignCenter)
        self.panel.setStyleSheet("border: 2px solid #4b0082;")

        self.text_box = QTextEdit(self)
        self.text_box.setFont(QFont("Arial", 14))
        self.text_box.setStyleSheet("padding: 10px;")

        lang_label = QLabel("Select Target Language:", self)
        lang_label.setFont(QFont("Arial", 14))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_camera_button)
        button_layout.addWidget(self.capture_button)
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.extract_button)
        button_layout.addWidget(lang_label)
        button_layout.addWidget(self.lang_combobox)
        button_layout.addWidget(self.translate_button)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.panel)
        layout.addWidget(self.text_box)

        self.setLayout(layout)
    
    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Cannot open camera")
        else:
            self.camera_running = True
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(10)

    def capture_image(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite('captured_image.png', frame)
                img = Image.open('captured_image.png')
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                img.save('captured_image.png')
                pixmap = QPixmap('captured_image.png')
                self.panel.setPixmap(pixmap)
                self.camera_running = False
                self.cap.release()
                self.timer.stop()
                QMessageBox.information(self, "Image Captured", "Image has been captured successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to capture image.")
        else:
            QMessageBox.critical(self, "Error", "Camera is not opened")

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened() and self.camera_running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.panel.setPixmap(QPixmap.fromImage(image))

    def extract_text(self):
        try:
            img = cv2.imread('captured_image.png')
            self.extracted_text = pytesseract.image_to_string(img)
            self.text_box.setText(self.extracted_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def translate_text(self):
        try:
            target_lang = self.lang_combobox.currentText()
            if not target_lang:
                QMessageBox.critical(self, "Error", "Please select a target language.")
                return
            target_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_lang)]
            translator = Translator()
            translated = translator.translate(self.extracted_text, dest=target_lang_code)
            self.text_box.setText(translated.text)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            img = Image.open(file_path)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            img.save('captured_image.png')
            pixmap = QPixmap('captured_image.png')
            self.panel.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication([])
    window = ImageTextExtractor()
    window.show()
    app.exec_()
