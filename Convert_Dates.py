import tkinter as tk
from tkinter import messagebox
import pyperclip
import re
from datetime import datetime

# استيراد كسول لـ hijri_converter
hijri_converter = None


def load_hijri_converter():
    global hijri_converter
    if hijri_converter is None:
        from hijri_converter import convert as hijri_converter


def find_date(text):
    # نمط للبحث عن التواريخ بتنسيقات مختلفة
    pattern = r'(\d{1,4})[-/.](\d{1,2})[-/.](\d{1,4})'
    match = re.search(pattern, text)
    if match:
        year, month, day = map(int, match.groups())
        # تصحيح الترتيب إذا كان اليوم أولاً
        if year <= 31 and day > 12:
            year, day = day, year
        return year, month, day
    return None


def format_date(year, month, day, separator1, separator2):
    return f"{day:02d}{separator2}{month:02d}{separator1}{year}"


def convert_date():
    load_hijri_converter()  # تحميل كسول لـ hijri_converter
    text = text_area.get("1.0", tk.END).strip()
    date_parts = find_date(text)

    if date_parts:
        year, month, day = date_parts

        # تحديد الفواصل من النص الأصلي
        separator_matches = re.findall(r'[-/.]', text)
        separator1 = separator_matches[0] if separator_matches else "/"
        separator2 = separator_matches[1] if len(separator_matches) > 1 else separator1

        # تحديد نوع التاريخ وتحويله
        if year > 1500:  # إذا كان التاريخ ميلادي
            converted_date = hijri_converter.Gregorian(year, month, day).to_hijri()
        else:  # إذا كان التاريخ هجري
            converted_date = hijri_converter.Hijri(year, month, day).to_gregorian()

        # تنسيق التاريخ المحول
        result_text = format_date(converted_date.year, converted_date.month, converted_date.day, separator1, separator2)

        result_entry.delete(0, tk.END)
        result_entry.insert(0, result_text)
    else:
        messagebox.showinfo("خطأ", "لم يتم العثور على تاريخ في النص.")


def copy_date():
    converted_date = result_entry.get()
    if converted_date:
        pyperclip.copy(converted_date)
        messagebox.showinfo("نجاح", "تم نسخ التاريخ.")
    else:
        messagebox.showinfo("خطأ", "لا يوجد تاريخ لنسخه.")


def do_popup(event):
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup.grab_release()


# إنشاء واجهة المستخدم
window = tk.Tk()
window.title("محول التاريخ")

# منطقة النص
text_area = tk.Text(window, height=5, width=50)
text_area.pack()

# إنشاء قائمة سياقية
popup = tk.Menu(window, tearoff=0)
popup.add_command(label="قص", command=lambda: text_area.event_generate("<<Cut>>"))
popup.add_command(label="نسخ", command=lambda: text_area.event_generate("<<Copy>>"))
popup.add_command(label="لصق", command=lambda: text_area.event_generate("<<Paste>>"))

# ربط القائمة السياقية بـ text_area
text_area.bind("<Button-3>", do_popup)

# زر التحويل
convert_button = tk.Button(window, text="تحويل", command=convert_date)
convert_button.pack()

# عرض النتيجة
result_label = tk.Label(window, text="التاريخ المحول:")
result_label.pack()
result_entry = tk.Entry(window, width=30)  # خانة لعرض التاريخ المحول
result_entry.pack()

# زر نسخ
copy_button = tk.Button(window, text="نسخ", command=copy_date)
copy_button.pack()

window.mainloop()