# دليل مذاكرة مشروع تصنيف النصوص — ملف متابعة مع Claude

هذا الملف يجمع أكواد السكاشن، وكود تعلّم الآلة المستخدم في المشروع، وخطة شرح متدرجة. استخدمه كمرجع في كل جلسة حتى نكمل من آخر نقطة وصلنا لها.

## تعليمات Claude وطريقة الشرح

أنت مدرس تشرح مشروع تعلم آلة لطالب مبتدئ. اشرح بالعربية المصرية البسيطة، واترك أسماء المكتبات والدوال والمتغيرات بالإنجليزية كما هي.

- ابدأ من أول موضوع غير مكتمل في قائمة التقدم، ولا تشرح الملف كله في رد واحد.
- في كل مرة خذ مفهومًا واحدًا أو مقطع كود صغيرًا. لا تنتقل للجزء التالي حتى أقول إن الجزء الحالي واضح.
- قبل شرح الكود، اشرح المشكلة التي يحلها ذلك الجزء وما الذي يدخل إليه وما الذي يخرجه.
- اشرح كل سطر أو مجموعة أسطر مترابطة: معنى المتغير، شكل البيانات، وظيفة الدالة، ولماذا نحتاجها.
- استخدم أمثلة صغيرة بأرقام أو برسائل قصيرة، واربط أسماء مثل X_train و y_train بمثال واضح.
- وضّح الفرق بين أمثلة السكاشن وبين كود المشروع. لا تقل إن داتا Iris أو Breast Cancer هي داتا المشروع؛ مشروعنا داتا رسائل وإيميلات ووظائف.
- ميّز بين خوارزمية التصنيف الأساسية وبين K-Means الإضافي. لا تصف درجات الاحتمال على أنها ضمان أو إثبات لهوية المرسل.
- لا تخترع مخرجات أو نتائج. استخدم جدول النتائج الموجود في هذا الملف.
- بعد كل مقطع، اسألني سؤالين قصيرين للتأكد من الفهم، ثم اطلب مني أشرح الفكرة بكلامي.
- لا تضع علامة [x] على موضوع إلا بعد أن أشرح فكرته بشكل صحيح أو أقول بوضوح إنني فهمته.
- بعد كل جلسة، أخرج لي نسخة محدثة من قسم «حالة التقدم» أدناه. إذا كان بإمكانك تعديل هذا الملف فحدّثه؛ وإذا لم يكن بإمكانك، أعطني القسم المحدث لألصقه مكانه.
- عند بدء محادثة جديدة، اقرأ حالة التقدم أولًا، ثم أكمل من أول مربع غير مكتمل ولا تعِد شرح الأجزاء المنتهية إلا إذا طلبت ذلك.
- إذا أجبت خطأ، صحح الفكرة بمثال بسيط ثم اسألني مرة أخرى، ولا تحرّك علامة الإنجاز قبل أن أفهم.

## حالة التقدم — حدّثها بعد كل جلسة

آخر نقطة وصلنا لها: لم نبدأ بعد.

- [ ] 1. الفكرة العامة: بيانات، خصائص X، هدف y، تصنيف مقابل انحدار
- [ ] 2. Linear Regression على بيانات المنازل
- [ ] 3. Polynomial Regression ولماذا نضيف خصائص تربيعية
- [ ] 4. Logistic Regression على بيانات Breast Cancer
- [ ] 5. KNN على بيانات Iris
- [ ] 6. K-Means و StandardScaler و PCA
- [ ] 7. تقييم المصنف: Confusion Matrix و Accuracy و Precision و Recall و F1 و ROC-AUC
- [ ] 8. تنظيم بيانات مشروعنا وقراءة المصادر والملصقات
- [ ] 9. تنظيف النص و TF-IDF وخصائص الكلمات والحروف
- [ ] 10. تدريب Logistic Regression و KNN للمشروع
- [ ] 11. K-Means على الرسائل المريبة: ما الذي يفعله وما الذي لا يفعله
- [ ] 12. التقييم الداخلي والخارجي وقيود النتائج
- [ ] 13. حفظ المودل بملف joblib وتشغيله على نص جديد
- [ ] 14. شرح ملفات المشروع والتدرب على أسئلة المناقشة

## إعداد البيئة وتشغيل المشروع

### المكتبات

الحزم الموجودة في `requirements.txt` ووظيفتها في المشروع:

- `pandas`: قراءة جداول البيانات وتنظيمها.
- `numpy`: العمليات العددية والمصفوفات.
- `scikit-learn`: TF-IDF، وLogistic Regression، وKNN، وK-Means، وتقسيم البيانات ومقاييس التقييم.
- `matplotlib`: إنشاء الرسوم البيانية.
- `joblib`: حفظ النماذج المحفوظة وقراءتها.
- `openpyxl`: دعم قراءة ملفات Excel عند استخدامها؛ بيانات التدريب الحالية بصيغة CSV.
- `tkinter`: واجهة سطح المكتب، تأتي مع تثبيت Python على Windows ولا تثبّت من pip.

### أوامر Windows PowerShell

افتح PowerShell داخل مجلد المشروع. ينشئ الأمر الأول بيئة محلية باسم `.venv`، وهي مستثناة من Git:

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.gui_app
~~~

لإعادة تدريب النماذج على ملفات البيانات:

~~~powershell
.\.venv\Scripts\python.exe -m src.run_experiment
.\.venv\Scripts\python.exe -m src.gui_app
~~~

يحتاج التدريب إلى ملفات البيانات في المسارات الموضحة في `docs/DATA_LAYOUT.md`. تشغيل الواجهة باستخدام النماذج المرفقة لا يحتاج إلى ملفات البيانات. يجب أن تتطابق نسخة `scikit-learn` مع النسخة المحددة في `requirements.txt` لقراءة ملفات النماذج المحفوظة.
## المشروع في جمل بسيطة

المشروع يصنف النص الذي يدخله المستخدم إلى فئة سليمة أو مريبة. توجد ثلاثة نماذج مستقلة: واحد لرسائل SMS وتنبيهات الحساب، وواحد للإيميلات، وواحد لإعلانات الوظائف. المودل لا يفتح حسابات Gmail أو البنوك ولا يتحقق من رقم المرسل أو الرابط؛ هو يقرأ النص فقط ويعطي درجة مبنية على الأنماط التي تعلمها.

### حجم البيانات المستخدمة في التجربة

| النوع | الصفوف الخام | بعد التنظيف | تدريب / اختبار | صفوف المودل النهائي |
|---|---:|---:|---:|---:|
| SMS | 5983 | 5291 | 3968 / 1323 | 5292 |
| Email | 600 | 596 | 446 / 150 | 596 |
| وظائف | 12000 | 11970 | 8977 / 2993 | 11970 |

### الخوارزميات المستخدمة

- Logistic Regression: المصنف الأساسي لكل الأنواع الثلاثة.
- K-Nearest Neighbors: مقارنة إضافية للـSMS والإيميلات فقط.
- K-Means: يجمع رسائل الاحتيال المتشابهة للاستكشاف، ولا يصنف الرسالة إلى Spam أو Ham.
- Linear Regression: غير مستخدم في التصنيف النهائي؛ يتوقع قيمة رقمية مستمرة مثل سعر منزل، بينما هدفنا فئات نصية.

