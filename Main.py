from gui import DateConverterGUI
from Dates_functions import DateConverterLogic
import pyperclip
from tkinter import messagebox

def main():
    date_converter = DateConverterLogic()

    def convert_date():
        text = gui.text_area_convert.get("1.0", "end-1c").strip()
        result = date_converter.convert_date(text)
        gui.result_entry_convert.delete(0, 'end')
        gui.result_entry_convert.insert(0, result)

    def format_date_action():
        text = gui.text_area_format.get("1.0", "end-1c").strip()
        result = date_converter.format_date(text)
        gui.result_entry_format.delete(0, 'end')
        gui.result_entry_format.insert(0, result)

    def copy_date(entry):
        converted_date = entry.get()
        if converted_date:
            pyperclip.copy(converted_date)
            messagebox.showinfo("Success", "Date copied.")
        else:
            messagebox.showinfo("Error", "No date to copy.")

    gui = DateConverterGUI(
        convert_callback=convert_date,
        format_callback=format_date_action,
        copy_callback=copy_date
    )
    gui.run()

if __name__ == "__main__":
    main()