import cv2 as cv
import mediapipe as mp
import constants

class HandTracker:
    def __init__(self, max_num_hands = 1):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(
            static_image_mode = False,
            max_num_hands = max_num_hands,
            min_detection_confidence = constants.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence = constants.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def process(self, frame):
        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = self.hands.process(image_rgb)

        cursor = None
        gesture_id = 0  # default to unknown


        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]  # take first hand only
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            cursor = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))

            # Get gesture id if provided by the classifier
            if result.multi_handedness:
                classification = result.multi_handedness[0].classification[0]
                label = classification.label  # 'Left' or 'Right'

        
        # TODO - integrate gesture classifier
        gesture_id = 1

        return cursor, gesture_id
        