## معاني الرموز المشتركة في السكاشن والمشروع

- X: المدخلات أو الخصائص. في بيانات المنازل تكون أعمدة مثل الدخل وعدد الغرف؛ وفي مشروعنا تصبح خصائص النص بعد تحويله إلى أرقام.
- y: الإجابة الصحيحة التي يتعلمها المودل. في مشروعنا تكون ham أو spam.
- X_train و y_train: أمثلة التدريب التي يتعلم منها المودل.
- X_test و y_test: أمثلة الاختبار التي لم نستخدمها في التدريب، ونقارن بها التوقعات.
- fit: تعلم من بيانات التدريب.
- transform: تطبيق تحويل تم تعلمه مسبقًا على بيانات أخرى.
- predict: إرجاع الفئة المتوقعة.
- predict_proba: إرجاع درجات الفئات.
- random_state: يجعل التقسيم أو التهيئة قابلة لإعادة التكرار.
- test_size=0.2: يحجز 20% للاختبار و80% للتدريب.

## 1. كود Linear Regression من سكشن المنازل

هذا مثال السكشن على توقع قيمة رقمية: سعر المنزل. ليس كود المشروع النهائي. جُمعت خلايا السكشن في مثال واحد ليسهل شرح ترتيبها.

~~~python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = fetch_california_housing(as_frame=True)
df = data.frame

print(df.head())
print(df.info())

# Define features (X) and target (y)
X = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions and check the result
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.3f}")
print(f"R² Score: {r2:.3f}")
print("Intercept:", model.intercept_)

coefficients = pd.DataFrame(
    model.coef_,
    X.columns,
    columns=["Coefficient"]
)
print(coefficients)

# Plot income against house value
plt.scatter(df["MedInc"], df["MedHouseVal"], alpha=0.3)
plt.xlabel("Median Income")
plt.ylabel("Median House Value")
plt.title("Relationship between Income and House Value")
plt.show()

# Compare actual and predicted values
plt.scatter(y_test, y_pred, alpha=0.3, color="purple")
plt.xlabel("Actual House Value")
plt.ylabel("Predicted House Value")
plt.title("Actual vs Predicted House Values")
plt.show()
~~~

نقاط يشرحها Claude:

- MedHouseVal هو الهدف y، وبقية الأعمدة هي X.
- Linear Regression يتنبأ برقم مستمر؛ لذلك لا يناسب فئات ham/spam.
- MSE يقيس متوسط مربع الخطأ، وR² يقارن التوقع بخط أساس بسيط. لا نستخدم R² لمشروع التصنيف.
- تحميل California Housing قد يحتاج إنترنت أول مرة.
- رسم actual مقابل predicted يساعد على رؤية قرب التوقعات من القيم الحقيقية.

## 2. كود Polynomial Regression من السكشن نفسه

هذا مثال صناعي يولد بيانات على شكل منحنى، ثم يضيف X² للخصائص قبل تدريب Linear Regression. يسمى Polynomial Regression لأن التوسعة تعطي النموذج مدخلات تربيعية، لكن أداة التدريب ما زالت LinearRegression.

~~~python
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

# Generate sample data
X = np.random.rand(100, 1) * 10
y = 2.5 * X**2 - 1.5 * X + np.random.randn(100, 1)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Add polynomial features
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Train the model
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Make predictions
y_pred = model.predict(X_test_poly)

# Plot actual and predicted points
plt.scatter(X_test, y_test, color="blue")
plt.scatter(X_test, y_pred, color="red")
plt.title("Polynomial Regression")
plt.xlabel("X")
plt.ylabel("y")
plt.show()
~~~

نقطة مهمة للشرح: fit_transform يتعلم شكل التحويل من التدريب ويطبقه عليه؛ test يستخدم transform فقط حتى لا نعيد تعلم التحويل من بيانات الاختبار.

## 3. كود Logistic Regression من سكشن Breast Cancer

هذا مثال تصنيف ثنائي على بيانات أورام الثدي الجاهزة في scikit-learn. قيمة 0 تعني malignant وقيمة 1 تعني benign في المثال. في مشروعنا الملصقات مختلفة: ham و spam.

~~~python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    roc_auc_score,
)

# Load the dataset
data = load_breast_cancer()
X = data.data
y = data.target
feature_names = data.feature_names

df = pd.DataFrame(X, columns=feature_names)
df["target"] = y

print("Shape:", df.shape)
print("Classes:", data.target_names)
print(df["target"].value_counts())
print("Missing values:", df.isnull().sum().sum())
print(df.head())

# Show the class counts
counts = df["target"].value_counts().sort_index()
plt.figure(figsize=(5, 4))
plt.bar(
    ["Malignant (0)", "Benign (1)"],
    counts.values,
    color=["red", "blue"],
    alpha=0.6
)
plt.ylabel("Number of samples")
plt.title("Class Distribution")
plt.show()

# Plot the first two features
plt.figure(figsize=(7, 5))
plt.scatter(
    X[y == 0, 0],
    X[y == 0, 1],
    color="red",
    label="Malignant",
    alpha=0.6
)
plt.scatter(
    X[y == 1, 0],
    X[y == 1, 1],
    color="blue",
    label="Benign",
    alpha=0.6
)
plt.xlabel(feature_names[0])
plt.ylabel(feature_names[1])
plt.title("Breast Cancer Data (2 Features)")
plt.legend()
plt.grid(True)
plt.show()

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Scale using the training data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

print("Training done!")
print("Number of weights learned:", model.coef_.shape[1])
print("Bias (intercept):", model.intercept_[0].round(3))

# Predict classes and class probabilities
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

results = pd.DataFrame({
    "Actual": y_test[:10],
    "Predicted": y_pred[:10],
    "Prob(class 1)": y_prob[:10].round(3)
})
print(results)
print("Accuracy:", round(model.score(X_test_scaled, y_test), 3))

# Show the confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

disp = ConfusionMatrixDisplay(
    cm,
    display_labels=["Malignant (0)", "Benign (1)"]
)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()

# Print classification metrics
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("Precision:", round(precision_score(y_test, y_pred), 3))
print("Recall:", round(recall_score(y_test, y_pred), 3))
print("F1:", round(f1_score(y_test, y_pred), 3))
print(classification_report(
    y_test,
    y_pred,
    target_names=["Malignant", "Benign"]
))

# Draw the ROC curve
fpr_arr, tpr_arr, thresholds = roc_curve(y_test, y_prob)
auc = roc_auc_score(y_test, y_prob)
print(f"AUC = {auc:.4f}")

plt.figure(figsize=(7, 5))
plt.plot(
    fpr_arr,
    tpr_arr,
    linewidth=2,
    label=f"Logistic Regression (AUC = {auc:.3f})"
)
plt.plot([0, 1], [0, 1], "k--", label="Random guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate (Recall)")
plt.title("ROC Curve")
plt.legend()
plt.grid(True)
plt.show()
~~~

أسئلة لازم Claude يوضحها عند هذا المثال:

- لماذا هذا Classification وليس Regression؟
- لماذا نستخدم StandardScaler هنا؟ وما الفرق بين fit_transform و transform؟
- كيف نقرأ predict_proba والعمود [:, 1]؟
- لماذا لا تعني Accuracy وحدها أن كل الفئات اكتشفت جيدًا؟
- ما الذي تعنيه خانات Confusion Matrix؟
- ROC-AUC يقيس قدرة الفصل عند عتبات مختلفة، ولا يعني أن المودل مثاليًا.
- هذا المثال الطبي للتدريب فقط؛ لا تربطه ببيانات مشروع الرسائل.

