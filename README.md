# Capstone: a classroom weather station

Build a classroom weather and air station: ESP32 with MicroPython or the free Wokwi simulator first, MQTT, Node-RED or Grafana graphs, comparison with Open-Meteo, and a heat alert with SAFETY.md — USB power only.

[العربية](README.ar.md)

## What you will be able to do

- Run real free tools from a laptop or Codespaces
- Finish five milestones, each with checks you can self-verify
- Leave with a portfolio piece: a report, demo or tool tagged v1.0
- **Darsi never runs your code** — it reads your link and check file, then an advisory review

## Install once

### Windows

1. Install Python 3.12: open PowerShell and run winget install Python.Python.3.12
2. Install Git: winget install Git.Git
3. Install VS Code from https://code.visualstudio.com (free)
4. On GitHub, open https://github.com/darsi-org/iot-capstone and press Use this template, then Clone your copy
5. In the project folder run:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python check.py

### Mac

1. Install Homebrew from https://brew.sh if you don't have it
2. brew install python@3.12 git
3. Install VS Code from https://code.visualstudio.com
4. On GitHub open https://github.com/darsi-org/iot-capstone → Use this template → clone your copy
5. In the project folder run:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python check.py

### Codespaces / Colab

No computer of your own? Use GitHub Codespaces: open your copy → Code → Codespaces → Create codespace. Everything installs there. Or open a notebook in Google Colab, run the first cell that clones your repo, then run python check.py. Both work from a borrowed laptop; a phone browser is enough to read results.

## Start

Press **Use this template** on https://github.com/darsi-org/iot-capstone, clone your copy, then follow milestone 1.

## Milestones

### m1: Read a sensor (Wokwi first) (3 hours)

## Why this matters
No board? Wokwi simulates ESP32 + DHT22 in the browser for free. Hardware is optional, not a gate.

## Tools for this milestone
- **Wokwi** — ESP32 + DHT22 in the browser. Get it: https://wokwi.com — free account
- **MicroPython** — Python for microcontrollers. Get it: firmware link in README

## Do this
1. Clone https://github.com/darsi-org/iot-capstone. Open the Wokwi project linked in README, or flash a real ESP32.
2. Edit device/main.py: read temp and humidity every 10 seconds as JSON lines. Retry on failure; never save a fake 0.
3. Capture ~30 minutes into data/readings.jsonl (simulator: change values; hardware: leave running).
4. Run python check.py --milestone m1.

## You know you're done when
- ≥180 lines in data/readings.jsonl
- m1 passes

## If something goes wrong
- **Wokwi project won't open** → Use the public template link in README; sign in free
- **Sensor returns None** → Retry once after 2 seconds; skip the reading if still failing
- **Too few lines** → 10-second period × 30 minutes ≈ 180 lines; don't sleep longer

## What you should understand
You can read a sensor on a simulator or board and keep honest gaps instead of fake zeros.

**Hand in:** device/main.py, data/readings.jsonl, and darsi-check.json that passes m1.

### m2: Send it over MQTT (3 hours)

## Why this matters
MQTT is how many small devices talk. Secrets never belong in Git.

## Tools for this milestone
- **Mosquitto** — MQTT broker. Get it: docker compose in the starter, or a public test broker named in README for Wokwi
- **umqtt.simple / paho-mqtt** — publish and subscribe. Get it: device vs PC

## Do this
1. Start broker: docker compose up -d   (or use the public test broker for the simulator).
2. Publish each reading to darsi/<your-name>/room1. Write tools/listen.py that appends to data/mqtt.jsonl.
3. Keep Wi-Fi password in device/secrets.py listed in .gitignore. Run python check.py --milestone m2.

## You know you're done when
- data/mqtt.jsonl has ≥30 lines
- No secrets committed
- m2 passes

## If something goes wrong
- **Can't connect from Wokwi to local Mosquitto** → Use the public test broker named in README for the simulator path
- **Password committed by mistake** → Remove from history, rotate the password, keep secrets.py ignored

## What you should understand
You can publish sensor data over MQTT and keep credentials out of the repository.

