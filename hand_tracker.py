import cv2 as cv
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python.vision import GestureRecognizer
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerResult
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerOptions
from mediapipe.tasks.python.vision import RunningMode
import constants

class HandTracker:
    def __init__(self, model_path = constants.GESTURE_TASK_PATH):
        self.options = GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=RunningMode.VIDEO,
            num_hands=1
        )
        self.recognizer = GestureRecognizer.create_from_options(self.options)
        self.frame_idx = 0

    def process(self, frame):
        rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        result: GestureRecognizerResult = self.recognizer.recognize_for_video(mp_image, self.frame_idx)
        self.frame_idx += 1

        cursor = None
        gesture_id = 0  # Default: Unknown

        if not result.hand_landmarks or not result.handedness:
            return None, 0
        
        right_idx = None
        for i, handedness in enumerate(result.handedness):
            if handedness[0].category_name == "Left":
                right_idx = i
                break
        
        if right_idx is None:
            return None, 0  # No right hands detected
        
        hand_landmark = result.hand_landmarks[right_idx]
        index_tip = hand_landmark[8]  # first hand, landmark 8
        h, w, _ = frame.shape
        cursor = (int(index_tip.x * w), int(index_tip.y * h))

        if result.gestures:
            top_gesture = result.gestures[right_idx][0]
            label = top_gesture.category_name  # e.g. "Open_Palm"
            score = top_gesture.score  # not in use currently
            gesture_id = self.label_to_id(label)


        return cursor, gesture_id

    def label_to_id(self, label):
        mapping = {
            "Unknown": 0,
            "Closed_Fist": 1,
            "Open_Palm": 2,
            "Pointing_Up": 3,
            "Thumb_Down": 4,
            "Thumb_Up": 5,
            "Victory": 6,
            "ILoveYou": 7
        }
        return mapping.get(label, 0)