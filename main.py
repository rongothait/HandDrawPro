import time
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import text
from mediapipe.tasks.python import text
import cv2 as cv
from camera_handle import get_camera_frame, init_camera
import threading


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


latest_img_bgr = None  # global variable to store the latest image
img_lock = threading.Lock()

# create a hand landmarker instace with the live stram mode
def print_result(result, output_image: mp.Image, timestamp_ms: int):
    global latest_img_bgr
    img = output_image.numpy_view().copy()  # Make a copy to avoid memory issues
    h, w, _ = img.shape

    # check for right hand using handedness
    if result.hand_landmarks and result.handedness:
        for idx, handedness in enumerate(result.handedness):
            label = handedness[0].category_name # "Right" or "Left"
            if label == "Left":  # This is right hand actually, computer's left
                hand_landmarks = result.hand_landmarks[idx]
                index_finger_landmark = hand_landmarks[8]
                cx, cy = int(index_finger_landmark.x * w), int(index_finger_landmark.y * h)
                if 0 <= cx < w and 0 <= cy < h:
                    cv.circle(img, (cx, cy), 5, (0, 255, 0), -1)
    img_bgr = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    with img_lock:
        latest_img_bgr = img_bgr

options = HandLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = 'Assets/hand_landmarker.task'),
    running_mode = VisionRunningMode.LIVE_STREAM,
    result_callback = print_result,
    num_hands = 2
)

with HandLandmarker.create_from_options(options) as landmaker:
    cap = init_camera()
    while True:
        imgRGB = get_camera_frame(cap)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        landmaker.detect_async(mp_img, int(time.time() * 1000))

        with img_lock:
            if latest_img_bgr is not None:
                cv.imshow('Hand Landmarks', latest_img_bgr)
        if cv.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()