**Hand in:** Publisher, tools/listen.py, data/mqtt.jsonl, and darsi-check.json that passes m2.

### m3: Store and graph it (3 hours)

## Why this matters
Numbers become useful when a class can read them in ten seconds.

## Tools for this milestone
- **Node-RED or Grafana** — bilingual dashboard. Get it: docker compose in the starter
- **SQLite** — keeps history across restarts. Get it: tools/store.py

## Do this
1. Start Node-RED (or Grafana) from docker compose. Import flows/dashboard.json.
2. Store readings with tools/store.py or let Node-RED write them.
3. Dashboard: current temp, last 24 hours, daily min/max, labels in Arabic and English. Screenshot docs/dashboard.png.
4. Run python check.py --milestone m3.

## You know you're done when
- docs/dashboard.png exists
- flows/dashboard.json exists
- m3 passes

## If something goes wrong
- **Node-RED empty** → Check MQTT topic spelling and that listen/store is running
- **Units missing on chart** → Label every series with °C or %

## What you should understand
You can store readings and build a bilingual dashboard a classmate can read fast.

**Hand in:** Storage code, dashboard flow, docs/dashboard.png, and darsi-check.json that passes m3.

### m4: Check it against Open-Meteo (3 hours)

## Why this matters
Is your sensor right? Compare with a trusted outdoor source and explain the gap.

## Tools for this milestone
- **Open-Meteo** — hourly outdoor temperature API. Get it: https://open-meteo.com — free, no key

## Do this
1. Run: python tools/open_meteo.py <lat> <lon> for your town (Cairo default 30.04 31.24).
2. For 24 hours put the sensor outside in the shade, or use the simulator's outdoor values.
3. Compare hour by hour in the same timezone (Africa/Cairo). Save mean and max diff in results/compare.json. Explain sun, walls, ±0.5 °C sensor accuracy.
4. Run python check.py --milestone m4.

## You know you're done when
- results/compare.json has mean_diff and max_diff
- m4 passes

## If something goes wrong
- **Timezone mismatch** → Ask Open-Meteo for timezone=Africa/Cairo or convert both to UTC
- **Huge afternoon gap** → Likely sun or warm wall; move to shade and re-measure

## What you should understand
You can validate a sensor against an open weather API and explain systematic gaps.

**Hand in:** tools/open_meteo.py output, comparison chart/table, and darsi-check.json that passes m4.

### m5: Alerts, a case and v1.0 (3 hours)

## Why this matters
A classroom device must be useful and safe: USB only, no mains wiring.

## Tools for this milestone
- **Node-RED alert / LED** — fires once with a pause. Get it: flow + device pin
- **SAFETY.md** — USB only, dry, ventilated. Get it: you write it

## Do this
1. Alert when room >32 °C for 10 minutes: message to yourself + LED on. Add a pause so it does not repeat every reading.
2. Write SAFETY.md: USB only, no mains, ventilated case away from water.
3. Add tests for alert logic; CI runs them. Tag v1.0. Run python check.py --milestone m5.

## You know you're done when
- SAFETY.md exists
- Alert tests exist
- m5 passes

## If something goes wrong
- **Alert spam** → Set a cooldown of 30 minutes after firing
- **Tempted to wire mains power** → Stop. USB only for this project; ask a qualified adult for anything else

## What you should understand
You can ship a safe classroom alert with tested logic and written safety rules.

**Hand in:** Alert flow, SAFETY.md, tests, green Actions, v1.0, darsi-check.json that passes m5, and your explanation.

## The check

Run `python check.py` or `python check.py --milestone m2`. It only reads files, writes `darsi-check.json`, and prints English and Arabic. It uploads nothing.

## Review on Darsi

Send your repository link and `darsi-check.json` with each milestone on Darsi. Darsi reads your latest Actions run and release from GitHub's public API, adds an advisory AI review, then your teacher or the Darsi team reviews it. **Darsi never runs your code.**

## Safety

USB power only. No mains wiring. Keep the board in a ventilated case, away from water.

## Licence

MIT — see [LICENSE](LICENSE).
