"""Milestone 3: read data/mqtt.jsonl into data/readings.db (SQLite, built into Python), so the history survives restarts.

Keep one row per reading (time received, device, temp_c, humidity_pct), skip lines that aren't valid JSON,
and don't add a reading twice when you run it again.
"""
