from hijri_converter import convert
from datetime import datetime
import re
from tkinter import messagebox

class DateConverterLogic:
    def __init__(self):
        self.date_pattern = r'(\d{1,4})[-/.](\d{1,2})[-/.](\d{1,4})'

    def find_date(self, text):
        match = re.search(self.date_pattern, text)
        if match:
            part1, part2, part3 = map(int, match.groups())
            # If first number is year (YYYY-MM-DD)
            if part1 > 1000:
                year, month, day = part1, part2, part3
            # If it's DD-MM-YYYY
            else:
                day, month, year = part1, part2, part3
            return year, month, day
        return None

    def convert_date(self, text):
        if not text:
            messagebox.showinfo("Error", "Please enter a date.")
            return None

        date_parts = self.find_date(text)
        
        if date_parts:
            year, month, day = date_parts
            # Get original separator
            separator_matches = re.findall(r'[-/.]', text)
            separator = separator_matches[0] if separator_matches else "/"

            try:
                # Determine date type and convert
                if year > 1500:  # If Gregorian
                    converted = convert.Gregorian(year, month, day).to_hijri()
                else:  # If Hijri
                    converted = convert.Hijri(year, month, day).to_gregorian()

                # Always format as DD-MM-YYYY
                result = f"{converted.day:02d}{separator}{converted.month:02d}{separator}{converted.year}"
                return result
                
            except ValueError:
                messagebox.showinfo("Error", "Invalid date or conversion failed.")
                return None
        else:
            messagebox.showinfo("Error", "No date found in text.")
            return None

    def find_and_format_date(self, text):
        if not text:
            messagebox.showinfo("Error", "Please enter a date.")
            return None

        # Clean the text and find the date pattern
        text = text.strip()
        match = re.search(self.date_pattern, text)
        
        if not match:
            messagebox.showinfo("Error", "No valid date found.")
            return None

        # Extract the parts and separators
        part1, part2, part3 = map(int, match.groups())
        separator_matches = re.findall(r'[-/.]', text)
        separator = separator_matches[0] if separator_matches else "/"

        # Determine the date format and rearrange if needed
        if part1 > 1000:  # If first number is year (YYYY-MM-DD)
            year, month, day = part1, part2, part3
            # Rearrange to DD-MM-YYYY
            formatted_date = f"{day:02d}{separator}{month:02d}{separator}{year}"
        else:  # Assume DD-MM-YYYY format
            day, month, year = part1, part2, part3
            formatted_date = f"{day:02d}{separator}{month:02d}{separator}{year}"

        return formatted_date

    def format_date(self, text):
        try:
            return self.find_and_format_date(text)
        except ValueError:
            messagebox.showinfo("Error", "Invalid date format.")
            return None
