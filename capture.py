import cv2

def capture_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        return None
    cap.release()
    return frame
