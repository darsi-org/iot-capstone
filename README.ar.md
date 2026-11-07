<div dir="rtl">

# المشروع الختامي: محطة طقس للفصل


> **ملخص درسي قصير عن قصد.** الدرس في التطبيق بيعرض خطوات ضغط مختصرة. الـ README ده بيحفظ الأوامر الكاملة وإصلاح الأخطاء والخلفية لكل مرحلة — افتح قسم **المرحلة N** لما تحتاج تفاصيل.

ابنِ محطة طقس للفصل: ESP32 بـ MicroPython، أو محاكي Wokwi المجاني لو مفيش بورد، وMQTT، ولوحة Node-RED، ومقارنة مع Open-Meteo، وتنبيه حرارة آمن مع SAFETY.md — تغذية USB بس.

[English](README.md)

## هتقدر تعمل إيه

- تشغّل أدوات حقيقية مجانية من اللابتوب أو Codespaces
- تخلّص خمس مراحل، كل مرحلة ليها فحص تقدر تتأكد منه بنفسك
- تطلع بقطعة بورتفوليو: تقرير أو عرض أو أداة بإصدار v1.0
- **درسي مش بيشغّل كودك أبدًا** — بيقرا الرابط وملف الفحص وبمراجعة استشارية

## ثبّت مرة واحدة

### ويندوز

1. ثبّت Python 3.12: افتح PowerShell واكتب `winget install Python.Python.3.12`
2. ثبّت Git: `winget install Git.Git`
3. ثبّت VS Code من https://code.visualstudio.com مجانًا
4. على GitHub افتح https://github.com/darsi-org/iot-capstone واضغط **Use this template** عشان تعمل نسختك. وبعدين اعمل Clone لنسختك أنت، مش نسخة darsi-org: `git clone https://github.com/<your-username>/iot-capstone.git`
5. افتح PowerShell جديد، وادخل الفولدر بـ `cd iot-capstone`، وشغّل السطور دي واحد واحد:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python check.py
   ```

   لو PowerShell قال إن تشغيل السكربتات متقفل على الجهاز ده، مش محتاج تغيّر أي إعداد: استخدم Command Prompt وشغّل `.venv\Scripts\activate.bat` بداله، أو من غير تفعيل ابدأ كل أمر بـ `.venv\Scripts\python` (مثلًا `.venv\Scripts\python -m pip install -r requirements.txt`، وبعدين `.venv\Scripts\python check.py`).

### ماك

1. ثبّت Homebrew من https://brew.sh لو مش متثبت
2. ثبّت Python وGit: `brew install python@3.12 git`
3. ثبّت VS Code من https://code.visualstudio.com
4. على GitHub افتح https://github.com/darsi-org/iot-capstone واضغط **Use this template**، وبعدين اعمل Clone لنسختك: `git clone https://github.com/<your-username>/iot-capstone.git`
5. في Terminal ادخل الفولدر بـ `cd iot-capstone` وشغّل:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python check.py
   ```

### Codespaces

معندكش كمبيوتر؟ استخدم GitHub Codespaces، حتى من لابتوب مستعار: افتح نسختك → **Code** → **Codespaces** → **Create codespace**. Python وGit موجودين أصلًا. في الـ terminal بتاعه شغّل:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python check.py
```

متصفح الموبايل يكفي تقرا النتائج.

## البداية

اضغط **Use this template** على https://github.com/darsi-org/iot-capstone، Clone نسختك، وبعدين اتبع المرحلة ١.

## المراحل

### m1: اقرا حسّاس (Wokwi أولًا) (3 ساعات)

#### ليه ده مهم
معندكش بورد؟ Wokwi بيحاكي ESP32 + DHT22 في المتصفح مجانًا. العتاد اختياري، مش بوابة.

#### الأدوات للمرحلة دي
- **Wokwi** — ESP32 مع DHT22 في المتصفح. هتجيبه من: https://wokwi.com — حساب مجاني
- **MicroPython** — Python للمتحكمات الدقيقة. هتجيبه من: موجود في Wokwi؛ ولبورد حقيقي https://micropython.org/download/ESP32_GENERIC/

