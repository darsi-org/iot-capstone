<div dir="rtl">

# المشروع الختامي: محطة طقس للفصل


> **ملخص درسي قصير عن قصد.** الدرس في التطبيق بيعرض خطوات ضغط مختصرة. الـ README ده بيحفظ الأوامر الكاملة وإصلاح الأخطاء والخلفية لكل مرحلة — افتح قسم **المرحلة N** لما تحتاج تفاصيل.

ابنِ محطة طقس وهوا للفصل: ESP32 بـ MicroPython أو محاكي Wokwi المجاني أولًا، وMQTT، ورسوم Node-RED أو Grafana، ومقارنة مع Open-Meteo، وتنبيه حرارة مع SAFETY.md — تغذية USB بس.

[English](README.md)

## هتقدر تعمل إيه

- تشغّل أدوات حقيقية مجانية من اللابتوب أو Codespaces
- تخلّص خمس مراحل، كل مرحلة ليها فحص تقدر تتأكد منه بنفسك
- تطلع بقطعة بورتفوليو: تقرير أو عرض أو أداة بإصدار v1.0
- **درسي مش بيشغّل كودك أبدًا** — بيقرا الرابط وملف الفحص وبمراجعة استشارية

## ثبّت مرة واحدة

### ويندوز

١. ثبّت Python 3.12: افتح PowerShell واكتب winget install Python.Python.3.12
٢. ثبّت Git: winget install Git.Git
٣. ثبّت VS Code من https://code.visualstudio.com مجانًا
٤. على GitHub افتح https://github.com/darsi-org/iot-capstone واضغط Use this template، وبعدين Clone نسختك
٥. جوّه فولدر المشروع شغّل:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python check.py

### ماك

١. ثبّت Homebrew من https://brew.sh لو مش متثبت
٢. brew install python@3.12 git
٣. ثبّت VS Code من https://code.visualstudio.com
٤. على GitHub افتح https://github.com/darsi-org/iot-capstone → Use this template → Clone نسختك
٥. جوّه فولدر المشروع شغّل:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python check.py

### Codespaces / Colab

معندكش كمبيوتر؟ استخدم GitHub Codespaces: افتح نسختك → Code → Codespaces → Create codespace. كل حاجة هتتثبت هناك. أو افتح دفتر في Google Colab، شغّل أول خلية بتنسخ الريبو، وبعدين python check.py. الاتنين بيشتغلوا من لابتوب مستعار؛ ومتصفح الموبايل يكفي تقرا النتائج.

## البداية

اضغط **Use this template** على https://github.com/darsi-org/iot-capstone، Clone نسختك، وبعدين اتبع المرحلة ١.

## المراحل

### m1: اقرا حسّاس (Wokwi أولًا) (3 ساعات)

## ليه ده مهم
معندكش لوحة؟ Wokwi بيحاكي ESP32 + DHT22 في المتصفح مجانًا. العتاد اختياري، مش بوابة.

## الأدوات للمرحلة دي
- **Wokwi** — ESP32 مع DHT22 في المتصفح. هتجيبه من: https://wokwi.com — free account
- **MicroPython** — Python للمتحكمات الدقيقة. هتجيبه من: firmware link in README

## اعمل كده
1. Clone https://github.com/darsi-org/iot-capstone. افتح مشروع Wokwi في README، أو ارفع MicroPython على ESP32 حقيقية.
2. عدّل device/main.py: اقرا الحرارة والرطوبة كل ١٠ ثواني كسطور JSON. عيد المحاولة عند الفشل؛ متحفظش ٠ مزيفة.
3. التقط حوالي ٣٠ دقيقة في data/readings.jsonl (المحاكي: غيّر القيم؛ العتاد: سيبه شغّال).
4. شغّل python check.py --milestone m1.

## هتبقى خلصت لما
- ≥١٨٠ سطر في data/readings.jsonl
- m1 ناجحة

