# Groups Scripts MC

مجموعة سكربتات **Skript** لسيرفر ماينكرافت، مقسّمة إلى ثلاث مجموعات مستقلة قدر الإمكان:
مراقبة النواة (Core Boot)، إدارة الـ claims مع GriefPrevention، وأدوات الإدارة (Item Admin).

> هذه ملفات Skript على السيرفر وليست plugin. راجع المتطلبات والتكاملات في كل قسم قبل النشر،
> واختبرها على سيرفر تجريبي أولاً.

**نظرة سريعة (بالعربية):** انسخ الملفات المطلوبة من مجلدات المجموعات إلى `plugins/Skript/scripts/`،
ثم أعد تحميل Skript وراجع الكونسول لأي أخطاء في التحليل. إذا استخدمت مجموعة Claim أو Item Admin،
فاستخدم الملفات من المجموعتين معاً لأن `/quickfix glitch` يعتمد على متغيرات `security_guard.sk` في مجلد Claim.

---

## المجموعات

### 1. Core Boot

![Core Boot](Core%20boot/core-boot.jpg)

طبقة مركزية للتنبيه والتسجيل تستقبل التقارير من السكربتات الأخرى. تعمل في وضع **المراقبة فقط**
ولا تلغي أي حدث في اللعب.

| الملف | الوظيفة |
|---|---|
| [core_boot.sk](Core%20boot/core_boot.sk) | حالة النواة (ONLINE/OFFLINE)، تخزين السجلات، طباعة التنبيهات (INFO / WARNING / CRITICAL) في الكونسول. |
| [event_watchdog.sk](Core%20boot/event_watchdog.sk) | مراقبة الحركة والكسر والدردشة والأوامر، والإبلاغ عن النشاط الزائد عبر دالة النواة. |

**الدوال المتاحة**

| الدالة | الوصف |
|---|---|
| `zmx_core_alert(source, level, detail, advice)` | إرسال تنبيه مركزي. `level` = `INFO` أو `WARNING` أو `CRITICAL`. |
| `zmx_core_status()` | حالة النواة. |
| `zmx_core_log_count()` | عدد سجلات النواة. |
| `zmx_core_get_logs(limit)` | آخر `limit` سجلاً من النواة. |
| `zmx_event_alert(source, level, detail, advice)` | يغلّف `zmx_core_alert` ويحفظ نسخة محلية. |
| `zmx_event_get_logs(limit)` | آخر `limit` سجلاً من Event Watchdog. |

**الإعدادات الافتراضية (Event Watchdog)**

- حد التكرار للحركة والدردشة والأوامر: `50`.
- حد كسر الكتل: `100`.
- فترة إعادة تعيين العدادات: `5` ثوانٍ.

---

### 2. Claim (GriefPrevention)

![Claim](claim%20(GriefPrevention)/claim-griefprevention.jpg)

يربط عدد claim blocks المسموح للاعب بمستوى AuraSkills، ويضيف واجهة `/claimgui`، ومراقبة للتجاوزات.

| الملف | الوظيفة |
|---|---|
| [claim_by_level.sk](claim%20(GriefPrevention)/claim_by_level.sk) | يحسب الحد من المستوى، يطبّقه عند الدخول وعند تغيّر المستوى، ويعيد الضبط عند التجاوز (Strict Mode). |
| [claim_gui.sk](claim%20(GriefPrevention)/claim_gui.sk) | واجهة `/claimgui` تعرض المستوى وclaim blocks المتاحة وزر مزامنة. |
| [security_guard.sk](claim%20(GriefPrevention)/security_guard.sk) | مراقبة: حدود ارتفاع العالم، تجاوز الـ claims، دخول منطقة غير مملوكة (كونسول فقط)، TPS، والإضافات المعطّلة. |

**حساب الحد**

- الحد الأساسي عند المستوى 1: `100`.
- الزيادة لكل مستوى: `75`.
- الحد الأقصى: `50000`.
- الصيغة: `100 + 75 × (المستوى − 1)`، مع سقف `50000`.
- يطبّق الحد بالأمر الكونسولي `acb <player> set <amount>`.
- فحص التجاوز كل `120` ثانية (`audit-interval`) ويمكن إيقاف الإعادة التلقائية بـ `strict-mode: false`.

**المتطلبات**

- Skript **2.12+**.
- AuraSkills (للمستوى عبر placeholder `%auraskills_level%`).
- GriefPrevention (`%griefprevention_remainingclaims%`).
- PlaceholderAPI.
- إضافة توفّر الأمر `acb`.

---

### 3. Item Admin

![Item Admin](item%20admin/item-admin.jpg)

كتاب إداري بحسب الرتبة يفتح لوحة إدارة، مع سجل تدقيق وأوامر إصلاح سريعة.

| الملف | الوظيفة |
|---|---|
| [admin_item.sk](item%20admin/admin_item.sk) | `/getadminitem` وكتاب يفتح لوحة الإدارة عند النقر الأيمن. |
| [admin_gui.sk](item%20admin/admin_gui.sk) | لوحة 27 خانة بأزرار حسب الرتبة. |
| [admin_permissions.sk](item%20admin/admin_permissions.sk) | الدالة `hasAdminPermission(player, action)` وقواعد الرتب. |
| [admin_audit.sk](item%20admin/admin_audit.sk) | سجل إجراءات الإدارة و`/auditlog`. |
| [admin_quickfix.sk](item%20admin/admin_quickfix.sk) | `/quickfix lag`، `/quickfix glitch`، `/quickfix chunks`. |

**الرتب**

