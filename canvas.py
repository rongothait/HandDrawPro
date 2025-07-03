import cv2 as cv
import numpy as np
import constants

class Canvas:
    def __init__(self):
        self.strokes = []  # List of (List of points, color)
        self.current_stroke = []  # points while drawing
        self.current_color = constants.DEFAULT_COLOR

    """
    init current_stroke array and set color
    """
    def start_new_stroke(self, color = None):
        self.current_stroke = []
        self.current_color = color if color else constants.DEFAULT_COLOR

    def add_point(self, point):
        self.current_stroke.append(point)
    
    def finish_stroke(self):
        if self.current_stroke:
            self.strokes.append((self.current_stroke.copy(), self.current_color))
            self.current_stroke = []
    
    def draw(self, frame):
        # draw all completed strokes
        for stroke, color in self.strokes:
            for i in range(1, len(stroke)):
                cv.line(frame, stroke[i-1], stroke[i], color, 3)  # a line between the current point to previous one (so it will be continous)
        
        # draw the current stroke in progress
        for i in range(1, len(self.current_stroke)):
            cv.line(frame, self.current_stroke[i - 1], self.current_stroke[i], self.current_color, 3)

    def find_stroke_near(self, point, threshold = 30):
        """Return index of stroke if point is near any stroke point"""
        for idx, (stroke, _) in enumerate(self.strokes):
            for pt in stroke:
                if self._distance(pt, point) < threshold:
                    return idx
        
        return None
    
    def move_stroke(self, index, dx, dy):
        """ sets in place the moved stroke """
        stroke, color = self.strokes[index]
        moved = [(x + dx, y + dy) for (x, y) in stroke]
        self.strokes[index] = (moved, color)
    
    def delete_stroke(self, index):
        if 0 <= index < len(self.strokes):
            del self.strokes[index]
    
    def undo(self):
        """ think about deleteing """
        if self.strokes:
            self.strokes.pop()
    
    def _distance(self, p1, p2):
        dist_sqr = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
        return dist_sqr**0.5
    
        


