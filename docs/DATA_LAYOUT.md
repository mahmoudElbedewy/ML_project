# ملفات البيانات

لا تُرفع ملفات البيانات إلى المستودع. ملفات النماذج وملخص النتائج اللازمة لتشغيل الواجهة مرفقة؛ تنزيل البيانات مطلوب فقط عند إعادة التدريب.

## الملفات المطلوبة لإعادة التدريب

ضع الملفات بهذه الأسماء والمسارات:

```text
data/raw/
├── email/
│   ├── bilingual/
│   │   ├── legit-bilingual.csv
│   │   └── phishing-bilingual.csv
│   └── external_test/
│       └── Phishing_validation_emails.csv   (اختياري)
├── jobs/
│   └── job_postings_train.csv
└── sms/
    ├── arabic/
    │   └── Arabic_Spam.csv
    ├── external_test/
    │   └── final_dataset_output.csv          (اختياري)
    └── multilingual/
        └── data-augmented.csv
```

ملف `job_postings_test.csv` غير مطلوب؛ لا يحتوي على تسميات صحيحة، لذلك لا يستخدمه التدريب أو التقييم.

## تنزيل الملفات

نزّل البيانات من صفحاتها الأصلية، ثم فك ضغط الملفات عند الحاجة وانقل ملفات CSV إلى المسارات أعلاه:

- [Arabic SMS Spam Data](https://github.com/KhalidAlsantali/Arabic-SMS-Spam-Data)
- [Multilingual SMS Spam Collection](https://huggingface.co/datasets/dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset/tree/main)
- [English/Arabic phishing email corpus](https://www.kaggle.com/datasets/saidasalloum/englisharabic-phishing-email-corpus)
- [Phishing validation emails](https://zenodo.org/records/13474746)
- [Fake job posting dataset](https://www.kaggle.com/competitions/fake-job-posting/data)

تأكد أن كل ملف يحمل الاسم المطلوب في الشجرة. ملفا الاختبار الخارجيان اختياريان؛ عند غيابهما يستمر التدريب والتقييم الداخلي.

## ما الذي تحتويه البيانات؟

- `Arabic_Spam.csv`: رسائل عربية بعلامات Ham وSpam. بعد التنظيف وإزالة التكرار، بقي 463 مثالًا في التجربة الحالية.
- `data-augmented.csv`: مجموعة رسائل SMS متعددة اللغات فيها 5,572 صفًا. يستخدم المشروع النص العربي فقط؛ كثير من هذه الرسائل مترجم آليًا وليست رسائل مصرية أصلية. بقي 4,828 مثالًا بعد الفلترة والتنظيف في التجربة الحالية.
- ملف الرسائل الخارجية: 55 بلاغًا عربيًا مصنفًا كلها Scam. يُستخدم كتحدٍ خارجي وتُعرض قيمة Recall فقط؛ لا يمكن حساب Accuracy من فئة واحدة.
- ملفا البريد الثنائي اللغة: 150 رسالة سليمة و150 تصيد، ولكل رسالة نسخ لغوية مرتبطة تُقسّم معًا لتجنب تسرب النسخة المترجمة بين التدريب والاختبار.
- ملف البريد الخارجي: 2,000 رسالة إنجليزية، نصفها سليم والنصف الآخر تصيّد، ولا يدخل في التدريب.
- `job_postings_train.csv`: 12,000 إعلان وظيفة مصنفًا، منها 11,411 سليمًا و589 احتياليًا قبل التنظيف. تُجمع حقول الإعلان النصية للتصنيف.

الأعداد النهائية تتغير قليلًا بعد حذف النصوص الفارغة والتكرارات. البيانات الإنجليزية لا تمثل إعلانات أو رسائل مصرية، والرسائل العربية المترجمة لا تمثل SMS مصرية أصلية.