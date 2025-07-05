DEFAULT_COLOR = (50, 55, 75)
DEFAULT_TEXT_COLOR = (50, 55, 75)
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5

# Map Gesture ID to mode_name
GESTURE_TO_MODE = {
    3 : 'draw',  # Open_palm
    1 : 'drag',  # Closed_Fist
    6 : 'erase', # Victory
    0 : 'idle'   # Unkown
}


# paths
GESTURE_TASK_PATH = "./Assets/gesture_recognizer.task"