#### اعمل كده
1. جهّز نسختك زي **ثبّت مرة واحدة** (نسختك أنت، مش نسخة darsi-org). وبعدين اعمل مشروع Wokwi زي [README.wokwi.md](README.wokwi.md)، أو ارفع MicroPython على ESP32 حقيقية.
2. عدّل device/main.py: اقرا الحرارة والرطوبة كل ١٠ ثواني كسطور JSON. عيد المحاولة عند الفشل؛ متحفظش ٠ مزيفة.
3. التقط حوالي ٣٠ دقيقة في data/readings.jsonl (المحاكي: غيّر القيم؛ العتاد: سيبه شغّال).
4. شغّل python check.py --milestone m1.

#### هتبقى خلصت لما
- ≥١٨٠ سطر في data/readings.jsonl
- m1 ناجحة

#### لو حاجة وقفت
- **مشروع Wokwi مش بيفتح** → سجّل مجانًا على https://wokwi.com وامشي على README.wokwi.md خطوة خطوة
- **الحسّاس بيرجع None** → حاول مرة بعد ثانيتين؛ تخطّى القراءة لو لسه فشلت
- **سطور قليلة** → فترة ١٠ ثواني × ٣٠ دقيقة ≈ ١٨٠ سطر؛ متنمش أطول

#### إيه اللي لازم تفهمه
تقدر تقرا حسّاس على محاكي أو بورد وتحافظ على فجوات صادقة بدل أصفار مزيفة.

**المطلوب تسليمه:** device/main.py، وdata/readings.jsonl، وdarsi-check.json بيجتاز m1.

### m2: ابعتها عبر MQTT (3 ساعات)

#### ليه ده مهم
MQTT هو طريقة أجهزة صغيرة كتير بتتكلم. الأسرار ملهاش مكان في Git.

#### الأدوات للمرحلة دي
- **test.mosquitto.org** — وسيط MQTT عام للتجربة (Mosquitto)، على المنفذ 1883، من غير حساب. هتجيبه من: مفيش حاجة تتثبّت؛ البورد اللي في Wokwi والبورد الحقيقي على الواي فاي الاتنين بيوصلوله
- **umqtt.simple / paho-mqtt** — نشر واشتراك. هتجيبه من: umqtt.simple جوّه MicroPython على البورد (وفي Wokwi)؛ وpaho-mqtt، عشان tools/listen.py على جهازك، موجود في requirements.txt

#### اعمل كده
1. استخدم وسيط الاختبار العام test.mosquitto.org على المنفذ 1883، سواء معاك بورد أو لأ. في Wokwi البورد بيدخل شبكة الواي فاي Wokwi-GUEST (من غير كلمة سر)؛ والبورد الحقيقي بيدخل الواي فاي بتاعك، واسمها وكلمة السر بتاعتها في device/secrets.py (انسخه من device/secrets.example.py). ولا واحد فيهم يقدر يوصل لوسيط على localhost بتاع جهازك، عشان كده قالب البداية مفيهوش وسيط محلي.
2. انشر كل قراءة على `darsi/<nickname>/room1`. أي حد يقدر يقرا الوسيط العام: استخدم اسم مستعار مش اسمك، وابعت قراءات الأوضة بس. اكتب tools/listen.py: بيشترك في `darsi/<nickname>/#` على نفس الوسيط، وبيضيف كل رسالة على data/mqtt.jsonl ومعاها الوقت اللي جهازك استلمها فيه (ساعة البورد الحقيقي بتبدأ من سنة ٢٠٠٠ لحد ما تتظبط).
3. خلي كلمة سر الواي فاي في device/secrets.py، اللي .gitignore بيستبعده. شغّل python check.py --milestone m2.

#### هتبقى خلصت لما
- data/mqtt.jsonl فيه ≥٣٠ سطر
- مفيش أسرار متعملها commit
- m2 ناجحة

#### لو حاجة وقفت
- **مفيش حاجة بتوصل لـ tools/listen.py** → الطرفين لازم يستخدموا test.mosquitto.org على المنفذ 1883 ونفس الموضوع بالظبط؛ الموضوع بيفرّق بين الحروف الكبيرة والصغيرة
- **الشبكة عندك قافلة المنفذ 1883** → وصّل tools/listen.py عن طريق WebSockets بدل كده: ابعت `transport="websockets"` وإنت بتعمل عميل paho، واستخدم test.mosquitto.org على المنفذ 8080. والبورد اللي في Wokwi بيفضل ينشر على 1883
- **كلمة سر اتعمل لها commit بالغلط** → شيلها من التاريخ، وغيّر كلمة السر، وخلي secrets.py متجاهَل

