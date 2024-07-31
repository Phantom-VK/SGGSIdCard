import tkinter as tk
from tkinter import messagebox
from id_card import create_id_card

def generate_id_card():
    details = {
        "name": name_entry.get(),
        "reg_no": reg_no_entry.get(),
        "branch": branch_entry.get(),
        "dob": dob_entry.get(),
        "mob_no": mob_no_entry.get(),
        "photo_path": photo_path_entry.get()
    }
    create_id_card(details)
    messagebox.showinfo("Success", "ID Card created successfully!")

root = tk.Tk()
root.title("ID Card Generator")

tk.Label(root, text="Full Name").grid(row=0)
tk.Label(root, text="Reg. No.").grid(row=1)
tk.Label(root, text="Branch").grid(row=2)
tk.Label(root, text="Date of Birth").grid(row=3)
tk.Label(root, text="Mobile Number").grid(row=4)
tk.Label(root, text="Photo Path").grid(row=5)

name_entry = tk.Entry(root)
reg_no_entry = tk.Entry(root)
branch_entry = tk.Entry(root)
dob_entry = tk.Entry(root)
mob_no_entry = tk.Entry(root)
photo_path_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
reg_no_entry.grid(row=1, column=1)
branch_entry.grid(row=2, column=1)
dob_entry.grid(row=3, column=1)
mob_no_entry.grid(row=4, column=1)
photo_path_entry.grid(row=5, column=1)

tk.Button(root, text='Generate ID Card', command=generate_id_card).grid(row=6, column=1, pady=4)

root.mainloop()
