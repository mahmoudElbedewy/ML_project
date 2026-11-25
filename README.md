# تشغيل المشروع

## المتطلبات

- Windows 10 أو أحدث.
- Git.
- Python 3.12، مع مكوّن Tcl/Tk الذي يوفّر مكتبة Tkinter.
- اتصال بالإنترنت لتنزيل المشروع وتثبيت المكتبات أول مرة.

النماذج وملفات نتائج العرض مرفقة بالمشروع؛ لا تحتاج إلى تنزيل ملفات البيانات لتشغيل الواجهة.

## تنزيل المشروع

افتح PowerShell في المجلد الذي تريد حفظ المشروع فيه، ثم نفّذ:

```powershell
git clone https://github.com/mahmoudElbedewy/ML_project.git
cd ML_project
```

## التثبيت والتشغيل

نفّذ الأوامر التالية من داخل مجلد `ML_project`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.gui_app
```

إذا لم يتوفر الأمر `py`، استخدم `python -m venv .venv` بدل السطر الأول. بعد تثبيت المكتبات، تعمل الواجهة دون اتصال بالإنترنت.

## إعادة التدريب (اختياري)

نزّل ملفات البيانات وضعها في المسارات الموضحة في [دليل البيانات](docs/DATA_LAYOUT.md)، ثم شغّل:

```powershell
.\.venv\Scripts\python.exe -m src.run_experiment
.\.venv\Scripts\python.exe -m src.gui_app
```

تُحفظ النماذج والنتائج الجديدة داخل `models/` و`outputs/`.