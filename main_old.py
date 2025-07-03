import time
import mediapipe as mp
import cv2 as cv
from camera_handle import get_camera_frame, init_camera 
import threading
import numpy as np


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


latest_img_bgr = None  # global variable to store the latest image
img_lock = threading.Lock()
trail_canvas = None  # Initialize trail_canvas
prev_point = None
drawing_enabled = False
delete_drawing = False


# create a hand landmarker instace with the live stram mode
def print_result(result, output_image: mp.Image, timestamp_ms: int):
    global latest_img_bgr, trail_canvas, prev_point, delete_drawing
    img = output_image.numpy_view().copy()
    h, w, _ = img.shape

    if trail_canvas is None:
        trail_canvas = np.zeros_like(img)

    # check for right hand using handedness
    fingertip_found = False
    if result.hand_landmarks and result.handedness:
        for idx, handedness in enumerate(result.handedness):
            label = handedness[0].category_name
            if label == "Left":  # This is your right hand
                hand_landmarks = result.hand_landmarks[idx]
                index_finger_landmark = hand_landmarks[8]
                cx, cy = int(index_finger_landmark.x * w), int(index_finger_landmark.y * h)
                if 0 <= cx < w and 0 <= cy < h:
                    if drawing_enabled:
                        if prev_point is not None:
                            cv.line(trail_canvas, prev_point, (cx, cy), (255, 255, 255), 5)
                        prev_point = (cx, cy)
                        fingertip_found = True
                    else:
                        prev_point = (cx, cy)
                        fingertip_found = True
                break  # Only track one hand
    if not fingertip_found:
        prev_point = None  # Reset if hand not found
    
    # text for drawing enabled / disabled
    color_of_text = (41, 115, 115) if drawing_enabled else (255, 133, 82)
    cv.putText(img, "Drawing", (10, 30), cv.FONT_HERSHEY_SIMPLEX , 0.9, color_of_text, 2)

    # text for right index finger detected or not
    color_of_text = (41, 115, 115) if fingertip_found else (255, 133, 82)
    cv.putText(img, "Right Index Finger", (w - 280, 30), cv.FONT_HERSHEY_SIMPLEX , 0.9, color_of_text, 2)

    if delete_drawing:
        img_bgr = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        delete_drawing = False
        trail_canvas = None
    else:
        overlay = cv.addWeighted(img, 0.8, trail_canvas, 1.0, 0)
        img_bgr = cv.cvtColor(overlay, cv.COLOR_RGB2BGR)

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
        key =  cv.waitKey(1) & 0xff
        if key == ord(' '):
            drawing_enabled = not drawing_enabled
        if key == ord('q'):
            break
        if key == ord('e'):
            delete_drawing = True
            pass
            

    cap.release()
    cv.destroyAllWindows()