## لو حاجة وقفت
- **مشروع Wokwi مش بيفتح** → استخدم رابط القالب العام في README؛ سجّل مجانًا
- **الحسّاس بيرجع None** → حاول مرة بعد ثانيتين؛ تخطّى القراءة لو لسه فشلت
- **سطور قليلة** → فترة ١٠ ثواني × ٣٠ دقيقة ≈ ١٨٠ سطر؛ متنمش أطول

## إيه اللي لازم تفهمه
تقدر تقرا حسّاس على محاكي أو لوحة وتحافظ على فجوات صادقة بدل أصفار مزيفة.

**المطلوب تسليمه:** device/main.py، وdata/readings.jsonl، وdarsi-check.json بيجتاز m1.

### m2: ابعتها عبر MQTT (3 ساعات)

## ليه ده مهم
MQTT هو طريقة أجهزة صغيرة كتير بتتكلم. الأسرار ملهاش مكان في Git.

## الأدوات للمرحلة دي
- **Mosquitto** — وسيط MQTT. هتجيبه من: docker compose in the starter, or a public test broker named in README for Wokwi
- **umqtt.simple / paho-mqtt** — نشر واشتراك. هتجيبه من: device vs PC

## اعمل كده
1. شغّل الوسيط: docker compose up -d أو وسيط الاختبار العام للمحاكي.
2. انشر كل قراءة على darsi/<اسمك>/room1. اكتب tools/listen.py بيضيف على data/mqtt.jsonl.
3. خلي باسورد الواي فاي في device/secrets.py الموجود في .gitignore. شغّل python check.py --milestone m2.

## هتبقى خلصت لما
- data/mqtt.jsonl فيه ≥٣٠ سطر
- مفيش أسرار متعملها commit
- m2 ناجحة

## لو حاجة وقفت
- **Wokwi مش واصل لـ Mosquitto المحلي** → استخدم وسيط الاختبار العام المذكور في README لمسار المحاكي
- **باسورد اتعمل له commit بالغلط** → شيّله من التاريخ، غيّر الباسورد، خلي secrets.py متتجاهل

## إيه اللي لازم تفهمه
تقدر تنشر بيانات الحسّاس عبر MQTT وتحافظ على بيانات الدخول برة الريبو.

**المطلوب تسليمه:** الناشر، وtools/listen.py، وdata/mqtt.jsonl، وdarsi-check.json بيجتاز m2.

### m3: خزّن وارسم (3 ساعات)

## ليه ده مهم
الأرقام بتفيد لما الفصل يقدر يقراها في عشر ثواني.

## الأدوات للمرحلة دي
- **Node-RED or Grafana** — لوحة متابعة بلغتين. هتجيبه من: docker compose in the starter
- **SQLite** — بيحافظ على التاريخ بعد إعادة التشغيل. هتجيبه من: tools/store.py

## اعمل كده
1. شغّل Node-RED أو Grafana من docker compose. استورد flows/dashboard.json.
2. خزّن القراءات بـ tools/store.py أو سيّب Node-RED يكتب.
3. اللوحة: الحرارة الحالية، وآخر ٢٤ ساعة، وأدنى/أقصى يومي، عناوين بالعربي والإنجليزي. سكرين docs/dashboard.png.
4. شغّل python check.py --milestone m3.

## هتبقى خلصت لما
- docs/dashboard.png موجود
- flows/dashboard.json موجود
- m3 ناجحة

## لو حاجة وقفت
- **Node-RED فاضي** → اتأكد من هجاء موضوع MQTT وإن listen/store شغّالين
- **الوحدات ناقصة على الرسم** → عنون كل سلسلة بـ °C أو %

## إيه اللي لازم تفهمه
تقدر تخزّن القراءات وتبني لوحة بلغتين زميل يقدر يقراها بسرعة.

**المطلوب تسليمه:** كود التخزين، وتدفّق اللوحة، وdocs/dashboard.png، وdarsi-check.json بيجتاز m3.

### m4: قارنها بـ Open-Meteo (3 ساعات)

