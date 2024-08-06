import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry
import logging
import check_inputs
from id_card import create_id_card
from pdf_converter import convert_to_pdf
from firebase_config import initialize_firebase, fetch_student_details
from firebase_admin import db

# Initialize Firebase
initialize_firebase()


def resource_path(relative_path):
    """ Get absolute path to resource, works for development and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def show_image(image_path, label):
    """
    Display an image on the specified label.
    """
    img = Image.open(resource_path(image_path))
    img = img.resize((300, 500))
    img = ImageTk.PhotoImage(img)
    label.configure(image=img)
    label.image = img


class IDCardApp:
    def __init__(self, root):
        self.right_pane = None
        self.middle_pane = None
        self.paned_window = None
        self.left_pane = None
        self.root = root
        self.root.title("SGGSIdCard Generator")
        self.root.geometry("1920x1080")

        self.entries = {}
        self.image_labels = {
            "front": None,
            "back": None,
        }
        self.current_image_path = None
        self.current_student_name = None

        self.initial_widgets = []
        self.create_widgets()

    def create_widgets(self):
        """
        Create the main layout with three panes.
        """
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Middle and Right Panes - ID Card Preview
        self.middle_pane = self._create_preview_pane("Front")
        self.right_pane = self._create_preview_pane("Back")
        self.paned_window.add(self.middle_pane, stretch="always")
        self.paned_window.add(self.right_pane, stretch="always")

        self._create_input_pane()

    def _create_input_pane(self):
        """
        Create the input input_pane with entry fields and buttons.
        """

        # Destroy existing widgets in the left pane if they exist
        if hasattr(self, 'left_pane') and self.left_pane is not None:
            for widget in self.left_pane.winfo_children():
                widget.destroy()
            self.left_pane.destroy()

        input_pane = CTkFrame(self.paned_window)

        self.reg_label = CTkLabel(input_pane, text="Enter Reg. No.")
        self.reg_label.pack(pady=10)
        self.initial_widgets.append(self.reg_label)

        self.reg_entry = CTkEntry(input_pane)
        self.reg_entry.pack(pady=10)
        self.initial_widgets.append(self.reg_entry)

        self.generate_btn = CTkButton(input_pane, text="Generate ID Card", command=self.generate_id_card)
        self.generate_btn.pack(pady=10)
        self.initial_widgets.append(self.generate_btn)

        self.or_label = CTkLabel(input_pane, text="OR")
        self.or_label.pack(pady=10)
        self.initial_widgets.append(self.or_label)

        self.new_student_btn = CTkButton(input_pane, text="Add New Student", command=self.add_new_student)
        self.new_student_btn.pack(pady=10)
        self.initial_widgets.append(self.new_student_btn)

        self.convert_to_pdf_btn = CTkButton(input_pane, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_to_pdf_btn.pack(pady=10)
        self.initial_widgets.append(self.convert_to_pdf_btn)

        # Left Pane - Input Options
        self.left_pane = input_pane
        self.paned_window.add(input_pane, stretch="always")

    def _create_preview_pane(self, side):
        """
        Create a preview pane for displaying ID card images.
        """
        pane = CTkFrame(self.paned_window)

        label = CTkLabel(pane, text=f"{side} Side of ID Card")
        label.pack(pady=10)

        image_label = CTkLabel(pane)
        image_label.pack(pady=10)
        self.image_labels[side.lower()] = image_label

        return pane

    def generate_id_card(self):
        """
        Generate an ID card for the entered registration number.
        """
        reg_no = self.reg_entry.get().upper()
        if not check_inputs.check_reg(reg_no):
            messagebox.showerror("Error", "Invalid registration number format.")
            return

        details = fetch_student_details(reg_no)
        if details:
            front_image_path, back_image_path = create_id_card(details)
            show_image(front_image_path, self.image_labels["front"])
            show_image(back_image_path, self.image_labels["back"])
            self.current_image_path = front_image_path  # Storefront image path for conversion
            self.current_student_name = details["name"]
        else:
            messagebox.showerror("Error", "No student details found in the database")

    def add_new_student(self):
        """
        Display the form for adding a new student.
        """
        # Destroy existing widgets in the left pane
        for widget in self.left_pane.winfo_children():
            widget.destroy()

        # Add form widgets
        labels = ["Name", "Reg. No.", "Branch", "DOB", "Mob. No.", "Parent Mob. No.", "Address"]
        keys = ["name", "reg_no", "branch", "dob", "mob_no", "parent_mob_no", "address"]

        for label, key in zip(labels, keys):
            CTkLabel(self.left_pane, text=label).pack(pady=5)
            entry = CTkEntry(self.left_pane)
            entry.pack(pady=5)
            self.entries[key] = entry

        submit_button = CTkButton(self.left_pane, text="Submit", command=self.submit_new_student)
        submit_button.pack(pady=20)

        back_button = CTkButton(self.left_pane, text="Back", command=self.show_initial_widgets)
        back_button.pack(pady=5)

    def show_initial_widgets(self):
        """
        Restore the initial widgets in the left pane.
        """
        # Destroy existing widgets in the left pane
        for widget in self.left_pane.winfo_children():
            widget.destroy()

        # Restore initial widgets
        self._create_input_pane()

    def submit_new_student(self):
        """
        Submit the new student details to Firebase.
        """
        details = {
            "name": self.entries["name"].get(),
            "reg_no": self.entries["reg_no"].get(),
            "branch": self.entries["branch"].get(),
            "dob": self.entries["dob"].get(),
            "mob_no": self.entries["mob_no"].get(),
            "parent_mob_no": self.entries["parent_mob_no"].get(),
            "address": self.entries["address"].get()
        }
        ref = db.reference(f'/students/{details["reg_no"].upper()}')
        ref.set(details)
        messagebox.showinfo("Success", "Student added successfully!")
        self.show_initial_widgets()

    def convert_to_pdf(self):
        """
        Convert the current ID card images to a PDF.
        """
        if self.current_image_path:
            back_image_path = self.current_image_path.replace("front", "back")

            convert_to_pdf(self.current_image_path, back_image_path, self.current_student_name)
            messagebox.showinfo("Success", "ID Card successfully converted to PDF and saved to Downloads folder")
        else:
            messagebox.showerror("Error", "No image to convert")


if __name__ == "__main__":
    root = CTk()
    app = IDCardApp(root)
    root.mainloop()