## 4. كود KNN من سكشن Iris

المثال يستخدم KNN للتصنيف. يبحث عن أقرب K أمثلة تدريب ثم يتوقع الفئة الأكثر شيوعًا بينها. المثال يقيس المسافة على خصائص Iris الرقمية.

~~~python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train KNN and predict
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
~~~

السكشن يعرض كذلك اختلاف weights:

~~~python
# Option 1: closer neighbors matter more
knn = KNeighborsClassifier(n_neighbors=3, weights="distance")

# Option 2: all neighbors have equal weight
knn = KNeighborsClassifier(n_neighbors=3, weights="uniform")
~~~

- distance يجعل الجيران الأقرب يؤثرون أكثر.
- uniform يعطي كل جار الوزن نفسه.
- اختيار K الصغير يجعل النتيجة حساسة للضوضاء، وK الكبير قد يجعل الحدود أنعم.
- يشرح السكشن استعمال Cross Validation لاختيار K، لكنه لا يعرض كود Cross Validation كاملًا.
- مثال السكشن يستخدم StandardScaler وبيانات أرقام. مشروعنا يستخدم TF-IDF ومقياس cosine لأن خصائص النص مختلفة.
- الشرائح الأولى تشرح المسافات والتصويت برسم، ولا يظهر فيها كود Python مستقل.

## 5. كود K-Means من سكشن Iris

K-Means لا يحتاج y ليتعلم المجموعات. الهدف منه تكوين clusters بحسب قرب الخصائص. المثال يحمل y لعرضه في جدول فقط؛ K-Means نفسه يتعلم من X_scaled.

~~~python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the dataset
iris = load_iris()
X = iris.data
y = iris.target

# Inspect the rows
iris_df = pd.DataFrame(X, columns=iris.feature_names)
iris_df["target"] = y
print("First 5 rows of the Iris dataset:")
print(iris_df.head())

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means
kmeans = KMeans(
    n_clusters=3,
    init="k-means++",
    n_init=10,
    random_state=42
)
kmeans.fit(X_scaled)
clusters = kmeans.labels_

# Reduce the features to two dimensions for plotting
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot the clusters
plt.figure(figsize=(8, 6))
plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=clusters,
    s=70,
    edgecolors="black"
)
plt.title("K-Means Clustering on Iris Dataset (PCA Visualization)")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.grid(True)
plt.show()
~~~

ملاحظة: شرائح Step 6 و Step 7 تكرر كود PCA. هنا جمعناه مرة واحدة في مثال متصل. اشرح أن PCA هنا لتصوير النقاط في بعدين؛ هو ليس خوارزمية K-Means ولا التصنيف النهائي.

## أين تقف حدود السكاشن وأين تبدأ إضافات المشروع؟

### ما يأتي مباشرة من أساس السكاشن

- تصنيف بإشراف مع X و y وتقسيم Train/Test.
- تدريب Logistic Regression وتوقع فئة واحتمالات.
- مقارنة KNN كمصنف.
- تجميع K-Means غير المراقب.
- تقييم التصنيف باستخدام Confusion Matrix ومقاييس التصنيف.
- Linear Regression وPolynomial Regression أمثلة منفصلة للتوقع الرقمي، وليسا جزءًا من مصنف النصوص.

### إضافات المشروع التي يجب تعلمها فوق السكاشن

- تنظيف النص العربي والإنجليزي: توحيد الأرقام العربية، إزالة التشكيل والتطويل، وتوحيد بعض الحروف.
- TF-IDF يحول الرسائل إلى مصفوفة sparse من الأرقام.
- خصائص الكلمات تستخدم كلمات مفردة وثنائيات كلمات؛ خصائص الحروف تلتقط أجزاء الكلمات والأخطاء الإملائية.
- FeatureUnion يجمع تمثيل الكلمات وتمثيل الحروف في X واحدة.
- لا نستخدم StandardScaler مع TF-IDF في مشروعنا؛ TF-IDF يطبع المتجهات افتراضيًا، وKNN يستخدم cosine.
- نعمل fit للـvectorizer على نصوص التدريب فقط ثم transform للاختبار لتجنب تسرب معلومات الاختبار.
- إزالة النصوص المكررة أو المتعارضة قبل تقسيم البيانات.
- الإيميلات المترجمة لها group_id حتى لا تقع نسخة في التدريب ونسختها المقابلة في الاختبار.
- class_weight="balanced" يساعد Logistic Regression على التعامل مع عدم توازن فئات SMS والوظائف.
- حفظ vectorizer والمصنف معًا في joblib، حتى يستخدم التطبيق التحويل نفسه الذي تعلمه المودل.
- التفسير يعرض كلمات ساهمت في رفع أو خفض درجة Spam من معاملات Logistic Regression؛ لا يثبت أن تلك الكلمات سبب قطعي.
- تقييم خارجي يكشف اختلاف المجال واللغة عن بيانات التدريب.

## خريطة ملفات المشروع

- src/config.py: مسارات البيانات والنماذج والنتائج.
- src/data.py: قراءة الملفات، توحيد labels إلى ham/spam، وتنظيم نصوص SMS والإيميل والوظائف.
- src/features.py: تنظيف النص وإنشاء TF-IDF للكلمات والحروف.
- src/modeling.py: إزالة التكرار، التقسيم، تدريب Logistic Regression وKNN، الحسابات، K-Means، وشرح الكلمات.
- src/run_experiment.py: تشغيل التجارب، حفظ القياسات والرسوم والنماذج.
- جزء الواجهة فقط من src/gui_app.py يحمل ملفات joblib ويمرر النص الجديد للـvectorizer ثم للمصنف.
- models/sms_pipeline.joblib و email_pipeline.joblib و jobs_pipeline.joblib: النماذج المحفوظة. لا تحتوي الداتا التدريبية نفسها.
- ملف الواجهة الكامل غير مضمّن لأن المطلوب مذاكرة الماشين؛ أُدرج فقط المقطع الذي يربط النص بالمودل.

## نتائج التجربة المسجلة في outputs/metrics.csv

هذه أرقام من تشغيل المشروع الفعلي. لا تعد Claude أن نتيجة التدريب الداخلي ستظهر نفسها على رسائل حقيقية مختلفة.

| نوع البيانات | الاختبار | النموذج | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---:|---:|---:|---:|---:|
| SMS | داخلي stratified test، 1323 صفًا | Logistic Regression | 0.982 | 0.946 | 0.926 | 0.936 | 0.986 |
| SMS | داخلي stratified test، 1323 صفًا | KNN | 0.969 | 0.968 | 0.810 | 0.882 | 0.970 |
| SMS | خارجي، 55 رسالة احتيال فقط | Logistic Regression | غير محسوب | غير محسوب | 0.564 | غير محسوب | غير محسوب |
| Email | داخلي stratified test، 150 صفًا | Logistic Regression | 0.967 | 0.949 | 0.987 | 0.968 | 0.994 |
| Email | داخلي stratified test، 150 صفًا | KNN | 0.927 | 0.882 | 0.987 | 0.932 | 0.972 |
| Email | خارجي مستقل، 2000 إيميل إنجليزي | Logistic Regression | 0.664 | 0.598 | 1.000 | 0.749 | 0.912 |
| وظائف | داخلي stratified test، 2993 صفًا | Logistic Regression | 0.983 | 0.820 | 0.837 | 0.828 | 0.976 |

