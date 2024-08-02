import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from id_card import create_id_card
from pdf_converter import convert_to_pdf
from firebase_config import initialize_firebase, fetch_student_details
from firebase_admin import db
from check_inputs import check_reg

# Initialize Firebase
initialize_firebase()


class IDCardApp:
    def __init__(self, root):
        self.current_student_name = None
        self.current_image_path = None
        self.entries = None
        self.back_btn = None
        self.convert_to_pdf_btn = None
        self.image_label = None
        self.new_student_btn = None
        self.or_label = None
        self.generate_idcard_btn = None
        self.reg_no_entry = None
        self.reg_no_label = None
        self.right_pane = None
        self.left_pane = None
        self.paned_window = None
        self.root = root
        self.root.title("ID Card Generator")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#E0F7FA")
        self.style.configure("TButton", background="#81D4FA", foreground="black", font=("Arial", 12, "bold"))
        self.style.configure("TLabel", background="#E0F7FA", foreground="black", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12))

        self.create_widgets()

    def create_widgets(self):
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_pane = ttk.Frame(self.paned_window, width=300)
        self.paned_window.add(self.left_pane, weight=1)

        self.right_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_pane, weight=3)

        self.create_left_pane_widgets()
        self.create_right_pane_widgets()

    def create_left_pane_widgets(self):
        # Clear left pane first
        for widget in self.left_pane.winfo_children():
            widget.destroy()

        self.reg_no_label = ttk.Label(self.left_pane, text="Enter Reg.No. (max 10 characters):")
        self.reg_no_label.pack(pady=5)

        self.reg_no_entry = ttk.Entry(self.left_pane)
        self.reg_no_entry.pack(pady=5)

        self.generate_idcard_btn = ttk.Button(self.left_pane, text="Generate ID Card",
                                              command=self.generate_id_card_from_entry)
        self.generate_idcard_btn.pack(fill="x", pady=10, padx=10)

        self.or_label = ttk.Label(self.left_pane, text="OR")
        self.or_label.pack(pady=10)

        self.new_student_btn = ttk.Button(self.left_pane, text="Add New Student", command=self.add_new_student)
        self.new_student_btn.pack(fill="x", pady=10, padx=10)

    def create_right_pane_widgets(self):
        self.image_label = ttk.Label(self.right_pane)
        self.image_label.pack(pady=10)

        self.convert_to_pdf_btn = ttk.Button(self.right_pane, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_to_pdf_btn.pack()
        self.convert_to_pdf_btn.pack_forget()  # Hide the button initially

    def generate_id_card_from_entry(self):
        reg_no = self.reg_no_entry.get().upper()
        if not check_reg(reg_no):
            messagebox.showerror("Error", "Invalid Registration Number")
            return
        self.generate_id_card(reg_no)

    def add_new_student(self):
        # Clear left pane first
        for widget in self.left_pane.winfo_children():
            widget.destroy()

        self.back_btn = ttk.Button(self.left_pane, text="Back", command=self.create_left_pane_widgets)
        self.back_btn.pack(fill="x", pady=10, padx=10)

        labels = ["Name", "Reg. No.", "Branch", "DOB", "Mob. No."]
        self.entries = {}
        for label in labels:
            ttk.Label(self.left_pane, text=label).pack(pady=5)
            entry = ttk.Entry(self.left_pane)
            entry.pack(pady=5)
            self.entries[label.lower()] = entry

        submit_button = ttk.Button(self.left_pane, text="Submit", command=self.submit_new_student)
        submit_button.pack(pady=20)

    def submit_new_student(self):
        reg_no = self.entries["reg. no."].get().upper()
        if not check_reg(reg_no):
            messagebox.showerror("Error", "Invalid Registration Number")
            return
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
        self.create_left_pane_widgets()

    def generate_id_card(self, reg_no):
        details = fetch_student_details(reg_no)
        if details:
            image_path = create_id_card(details)
            self.show_image(image_path)
            self.current_image_path = image_path
            self.current_student_name = details["name"]
            self.convert_to_pdf_btn.pack()  # Show the button after generating the ID card
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


if __name__ == "__main__":
    root = tk.Tk()
    app = IDCardApp(root)
    root.mainloop()
