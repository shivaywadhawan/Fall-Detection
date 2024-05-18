import time
import os
import json
import board

import adafruit_connection_manager
import wifi
import adafruit_mpu6050
import busio
from board import *

import adafruit_requests

SCL = board.IO1
SDA = board.IO0

# Wi-Fi details
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
TABLE_URL = f"{SUPABASE_URL}/rest/v1/528"

# Initialize MPU6050
i2c = busio.I2C(SCL, SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Initialize Adafruit requests session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Number of readings
readings_count = 4
duration = 6

try:
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi connected!")

for i in range(readings_count):
    print("Starting Reading", i + 1)
    start_time = time.monotonic()
    data = []
    while time.monotonic() - start_time < duration:
        elapsed_time = time.monotonic() - start_time
        accel_x, accel_y, accel_z = mpu.acceleration
        gyro_x, gyro_y, gyro_z = mpu.gyro
        reading = {
            "id": i + 1,  # Incrementing ID for each set of readings
            "t(s)": elapsed_time,
            "aX": accel_x,
            "aY": accel_y,
            "aZ": accel_z,
            "gX": gyro_x,
            "gY": gyro_y,
            "gZ": gyro_z
        }
        data.append(reading)
        print("%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (
            elapsed_time, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z))
        time.sleep(0.01)
    print("End of Reading", i + 1)

    # Send readings to Supabase
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.post(TABLE_URL, headers=headers, json=data)
    if response.status_code == 201:
        print("Data sent successfully!")
    else:
        print("Failed to send data:", response.text)
    response.close()

    if i < readings_count - 1:
        print("Preparing for the next reading...")
        time.sleep(2)

# Close the requests session
# requests.close()