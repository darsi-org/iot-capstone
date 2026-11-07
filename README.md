# Capstone: a classroom weather station


> **Darsi briefs are short on purpose.** The in-app lesson shows tight numbered clicks. This README keeps the full commands, error fixes, and background for each milestone — open the matching **Milestone N** section when you need detail.

Build a classroom weather station: an ESP32 with MicroPython, or the free Wokwi simulator if you have no board, MQTT, a Node-RED dashboard, a check against Open-Meteo, and a safe heat alert with SAFETY.md — USB power only.

[العربية](README.ar.md)

## What you will be able to do

- Run real free tools from a laptop or Codespaces
- Finish five milestones, each with checks you can self-verify
- Leave with a portfolio piece: a report, demo or tool tagged v1.0
- **Darsi never runs your code** — it reads your link and check file, then an advisory review

## Install once

### Windows

1. Install Python 3.12: open PowerShell and run `winget install Python.Python.3.12`
2. Install Git: `winget install Git.Git`
3. Install VS Code from https://code.visualstudio.com (free)
4. On GitHub, open https://github.com/darsi-org/iot-capstone and press **Use this template** to make your own copy. Then clone your copy, not darsi-org's: `git clone https://github.com/<your-username>/iot-capstone.git`
5. Open a new PowerShell, go into the folder with `cd iot-capstone`, and run these lines one at a time:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python check.py
   ```

   If PowerShell says running scripts is disabled on this system, you don't need to change any setting: use Command Prompt and run `.venv\Scripts\activate.bat` instead, or skip activating and start every command with `.venv\Scripts\python` (for example `.venv\Scripts\python -m pip install -r requirements.txt`, then `.venv\Scripts\python check.py`).

### Mac

1. Install Homebrew from https://brew.sh if you don't have it
2. Install Python and Git: `brew install python@3.12 git`
3. Install VS Code from https://code.visualstudio.com
4. On GitHub, open https://github.com/darsi-org/iot-capstone, press **Use this template**, then clone your copy: `git clone https://github.com/<your-username>/iot-capstone.git`
5. In Terminal, go into the folder with `cd iot-capstone` and run:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python check.py
   ```

### Codespaces

No computer of your own? Use GitHub Codespaces, from a borrowed laptop too: open your copy → **Code** → **Codespaces** → **Create codespace**. Python and Git are already there. In its terminal, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python check.py
```

A phone browser is enough to read the results.

## Start

Press **Use this template** on https://github.com/darsi-org/iot-capstone, clone your copy, then follow milestone 1.

## Milestones

### m1: Read a sensor (Wokwi first) (3 hours)

#### Why this matters
No board? Wokwi simulates ESP32 + DHT22 in the browser for free. Hardware is optional, not a gate.

#### Tools for this milestone
- **Wokwi** — ESP32 + DHT22 in the browser. Get it: https://wokwi.com — free account
- **MicroPython** — Python for microcontrollers. Get it: built into Wokwi; for a real board, https://micropython.org/download/ESP32_GENERIC/

