import cv2 as cv

def init_camera(idx = 0):
    cap = cv.VideoCapture(idx)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")
    return cap

def get_camera_frame(cap):
    success, img = cap.read()
    if not success:
        raise RuntimeError("Failed to read frame from camera")
    img = cv.flip(img, 1)  # Flip the frame horizontally
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # Convert BGR to RGB
    return imgRGB