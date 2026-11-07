# Wokwi path (no hardware)

1. Open https://wokwi.com and sign in free.
2. Start a new ESP32 project with MicroPython: https://wokwi.com/projects/new/micropython-esp32
3. Add a **DHT22** sensor (the blue + button) and wire it: VCC to 3V3, GND to GND, SDA (data) to pin D15, which `device/main.py` reads.
4. Paste `device/main.py` into main.py and press the green play button. A JSON line appears in the serial monitor every 10 seconds.
5. Click the DHT22 while it runs and change the temperature and humidity, so your 30 minutes have some variety.
6. Copy about 180 JSON lines from the serial monitor into `data/readings.jsonl`, one per line.

For milestone 2 (MQTT), the simulated board joins the Wi-Fi network `Wokwi-GUEST` (no password) and reaches the internet, but not your computer. So it publishes to the public test broker test.mosquitto.org on port 1883, on a topic with a nickname such as `darsi/<nickname>/room1`, never your name: anyone can read a public broker.

Hardware is optional. Wokwi is first-class for this capstone.
