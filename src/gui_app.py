from __future__ import annotations

import json
import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import joblib
import matplotlib
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .config import METADATA_PATH, METRICS_PATH, MODEL_PATHS, REVIEWED_EXAMPLES_FILE
from .data import load_reviewed_examples
from .features import normalize_text
from .modeling import explain_message


matplotlib.rcParams["font.family"] = "Segoe UI"
matplotlib.rcParams["axes.unicode_minus"] = False

COLORS = {
    "navy": "#17324D",
    "teal": "#0E7490",
    "blue": "#3977A8",
    "orange": "#D97706",
    "pale": "#F3F6F9",
    "ink": "#213547",
    "muted": "#586A79",
    "line": "#D9E2E9",
    "white": "#FFFFFF",
}

PROFILE_LABELS = {
    "sms": "رسالة SMS أو تنبيه حساب",
    "email": "إيميل",
    "jobs": "إعلان وظيفة",
}
PROFILE_TERMS = {
    "sms": {"safe": "رسالة عادية", "risk": "رسالة مزعجة أو مريبة", "item": "الرسالة"},
    "email": {"safe": "إيميل سليم", "risk": "إيميل تصيّد أو مزعج", "item": "الإيميل"},
    "jobs": {"safe": "إعلان يبدو سليمًا", "risk": "إعلان يبدو احتياليًا", "item": "الإعلان"},
}


