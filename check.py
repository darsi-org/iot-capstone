#!/usr/bin/env python3
"""Darsi capstone check.

Looks at the files in this folder and writes darsi-check.json, which you send to Darsi with your milestone.
It only reads files: it never uploads anything, and Darsi never runs your code. Standard library only.

    python check.py              # every milestone
    python check.py --milestone m2
    python check.py --strict     # exit 1 if a milestone you asked for fails (used by CI if you want it)
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

SPEC = json.loads(r'''{
 "track": "iot",
 "repo": "iot-capstone",
 "milestones": [
  {
   "id": "m1",
   "en": "Milestone 1: Read a sensor (Wokwi first)",
   "ar": "المرحلة ١: اقرا حسّاس (Wokwi أولًا)",
   "checks": [
    {
     "type": "lines",
     "path": "data/readings.jsonl",
     "min": 180,
     "en": "30 minutes of readings (180 lines) in data/readings.jsonl",
     "ar": "٣٠ دقيقة من القراءات (١٨٠ سطرًا) في data/readings.jsonl"
    }
   ]
  },
  {
   "id": "m2",
   "en": "Milestone 2: Send it over MQTT",
   "ar": "المرحلة ٢: ابعتها عبر MQTT",
   "checks": [
    {
     "type": "lines",
     "path": "data/mqtt.jsonl",
     "min": 30,
     "en": "Readings heard over MQTT in data/mqtt.jsonl",
     "ar": "قراءات سُمعت عبر MQTT في data/mqtt.jsonl"
    },
    {
     "type": "text",
     "path": ".gitignore",
     "needles": [
      "secrets.py"
     ],
     "en": ".gitignore leaves out secrets.py",
     "ar": "يستبعد .gitignore الملف secrets.py"
    },
    {
     "type": "nosecret",
     "en": "No passwords, tokens or keys are in the files",
     "ar": "لا توجد كلمات سر أو رموز أو مفاتيح في الملفات"
    }
   ]
  },
  {
   "id": "m3",
   "en": "Milestone 3: Store and graph it",
   "ar": "المرحلة ٣: خزّن وارسم",
   "checks": [
    {
     "type": "file",
     "path": "docs/dashboard.png",
     "en": "A dashboard screenshot in docs/",
     "ar": "لقطة للوحة المتابعة في docs/"
    },
    {
     "type": "file",
     "path": "flows/dashboard.json",
     "en": "flows/dashboard.json exists",
     "ar": "الملف flows/dashboard.json موجود"
    }
   ]
  },
  {
   "id": "m4",
   "en": "Milestone 4: Check it against Open-Meteo",
   "ar": "المرحلة ٤: قارنها بـ Open-Meteo",
   "checks": [
    {
     "type": "json",
     "path": "results/compare.json",
     "key": "mean_diff",
     "en": "results/compare.json has the mean difference",
     "ar": "يحتوي results/compare.json على متوسط الفرق"
    },
    {
     "type": "json",
     "path": "results/compare.json",
     "key": "max_diff",
     "en": "…and the largest difference",
     "ar": "…وأكبر فرق"
    }
   ]
  },
  {
   "id": "m5",
   "en": "Milestone 5: Alerts, a case and v1.0",
   "ar": "المرحلة ٥: تنبيهات وعلبة وv1.0",
   "checks": [
    {
     "type": "file",
     "path": "SAFETY.md",
     "en": "SAFETY.md exists",
     "ar": "الملف SAFETY.md موجود"
    },
    {
     "type": "glob",
     "pattern": "tests/test_alert*.py",
     "min": 1,
     "en": "Tests for the alert logic",
     "ar": "اختبارات لمنطق التنبيه"
    },
    {
     "type": "nosecret",
     "en": "No passwords, tokens or keys are in the files",
     "ar": "لا توجد كلمات سر أو رموز أو مفاتيح في الملفات"
    }
   ]
  }
 ]
}''')

LOCAL = re.compile(r"^(https?://)?(localhost|127(\.\d{1,3}){3}|\[::1\]|[a-z0-9-]+\.localhost)(:\d+)?(/.*)?$", re.I)
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|(password|passwd|api_key|token)\s*=\s*['\"][^'\"\s]{4,}['\"])", re.I)
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".ipynb_checkpoints"}


def here(p):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), p)


def read(p):
    try:
        with open(here(p), encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def load_json(p):
    t = read(p)
    if t is None:
        return None
    try:
        return json.loads(t)
    except ValueError:
        return None


def files(pattern):
    return [f for f in glob.glob(here(pattern), recursive=True) if os.path.isfile(f)]


def dig(obj, key):
    for k in key.split("."):
        if not isinstance(obj, dict) or k not in obj:
            return None
        obj = obj[k]
    return obj


def ports_local(p):
    t = read(p)
    if t is None:
        return False
    found = re.findall(r"^\s*-\s*['\"]?([^'\"\s#]+:\d+(?::\d+)?)['\"]?\s*$", t, re.M)
    mapped = [x for x in found if re.match(r"^[\w.\[\]:]*\d+:\d+$", x)]
    return bool(mapped) and all(x.startswith("127.0.0.1:") for x in mapped)


def scan_meta(d):
    m = load_json(d + "/scan-meta.json")
    if not isinstance(m, dict):
        return None
    return {"tool": str(m.get("tool", ""))[:40], "target": str(m.get("target", ""))[:300]}


def no_secrets():
    root = here(".")
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith((".png", ".jpg", ".duckdb", ".db", ".zip", ".pdf")) or fn in ("check.py", "secrets.py", ".env"):
                continue
            try:
                with open(os.path.join(dp, fn), encoding="utf-8", errors="ignore") as f:
                    if SECRET.search(f.read(200000)):
                        return False
            except OSError:
                pass
    return True


def run(c):
    k = c["type"]
    if k == "file":
        return os.path.isfile(here(c["path"]))
    if k == "glob":
        return len(files(c["pattern"])) >= c.get("min", 1)
    if k == "text":
        t = (read(c["path"]) or "").lower()
        return bool(t) and all(n.lower() in t for n in c["needles"])
    if k == "regex":
        t = read(c["path"])
        return t is not None and len(re.findall(c["pattern"], t, re.M | re.I)) >= c.get("min", 1)
    if k == "lines":
        t = read(c["path"]) or ""
        return len([x for x in t.splitlines() if x.strip()]) >= c["min"]
    if k == "json":
        v = dig(load_json(c["path"]), c["key"])
        if "eq" in c:
            return v == c["eq"]
        return v is not None
    if k == "ports":
        return ports_local(c["path"])
    if k == "scan":
        m = scan_meta(c["dir"])
        return bool(m) and m["tool"] == c["tool"] and bool(LOCAL.match(m["target"]))
    if k == "nosecret":
        return no_secrets()
    raise ValueError(k)


def metrics():
    out = {}
    for f in sorted(files("results/*.json"))[:20]:
        try:
            with open(f, encoding="utf-8") as h:
                d = json.load(h)
        except (OSError, ValueError):
            continue
        name = os.path.splitext(os.path.basename(f))[0]
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, (int, float, bool)) or (isinstance(v, str) and len(v) < 200):
                    out[f"{name}.{k}"[:60]] = v
    return dict(list(out.items())[:40])


def main(argv):
    only = argv[argv.index("--milestone") + 1] if "--milestone" in argv else None
    strict = "--strict" in argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = {"darsi": 1, "track": SPEC["track"], "starter": SPEC["repo"], "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "milestones": {}}
    failed = False
    for m in SPEC["milestones"]:
        if only and m["id"] != only:
            continue
        checks = []
        for i, c in enumerate(m["checks"], 1):
            try:
                ok = bool(run(c))
            except Exception:  # a broken file is a failed check, never a crash
                ok = False
            checks.append({"id": f"{m['id']}-{i}", "ok": ok, "en": c["en"], "ar": c["ar"]})
        ok = all(x["ok"] for x in checks)
        failed = failed or not ok
        result["milestones"][m["id"]] = {"ok": ok, "checks": checks}
        print(f"\n{m['id']}  {'PASS' if ok else 'not yet'}  {m['en']}")
        print(f"    {'ناجح' if ok else 'لم يكتمل بعد'}  {m['ar']}")
        for x in checks:
            mark = "[x]" if x["ok"] else "[ ]"
            print(f"  {mark} {x['en']}")
            print(f"      {x['ar']}")
    result["metrics"] = metrics()
    scans = [s for s in (scan_meta(d) for d in ("reports/before", "reports/after")) if s]
    result["scans"] = scans
    for s in scans:
        if not LOCAL.match(s["target"]):
            print(f"\n!! A scan targeted {s['target']}: only this computer (localhost) is allowed.")
            print("!! استهدف أحد الفحوص عنوانًا غير هذا الكمبيوتر: المسموح به هو localhost فقط.")
    with open(here("darsi-check.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\nWrote darsi-check.json: send it with your milestone on Darsi.")
    print("كُتب الملف darsi-check.json: أرسله مع مرحلتك على درسي.")
    return 1 if strict and failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
