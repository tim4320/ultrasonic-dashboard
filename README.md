# Ultrasonic Distance Web Dashboard

A Flask + Arduino-based real-time distance monitor using an HC-SR04 ultrasonic sensor. 

Features:
- Real-time chart using Chart.js
- Distance threshold control
- LED auto/manual toggle
- Dark mode
- CSV data logging + download

## Requirements

- Arduino Uno (or similar)
- HC-SR04 Ultrasonic Sensor
- Python 3.x
- pip install -r requirements.txt

## Run the Server

```bash
python distance_server.py