def review_key(value: object) -> str:
    text = normalize_text(value)
    text = re.sub(r"[#@+:/.-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


class MessageSafetyApp:
    def __init__(self, root: tk.Tk) -> None:
        missing = [str(path) for path in MODEL_PATHS.values() if not path.exists()]
        if missing:
            raise FileNotFoundError(
                "شغّل أولًا أمر التدريب: python -m src.run_experiment\n\n" + "\n".join(missing)
            )

        self.root = root
        self.models = {profile: joblib.load(path) for profile, path in MODEL_PATHS.items()}
        self.reviewed_labels: dict[str, str] = {}
        for profile in MODEL_PATHS:
            reviewed = load_reviewed_examples(profile)
            self.reviewed_labels.update(
                {f"{profile}:{review_key(row.text)}": row.label for row in reviewed.itertuples(index=False)}
            )

        self.root.title("فاحص الرسائل والإيميلات وإعلانات الوظائف")
        self.root.geometry("1180x850")
        self.root.minsize(820, 600)
        self.root.configure(bg=COLORS["pale"])
        self.root.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.root.bind_all("<Button-4>", self._on_mousewheel_linux, add="+")
        self.root.bind_all("<Button-5>", self._on_mousewheel_linux, add="+")
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self.root, bg=COLORS["navy"], padx=24, pady=17)
        header.pack(fill="x")
        tk.Label(
            header,
            text="فاحص الرسائل والإيميلات وإعلانات الوظائف",
            bg=COLORS["navy"],
            fg=COLORS["white"],
            font=("Segoe UI", 20, "bold"),
            anchor="e",
        ).pack(fill="x")
        tk.Label(
            header,
            text="اختر نوع النص، واكتب المحتوى، ثم راجع تقييم النموذج وأسباب النتيجة.",
            bg=COLORS["navy"],
            fg="#D9E8F2",
            font=("Segoe UI", 11),
            anchor="e",
        ).pack(fill="x", pady=(5, 0))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COLORS["pale"], borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 8), font=("Segoe UI", 10))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=14, pady=(12, 14))
        self.scroll_canvases: list[tk.Canvas] = []

        self.analysis_tab = self._add_scrollable_tab("تحليل نص")
        self.results_tab = self._add_scrollable_tab("نتائج التجربة")
        self.about_tab = self._add_scrollable_tab("شرح المشروع")
        self._build_analysis_tab()
        self._build_results_tab()
        self._build_about_tab()

    def _add_scrollable_tab(self, title: str) -> tk.Frame:
        wrapper = tk.Frame(self.tabs, bg=COLORS["pale"])
        canvas = tk.Canvas(wrapper, bg=COLORS["pale"], highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLORS["pale"], padx=18, pady=16)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        content.bind(
            "<Configure>",
            lambda _event, target=canvas: target.configure(scrollregion=target.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event, target=canvas, item=window_id: target.itemconfigure(item, width=event.width),
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.tabs.add(wrapper, text=title)
        self.scroll_canvases.append(canvas)
        return content

    def _on_mousewheel(self, event: tk.Event) -> None:
        if isinstance(event.widget, tk.Text):
            return
        if not self.scroll_canvases:
            return
        canvas = self.scroll_canvases[self.tabs.index("current")]
        units = int(-event.delta / 120) if event.delta else 0
        if units == 0 and event.delta:
            units = -1 if event.delta > 0 else 1
        canvas.yview_scroll(units, "units")
        return "break"

    def _on_mousewheel_linux(self, event: tk.Event) -> None:
        if not self.scroll_canvases or isinstance(event.widget, tk.Text):
            return
        canvas = self.scroll_canvases[self.tabs.index("current")]
        canvas.yview_scroll(-1 if event.num == 4 else 1, "units")
        return "break"

    def _paste_message(self, _event: tk.Event | None = None) -> str:
        try:
            content = self.root.clipboard_get()
        except tk.TclError:
            self.root.bell()
            return "break"

        try:
            self.message_box.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        self.message_box.insert("insert", content)
        self.message_box.tag_add("rtl", "1.0", "end")
        return "break"

    def _show_message_menu(self, event: tk.Event) -> str:
        self.message_box.focus_set()
        try:
            self.message_box.index("sel.first")
        except tk.TclError:
            self.message_box.mark_set("insert", f"@{event.x},{event.y}")
        self.message_menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def _copy_message(self) -> None:
        self.message_box.event_generate("<<Copy>>")

    def _cut_message(self) -> None:
        self.message_box.event_generate("<<Cut>>")

    def _select_all_message(self, _event: tk.Event | None = None) -> str:
        self.message_box.tag_add("sel", "1.0", "end-1c")
        return "break"

    def _resize_result_text(self, event: tk.Event) -> None:
        wrap = max(260, event.width - 40)
        self.prediction_label.configure(wraplength=wrap)
        self.result_warning_label.configure(wraplength=wrap)

    def _build_analysis_tab(self) -> None:
        tk.Label(
            self.analysis_tab,
            text="اختر نوع النص",
            bg=COLORS["pale"],
            fg=COLORS["ink"],
            font=("Segoe UI", 12, "bold"),
            anchor="e",
        ).pack(fill="x", pady=(0, 5))

        self.profile_var = tk.StringVar(value=PROFILE_LABELS["sms"])
        self.profile_by_label = {label: key for key, label in PROFILE_LABELS.items()}
        self.profile_select = ttk.Combobox(
            self.analysis_tab,
            textvariable=self.profile_var,
            values=list(PROFILE_LABELS.values()),
            state="readonly",
            font=("Segoe UI", 11),
            justify="right",
        )
        self.profile_select.pack(fill="x", pady=(0, 12))
        self.profile_select.bind("<<ComboboxSelected>>", self._profile_changed)

        tk.Label(
            self.analysis_tab,
            text="الصق النص الذي تريد فحصه",
            bg=COLORS["pale"],
            fg=COLORS["ink"],
            font=("Segoe UI", 12, "bold"),
            anchor="e",
        ).pack(fill="x", pady=(0, 7))

        message_frame = tk.Frame(self.analysis_tab, bg=COLORS["white"])
        message_frame.pack(fill="x")
        message_scrollbar = ttk.Scrollbar(message_frame, orient="vertical")
        self.message_box = tk.Text(
            message_frame,
            height=8,
            wrap="word",
            font=("Segoe UI", 12),
            padx=12,
            pady=10,
            relief="solid",
            borderwidth=1,
            undo=True,
            yscrollcommand=message_scrollbar.set,
        )
        message_scrollbar.configure(command=self.message_box.yview)
        self.message_box.tag_configure("rtl", justify="right")
        self.message_box.bind("<Control-v>", self._paste_message)
        self.message_box.bind("<Control-V>", self._paste_message)
        self.message_box.bind("<Shift-Insert>", self._paste_message)
        self.message_box.bind("<Control-a>", self._select_all_message)
        self.message_box.bind("<Button-3>", self._show_message_menu)
        self.message_menu = tk.Menu(self.root, tearoff=0)
        self.message_menu.add_command(label="لصق", command=self._paste_message)
        self.message_menu.add_command(label="نسخ", command=self._copy_message)
        self.message_menu.add_command(label="قص", command=self._cut_message)
        self.message_menu.add_separator()
        self.message_menu.add_command(label="تحديد الكل", command=self._select_all_message)
        message_scrollbar.pack(side="right", fill="y")
        self.message_box.pack(side="left", fill="both", expand=True)

        button_row = tk.Frame(self.analysis_tab, bg=COLORS["pale"])
        button_row.pack(fill="x", pady=10)
        self._button(button_row, "حلّل النص", self.analyze, COLORS["teal"]).pack(side="right", padx=(6, 0))
        self._button(button_row, "فتح ملف نصي", self.open_text_file, COLORS["blue"]).pack(side="right", padx=6)
        self._button(button_row, "علّمها سليمة", lambda: self.save_review("ham"), "#3977A8").pack(side="right", padx=6)
        self._button(button_row, "علّمها مريبة", lambda: self.save_review("spam"), "#B45309").pack(side="right", padx=6)
        self._button(button_row, "مسح", self.clear, "#637789").pack(side="right", padx=6)

        self.result_card = tk.Frame(
            self.analysis_tab,
            bg=COLORS["white"],
            padx=16,
            pady=14,
            highlightbackground=COLORS["line"],
            highlightthickness=1,
        )
        self.result_card.pack(fill="x", pady=(5, 0))
        self.prediction_label = tk.Label(
            self.result_card,
            text="اكتب نصًا ثم اضغط على تحليل النص",
            bg=COLORS["white"],
            fg=COLORS["ink"],
            font=("Segoe UI", 14, "bold"),
            anchor="e",
            justify="right",
            wraplength=1000,
        )
        self.prediction_label.pack(fill="x")
        self.probability_label = tk.Label(
            self.result_card,
            text="",
            bg=COLORS["white"],
            fg=COLORS["muted"],
            font=("Segoe UI", 11),
            anchor="e",
            justify="right",
        )
        self.probability_label.pack(fill="x", pady=(6, 2))
        self.chart_frame = tk.Frame(self.result_card, bg=COLORS["white"])
        self.chart_frame.pack(fill="x", pady=(0, 6))

        tk.Label(
            self.result_card,
            text="الكلمات التي أثرت في النتيجة",
            bg=COLORS["white"],
            fg=COLORS["ink"],
            font=("Segoe UI", 11, "bold"),
            anchor="e",
        ).pack(fill="x", pady=(6, 4))
        explanation_frame = tk.Frame(self.result_card, bg=COLORS["white"])
        explanation_frame.pack(fill="x")
        explanation_scrollbar = ttk.Scrollbar(explanation_frame, orient="vertical")
        self.explanation_box = tk.Text(
            explanation_frame,
            height=5,
            wrap="word",
            font=("Segoe UI", 11),
            bg=COLORS["white"],
            fg=COLORS["muted"],
            padx=8,
            pady=6,
            relief="solid",
            borderwidth=1,
            yscrollcommand=explanation_scrollbar.set,
        )
        explanation_scrollbar.configure(command=self.explanation_box.yview)
        self.explanation_box.tag_configure("rtl", justify="right", spacing1=3, spacing3=5)
        explanation_scrollbar.pack(side="right", fill="y")
        self.explanation_box.pack(side="left", fill="both", expand=True)
        self.explanation_box.configure(state="disabled")

        self.result_warning_label = tk.Label(
            self.result_card,
            text="الدرجات تقدير نصّي من الموديل؛ لا تثبت هوية المرسل ولا تؤكد وحدها أن النص آمن أو احتيالي.",
            bg=COLORS["white"],
            fg="#7A5A19",
            font=("Segoe UI", 9),
            anchor="e",
            justify="right",
            wraplength=1000,
        )
        self.result_warning_label.pack(fill="x", pady=(10, 0))
        self.result_card.bind("<Configure>", self._resize_result_text)

    def _build_results_tab(self) -> None:
        tk.Label(
            self.results_tab,
            text="تقييم النماذج على نصوص لم تدخل في تدريب كل تجربة",
            bg=COLORS["pale"],
            fg=COLORS["ink"],
            font=("Segoe UI", 13, "bold"),
            anchor="e",
        ).pack(fill="x", pady=(0, 8))

        metrics = self._read_metrics()
        columns = ("profile", "evaluation", "model", "accuracy", "precision", "recall", "f1", "roc_auc")
        table_frame = tk.Frame(self.results_tab, bg=COLORS["pale"])
        table_frame.pack(fill="x", pady=(0, 12))
        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        headings = {
            "profile": "نوع النص",
            "evaluation": "مجموعة التقييم",
            "model": "النموذج",
            "accuracy": "الصحة الكلية",
            "precision": "الإحكام",
            "recall": "الاسترجاع",
            "f1": "درجة F1",
            "roc_auc": "مساحة ROC",
        }
        widths = {"profile": 125, "evaluation": 190, "model": 175, "accuracy": 100, "precision": 90, "recall": 95, "f1": 90, "roc_auc": 95}
        for column in columns:
            table.heading(column, text=headings[column])
            table.column(column, width=widths[column], anchor="center", stretch=True)
        if not metrics.empty:
            for _, row in metrics.iterrows():
                evaluation = str(row.get("evaluation_set", ""))
                evaluation_display = {
                    "stratified_test": "اختبار داخلي",
                    "independent_external_test": "اختبار خارجي مستقل",
                    "positive_only_external_challenge": "رسائل احتيال فقط",
                }.get(evaluation, evaluation)
                values = [
                    {"sms": "SMS وتنبيهات", "email": "إيميلات", "jobs": "وظائف"}.get(str(row.get("profile", "")), ""),
                    evaluation_display,
                    {"Logistic Regression": "الانحدار اللوجستي", "K-Nearest Neighbors": "أقرب الجيران"}.get(
                        str(row.get("model", "")), str(row.get("model", ""))
                    ),
                    *[self._format_metric(row.get(key)) for key in ("accuracy", "precision", "recall", "f1", "roc_auc")],
                ]
                table.insert("", "end", values=values)
        table_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
        table.configure(xscrollcommand=table_scrollbar.set)
        table.pack(fill="x")
        table_scrollbar.pack(fill="x")

        self.data_scope_label = self._read_only_text(self.results_tab, height=5)
        self.data_scope_label.pack(fill="x", pady=(0, 10))
        self._set_data_scope()

        self.external_sms_label = self._read_only_text(self.results_tab, height=3)
        self.external_sms_label.pack(fill="x", pady=(0, 8))
        self.external_email_label = self._read_only_text(self.results_tab, height=3)
        self.external_email_label.pack(fill="x", pady=(0, 8))
        self._set_external_summaries()

        tk.Label(
            self.results_tab,
            text="تفسير الدرجات",
            bg=COLORS["pale"],
            fg=COLORS["ink"],
            font=("Segoe UI", 12, "bold"),
            anchor="e",
        ).pack(fill="x", pady=(8, 5))
        note = (
            "الـAccuracy وحدها قد تخفي الأخطاء، خصوصًا في بيانات الوظائف لأن الإعلانات الاحتيالية قليلة. "
            "راجع Precision وRecall وF1 معًا. بيانات الوظائف والإيميلات الإنجليزية لا تمثل السوق المصري، "
            "ورسائل SMS المترجمة ليست رسائل مصرية أصلية."
        )
        note_box = self._read_only_text(self.results_tab, height=4)
        note_box.pack(fill="x", pady=(0, 12))
        self._set_read_only_text(note_box, note)

        for profile in ("sms", "email", "jobs"):
            image_path = MODEL_PATHS[profile].parent.parent / "outputs" / "figures" / f"{profile}_confusion_matrix.png"
            if image_path.exists():
                try:
                    image = tk.PhotoImage(file=str(image_path))
                    image = image.subsample(2, 2)
                    setattr(self, f"{profile}_confusion_image", image)
                    tk.Label(
                        self.results_tab,
                        text={"sms": "مصفوفة أخطاء SMS", "email": "مصفوفة أخطاء الإيميل", "jobs": "مصفوفة أخطاء الوظائف"}[profile],
                        bg=COLORS["pale"],
                        fg=COLORS["ink"],
                        font=("Segoe UI", 11, "bold"),
                        anchor="e",
                    ).pack(fill="x", pady=(8, 3))
                    tk.Label(self.results_tab, image=image, bg=COLORS["pale"]).pack(anchor="center", pady=(0, 12))
                except tk.TclError:
                    continue

    def _build_about_tab(self) -> None:
        text = (
            "فكرة المشروع\n"
            "برنامج محلي يفحص ثلاثة أنواع من النصوص: رسائل SMS وتنبيهات الحسابات، الإيميلات، وإعلانات الوظائف. "
            "يختار المستخدم النوع، ثم يلصق النص ليحصل على تقدير من نموذج مخصص لهذا النوع.\n\n"
            "لماذا ثلاثة نماذج؟\n"
            "الرسالة القصيرة تختلف عن الإيميل وعن إعلان الوظيفة. لذلك يتدرّب نموذج منفصل لكل نوع بدل خلطها في تدريب واحد. "
            "النماذج تستخدم الانحدار اللوجستي مع TF-IDF للكلمات ومقاطع الحروف. في SMS والإيميل نقارن أيضًا بخوارزمية أقرب الجيران.\n\n"
            "مصادر البيانات\n"
            "SMS: مجموعة عربية صغيرة، ومجموعة رسائل إنجليزية تُرجمت آليًا إلى العربية.\n"
            "الإيميل: أمثلة عربية وإنجليزية سليمة أو تصيّد، مع مجموعة إنجليزية خارجية للاختبار.\n"
            "الوظائف: إعلانات إنجليزية سليمة واحتيالية، مع تدريب واختبار من الجزء المصنّف.\n\n"
            "كيف تُقرأ النتيجة؟\n"
            "الدرجة تعبر عن نمط النص الذي تعلّمه الموديل من البيانات. الكلمات المعروضة توضح بعض السمات التي رفعت أو خفضت درجة الخطر. "
            "هذه ليست دقة مضمونة للرسالة الجديدة وليست إثباتًا لهوية المرسل.\n\n"
            "حدود مهمة\n"
            "بيانات SMS المترجمة ليست رسائل مصرية أصلية. بيانات البريد والوظائف باللغة الإنجليزية، وبيانات الوظائف قديمة. "
            "النص وحده لا يكشف دائمًا إن كان اسم البنك أو الشركة مُنتحلًا؛ فذلك يحتاج إلى فحص المرسل والرابط وترويسات البريد.\n\n"
            "التصحيح اليدوي\n"
            "يمكن حفظ تصنيفك للنص الحالي. يُستخدم التصحيح في تدريب المجال الذي اخترته بعد إغلاق البرنامج وإعادة تشغيل التجربة. "
            "تصحيح رسالة واحدة يعالج هذا المثال ولا يعلّم قاعدة عامة عن كل رسائل الجهة."
        )
        about_box = self._read_only_text(self.about_tab, height=24)
        about_box.pack(fill="x")
        self._set_read_only_text(about_box, text)

    def _read_only_text(self, parent: tk.Widget, height: int) -> tk.Text:
        frame = tk.Frame(parent, bg=COLORS["white"])
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        widget = tk.Text(
            frame,
            wrap="word",
            height=height,
            font=("Segoe UI", 10),
            bg=COLORS["white"],
            fg=COLORS["ink"],
            padx=12,
            pady=9,
            relief="solid",
            borderwidth=1,
            yscrollcommand=scrollbar.set,
        )
        scrollbar.configure(command=widget.yview)
        widget.tag_configure("rtl", justify="right", spacing1=3, spacing3=6)
        scrollbar.pack(side="right", fill="y")
        widget.pack(side="left", fill="both", expand=True)
        frame.pack(fill="x")
        widget.configure(state="disabled")
        widget._frame = frame
        return widget

    @staticmethod
    def _set_read_only_text(widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value, "rtl")
        widget.configure(state="disabled")
        widget.yview_moveto(0)

    @staticmethod
    def _button(parent: tk.Widget, title: str, command, color: str) -> tk.Button:
        return tk.Button(
            parent,
            text=title,
            command=command,
            bg=color,
            fg=COLORS["white"],
            activebackground=color,
            activeforeground=COLORS["white"],
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    @staticmethod
    def _read_metrics() -> pd.DataFrame:
        return pd.read_csv(METRICS_PATH) if METRICS_PATH.exists() else pd.DataFrame()

    @staticmethod
    def _format_metric(value: object) -> str:
        try:
            if pd.isna(value):
                return "—"
            return f"{float(value):.3f}"
        except (TypeError, ValueError):
            return "—"

    def _set_data_scope(self) -> None:
        if not METADATA_PATH.exists():
            self._set_read_only_text(self.data_scope_label, "شغّل التجربة لعرض أحجام البيانات المستخدمة.")
            return
        summary = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        lines = []
        for profile, details in summary.get("profiles", {}).items():
            raw = details.get("raw_data", {})
            cleaned = details.get("clean_data", {})
            name = PROFILE_LABELS.get(profile, profile)
            lines.append(
                f"{name}: {raw.get('rows', 0):,} نص قبل التنظيف، "
                f"{cleaned.get('rows', 0):,} بعد حذف التكرار؛ "
                f"عادي {cleaned.get('ham', 0):,} ومريب {cleaned.get('spam', 0):,}."
            )
            for source, counts in cleaned.get("by_source", {}).items():
                lines.append(
                    f"  {source}: {counts.get('ham', 0):,} عادي و{counts.get('spam', 0):,} مريب."
                )
        self._set_read_only_text(self.data_scope_label, "\n".join(lines))

    def _set_external_summaries(self) -> None:
        if not METADATA_PATH.exists():
            message = "شغّل التجربة لعرض الاختبارات الخارجية."
            self._set_read_only_text(self.external_sms_label, message)
            self._set_read_only_text(self.external_email_label, message)
            return
        summary = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        profiles = summary.get("profiles", {})
        sms = profiles.get("sms", {}).get("external_test", {})
        if sms.get("rows"):
            sms_text = (
                f"اختبار SMS الخارجي: اكتشف الموديل {sms.get('spam_detected', 0)} من {sms['rows']} "
                f"رسالة مصنفة احتيالًا (استرجاع {sms.get('recall', 0):.1%}). هذه المجموعة لا تحتوي رسائل سليمة، "
                "لذلك لا نحسب منها الصحة الكلية."
            )
        else:
            sms_text = "لم تتوفر مجموعة SMS خارجية للاختبار."
        self._set_read_only_text(self.external_sms_label, sms_text)

        email = profiles.get("email", {}).get("external_test", {})
        if email.get("rows"):
            email_text = (
                f"اختبار الإيميل الخارجي: {email['rows']:,} رسالة إنجليزية؛ "
                f"الصحة {email.get('accuracy', 0):.1%}، والإحكام {email.get('precision', 0):.1%}، "
                f"والاسترجاع {email.get('recall', 0):.1%}، وF1 {email.get('f1', 0):.3f}."
            )
        else:
            email_text = "لم تتوفر مجموعة إيميلات خارجية للاختبار."
        self._set_read_only_text(self.external_email_label, email_text)

    def _profile(self) -> str:
        return self.profile_by_label.get(self.profile_var.get(), "sms")

    def _profile_changed(self, _event=None) -> None:
        profile = self._profile()
        self.prediction_label.configure(text=f"اكتب {PROFILE_TERMS[profile]['item']} ثم اضغط على تحليل النص", fg=COLORS["ink"])
        self.probability_label.configure(text="")
        self._set_read_only_text(self.explanation_box, "")
        for child in self.chart_frame.winfo_children():
            child.destroy()

    def open_text_file(self) -> None:
        path = filedialog.askopenfilename(
            title="اختيار ملف نصي",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            content = Path(path).read_text(encoding="utf-8", errors="replace")
            self.message_box.delete("1.0", "end")
            self.message_box.insert("1.0", content, "rtl")

    def clear(self) -> None:
        self.message_box.delete("1.0", "end")
        self._profile_changed()

    def save_review(self, label: str) -> None:
        text = self.message_box.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("نص فارغ", "اكتب النص أولًا.")
            return
        profile = self._profile()
        REVIEWED_EXAMPLES_FILE.parent.mkdir(parents=True, exist_ok=True)
        if REVIEWED_EXAMPLES_FILE.exists():
            reviewed = pd.read_csv(REVIEWED_EXAMPLES_FILE)
        else:
            reviewed = pd.DataFrame(columns=["profile", "text", "label", "source"])
        if "profile" not in reviewed:
            reviewed["profile"] = "sms"
        reviewed = reviewed[~((reviewed["profile"] == profile) & (reviewed["text"].map(review_key) == review_key(text)))]
        reviewed.loc[len(reviewed)] = {"profile": profile, "text": text, "label": label, "source": "User review"}
        reviewed.to_csv(REVIEWED_EXAMPLES_FILE, index=False, encoding="utf-8-sig")
        self.reviewed_labels[f"{profile}:{review_key(text)}"] = label
        self.analyze()
        messagebox.showinfo(
            "تم حفظ التصحيح",
            "حُفظ المثال لهذا النوع من النصوص. أغلق الواجهة، ثم شغّل python -m src.run_experiment لإعادة التدريب.",
        )

    def analyze(self) -> None:
        text = self.message_box.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("نص فارغ", "اكتب النص أولًا.")
            return
        profile = self._profile()
        pipeline = self.models[profile]
        classifier = pipeline["classifier"]
        vectorizer = pipeline["vectorizer"]
        probabilities = classifier.predict_proba(vectorizer.transform([text]))[0]
        classes = list(classifier.classes_)
        risk_score = float(probabilities[classes.index("spam")])
        safe_score = float(probabilities[classes.index("ham")])
        reviewed_label = self.reviewed_labels.get(f"{profile}:{review_key(text)}")
        terms = PROFILE_TERMS[profile]

        if reviewed_label == "ham":
            title = f"تصنيفك المحفوظ: {terms['safe']}"
            color = COLORS["teal"]
        elif reviewed_label == "spam":
            title = f"تصنيفك المحفوظ: {terms['risk']}"
            color = COLORS["orange"]
        elif risk_score >= 0.5:
            title = f"الموديل يراها أقرب إلى: {terms['risk']}"
            color = COLORS["orange"]
        else:
            title = f"الموديل يراها أقرب إلى: {terms['safe']}"
            color = COLORS["teal"]

        self.prediction_label.configure(text=title, fg=color)
        score_title = "درجات الموديل العام قبل تصحيحك:" if reviewed_label else "درجات الموديل:"
        self.probability_label.configure(
            text=f"{score_title}\nدرجة النص المريب: {risk_score * 100:.1f}٪\nدرجة النص السليم: {safe_score * 100:.1f}٪"
        )
        self._draw_probability_chart(safe_score, risk_score)

        explanation = explain_message(pipeline, text)
        positive = ", ".join(term for term, _ in explanation["spam"]) or "لم تظهر كلمات واضحة رفعت الدرجة."
        negative = ", ".join(term for term, _ in explanation["ham"]) or "لم تظهر كلمات واضحة خفضت الدرجة."
        if reviewed_label:
            note = "التصنيف الظاهر محفوظ من تصحيحك؛ النسب المعروضة ما زالت درجات الموديل قبل هذا التصحيح."
        elif profile == "sms":
            note = "جزء من تدريب SMS مترجم آليًا؛ قد يختلف عن رسائل الشركات المصرية."
        elif profile == "email":
            note = "داتا الإيميل محدودة، والاختبار الخارجي باللغة الإنجليزية."
        else:
            note = "داتا الوظائف بالإنجليزية وقديمة؛ لا تعتبر النتيجة حكمًا على إعلان مصري."
        self._set_read_only_text(
            self.explanation_box,
            f"كلمات رفعت درجة الخطر: {positive}\nكلمات خفضت درجة الخطر: {negative}\n{note}",
        )

    def _draw_probability_chart(self, safe_score: float, risk_score: float) -> None:
        for child in self.chart_frame.winfo_children():
            child.destroy()
        width = max(560, self.chart_frame.winfo_width() - 30)
        figure = Figure(figsize=(min(10.5, width / 100), 1.7), dpi=100)
        axis = figure.add_subplot(111)
        axis.barh(["Safe", "Suspicious"], [safe_score, risk_score], color=[COLORS["teal"], COLORS["orange"]])
        axis.set_xlim(0, 1)
        axis.set_xlabel("Model score")
        axis.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        axis.grid(axis="x", alpha=0.2)
        figure.tight_layout(pad=0.8)
        canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x")
        self.probability_figure = figure
        self.probability_canvas = canvas


def main() -> None:
    root = tk.Tk()
    try:
        MessageSafetyApp(root)
    except FileNotFoundError as error:
        root.destroy()
        messagebox.showerror("النماذج غير جاهزة", str(error))
        return
    root.mainloop()


if __name__ == "__main__":
    main()
