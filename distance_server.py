from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
import serial
import threading
import time
import csv
from io import StringIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Update this with your correct serial port
ser = serial.Serial('/dev/tty.usbmodem146401', 9600, timeout=1)
# For Windows: ser = serial.Serial('COM3', 9600, timeout=1)

distance = 0
threshold = 15
led_on = False
auto_mode = False
csv_data = [("Time", "Distance")]

def serial_reader():
    global distance, led_on
    while True:
        try:
            line = ser.readline().decode().strip()
            if line.startswith("D:") and "L:" in line:
                parts = line.split(',')
                distance_str = parts[0].split(':')[1]
                led_str = parts[1].split(':')[1]

                distance = float(distance_str)
                led_on = led_str == '1'

                timestamp = time.strftime("%H:%M:%S")
                csv_data.append((timestamp, distance))

                if auto_mode:
                    led_on = distance < threshold
                    ser.write(b'H' if led_on else b'L')

                socketio.emit('distance', {
                    'value': distance,
                    'led': led_on
                })
        except Exception as e:
            print("Serial error:", e)


@socketio.on('threshold')
def set_threshold(data):
    global threshold
    threshold = float(data['value'])

@socketio.on('led_toggle')
def toggle_led(data):
    global led_on, auto_mode
    auto_mode = False
    led_on = data['on']
    ser.write(b'H' if led_on else b'L')

@socketio.on('led_auto')
def enable_auto():
    global auto_mode
    auto_mode = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(csv_data)
    output.seek(0)
    return send_file(output, mimetype='text/csv', download_name='distance_log.csv', as_attachment=True)

if __name__ == '__main__':
    threading.Thread(target=serial_reader, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