## ليه ده مهم
حسّاسك صح؟ قارن بمصدر خارجي موثوق واشرح الفجوة.

## الأدوات للمرحلة دي
- **Open-Meteo** — API حرارة خارجية كل ساعة. هتجيبه من: https://open-meteo.com — free, no key

## اعمل كده
1. شغّل: python tools/open_meteo.py <lat> <lon> لمدينتك.
2. لمدة ٢٤ ساعة حط الحسّاس برة في الضل، أو استخدم قيم برة في المحاكي.
3. قارن ساعة بساعة بنفس المنطقة الزمنية. احفظ متوسط وأكبر فرق في results/compare.json. اشرح شمس وجدران ودقة ±٠.٥ درجة.
4. شغّل python check.py --milestone m4.

## هتبقى خلصت لما
- results/compare.json فيه mean_diff وmax_diff
- m4 ناجحة

## لو حاجة وقفت
- **اختلاف منطقة زمنية** → اطلب timezone=Africa/Cairo أو حوّل الاتنين لـ UTC
- **فجوة عصر كبيرة** → غالبًا شمس أو جدار دافئ؛ انقل للضل وقيس تاني

## إيه اللي لازم تفهمه
تقدر تتحقق من حسّاس مقابل API طقس مفتوح وتشرح الفجوات المنتظمة.

**المطلوب تسليمه:** ناتج tools/open_meteo.py، ورسم/جدول مقارنة، وdarsi-check.json بيجتاز m4.

### m5: تنبيهات وعلبة وv1.0 (3 ساعات)

## ليه ده مهم
جهاز فصل لازم يكون مفيد وآمن: USB بس، ومفيش توصيل كهرباء منزلية.

## الأدوات للمرحلة دي
- **Node-RED alert / LED** — بيزعق مرة مع مهلة. هتجيبه من: flow + device pin
- **SAFETY.md** — USB بس، نشف، مهوّى. هتجيبه من: you write it

## اعمل كده
1. تنبيه لما الأوضة >٣٢ درجة لمدة ١٠ دقايق: رسالة لنفسك + LED. زوّد مهلة عشان متتكررش كل قراءة.
2. اكتب SAFETY.md: USB بس، مفيش كهرباء منزلية، علبة مهوّاة بعيد عن المية.
3. زوّد اختبارات لمنطق التنبيه؛ CI يشغّلها. حط v1.0. شغّل python check.py --milestone m5.

## هتبقى خلصت لما
- SAFETY.md موجود
- اختبارات التنبيه موجودة
- m5 ناجحة

## لو حاجة وقفت
- **تنبيهات بتكرر** → حط تهدئة ٣٠ دقيقة بعد الإطلاق
- **غويت توصل كهرباء منزلية** → وقف. USB بس؛ اسأل بالغ مؤهّل لأي حاجة تانية

## إيه اللي لازم تفهمه
تقدر تطلق تنبيه فصل آمن بمنطق مختبَر وقواعد سلامة مكتوبة.

**المطلوب تسليمه:** تدفّق التنبيه، وSAFETY.md، والاختبارات، وActions أخضر، وv1.0، وdarsi-check.json بيجتاز m5، وشرحك.

## الفحص

شغّل `python check.py` أو `python check.py --milestone m2`. بيقرا الملفات بس، بيكتب `darsi-check.json`، وبيطبّع بالإنجليزي والعربي. مش بيرفع حاجة.

## المراجعة على درسي

ابعت رابط الريبو و`darsi-check.json` مع كل مرحلة على درسي. درسي بيقرا آخر تشغيل Actions والإصدار من واجهة GitHub العامة، بيضيف مراجعة استشارية بالذكاء الاصطناعي، وبعدين معلّمك أو فريق درسي بيراجع. **درسي مش بيشغّل كودك.**

## السلامة

التغذية عبر USB فقط. لا توصيلات بالكهرباء المنزلية. ضع اللوحة في علبة مهوّاة بعيدًا عن الماء.

## الترخيص

MIT — شوف [LICENSE](LICENSE).

</div>
