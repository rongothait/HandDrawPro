# 🖐️ HandDraw Pro

**HandDraw Pro** is a gesture-controlled drawing canvas built with [MediaPipe](https://developers.google.com/mediapipe), OpenCV, and SQLite. It uses real-time hand tracking and gesture recognition to let users draw, erase, drag, and undo using only hand gestures — no keyboard or mouse needed.

---

## 🎥 Demo

[Watch the demo video](https://www.youtube.com/watch?v=ADiWDQXGUSc)

---

## ✨ Features

- 👆 **Index finger as a cursor** 
- ✋ **Gesture-based mode switching** (no buttons!)
- 🖌️ **Draw** by raising the index finger
- ✊ **Drag** any stroke using a closed fist
- ✌️ **Erase** strokes with the Victory sign
- 👍 **Change color** with a thumbs-up gesture
- 👎 **Undo** the last draw operation with a thumbs-down gesture
- 🎨 **Live color preview** on screen
- 💾 **SQLite integration** to store all strokes and gestures

---

## 🛠️ Tech Stack

- **MediaPipe Tasks API** — hand + gesture recognition
- **OpenCV** — video feed, drawing, overlays
- **SQLite** — persistent stroke and gesture storage
- **Python** — main application logic

---

## 🧠 Architecture Overview
HANDPAINT/
├── main.py # Main loop: gestures, modes, rendering
├── canvas.py # Stroke management + undo stack
├── hand_tracker.py # MediaPipe hand + gesture tracker
├── database.py # SQLite integration
├── Assets/gesture_recognizer.task # Pretrained model from Google
└── drawings.db # Local database (auto-generated)

## 🧪 Supported Gestures

| Gesture         | Mode / Action       |
|-----------------|---------------------|
| ✋ Open Palm     | Idle mode           |
| ☝️ Pointing Up   | Draw                |
| ✊ Closed Fist   | Drag mode           |
| ✌️ Victory       | Erase mode          |
| 👍 Thumbs Up     | Change color        |
| 👎 Thumbs Down   | Undo last stroke    |
---

## 💡 How It Works

1. MediaPipe tracks hand landmarks and predicts the gesture
2. Your **index finger tip** is always treated as a “cursor”
3. Gesture switches the **mode** (`draw`, `drag`, `erase`, etc.)
4. Actions update both the **canvas** and the **SQLite database**

---

## 🧰 Setup & Run

### 📦 Requirements
python 3.7 - 3.10

```bash
pip install opencv-python mediapipe
