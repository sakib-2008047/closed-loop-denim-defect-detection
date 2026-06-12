"""
Raspberry Pi motor-control server (embedded control node).

Listens for inspection-state commands ("OK" / "DEFECT") from the PC detection
client over a TCP socket and drives the hardware via GPIO:

    OK     -> motor RUNNING,  green LED on
    DEFECT -> motor STOPPED,  red LED + buzzer on
    idle   -> everything off (safe startup / on PC disconnect)

Wiring (BCM pin numbering):
    L298N  IN1  -> GPIO 23
    L298N  IN2  -> GPIO 24
    Green LED   -> GPIO 27
    Red LED     -> GPIO 17
    Buzzer      -> GPIO 22

Run on the Raspberry Pi:  python3 motor_control_server.py
Requires: gpiozero  (pip install gpiozero)
"""

from gpiozero import DigitalOutputDevice
import socket
import sys

# L298N motor-driver control pins
IN1 = DigitalOutputDevice(23)
IN2 = DigitalOutputDevice(24)

# Status indicators
GREEN_LED = DigitalOutputDevice(27)
RED_LED = DigitalOutputDevice(17)
BUZZER = DigitalOutputDevice(22)

HOST = "0.0.0.0"
PORT = 65432  # MUST match PI_PORT in detection/detect_with_pi_control.py


def idle_state():
    # Everything OFF (safe state)
    IN1.off()
    IN2.off()
    GREEN_LED.off()
    RED_LED.off()
    BUZZER.off()
    print("State: IDLE - Waiting for signal")


def run_motor():
    IN1.on()
    IN2.off()
    GREEN_LED.on()
    RED_LED.off()
    BUZZER.off()
    print("State: OK - Motor RUNNING")


def stop_motor():
    IN1.off()
    IN2.off()
    GREEN_LED.off()
    RED_LED.on()
    BUZZER.on()
    print("State: DEFECT - Motor STOPPED")


def start_server():
    idle_state()  # safe startup with no alarm
    print("System Ready - Waiting for PC...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print("Connected:", addr)
            with conn:
                while True:
                    data = conn.recv(1024)
                    # If PC disconnected
                    if not data:
                        print("PC Disconnected")
                        idle_state()
                        break

                    command = data.decode().strip().upper()
                    if "OK" in command:
                        run_motor()
                    elif "DEFECT" in command:
                        stop_motor()
                    else:
                        print("Unknown command:", command)


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        idle_state()
        sys.exit(0)
