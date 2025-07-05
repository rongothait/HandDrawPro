import sqlite3
from datetime import datetime

class DrawingDatabase:
    def __init__(self, db_path = "drawings.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Drawings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    gesture_id INTEGER
                    )
            """)
        

        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS strokes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        drawing_id INTEGER,
                        color TEXT
                        )
                       """)
        

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Points (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       stroke_id INTEGER,
                       x INTEGER,
                       y INTEGER,
                       point_order INTEGER
                       )
                       """)
        
        self.conn.commit()



    def save_drawing(self, strokes, gesture_id):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()

        # 1. insert the new drawing
        cursor.execute("INSERT INTO Drawings (timestamp, gesture_id) VALUES (?, ?)", (timestamp, gesture_id))
        drawing_id = cursor.lastrowid

        # 2. Insert strokes + points
        for stroke_points, color in strokes:
            cursor.execute("INSERT INTO Strokes (drawing_id, color) VALUES (?, ?)", (drawing_id, str(color)))
            stroke_id = cursor.lastrowid
        
            for order, (x,y) in enumerate(stroke_points):
                cursor.execute(
                    "INSERT INTO Points (stroke_id, x, y, point_order) VALUES (?, ?, ?, ?)", (stroke_id, x, y, order)
                )
        
        self.conn.commit()

    
    def load_last_drawing(self):
        cursor = self.conn.cursor()

        # 1. Get most recent drawing
        cursor.execute("SELECT id FROM Drawings ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return []
        
        drawing_id = row[0]

        # 2. load strokes for that drawing
        cursor.execute("SELECT id, color FROM Strokes WHERE drawing_id = ?", (drawing_id,))
        strokes_data = cursor.fetchall()

        loaded_strokes = []
        for stroke_id, color_str in strokes_data:
            # convert string like (255, 255, 255) back to tuple
            color = eval(color_str)

            # 3. load poionts
            cursor.execute("SELECT x,y FROM Points WHERE stroke_id = ? ORDER BY point_order ASC", (stroke_id,))
            points = cursor.fetchall()

            loaded_strokes.append((points, color))
    
        return loaded_strokes
    
    def delete_last_stroke(self):
        cursor = self.conn.cursor()

        # Get last stroke inserted
        cursor.execute("SELECT id FROM strokes ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return
        
        stroke_id = row[0]

        # Delete points forst (due to Foreign Key if used)
        cursor.execute("DELETE FROM Points WHERE stroke_id = ?", (stroke_id, ))
        cursor.execute("DELETE FROM Strokes WHERE id = ?", (stroke_id,))

        self.conn.commit()
    
                           

