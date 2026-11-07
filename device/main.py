# MicroPython for ESP32 + DHT22 (works in the Wokwi simulator too). Prints one JSON line every 10 seconds.
import time
import json
import dht
from machine import Pin

sensor = dht.DHT22(Pin(15))
while True:
    try:
        sensor.measure()
        # "t" counts from 2000 until the clock is set (ntptime.settime() after Wi-Fi): milestone 4 uses the time it was received.
        print(json.dumps({"t": time.time(), "temp_c": sensor.temperature(), "humidity_pct": sensor.humidity(), "device": "room1"}))
    except OSError:
        pass  # milestone 1: retry once, and never save a fake 0
    time.sleep(10)
