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
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill="x", expand=True)

        self.new_student_btn = ttk.Button(self.frame, text="Add New Student", command=self.add_new_student)
        self.new_student_btn.pack(fill="x")

        self.generate_idcard_btn = ttk.Button(self.frame, text="Generate ID Card of Existing Student",
                                              command=self.generate_id_card)
        self.generate_idcard_btn.pack(fill="x", pady=5)

        self.image_label = ttk.Label(self.root)
        self.image_label.pack(pady=10)

        self.convert_to_pdf_btn = ttk.Button(self.root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_to_pdf_btn.pack()

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
        ref = db.reference(f'/students/{details["reg_no"]}')
        ref.set(details)
        messagebox.showinfo("Success", "Student added successfully!")

    def generate_id_card(self):
        details = fetch_student_details()
        # Assuming we want to generate ID card for the first student in the database
        if details:
            for reg_no, student_details in details.items():
                image_path = create_id_card(student_details)
                self.show_image(image_path)
                self.current_image_path = image_path
                break
        else:
            messagebox.showerror("Error", "No student details found in the database")

    def show_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((400, 300))
        img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img)
        self.image_label.image = img

    def convert_to_pdf(self):
        if hasattr(self, "current_image_path"):
            convert_to_pdf(self.current_image_path)
            messagebox.showinfo("Success", "ID Card successfully converted to PDF")
        else:
            messagebox.showerror("Error", "No image to convert")


if __name__ == "__main__":
    root = tk.Tk()
    app = IDCardApp(root)
    root.mainloop()
