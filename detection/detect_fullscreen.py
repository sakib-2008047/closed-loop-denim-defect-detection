"""
Full-screen real-time fabric defect detection.

Identical to detect_realtime.py but displays output full-screen, suitable for
a dedicated inspection monitor. Press 'q' to quit.
"""

from ultralytics import YOLO
import cv2

MODEL_PATH = "weights/best.pt"

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(0)

# Full-screen window
cv2.namedWindow("Fabric Defect Detection", cv2.WINDOW_NORMAL)
cv2.setWindowProperty(
    "Fabric Defect Detection",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN,
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.6, imgsz=640, stream=False)
    annotated = results[0].plot()
    cv2.imshow("Fabric Defect Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
