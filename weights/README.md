# Weights

Place your trained YOLOv8n checkpoint here as `best.pt`.

The detection scripts in `../detection/` load `weights/best.pt` by default. After
training (see `../training/train_yolov8n.ipynb`), copy the best checkpoint from
`runs/detect/<run-name>/weights/best.pt` into this folder, or update `MODEL_PATH`
in the detection scripts to point at it.

The `best.pt` for YOLOv8n is small (~6 MB) and can be committed directly to GitHub.
