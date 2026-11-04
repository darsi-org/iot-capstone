"""Fetch hourly outdoor temperature from Open-Meteo (free, no key) for your town. Usage: python tools/open_meteo.py 30.04 31.24"""
import json
import pathlib
import sys

import requests

lat, lon = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("30.04", "31.24")
r = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": lat, "longitude": lon, "hourly": "temperature_2m", "past_days": 2, "timezone": "Africa/Cairo"}, timeout=30)
r.raise_for_status()
pathlib.Path("data").mkdir(exist_ok=True)
pathlib.Path("data/open_meteo.json").write_text(json.dumps(r.json()), encoding="utf-8")
print("saved data/open_meteo.json")