#### إيه اللي لازم تفهمه
تقدر تنشر بيانات الحسّاس عبر MQTT وتحافظ على بيانات الدخول برة المستودع.

**المطلوب تسليمه:** الناشر بتاعك (device/main.py)، وtools/listen.py، وdata/mqtt.jsonl، وdarsi-check.json بيجتاز m2.

### m3: خزّن وارسم (3 ساعات)

#### ليه ده مهم
الأرقام بتفيد لما الفصل يقدر يقراها في عشر ثواني.

#### الأدوات للمرحلة دي
- **Node-RED** — لوحة متابعة بلغتين. هتجيبه من: docker compose اللي في قالب البداية (http://127.0.0.1:1880)، مع Docker Desktop (https://www.docker.com/products/docker-desktop/) أو في Codespaces. Grafana مش موجود؛ وNode-RED كفاية
- **SQLite** — بيحافظ على التاريخ بعد إعادة التشغيل. هتجيبه من: جوّه Python؛ وtools/store.py فيه المخطط

#### اعمل كده
1. شغّل Node-RED بـ `docker compose up -d` وافتح http://127.0.0.1:1880. في Codespaces افتح تبويب Ports، ودوّر على 1880 واضغط أيقونة الكرة الأرضية. زوّد عناصر اللوحة (Menu → Manage palette → Install → @flowfuse/node-red-dashboard). في عنصر **mqtt in** زوّد الوسيط test.mosquitto.org على المنفذ 1883، والموضوع `darsi/<nickname>/#`، زي tools/listen.py بالظبط.
2. خزّن القراءات بـ tools/store.py (اكتبه من المخطط اللي فيه) أو سيّب Node-RED يكتب.
3. اللوحة: الحرارة الحالية، وآخر ٢٤ ساعة، وأدنى/أقصى يومي، عناوين بالعربي والإنجليزي. سكرين docs/dashboard.png. صدّر الـ flow (Menu → Export → Download) واحفظه باسم flows/dashboard.json.
4. شغّل python check.py --milestone m3.

#### هتبقى خلصت لما
- docs/dashboard.png موجود
- flows/dashboard.json موجود
- m3 ناجحة

#### لو حاجة وقفت
- **Node-RED فاضي** → راجع عنصر mqtt in: test.mosquitto.org، والمنفذ 1883، والموضوع بتاعك بالظبط؛ واتأكد إن البورد بينشر
- **الوحدات ناقصة على الرسم** → عنون كل سلسلة بـ °C أو %

#### إيه اللي لازم تفهمه
تقدر تخزّن القراءات وتبني لوحة بلغتين زميل يقدر يقراها بسرعة.

**المطلوب تسليمه:** كود التخزين، وتدفّق اللوحة، وdocs/dashboard.png، وdarsi-check.json بيجتاز m3.

### m4: قارنها بـ Open-Meteo (3 ساعات)

#### ليه ده مهم
حسّاسك صح؟ قارن بمصدر خارجي موثوق واشرح الفجوة.

#### الأدوات للمرحلة دي
- **Open-Meteo** — API حرارة خارجية كل ساعة. هتجيبه من: https://open-meteo.com — مجاني ومن غير مفتاح

#### اعمل كده
1. حط الحسّاس برة في الضل لمدة ٢٤ ساعة. مفيش بورد؟ حسّاس Wokwi بيقول بس القيم اللي إنت حاططها، فمقارنته مش بتثبت حاجة: استخدم سجل حقيقي لـ ٢٤ ساعة من بورد زميلك أو مدرّسك، أو قارن Open-Meteo بقراءات محطة أرصاد قريبة كل ساعة من https://meteostat.net (القاهرة: محطة المطار، HECA؛ استخدم زر Export بتاعها).
2. أول ما الـ ٢٤ ساعة يخلصوا، شغّل `python tools/open_meteo.py <lat> <lon>` لمدينتك (القاهرة هي الافتراضي، 30.04 31.24). بيحفظ آخر يومين، ساعة بساعة، في data/open_meteo.json.
3. قارن ساعة بساعة بنفس المنطقة الزمنية. احفظ متوسط وأكبر فرق في results/compare.json. اشرح شمس وجدران ودقة ±٠.٥ درجة.
4. شغّل python check.py --milestone m4.

#### هتبقى خلصت لما
- results/compare.json فيه mean_diff وmax_diff
- m4 ناجحة

#### لو حاجة وقفت
- **اختلاف منطقة زمنية** → اطلب timezone=Africa/Cairo أو حوّل الاتنين لـ UTC
- **أوقات القراءات في سنة ٢٠٠٠** → ساعة البورد متظبطتش: استخدم الوقت اللي tools/listen.py استلم فيه كل رسالة، أو نادِ ntptime.settime() على البورد بعد ما الواي فاي يشتغل
- **فجوة عصر كبيرة** → غالبًا شمس أو جدار دافئ؛ انقل للضل وقيس تاني

#### إيه اللي لازم تفهمه
تقدر تتحقق من حسّاس مقابل API طقس مفتوح وتشرح الفجوات المنتظمة.

**المطلوب تسليمه:** data/open_meteo.json (من tools/open_meteo.py)، وresults/compare.json، ورسم أو جدول مقارنة، وdarsi-check.json بيجتاز m4.

### m5: تنبيه حرارة آمن وv1.0 (3 ساعات)

#### ليه ده مهم
جهاز فصل لازم يكون مفيد وآمن: USB بس، ومفيش توصيل كهرباء منزلية.

#### الأدوات للمرحلة دي
- **Node-RED alert / LED** — بيزعق مرة مع مهلة. هتجيبه من: تدفّق في Node-RED وطرف على البورد
- **SAFETY.md** — USB بس، ناشف، فيه تهوية. هتجيبه من: إنت بتكتبه

#### اعمل كده
1. زوّد تنبيه حرارة بيشتغل مرة واحدة لما الفصل يفضل فوق ٣٢ درجة مئوية لمدة ١٠ دقايق (رسالة لنفسك وLED بينوّر)، وبعدين يستنى ٣٠ دقيقة قبل ما يشتغل تاني، عشان ميتكررش مع كل قراءة.
2. اكتب SAFETY.md: USB بس، مفيش كهرباء منزلية، علبة مهوّاة بعيد عن المية.
3. زوّد اختبارات لمنطق التنبيه في tests/test_alert.py (check.py بيدوّر على tests/test_alert*.py)؛ CI يشغّلها. حط v1.0. شغّل python check.py --milestone m5.

#### هتبقى خلصت لما
- SAFETY.md موجود
- اختبارات التنبيه موجودة
- m5 ناجحة

#### لو حاجة وقفت
- **تنبيهات بتكرر** → حط تهدئة ٣٠ دقيقة بعد الإطلاق
- **غويت توصل كهرباء منزلية** → وقف. USB بس؛ اسأل بالغ مؤهّل لأي حاجة تانية

#### إيه اللي لازم تفهمه
تقدر تطلق تنبيه فصل آمن بمنطق مختبَر وقواعد سلامة مكتوبة.

**المطلوب تسليمه:** تدفّق التنبيه، وSAFETY.md، وtests/test_alert.py، وActions أخضر، وإصدار v1.0، وdarsi-check.json بيجتاز m5، وشرحك.

## الفحص

شغّل `python check.py` أو `python check.py --milestone m2`. بيقرا الملفات بس، بيكتب `darsi-check.json`، وبيطبّع بالإنجليزي والعربي. مش بيرفع حاجة.

## المراجعة على درسي

ابعت رابط المستودع و`darsi-check.json` مع كل مرحلة على درسي. درسي بيقرا آخر تشغيل Actions والإصدار من واجهة GitHub العامة، بيضيف مراجعة استشارية بالذكاء الاصطناعي، وبعدين معلّمك أو فريق درسي بيراجع. **درسي مش بيشغّل كودك.**

## السلامة

تغذية USB بس. مفيش أي توصيل بكهربا البيت. حط البورد في علبة فيها تهوية، بعيد عن المية.

## الترخيص

MIT — شوف [LICENSE](LICENSE).

</div>
