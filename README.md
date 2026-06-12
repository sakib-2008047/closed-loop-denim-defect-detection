# A Closed-Loop YOLOv8 System for Real-Time Denim Defect Detection and Control

Source code for the undergraduate thesis *"A Closed-Loop YOLOv8 System for Real-Time
Denim Defect Detection and Control"* (Department of Industrial and Production
Engineering, BUET).

Conventional automated fabric-inspection systems are **open-loop**: they detect and
display defects but take no physical action, so defective fabric keeps moving past the
inspection point. This project implements a **closed-loop "Detect–Decide–Act" pipeline**.
A YOLOv8n detector runs on a GPU-accelerated PC and streams an inspection state over a
TCP socket to a Raspberry Pi 5, which halts the fabric-transport motor and raises
LED/buzzer alerts the moment a defect is detected.

## System architecture

```
  ┌──────────────┐   1080p HDMI    ┌────────────────────────┐   "OK"/"DEFECT"   ┌──────────────────────┐
  │  4K camera   │ ─────────────►  │   Host PC (GPU)        │ ───TCP / Wi-Fi──► │   Raspberry Pi 5     │
  │  + LED ring  │   capture card  │   YOLOv8n inference    │     socket        │   GPIO control       │
  └──────────────┘                 │   Detect → Decide      │                   │   motor + LED + buzz │
         ▲                         └────────────────────────┘                   └──────────┬───────────┘
         │ continuous fabric                                                                │ stop / run
         └────────────────────────────────  Fabric transport (DC motor + L298N) ───────────┘
```

The PC is the TCP **client** (`detection/detect_with_pi_control.py`); the Raspberry Pi
is the TCP **server** (`raspberry_pi/motor_control_server.py`). State is transmitted only
on transitions ("OK" ↔ "DEFECT") to keep the link light.

## Repository structure

```
.
├── data.yaml                          # YOLO dataset config (4 defect classes)
├── requirements.txt                   # PC-side dependencies
├── preprocessing/                     # dataset preparation (Appendix A)
│   ├── 01_resize_images.py
│   ├── 02_rename_images.py
│   └── 03_augment_images.py           # offline rotation/flip/brightness augmentation
├── training/
│   └── train_yolov8n.ipynb            # Colab training, validation & FPS benchmark (Appendix B)
├── detection/                         # PC / host inference (Appendix C)
│   ├── detect_realtime.py             # windowed live detection
│   ├── detect_fullscreen.py           # full-screen live detection
│   └── detect_with_pi_control.py      # closed-loop client (sends state to the Pi)
├── raspberry_pi/
│   └── motor_control_server.py        # embedded TCP server: motor + LED + buzzer
└── weights/
    └── (place trained best.pt here)
```

## Defect classes

| ID | Class           | Type       |
|----|-----------------|------------|
| 0  | Holes           | Structural |
| 1  | Abrasion_Mark   | Surface    |
| 2  | Oil_Stain       | Surface    |
| 3  | Missing_Yarn    | Structural |

## Hardware

- 4K industrial camera (YCS-X80) with macro lens (MC75L-B3) and LED ring light, via an HDMI→USB capture card
- GPU-equipped host PC (CUDA) for inference
- Raspberry Pi 5 (embedded control node)
- L298N H-bridge motor driver + 12 V DC motor (fabric transport)
- Green/Red LEDs and an active buzzer; bifurcated 12 V (motor) / USB-C (Pi) power

GPIO wiring (BCM): L298N IN1→23, IN2→24, Green LED→27, Red LED→17, Buzzer→22.

## Installation

```bash
git clone https://github.com/<your-username>/closed-loop-denim-defect-detection.git
cd closed-loop-denim-defect-detection
pip install -r requirements.txt
```

For GPU acceleration, install the CUDA build of PyTorch for your system from
<https://pytorch.org/get-started/locally/>. On the Raspberry Pi, install `gpiozero`.

## Usage

**1. Prepare the dataset (optional — only if rebuilding from raw images).**
Edit the folder/prefix variables at the top of each script, then run:
```bash
python preprocessing/01_resize_images.py
python preprocessing/02_rename_images.py
python preprocessing/03_augment_images.py
```
Arrange the result in standard YOLO format (`images/{train,val}`, `labels/{train,val}`)
and update `data.yaml`.

**2. Train.** Open `training/train_yolov8n.ipynb` in Google Colab (GPU runtime) and run
the cells. They train YOLOv8n for 100 epochs at 768×768, validate at 768 and 640, and
benchmark inference speed. Copy the resulting `best.pt` into `weights/`.

**3. Run detection.**
```bash
# Detection only (no hardware)
python detection/detect_realtime.py

# Closed-loop with the Raspberry Pi:
#   a) on the Pi:
python3 raspberry_pi/motor_control_server.py
#   b) on the PC (set PI_IP first, see below):
python detection/detect_with_pi_control.py
```

### Configuration notes

- **Model path:** detection scripts load `weights/best.pt`. Change `MODEL_PATH` to use a
  different checkpoint.
- **Raspberry Pi IP/port:** in `detection/detect_with_pi_control.py` set `PI_IP` to your
  Pi's LAN address. `PI_PORT` (65432) **must match** `PORT` in
  `raspberry_pi/motor_control_server.py`.
- **Confidence threshold:** detection runs at `conf=0.6`; inference resolution is `imgsz=640`.

## Results (from the thesis)

Validation set (300 images), `best.pt`:

| Metric            | Value  |
|-------------------|--------|
| mAP@0.5           | 0.889  |
| mAP@0.5:0.95      | 0.584  |
| Precision         | 0.857  |
| Recall            | 0.863  |

Per-class AP@0.5: Oil_Stain 0.995 · Holes 0.967 · Missing_Yarn 0.871 · Abrasion_Mark 0.723.

Real-time (deployed system): structural defects detected reliably across all tested
conveyance speeds (1.90 / 3.55 / 4.58 cm/s), including **100% detection of holes > 3 mm**;
low-contrast surface defects (abrasion marks, small oil stains) degrade with speed.

> **Note:** all defects were induced under controlled laboratory conditions, so these
> figures are an upper-bound estimate pending validation on genuine production-line defects.

## Citation

```bibtex
@misc{kormokar_sakib_2025_denim,
  title  = {A Closed-Loop YOLOv8 System for Real-Time Denim Defect Detection and Control},
  author = {Kormokar, Chaon Ronjon and Sakib, Md. Nazimus},
  year   = {2025},
  school = {Bangladesh University of Engineering and Technology (BUET)},
  note   = {B.Sc. thesis, Department of Industrial and Production Engineering}
}
```

## License

Released under the [MIT License](LICENSE).

## Authors

- Md. Nazimus Sakib (2008047)

Supervised by Dr. Nafis Ahmad, Professor, Department of Industrial and Production
Engineering, BUET.