#### Do this
1. Set up your copy as in **Install once** (your copy, not darsi-org's). Then make the Wokwi project as in [README.wokwi.md](README.wokwi.md), or flash MicroPython on a real ESP32.
2. Edit device/main.py: read temp and humidity every 10 seconds as JSON lines. Retry on failure; never save a fake 0.
3. Capture ~30 minutes into data/readings.jsonl (simulator: change values; hardware: leave running).
4. Run python check.py --milestone m1.

#### You know you're done when
- ≥180 lines in data/readings.jsonl
- m1 passes

#### If something goes wrong
- **Wokwi project won't open** → Sign in free at https://wokwi.com and follow README.wokwi.md step by step
- **Sensor returns None** → Retry once after 2 seconds; skip the reading if still failing
- **Too few lines** → 10-second period × 30 minutes ≈ 180 lines; don't sleep longer

#### What you should understand
You can read a sensor on a simulator or board and keep honest gaps instead of fake zeros.

**Hand in:** device/main.py, data/readings.jsonl, and darsi-check.json that passes m1.

### m2: Send it over MQTT (3 hours)

#### Why this matters
MQTT is how many small devices talk. Secrets never belong in Git.

#### Tools for this milestone
- **test.mosquitto.org** — a public test MQTT broker (Mosquitto), port 1883, no account. Get it: nothing to install; a board in Wokwi and a real board on Wi-Fi both reach it
- **umqtt.simple / paho-mqtt** — publish and subscribe. Get it: umqtt.simple is built into MicroPython on the board (and in Wokwi); paho-mqtt, for tools/listen.py on your computer, is in requirements.txt

#### Do this
1. Use the public test broker test.mosquitto.org, port 1883, with or without a board. In Wokwi the board joins the Wi-Fi network Wokwi-GUEST (no password); a real board joins your Wi-Fi, with its name and password in device/secrets.py (copy device/secrets.example.py). Neither can reach a broker on your computer's localhost, so this starter has no local broker.
2. Publish each reading to `darsi/<nickname>/room1`. Anyone can read a public broker: use a nickname, not your name, and send only room readings. Write tools/listen.py: it subscribes to `darsi/<nickname>/#` on the same broker and appends each message to data/mqtt.jsonl, with the time your computer received it (a real board's clock starts in 2000 until it is set).
3. Keep Wi-Fi password in device/secrets.py listed in .gitignore. Run python check.py --milestone m2.

#### You know you're done when
- data/mqtt.jsonl has ≥30 lines
- No secrets committed
- m2 passes

#### If something goes wrong
- **Nothing arrives in tools/listen.py** → Both sides must use test.mosquitto.org, port 1883, and the same topic; topics are case-sensitive
- **Your network blocks port 1883** → Connect tools/listen.py over WebSockets instead: pass `transport="websockets"` when you create the paho client, and use test.mosquitto.org port 8080. A board in Wokwi still publishes on 1883
- **Password committed by mistake** → Remove from history, rotate the password, keep secrets.py ignored

#### What you should understand
You can publish sensor data over MQTT and keep credentials out of the repository.

**Hand in:** Your publisher (device/main.py), tools/listen.py, data/mqtt.jsonl, and darsi-check.json that passes m2.

### m3: Store and graph it (3 hours)

#### Why this matters
Numbers become useful when a class can read them in ten seconds.

#### Tools for this milestone
- **Node-RED** — bilingual dashboard. Get it: docker compose in the starter (http://127.0.0.1:1880), with Docker Desktop (https://www.docker.com/products/docker-desktop/) or in Codespaces. Grafana isn't included; Node-RED is enough
- **SQLite** — keeps history across restarts. Get it: built into Python; tools/store.py has the outline

#### Do this
1. Start Node-RED with `docker compose up -d` and open http://127.0.0.1:1880. In Codespaces, open the Ports tab, find 1880 and press the globe icon. Add the dashboard nodes (Menu → Manage palette → Install → @flowfuse/node-red-dashboard). In an **mqtt in** node, add the broker test.mosquitto.org, port 1883, and the topic `darsi/<nickname>/#`, the same as tools/listen.py.
2. Store readings with tools/store.py (write it from its outline) or let Node-RED write them.
3. Dashboard: current temp, last 24 hours, daily min/max, labels in Arabic and English. Screenshot docs/dashboard.png. Export the flow (Menu → Export → Download) and save it as flows/dashboard.json.
4. Run python check.py --milestone m3.

#### You know you're done when
- docs/dashboard.png exists
- flows/dashboard.json exists
- m3 passes

#### If something goes wrong
- **Node-RED empty** → Check the mqtt in node: test.mosquitto.org, port 1883, your exact topic; and check that the board is publishing
- **Units missing on chart** → Label every series with °C or %

#### What you should understand
You can store readings and build a bilingual dashboard a classmate can read fast.

**Hand in:** Storage code, dashboard flow, docs/dashboard.png, and darsi-check.json that passes m3.

### m4: Check it against Open-Meteo (3 hours)

#### Why this matters
Is your sensor right? Compare with a trusted outdoor source and explain the gap.

#### Tools for this milestone
- **Open-Meteo** — hourly outdoor temperature API. Get it: https://open-meteo.com — free, no key

#### Do this
1. For 24 hours put the sensor outdoors in the shade. No board? Wokwi's sensor only reports the values you set, so comparing it proves nothing: use a real 24-hour log from a classmate's or your teacher's board, or compare Open-Meteo with a nearby weather station's hourly readings from https://meteostat.net (Cairo: the airport station, HECA; use its Export button).
2. Right after those 24 hours, run `python tools/open_meteo.py <lat> <lon>` for your town (Cairo is the default, 30.04 31.24). It saves the last two days, hour by hour, in data/open_meteo.json.
3. Compare hour by hour in the same timezone (Africa/Cairo). Save mean and max diff in results/compare.json. Explain sun, walls, ±0.5 °C sensor accuracy.
4. Run python check.py --milestone m4.

#### You know you're done when
- results/compare.json has mean_diff and max_diff
- m4 passes

#### If something goes wrong
- **Timezone mismatch** → Ask Open-Meteo for timezone=Africa/Cairo or convert both to UTC
- **Your readings' times are in the year 2000** → The board's clock was never set: use the time tools/listen.py received each message, or call ntptime.settime() on the board once Wi-Fi is up
- **Huge afternoon gap** → Likely sun or warm wall; move to shade and re-measure

#### What you should understand
You can validate a sensor against an open weather API and explain systematic gaps.

**Hand in:** data/open_meteo.json (from tools/open_meteo.py), results/compare.json, a comparison chart or table, and darsi-check.json that passes m4.

### m5: A safe heat alert and v1.0 (3 hours)

#### Why this matters
A classroom device must be useful and safe: USB only, no mains wiring.

#### Tools for this milestone
- **Node-RED alert / LED** — fires once with a pause. Get it: flow + device pin
- **SAFETY.md** — USB only, dry, ventilated. Get it: you write it

#### Do this
1. Add a heat alert that fires once when the room stays above 32 °C for 10 minutes (a message to yourself and an LED on), then waits 30 minutes before it can fire again, so it doesn't repeat every reading.
2. Write SAFETY.md: USB only, no mains, ventilated case away from water.
3. Add tests for the alert logic in tests/test_alert.py (check.py looks for tests/test_alert*.py); CI runs them. Tag v1.0. Run python check.py --milestone m5.

#### You know you're done when
- SAFETY.md exists
- Alert tests exist
- m5 passes

#### If something goes wrong
- **Alert spam** → Set a cooldown of 30 minutes after firing
- **Tempted to wire mains power** → Stop. USB only for this project; ask a qualified adult for anything else

#### What you should understand
You can ship a safe classroom alert with tested logic and written safety rules.

**Hand in:** Alert flow, SAFETY.md, tests/test_alert.py, green Actions, a v1.0 release, darsi-check.json that passes m5, and your explanation.

## The check

Run `python check.py` or `python check.py --milestone m2`. It only reads files, writes `darsi-check.json`, and prints English and Arabic. It uploads nothing.

## Review on Darsi

Send your repository link and `darsi-check.json` with each milestone on Darsi. Darsi reads your latest Actions run and release from GitHub's public API, adds an advisory AI review, then your teacher or the Darsi team reviews it. **Darsi never runs your code.**

## Safety

USB power only. No mains wiring. Keep the board in a ventilated case, away from water.

## Licence

MIT — see [LICENSE](LICENSE).
