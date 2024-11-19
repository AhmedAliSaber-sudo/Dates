import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class DateConverterGUI:
    def __init__(self, convert_callback, format_callback, copy_callback):
        self.window = tk.Tk()
        self.window.title("Dateso")
        self.window.geometry("300x300")
        self.window.resizable(False, False)
        
        self.setup_window_icon()
        self.create_widgets()
        self.setup_callbacks(convert_callback, format_callback, copy_callback)
        self.create_context_menu()

    def setup_window_icon(self):
        try:
            import sys
            import os
            
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(base_path, 'calendar_icon.ico')
            self.window.iconbitmap(icon_path)
            
        except Exception as e:
            print(f"Could not load icon: {e}")

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Convert tab
        self.convert_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.convert_frame, text='Convert')
        self.create_convert_widgets()

        # Format tab
        self.format_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.format_frame, text='Format')
        self.create_format_widgets()

    def create_convert_widgets(self):
        ttk.Label(self.convert_frame, text="Convert Date:").pack(pady=5)
        self.text_area_convert = tk.Text(self.convert_frame, height=4, width=40)
        self.text_area_convert.pack(pady=5)

        self.convert_button = ttk.Button(self.convert_frame, text="Convert")
        self.convert_button.pack(pady=5)

        ttk.Label(self.convert_frame, text="Converted Date:").pack(pady=5)
        self.result_entry_convert = ttk.Entry(self.convert_frame, width=40)
        self.result_entry_convert.pack(pady=5)

        self.copy_button_convert = ttk.Button(self.convert_frame, text="Copy")
        self.copy_button_convert.pack(pady=5)

    def create_format_widgets(self):
        ttk.Label(self.format_frame, text="Format Date:").pack(pady=5)
        self.text_area_format = tk.Text(self.format_frame, height=4, width=40)
        self.text_area_format.pack(pady=5)

        self.format_button = ttk.Button(self.format_frame, text="Format")
        self.format_button.pack(pady=5)

        ttk.Label(self.format_frame, text="Formatted Date:").pack(pady=5)
        self.result_entry_format = ttk.Entry(self.format_frame, width=40)
        self.result_entry_format.pack(pady=5)

        self.copy_button_format = ttk.Button(self.format_frame, text="Copy")
        self.copy_button_format.pack(pady=5)

    def setup_callbacks(self, convert_callback, format_callback, copy_callback):
        self.convert_button.config(command=convert_callback)
        self.format_button.config(command=format_callback)
        self.copy_button_convert.config(command=lambda: copy_callback(self.result_entry_convert))
        self.copy_button_format.config(command=lambda: copy_callback(self.result_entry_format))

    def create_context_menu(self):
        self.popup = tk.Menu(self.window, tearoff=0)
        self.popup.add_command(label="Cut", command=self.cut)
        self.popup.add_command(label="Copy", command=self.copy)
        self.popup.add_command(label="Paste", command=self.paste)

        self.text_area_convert.bind("<Button-3>", self.show_popup)
        self.text_area_format.bind("<Button-3>", self.show_popup)

    def show_popup(self, event):
        self.popup.tk_popup(event.x_root, event.y_root)

    def cut(self):
        self.window.focus_get().event_generate("<<Cut>>")

    def copy(self):
        self.window.focus_get().event_generate("<<Copy>>")

    def paste(self):
        self.window.focus_get().event_generate("<<Paste>>")

    def run(self):
        self.window.mainloop()