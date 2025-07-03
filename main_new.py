import cv2 as cv
from hand_tracker import HandTracker
from canvas import Canvas
from constants import GESTURE_TO_MODE

def main():
    cap = cv.VideoCapture(0)
    hand_tracker = HandTracker()
    canvas = Canvas()

    current_mode = "idle"
    selected_stroke_idx = None
    prev_cursor = None

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv.flip(frame, 1)

        cursor, gesture_id = hand_tracker.process(frame)

        # 1. set mode based on gesture
        current_mode = GESTURE_TO_MODE.get(gesture_id, "idle")

        # 2. perform action based on mode
        if cursor:
            if current_mode == "draw":
                canvas.add_point(cursor)
            
            elif current_mode == "drag":
                if selected_stroke_idx is None:
                    selected_stroke_idx = canvas.find_stroke_near(cursor)
                    prev_cursor = cursor
                
                else:
                    dx = cursor[0] - prev_cursor[0]
                    dy = cursor[1] - prev_cursor[1]
                    canvas.move_stroke(selected_stroke_idx, dx, dy)
                    prev_cursor = cursor
            
            elif current_mode == "erase":
                idx = canvas.find_stroke_near(cursor)
                if idx is not None:
                    canvas.delete_stroke(idx)

        # 3. Finalize stroke when gesture changes from drwa - > other
        if current_mode != "draw" and canvas.current_stroke:
            canvas.finish_stroke()
        
        # 4. reset drag when gesture leaves drag mode
        if current_mode != "drag":
            selected_stroke_idx = None
            prev_cursor = None

        
        # 5. Draw Everything
        canvas.draw(frame)

        # 6. overlay text for mode
        cv.putText(frame, f"Mode: {current_mode}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 7. show image
        cv.imshow("HandDraw Pro", frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
