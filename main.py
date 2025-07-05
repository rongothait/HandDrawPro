import cv2 as cv
from hand_tracker import HandTracker
from canvas import Canvas
from constants import GESTURE_TO_MODE
import constants
from database import DrawingDatabase

def main():
    db = DrawingDatabase()
    cap = cv.VideoCapture(0)
    hand_tracker = HandTracker()
    canvas = Canvas()

    current_mode = "idle"
    current_color_idx = 0
    selected_stroke_idx = None
    prev_cursor = None
    last_gesture_id = None

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv.flip(frame, 1)
        h, w = frame.shape[:2]

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

            elif current_mode == "undo" and last_gesture_id != 4:
                canvas.undo_last_stroke()
                db.delete_last_stroke()
            
            elif current_mode == "change_color" and last_gesture_id != 5:
                current_color_idx = (current_color_idx + 1) % len(constants.COLOR_PALLATE)
                canvas.current_color = constants.COLOR_PALLATE[current_color_idx]

            last_gesture_id = gesture_id

        # 3. Finalize stroke when gesture changes from draw - > other
        if current_mode != "draw" and canvas.current_stroke:
            canvas.finish_stroke()

            # save the last stroke into the dabase (for demo - each stroke is a different drawing)
            db.save_drawing([canvas.strokes[-1]], gesture_id)
        
        # 4. reset drag when gesture leaves drag mode
        if current_mode != "drag":
            selected_stroke_idx = None
            prev_cursor = None

        
        # 5. Draw Everything
        canvas.draw(frame)

        # Small color circle (e.g., top-left corner)
        circle_center = (w - 30, 30)  # x, y position on screen
        circle_radius = 15
        circle_color = canvas.current_color

        cv.circle(frame, circle_center, circle_radius, circle_color, -1)  # filled circle
        cv.circle(frame, circle_center, circle_radius, (255, 255, 255), 2)  # white border

        # 6. overlay text for mode
        cv.putText(frame, f"Mode: {current_mode}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 1, constants.DEFAULT_TEXT_COLOR, 2)

        # 7. show image
        cv.imshow("HandDraw Pro", frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
