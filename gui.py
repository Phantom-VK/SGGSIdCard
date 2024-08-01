import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from id_card import create_id_card
from pdf_converter import convert_to_pdf
from firebase_config import initialize_firebase, fetch_student_details
from firebase_admin import db

# Initialize Firebase
initialize_firebase()


class IDCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ID Card Generator")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_pane = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.left_pane, weight=1)

        self.right_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_pane, weight=3)

        self.new_student_btn = ttk.Button(self.left_pane, text="Add New Student", command=self.add_new_student)
        self.new_student_btn.pack(fill="x", pady=10, padx=10)

        self.generate_idcard_btn = ttk.Button(self.left_pane, text="Generate ID Card of Existing Student",
                                              command=self.generate_for_existing_student)
        self.generate_idcard_btn.pack(fill="x", pady=10, padx=10)

        self.image_label = ttk.Label(self.right_pane)
        self.image_label.pack(pady=10)

        self.convert_to_pdf_btn = ttk.Button(self.right_pane, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_to_pdf_btn.pack()

    def generate_for_existing_student(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Enter student registration no")
        new_window.geometry("400x200")

        tk.Label(new_window, text="Enter Reg.No.").pack(pady=5)
        self.entry = tk.Entry(new_window)
        self.entry.pack(pady=5)

        generate_btn = tk.Button(new_window, text="Generate",
                                 command=lambda: self.generate_id_card(self.entry.get().upper()))
        generate_btn.pack(pady=20)

    def add_new_student(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Add New Student")
        new_window.geometry("400x400")

        labels = ["Name", "Reg. No.", "Branch", "DOB", "Mob. No."]
        self.entries = {}
        for label in labels:
            tk.Label(new_window, text=label).pack(pady=5)
            entry = tk.Entry(new_window)
            entry.pack(pady=5)
            self.entries[label.lower()] = entry

        submit_button = tk.Button(new_window, text="Submit", command=self.submit_new_student)
        submit_button.pack(pady=20)

    def submit_new_student(self):
        details = {
            "name": self.entries["name"].get(),
            "reg_no": self.entries["reg. no."].get(),
            "branch": self.entries["branch"].get(),
            "dob": self.entries["dob"].get(),
            "mob_no": self.entries["mob. no."].get()
        }
        ref = db.reference(f'/students/{details["reg_no"].upper()}')
        ref.set(details)
        messagebox.showinfo("Success", "Student added successfully!")

    def generate_id_card(self, reg_no):
        details = fetch_student_details(reg_no)
        if details:
            image_path = create_id_card(details)
            self.show_image(image_path)
            self.current_image_path = image_path
            self.current_student_name = details["name"]
        else:
            messagebox.showerror("Error", "No student details found in the database")

    def show_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((300, 500))
        img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img)
        self.image_label.image = img

    def convert_to_pdf(self):
        if hasattr(self, "current_image_path"):
            convert_to_pdf(self.current_image_path, self.current_student_name)
            messagebox.showinfo("Success", "ID Card successfully converted to PDF and saved to Downloads folder")
        else:
            messagebox.showerror("Error", "No image to convert")