| الرتبة | الصلاحيات |
|---|---|
| Owner | كل الإجراءات، بما فيها Security Tools. |
| Admin | معظم الإجراءات، بدون Security Tools. |
| Helper | Clan Management و Player Management فقط. |

تُخزَّن الرتب في المتغير `{zmx.rank::<uuid>}`، ولا يوجد ربط بصلاحيات LuckPerms في الكود الحالي.

**الأوامر**

| الأمر | الوظيفة |
|---|---|
| `/getadminitem` | يعطي كتاب الإدارة لمن رتبته Owner أو Admin أو Helper. |
| `/openadmingui` | يفتح لوحة الإدارة للاعب المنفّذ. |
| `/auditlog` | يعرض سجل التدقيق. |
| `/quickfix lag` | ينفّذ الأمر الكونسولي `lagfix` (يتطلب توفّره). |
| `/quickfix glitch` | ينقل اللاعبين الذين لديهم تنبيه ارتفاع (`zmx.guard.glitch`) إلى spawn ويمسح التنبيه. |
| `/quickfix chunks` | يعيد توليد chunks العوالم (راجع قيود الصيغة أدناه). |

**التكاملات الخارجية**

أزرار اللوحة تستدعي أوامر كونسولية يجب أن توفّرها إضافات أو سكربتات أخرى:
`openclanmenu`، `openplayermenu`، `showserverstatus`، `quickadmin`، `securitytools`، `lagfix`، `adminaction`.

---

## الأدوات (tools/)

ملف واحد بثلاثة أوامر، من جذر المستودع:

```bash
python3 tools/repo_tool.py check     # فحص ملفات .sk الفعّالة (لا يعدّل شيئاً)
python3 tools/repo_tool.py release   # بناء ZIP لكل مجموعة في releases/ (ملفات .sk فقط)
python3 tools/repo_tool.py list      # عرض ملفات المستودع
```

يكتشف `check` الأخطاء الشائعة: اقتباس غير متوازن، أقواس `{ }` غير متوازنة، تبويب في المسافة البادئة،
قراءة معامل دالة كمتغير عام (مثل `{source}` بدل `{_source}`)، وعنوان كتلة بدون محتوى مُزاح.
وينبّه إلى تعليقات `#` داخل قيم `options`.

**ملاحظة:** الفحص لا يتحقق من صحة صيغة Skript الكاملة ولا من وجود الأوامر الخارجية؛ اختبار التحميل على السيرفر ضروري.

## المجلدات

| المسار | المحتوى |
|---|---|
| `Core boot/`, `claim (GriefPrevention)/`, `item admin/` | السكربتات الفعّالة وصور كل مجموعة. |
| `releases/` | ملفات ZIP محدّثة لكل مجموعة (تُبنى بـ `release`). |
| `archive/` | نسخ مُستبدلة. `security_guard_item-admin_v1.1.sk` دُمجت في `claim (GriefPrevention)/security_guard.sk`. |
| `archive/zips/` | ملفات ZIP القديمة قبل إعادة البناء. |
| `tools/` | أدوات الفحص والبناء. |

## التثبيت

1. خذ نسخة احتياطية من السيرفر وملفات Skript الحالية.
2. ثبّت Skript (2.12+ لمجموعة Claim) والإضافات المطلوبة.
3. راجع الإعدادات (`options`) والـ placeholders والأوامر في كل ملف.
4. انسخ الملفات المطلوبة إلى `plugins/Skript/scripts/`.
5. أعد تحميل Skript وراجع الكونسول لأي أخطاء تحليل.
6. اختبر كل ميزة على سيرفر تجريبي قبل الإنتاج.

حمّل المجموعات المترابطة معاً:
- **Event Watchdog** يستدعي دالة التنبيه في Core Boot.
- **Claim GUI** و**Claim Security Guard** يعتمدان على `{zmx.claim.allowed::*}` من `claim_by_level.sk`.
- **Item Admin Quick Fix** يعتمد على `{zmx.guard.glitch::*}` من `security_guard.sk`.

## القيود المعروفة

- **حركة Event Watchdog:** الحد الافتراضي `50` حركة في نافذة `5` ثوانٍ، والمشي الطبيعي قد يتجاوزه، فيظهر تحذير لكل لاعب يتحرك. الحد يحتاج ضبطاً.
- **تكرار فحص الـ claims:** `security_guard.sk` و`claim_by_level.sk` (Strict Mode) يفحصان التجاوز نفسه ويعيدان الضبط نفسه. النتيجة تنبيهان في الكونسول، والتعطيل يتم من مكان واحد فقط حالياً.
- **لوحة Item Admin:** `admin_gui.sk` ينفّذ أوامر الأزرار مباشرة، و`admin_permissions.sk` ينفّذ `adminaction` للأزرار نفسها، فقد يتكرر الإجراء. كما أن `admin_gui` لا يمر عبر `hasAdminPermission`.
- **صيغ تحتاج تحققاً على السيرفر:** `on skript event` في `admin_audit.sk`، و`on console command ... with arguments`، و`regenerate chunks`، و`tps`، و`owner of claim at`، و`loop all loaded plugins`. قد تحتاج إضافات غير مثبتة أو لا تعمل كما هي.
- **`/quickfix chunks`** و**`/auditlog`** يعتمدان على الصيغ أعلاه.
- **سجلات النواة** (`zmx.core.logs`، `zmx.event.logs`) تنمو بلا حد. يمكن إضافة سقف لاحقاً.
- **`core config`** غير موجود في هذا المستودع.

## الترخيص

لا يوجد ملف ترخيص. ما لم يُضف ترخيص، تبقى الحقوق لمالك المستودع؛ استأذن قبل إعادة النشر أو الدمج في مشروع آخر.
