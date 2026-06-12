"""
Resize all images in an input folder to a fixed square resolution.

Reads every image from `input_folder`, resizes each to IMG_SIZE x IMG_SIZE
with OpenCV, and writes the result to `output_folder`.

Note: YOLOv8 resizes internally to `imgsz` at train/inference time, so this
step is an optional dataset-normalisation utility. The final training pipeline
used the full-resolution augmented images (see ../training).
"""

import cv2
import os

# ---- Configuration ----------------------------------------------------------
input_folder = "dataset/original"
output_folder = "dataset/resized"
IMG_SIZE = 224  # target resolution (pixels)
# -----------------------------------------------------------------------------

os.makedirs(output_folder, exist_ok=True)

for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)
    img = cv2.imread(img_path)
    if img is None:
        continue

    resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    save_path = os.path.join(output_folder, img_name)
    cv2.imwrite(save_path, resized_img)

print("All images resized successfully!")
