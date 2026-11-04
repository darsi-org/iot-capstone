# MicroPython for ESP32 + DHT22 (works in the Wokwi simulator too). Prints one JSON line every 10 seconds.
import time
import json
import dht
from machine import Pin

sensor = dht.DHT22(Pin(15))
while True:
    try:
        sensor.measure()
        print(json.dumps({"t": time.time(), "temp_c": sensor.temperature(), "humidity_pct": sensor.humidity(), "device": "room1"}))
    except OSError:
        pass  # milestone 1: retry once, and never save a fake 0
    time.sleep(10)
