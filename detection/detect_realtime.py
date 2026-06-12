"""
Standard real-time fabric defect detection (windowed display).

Loads the trained YOLOv8n checkpoint and runs live inference on a connected
webcam. Detected defects are drawn on each frame and shown in a window.
Press 'q' to quit. Change the VideoCapture index (0 or 1) to select the camera.
"""

from ultralytics import YOLO
import cv2
import torch

# Place your trained best.pt in ../weights/ (or point this to
# runs/detect/<run-name>/weights/best.pt). Forward slashes work on Windows too.
MODEL_PATH = "weights/best.pt"

model = YOLO(MODEL_PATH)
device = 0 if torch.cuda.is_available() else "cpu"
print("Using device:", device)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # change index if needed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(
        source=frame, conf=0.6, imgsz=640,
        device=device, stream=False, half=False,
    )
    annotated = results[0].plot()
    cv2.imshow("Fabric Defect Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