تفسير حدود النتائج:

- مجموعة SMS الخارجية فيها رسائل احتيال فقط؛ لذلك نستطيع حساب كم اكتشف المودل منها، ولا نستطيع حساب Accuracy أو Precision منها.
- في اختبار البريد الخارجي كان Recall يساوي 1.0 لكن Accuracy 0.664 وPrecision 0.598؛ كل هذه الأرقام مهمة لئلا نختار رقمًا واحدًا مضللًا.
- أرقام الوظائف والإيميلات تعكس مجموعات إنجليزية قديمة وليست السوق المصري الحالي.
- جزء كبير من SMS العربي مترجم آليًا؛ ليس عينة ممثلة لكل رسائل شركات الاتصالات المصرية.
- درجات التطبيق ليست توثيقًا لهوية المرسل ولا دليلًا قاطعًا على الأمان أو الاحتيال.
- سبب عدم استعمال R² هو أن y هنا فئة وليس قيمة مستمرة.

## مقتطف ربط المودل برسالة جديدة في الواجهة

المقطع الفعلي المختصر من src/gui_app.py:

~~~python
self.models = {
    profile: joblib.load(path)
    for profile, path in MODEL_PATHS.items()
}

pipeline = self.models[profile]
classifier = pipeline["classifier"]
vectorizer = pipeline["vectorizer"]

probabilities = classifier.predict_proba(
    vectorizer.transform([text])
)[0]
~~~

اشرَح التسلسل: النص الخام، ثم نفس vectorizer المحفوظ يحوله إلى خصائص، ثم classifier يحسب درجة كل فئة. هذا يستخدم نموذجًا محفوظًا ولا يعيد التدريب أثناء إدخال الرسالة.

## طريقة مذاكرة مقترحة للمناقشة

- أولًا افهم لماذا نعدها Classification ولماذا Linear Regression ليس النموذج النهائي.
- بعد ذلك اشرح مثال Logistic Regression في السكشن: X/y، التقسيم، scaling، fit، predict، المقاييس.
- اشرح KNN ومتى يتأثر اختيار K والمسافة.
- اشرح K-Means كتحليل إضافي، ووضح أنه لا يستعمل labels.
- انتقل بعدها إلى اختلاف النصوص: normalization ثم TF-IDF ثم تدريب Logistic Regression.
- أخيرًا تتبع رسالة من واجهة التطبيق إلى المودل واحكِ حدود البيانات والاختبار الخارجي.

## أمثلة أسئلة للمناقشة

1. ما الفرق بين features و target في المشروع؟
2. لماذا نحول النص إلى أرقام؟ ما وظيفة TF-IDF؟
3. لماذا نعمل fit_transform على التدريب و transform على الاختبار؟
4. ما الفرق بين predict و predict_proba؟
5. لماذا اخترنا Logistic Regression للتصنيف؟
6. ماذا يضيف KNN هنا؟ وما الفرق بين distance و uniform weights؟
7. هل K-Means هو الذي يقرر Spam؟ لماذا؟
8. لماذا لا نستخدم Linear Regression أو R² للمهمة؟
9. ما الذي تثبته Accuracy وما الذي لا تثبته؟
10. لماذا أداء الاختبار الخارجي أضعف؟ ماذا يعني اختلاف المجال؟
11. هل ملف joblib يحتوي رسائل التدريب؟ هل يحتاج إلى الإنترنت عند تشغيل المودل؟
12. كيف تصل رسالة SMS جديدة من واجهة Tkinter إلى نتيجة المودل؟

## الملفات المصدرية الفعلية للمشروع

الأكواد التالية مأخوذة من النسخة الحالية للمشروع حتى يشرح Claude ما هو موجود فعلًا. اشرحها على دفعات صغيرة، ولا تحاول قراءة كل ملف دفعة واحدة.

### src/config.py

~~~python
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SMS_DIR = RAW_DIR / "sms"
EMAIL_DIR = RAW_DIR / "email"
JOBS_DIR = RAW_DIR / "jobs"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

SMS_ARABIC_FILE = SMS_DIR / "arabic" / "Arabic_Spam.csv"
SMS_MULTILINGUAL_FILE = SMS_DIR / "multilingual" / "data-augmented.csv"
SMS_EXTERNAL_FILE = SMS_DIR / "external_test" / "final_dataset_output.csv"

EMAIL_LEGIT_FILE = EMAIL_DIR / "bilingual" / "legit-bilingual.csv"
EMAIL_PHISHING_FILE = EMAIL_DIR / "bilingual" / "phishing-bilingual.csv"
EMAIL_EXTERNAL_FILE = EMAIL_DIR / "external_test" / "Phishing_validation_emails.csv"

JOBS_TRAIN_FILE = JOBS_DIR / "job_postings_train.csv"
JOBS_UNLABELED_FILE = JOBS_DIR / "job_postings_test.csv"

REVIEWED_EXAMPLES_FILE = PROJECT_ROOT / "data" / "reviewed_examples.csv"
MODEL_PATHS = {
    "sms": MODEL_DIR / "sms_pipeline.joblib",
    "email": MODEL_DIR / "email_pipeline.joblib",
    "jobs": MODEL_DIR / "jobs_pipeline.joblib",
}

METRICS_PATH = OUTPUT_DIR / "metrics.csv"
METADATA_PATH = OUTPUT_DIR / "experiment_summary.json"
RANDOM_STATE = 42
TEST_SIZE = 0.25
~~~


### src/data.py

~~~python
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .config import (
    EMAIL_EXTERNAL_FILE,
    EMAIL_LEGIT_FILE,
    EMAIL_PHISHING_FILE,
    JOBS_TRAIN_FILE,
    REVIEWED_EXAMPLES_FILE,
    SMS_ARABIC_FILE,
    SMS_EXTERNAL_FILE,
    SMS_MULTILINGUAL_FILE,
)


ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
BASE_COLUMNS = ["text", "label", "source", "source_file", "profile", "group_id", "language"]


def _column_key(value: object) -> str:
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(value).lower())


def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    try:
        return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1", low_memory=False)


def _find_column(frame: pd.DataFrame, names: tuple[str, ...]) -> str | None:
    by_key = {_column_key(column): str(column) for column in frame.columns}
    return next((by_key[_column_key(name)] for name in names if _column_key(name) in by_key), None)


def _standardize_labels(values: pd.Series) -> pd.Series:
    positive = {"spam", "junk", "scam", "phishing", "phishingemail", "fraud", "fraudulent", "1", "10", "true", "yes"}
    negative = {"ham", "legitimate", "normal", "notspam", "nonscam", "safe", "safeemail", "0", "00", "false", "no"}

    def convert(value: object) -> str | None:
        key = _column_key(value)
        if key in positive:
            return "spam"
        if key in negative:
            return "ham"
        return None

    return values.map(convert)


def _has_arabic(value: object) -> bool:
    return bool(ARABIC_RE.search(str(value or "")))


def _language(value: str) -> str:
    has_arabic = _has_arabic(value)
    has_latin = bool(re.search(r"[A-Za-z]", value))
    if has_arabic and has_latin:
        return "Mixed"
    if has_arabic:
        return "Arabic"
    if has_latin:
        return "English"
    return "Unknown"


# Put each source into the same text and label format.
def _frame(rows: list[dict[str, object]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=BASE_COLUMNS)
    result = pd.DataFrame(rows)
    for column in BASE_COLUMNS:
        if column not in result:
            result[column] = ""
    result["text"] = result["text"].fillna("").astype(str).str.strip()
    result["label"] = _standardize_labels(result["label"])
    result = result[(result["text"].str.len() > 0) & result["label"].notna()]
    return result[BASE_COLUMNS].reset_index(drop=True)


# Load the Arabic SMS examples.
def _load_sms_arabic() -> pd.DataFrame:
    if not SMS_ARABIC_FILE.exists():
        raise FileNotFoundError(f"ملف الرسائل العربية غير موجود: {SMS_ARABIC_FILE}")
    frame = _read_table(SMS_ARABIC_FILE)
    text_column = _find_column(frame, ("SMS", "message", "text"))
    label_column = _find_column(frame, ("Sentiment", "label", "class", "target"))
    if text_column is None or label_column is None:
        raise ValueError(f"أعمدة ملف الرسائل العربية غير متوقعة: {list(frame.columns)}")
    labels = _standardize_labels(frame[label_column])
    result = pd.DataFrame(
        {
            "text": frame[text_column].fillna("").astype(str).str.strip(),
            "label": labels,
            "source": "Arabic SMS corpus",
            "source_file": SMS_ARABIC_FILE.name,
            "profile": "sms",
            "group_id": [f"arabic-sms:{index}" for index in range(len(frame))],
            "language": "Arabic",
        }
    )
    return result[(result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


# Keep Arabic rows from the translated SMS file.
def _load_sms_translations() -> pd.DataFrame:
    if not SMS_MULTILINGUAL_FILE.exists():
        raise FileNotFoundError(f"ملف الرسائل متعددة اللغات غير موجود: {SMS_MULTILINGUAL_FILE}")
    frame = _read_table(SMS_MULTILINGUAL_FILE)
    text_column = _find_column(frame, ("text_ar", "Arabic", "Arabic Text"))
    label_column = _find_column(frame, ("labels", "label", "class", "target"))
    if text_column is None or label_column is None:
        raise ValueError(f"أعمدة ملف الرسائل متعددة اللغات غير متوقعة: {list(frame.columns)}")
    labels = _standardize_labels(frame[label_column])
    text = frame[text_column].fillna("").astype(str).str.strip()
    group_column = _find_column(frame, ("Unnamed: 0", "id", "index"))
    groups = frame[group_column].fillna("").astype(str) if group_column else pd.Series(range(len(frame)), index=frame.index).astype(str)
    result = pd.DataFrame(
        {
            "text": text,
            "label": labels,
            "source": "Machine-translated SMS",
            "source_file": SMS_MULTILINGUAL_FILE.name,
            "profile": "sms",
            "group_id": "translated-sms:" + groups,
            "language": "Arabic (machine translated)",
        }
    )
    arabic_mask = result["text"].map(_has_arabic)
    return result[arabic_mask & (result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


def load_sms_data() -> pd.DataFrame:
    return pd.concat([_load_sms_arabic(), _load_sms_translations()], ignore_index=True)


# Keep translated versions of one email in the same group.
def _load_bilingual_email_file(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"ملف الإيميلات غير موجود: {path}")
    frame = _read_table(path)
    id_column = _find_column(frame, ("No.", "No", "id", "number"))
    text_columns = [
        column
        for column in frame.columns
        if column != id_column and any(token in _column_key(column) for token in ("text", "message", "email"))
    ]
    if len(text_columns) < 2:
        raise ValueError(f"لم أجد حقلي النص العربي والإنجليزي في {path.name}: {list(frame.columns)}")

    rows: list[dict[str, object]] = []
    label_name = "spam" if label == "phishing" else "ham"
    for row_index, row in frame.iterrows():
        pair_number = row[id_column] if id_column else row_index
        for column in text_columns:
            text = str(row[column] or "").strip()
            if not text or text.lower() == "nan":
                continue
            rows.append(
                {
                    "text": text,
                    "label": label_name,
                    "source": "Bilingual email corpus",
                    "source_file": path.name,
                    "profile": "email",
                    "group_id": f"{label}:{pair_number}",
                    "language": _language(text),
                }
            )
    return _frame(rows)


def load_email_data() -> pd.DataFrame:
    legitimate = _load_bilingual_email_file(EMAIL_LEGIT_FILE, "legitimate")
    phishing = _load_bilingual_email_file(EMAIL_PHISHING_FILE, "phishing")
    return pd.concat([legitimate, phishing], ignore_index=True)


def load_email_external_test() -> pd.DataFrame:
    if not EMAIL_EXTERNAL_FILE.exists():
        return pd.DataFrame(columns=BASE_COLUMNS)
    frame = _read_table(EMAIL_EXTERNAL_FILE)
    text_column = _find_column(frame, ("Email Text", "text", "body", "message"))
    label_column = _find_column(frame, ("Email Type", "label", "class", "target"))
    if text_column is None or label_column is None:
        raise ValueError(f"أعمدة اختبار الإيميل غير متوقعة: {list(frame.columns)}")
    labels = _standardize_labels(frame[label_column])
    result = pd.DataFrame(
        {
            "text": frame[text_column].fillna("").astype(str).str.strip(),
            "label": labels,
            "source": "Independent English email set",
            "source_file": EMAIL_EXTERNAL_FILE.name,
            "profile": "email",
            "group_id": "",
            "language": "English",
        }
    )
    return result[(result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


# Join the job fields into one text sample.
def load_jobs_data() -> pd.DataFrame:
    if not JOBS_TRAIN_FILE.exists():
        raise FileNotFoundError(f"ملف إعلانات الوظائف غير موجود: {JOBS_TRAIN_FILE}")
    frame = _read_table(JOBS_TRAIN_FILE)
    label_column = _find_column(frame, ("fraudulent", "label", "target"))
    if label_column is None:
        raise ValueError(f"لم أجد عمود تصنيف الوظائف fraudulent في {JOBS_TRAIN_FILE.name}")
    text_columns = [
        column
        for column in (
            "title", "location", "department", "salary_range", "company_profile", "description",
            "requirements", "benefits", "employment_type", "required_experience", "required_education",
            "industry", "function",
        )
        if column in frame.columns
    ]
    if not text_columns:
        raise ValueError(f"لم أجد حقول وصف الوظيفة في {JOBS_TRAIN_FILE.name}")
    text = frame[text_columns].fillna("").astype(str).agg(" ".join, axis=1).str.strip()
    return _frame(
        [
            {
                "text": text.iloc[index],
                "label": frame[label_column].iloc[index],
                "source": "Job postings",
                "source_file": JOBS_TRAIN_FILE.name,
                "profile": "jobs",
                "group_id": "",
                "language": "English",
            }
            for index in range(len(frame))
        ]
    )


def load_profile_data() -> dict[str, pd.DataFrame]:
    return {"sms": load_sms_data(), "email": load_email_data(), "jobs": load_jobs_data()}


# Load separate rows for an extra model check.
def load_external_challenge(profile: str) -> pd.DataFrame:
    if profile == "sms":
        if not SMS_EXTERNAL_FILE.exists():
            return pd.DataFrame(columns=BASE_COLUMNS)
        frame = _read_table(SMS_EXTERNAL_FILE)
        language_column = _find_column(frame, ("language", "lang"))
        text_column = _find_column(frame, ("text", "message", "translation"))
        if text_column is None:
            return pd.DataFrame(columns=BASE_COLUMNS)
        if language_column is not None:
            language = frame[language_column].fillna("").astype(str).str.lower().str.strip()
            frame = frame[language.isin({"arabic", "ar", "ara", "العربية"})]
            labels = pd.Series("spam", index=frame.index)
        else:
            frame = frame[frame[text_column].fillna("").astype(str).map(_has_arabic)]
            labels = pd.Series("spam", index=frame.index)
        result = pd.DataFrame(
            {
                "text": frame[text_column].fillna("").astype(str).str.strip(),
                "label": labels,
                "source": "External Arabic scam reports",
                "source_file": SMS_EXTERNAL_FILE.name,
                "profile": "sms",
                "group_id": "",
                "language": "Arabic",
            }
        )
        return result[result["text"].str.len() > 0].drop_duplicates("text").reset_index(drop=True)
    if profile == "email":
        return load_email_external_test()
    return pd.DataFrame(columns=BASE_COLUMNS)


# Add examples that were checked by a person.
def load_reviewed_examples(profile: str | None = None) -> pd.DataFrame:
    if not REVIEWED_EXAMPLES_FILE.exists():
        return pd.DataFrame(columns=BASE_COLUMNS)
    frame = _read_table(REVIEWED_EXAMPLES_FILE)
    text_column = _find_column(frame, ("text", "message", "sms"))
    label_column = _find_column(frame, ("label", "class", "target"))
    profile_column = _find_column(frame, ("profile", "channel", "domain"))
    if text_column is None or label_column is None:
        return pd.DataFrame(columns=BASE_COLUMNS)
    selected = frame.copy()
    selected["label"] = _standardize_labels(selected[label_column])
    selected["profile"] = selected[profile_column].fillna("sms").astype(str) if profile_column else "sms"
    if profile:
        selected = selected[selected["profile"] == profile]
    result = pd.DataFrame(
        {
            "text": selected[text_column].fillna("").astype(str).str.strip(),
            "label": selected["label"],
            "source": "User-reviewed examples",
            "source_file": REVIEWED_EXAMPLES_FILE.name,
            "profile": selected["profile"],
            "group_id": "",
            "language": selected[text_column].fillna("").astype(str).map(_language),
        }
    )
    return result[(result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


def data_counts(frame: pd.DataFrame) -> dict[str, object]:
    if frame.empty:
        return {"rows": 0, "ham": 0, "spam": 0, "by_source": {}}
    counts = frame.groupby(["source", "label"], dropna=False).size().unstack(fill_value=0)
    source_counts = {
        str(source): {str(label): int(count) for label, count in row.items()}
        for source, row in counts.iterrows()
    }
    return {
        "rows": int(len(frame)),
        "ham": int((frame["label"] == "ham").sum()),
        "spam": int((frame["label"] == "spam").sum()),
        "by_source": source_counts,
    }
~~~


### src/features.py

~~~python
from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion


_DIACRITICS = re.compile(r"[\u064b-\u065f\u0670]")
_URL = re.compile(r"(?:https?://|www\.)\S+", flags=re.IGNORECASE)
_EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
_NON_TEXT = re.compile(r"[^\w\s<>#@+:/.-]", flags=re.UNICODE)
_WHITESPACE = re.compile(r"\s+")


# Clean common text patterns before making features.
def normalize_text(text: object) -> str:
    value = str(text or "").lower()
    value = value.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))
    value = _URL.sub(" <url> ", value)
    value = _EMAIL.sub(" <email> ", value)
    value = _DIACRITICS.sub("", value).replace("ـ", "")
    value = value.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي"}))
    value = _NON_TEXT.sub(" ", value)
    return _WHITESPACE.sub(" ", value).strip()


# Use words and character patterns as text features.
def build_vectorizer() -> FeatureUnion:
    word_features = TfidfVectorizer(
        preprocessor=normalize_text,
        lowercase=False,
        token_pattern=r"(?u)\b\w+\b",
        ngram_range=(1, 2),
        min_df=2,
        max_features=24000,
        sublinear_tf=True,
    )
    character_features = TfidfVectorizer(
        preprocessor=normalize_text,
        lowercase=False,
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=30000,
        sublinear_tf=True,
    )
    return FeatureUnion(
        [("word", word_features), ("char", character_features)],
        n_jobs=1,
    )
~~~


### src/modeling.py

~~~python
from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier

from .config import RANDOM_STATE, TEST_SIZE
from .features import build_vectorizer, normalize_text


# Remove repeated text and labels that disagree.
def remove_duplicates(frame: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    original_count = len(frame)
    result = frame.copy()
    result["normalized_text"] = result["text"].map(normalize_text)
    result = result[result["normalized_text"].str.len() > 0]
    conflicts = result.groupby("normalized_text")["label"].nunique()
    conflicting_texts = set(conflicts[conflicts > 1].index)
    result = result[~result["normalized_text"].isin(conflicting_texts)]
    result = result.drop_duplicates("normalized_text", keep="first").reset_index(drop=True)
    return result.drop(columns="normalized_text"), original_count - len(result)


# Keep paired email versions on the same side of the split.
def split_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    groups = frame.get("group_id")
    if groups is not None and groups.fillna("").astype(str).str.len().gt(0).all():
        splitter = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
        train_indices, test_indices = next(
            splitter.split(np.zeros(len(frame)), frame["label"], groups=groups.astype(str))
        )
    else:
        indices = np.arange(len(frame))
        train_indices, test_indices = train_test_split(
            indices,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=frame["label"],
        )
    return frame.iloc[train_indices].reset_index(drop=True), frame.iloc[test_indices].reset_index(drop=True)


# Calculate scores from the test labels and predictions.
def calculate_metrics(y_test: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray, classes: list[str]) -> dict[str, float]:
    spam_index = classes.index("spam")
    spam_scores = y_prob[:, spam_index]
    actual_positive = y_test == "spam"
    predicted_positive = y_pred == "spam"
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(actual_positive, predicted_positive, zero_division=0)),
        "recall": float(recall_score(actual_positive, predicted_positive, zero_division=0)),
        "f1": float(f1_score(actual_positive, predicted_positive, zero_division=0)),
        "roc_auc": float(roc_auc_score(actual_positive, spam_scores)),
    }


# Train the main Logistic Regression model.
def _fit_logistic(X_train, y_train: np.ndarray) -> LogisticRegression:
    model = LogisticRegression(
        max_iter=1200,
        class_weight="balanced",
        C=2.0,
        solver="liblinear",
        random_state=RANDOM_STATE,
    )
    model.fit(X_train, y_train)
    return model


# Train the models and compare their test results.
def train_and_evaluate(
    train: pd.DataFrame,
    test: pd.DataFrame,
    compare_knn: bool = False,
) -> dict[str, object]:
    vectorizer = build_vectorizer()
    # Learn text features from training data only.
    X_train = vectorizer.fit_transform(train["text"].tolist())
    X_test = vectorizer.transform(test["text"].tolist())
    y_train = train["label"].to_numpy()
    y_test = test["label"].to_numpy()

    model = _fit_logistic(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)
    classes = list(model.classes_)
    rows = [{"model": "Logistic Regression", **calculate_metrics(y_test, y_pred, y_prob, classes)}]
    knn_pred = None
    knn_prob = None

    if compare_knn:
        knn = KNeighborsClassifier(
            n_neighbors=min(5, len(train)),
            weights="distance",
            metric="cosine",
            algorithm="brute",
            n_jobs=-1,
        )
        # Compare a weighted KNN with the main model.
        knn.fit(X_train, y_train)
        knn_pred = knn.predict(X_test)
        knn_prob = knn.predict_proba(X_test)
        rows.append({"model": "K-Nearest Neighbors", **calculate_metrics(y_test, knn_pred, knn_prob, list(knn.classes_))})

    return {
        "pipeline": {"vectorizer": vectorizer, "classifier": model, "classes": model.classes_},
        "y_test": y_test,
        "logistic_predictions": y_pred,
        "logistic_probabilities": y_prob,
        "knn_predictions": knn_pred,
        "knn_probabilities": knn_prob,
        "metrics": pd.DataFrame(rows),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["ham", "spam"]),
        "feature_count": int(X_train.shape[1]),
    }


# Train the final model on all labeled examples.
def fit_final_pipeline(frame: pd.DataFrame) -> dict[str, object]:
    vectorizer = build_vectorizer()
    X = vectorizer.fit_transform(frame["text"].tolist())
    y = frame["label"].to_numpy()
    model = _fit_logistic(X, y)
    return {"vectorizer": vectorizer, "classifier": model, "classes": model.classes_}


# Group similar spam examples to inspect common patterns.
def cluster_spam_messages(texts: list[str], cluster_count: int = 5) -> pd.DataFrame:
    if len(texts) < 2:
        return pd.DataFrame(columns=["cluster", "message_count", "top_terms"])

    vectorizer = TfidfVectorizer(
        preprocessor=normalize_text,
        lowercase=False,
        token_pattern=r"(?u)\b\w+\b",
        ngram_range=(1, 2),
        min_df=2,
        max_features=12000,
        sublinear_tf=True,
    )
    X = vectorizer.fit_transform(texts)
    if X.shape[1] == 0:
        return pd.DataFrame(columns=["cluster", "message_count", "top_terms"])

    cluster_count = min(cluster_count, len(texts))
    kmeans = KMeans(n_clusters=cluster_count, random_state=RANDOM_STATE, n_init=5, max_iter=100)
    clusters = kmeans.fit_predict(X)
    terms = vectorizer.get_feature_names_out()
    rows = []
    for cluster_id, center in enumerate(kmeans.cluster_centers_):
        top = center.argsort()[-8:][::-1]
        rows.append(
            {
                "cluster": int(cluster_id),
                "message_count": int((clusters == cluster_id).sum()),
                "top_terms": ", ".join(terms[index] for index in top if center[index] > 0),
            }
        )
    return pd.DataFrame(rows).sort_values("cluster").reset_index(drop=True)


# Show which words moved the score up or down.
def explain_message(pipeline: dict[str, object], text: str, limit: int = 5) -> dict[str, list[tuple[str, float]]]:
    vectorizer = pipeline["vectorizer"]
    classifier = pipeline["classifier"]
    X = vectorizer.transform([text])
    names = vectorizer.get_feature_names_out()
    classes = list(classifier.classes_)
    positive_index = classes.index("spam")
    coefficients = classifier.coef_[positive_index]
    active = X.tocoo()
    accumulated: dict[str, float] = defaultdict(float)

    for column, value in zip(active.col, active.data):
        name = names[column]
        if not name.startswith("word__"):
            continue
        term = name[len("word__"):].replace("_", " ").strip()
        if term:
            accumulated[term] += float(value * coefficients[column])

    ranked = sorted(accumulated.items(), key=lambda item: item[1], reverse=True)
    return {
        "spam": [(term, score) for term, score in ranked if score > 0][:limit],
        "ham": [(term, score) for term, score in reversed(ranked) if score < 0][:limit],
    }
~~~


### src/run_experiment.py

~~~python
from __future__ import annotations

import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve

from .config import FIGURE_DIR, METADATA_PATH, METRICS_PATH, MODEL_DIR, MODEL_PATHS, OUTPUT_DIR, RANDOM_STATE
from .data import data_counts, load_external_challenge, load_profile_data, load_reviewed_examples
from .features import normalize_text
from .modeling import (
    calculate_metrics,
    cluster_spam_messages,
    fit_final_pipeline,
    remove_duplicates,
    split_data,
    train_and_evaluate,
)


PROFILE_NAMES = {"sms": "SMS and alerts", "email": "Email", "jobs": "Job postings"}


# Save plots for the test results.
def _save_figures(profile: str, details: dict[str, object], clusters: pd.DataFrame) -> None:
    actual = details["y_test"]
    matrix = details["confusion_matrix"]
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks([0, 1], labels=["Ham", "Spam"])
    ax.set_yticks([0, 1], labels=["Ham", "Spam"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"{PROFILE_NAMES[profile]} — Logistic Regression")
    for (row, column), value in np.ndenumerate(matrix):
        ax.text(column, row, str(value), ha="center", va="center", color="#17324D", fontsize=13)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{profile}_confusion_matrix.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    classifiers = [("Logistic Regression", details["logistic_probabilities"], details["pipeline"]["classifier"].classes_)]
    if details["knn_probabilities"] is not None:
        classifiers.append(("K-Nearest Neighbors", details["knn_probabilities"], ["ham", "spam"]))
    for name, probabilities, classes in classifiers:
        spam_index = list(classes).index("spam")
        false_positive, true_positive, _ = roc_curve(actual == "spam", probabilities[:, spam_index])
        ax.plot(false_positive, true_positive, label=f"{name} (AUC {auc(false_positive, true_positive):.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", color="#888888", label="Random reference")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve — {PROFILE_NAMES[profile]}")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{profile}_roc_curve.png", dpi=150)
    plt.close(fig)

    comparison = details["metrics"].set_index("model")
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    comparison["f1"].plot(kind="bar", color=["#0E7490", "#E58B42"][: len(comparison)], ax=ax)
    ax.set_ylim(0, 1)
    ax.set_ylabel("F1 score")
    ax.set_title(f"Model Comparison — {PROFILE_NAMES[profile]}")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{profile}_model_comparison.png", dpi=150)
    plt.close(fig)

    if not clusters.empty:
        fig, ax = plt.subplots(figsize=(7.2, 4.8))
        ax.bar(clusters["cluster"].astype(str), clusters["message_count"], color="#3977A8")
        ax.set_xlabel("Cluster number")
        ax.set_ylabel("Suspicious examples")
        ax.set_title(f"Unsupervised Text Groups — {PROFILE_NAMES[profile]}")
        ax.grid(axis="y", alpha=0.2)
        fig.tight_layout()
        fig.savefig(FIGURE_DIR / f"{profile}_clusters.png", dpi=150)
        plt.close(fig)


def _without_training_duplicates(external: pd.DataFrame, training: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    if external.empty:
        return external, 0
    training_keys = set(training["text"].map(normalize_text))
    external = external.copy()
    external["_key"] = external["text"].map(normalize_text)
    overlaps = external["_key"].isin(training_keys)
    removed = int(overlaps.sum())
    result = external.loc[~overlaps].drop(columns="_key").reset_index(drop=True)
    return result, removed


# Check the final model on separate data.
def _evaluate_external(
    profile: str,
    pipeline: dict[str, object],
    external: pd.DataFrame,
    metrics: list[dict[str, object]],
) -> dict[str, object]:
    if external.empty:
        return {"rows": 0}
    vectorizer = pipeline["vectorizer"]
    classifier = pipeline["classifier"]
    matrix = vectorizer.transform(external["text"].tolist())
    predictions = classifier.predict(matrix)
    probabilities = classifier.predict_proba(matrix)
    classes = list(classifier.classes_)
    positive_index = classes.index("spam")
    target = external["label"].to_numpy()

    if len(np.unique(target)) == 1:
        detected = int((predictions == "spam").sum())
        recall = float((predictions == "spam").mean())
        result = {"rows": int(len(external)), "spam_detected": detected, "recall": recall}
        metrics.append(
            {
                "profile": profile,
                "evaluation_set": "positive_only_external_challenge",
                "model": "Logistic Regression",
                "accuracy": np.nan,
                "precision": np.nan,
                "recall": recall,
                "f1": np.nan,
                "roc_auc": np.nan,
                "rows": len(external),
            }
        )
    else:
        result = {"rows": int(len(external)), **calculate_metrics(target, predictions, probabilities, classes)}
        metrics.append(
            {
                "profile": profile,
                "evaluation_set": "independent_external_test",
                "model": "Logistic Regression",
                **{key: result[key] for key in ("accuracy", "precision", "recall", "f1", "roc_auc")},
                "rows": len(external),
            }
        )

    pd.DataFrame(
        {
            "text": external["text"],
            "actual": target,
            "predicted": predictions,
            "spam_score": probabilities[:, positive_index],
        }
    ).to_csv(OUTPUT_DIR / f"{profile}_external_predictions.csv", index=False, encoding="utf-8-sig")
    return result


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading the SMS, email, and job-posting datasets...")
    raw_profiles = load_profile_data()
    metric_rows: list[dict[str, object]] = []
    summary: dict[str, object] = {"random_state": RANDOM_STATE, "profiles": {}}

    # Train one model for each text type.
    for profile, raw in raw_profiles.items():
        cleaned, removed = remove_duplicates(raw)
        if cleaned["label"].nunique() != 2 or cleaned["label"].value_counts().min() < 4:
            raise ValueError(f"بيانات {PROFILE_NAMES[profile]} لا تحتوي أمثلة كافية من الفئتين.")

        # Split the labeled rows for the model check.
        train, test = split_data(cleaned)
        compare_knn = profile in {"sms", "email"}
        print(
            f"{PROFILE_NAMES[profile]}: {len(cleaned):,} unique examples, "
            f"{len(train):,} train, {len(test):,} test."
        )
        print(f"Training Logistic Regression{' and KNN' if compare_knn else ''} on CPU...")
        # Train the models and score the test rows.
        details = train_and_evaluate(train, test, compare_knn=compare_knn)

        rows = details["metrics"].copy()
        rows.insert(0, "profile", profile)
        rows.insert(1, "evaluation_set", "stratified_test")
        rows["rows"] = len(test)
        metric_rows.extend(rows.to_dict(orient="records"))

        classes = list(details["pipeline"]["classifier"].classes_)
        positive_index = classes.index("spam")
        predictions = pd.DataFrame(
            {
                "text": test["text"],
                "source": test["source"],
                "actual": test["label"],
                "predicted": details["logistic_predictions"],
                "spam_score": details["logistic_probabilities"][:, positive_index],
            }
        )
        predictions.to_csv(OUTPUT_DIR / f"{profile}_test_predictions.csv", index=False, encoding="utf-8-sig")

        clusters = cluster_spam_messages(train.loc[train["label"] == "spam", "text"].tolist())
        clusters.to_csv(OUTPUT_DIR / f"{profile}_clusters.csv", index=False, encoding="utf-8-sig")
        _save_figures(profile, details, clusters)

        # Train the saved model on all labeled examples.
        final_data = pd.concat([cleaned, load_reviewed_examples(profile)], ignore_index=True)
        final_data, final_removed = remove_duplicates(final_data)
        final_pipeline = fit_final_pipeline(final_data)
        joblib.dump(final_pipeline, MODEL_PATHS[profile])

        external = load_external_challenge(profile)
        external, overlap_count = _without_training_duplicates(external, cleaned)
        external_summary = _evaluate_external(profile, final_pipeline, external, metric_rows)
        external_summary["training_overlaps_removed"] = overlap_count

        summary["profiles"][profile] = {
            "display_name": PROFILE_NAMES[profile],
            "raw_data": data_counts(raw),
            "clean_data": data_counts(cleaned),
            "duplicates_removed": int(removed),
            "training_rows": int(len(train)),
            "test_rows": int(len(test)),
            "feature_count": details["feature_count"],
            "final_model_rows": int(len(final_data)),
            "reviewed_examples_added": int(len(load_reviewed_examples(profile))),
            "model_path": str(MODEL_PATHS[profile]),
            "external_test": external_summary,
            "metrics": details["metrics"].to_dict(orient="records"),
        }

    # Save the scores and dataset details.
    pd.DataFrame(metric_rows).to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")
    summary["limitations"] = [
        "The SMS translation collection is machine-translated from an English benchmark and is not native Egyptian SMS.",
        "The Arabic SMS source is small, so the SMS result should be treated as a classroom prototype.",
        "The bilingual email collection is small; its English external set is reported separately.",
        "The job postings are English-language examples; they do not represent the current Egyptian job market.",
        "Text-only scores cannot authenticate a sender or prove that a message is safe or fraudulent.",
    ]
    METADATA_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nHeld-out results (higher is better):")
    print(pd.DataFrame(metric_rows).to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print("\nSaved three local models and their reports. The desktop app can now open offline.")
    print("Run: python -m src.gui_app")


if __name__ == "__main__":
    main()
~~~


### requirements.txt

~~~text
pandas>=2.1,<4.0
numpy>=1.26,<3.0
scikit-learn==1.9.1
matplotlib>=3.8,<4.0
joblib>=1.3,<2.0
openpyxl>=3.1,<4.0
~~~

## مواد السكاشن التي جُمعت هنا

- Kmean.pdf: K-Means على Iris، StandardScaler، ثم PCA للرسم.
- KNN section 5.pdf: شرح KNN ومثال Iris وخيارات weights.
- Logistic Regression (2).pdf: مثال Breast Cancer وخطوات التصنيف والتقييم.
- Linear Regression (2).pdf: مثال California Housing ومثال Polynomial Regression.

أكواد السكاشن جُمعت في أمثلة متصلة لتسهيل الشرح. أما الأكواد تحت عناوين src فهي نسخ من ملفات المشروع الفعلية وقت إعداد هذا الدليل.
