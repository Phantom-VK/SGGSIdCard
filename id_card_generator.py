import tkinter as tk

from id_card_design import generate_id_card

# Create the GUI
app = tk.Tk()
app.title("ID Card Generator")

tk.Label(app, text="Enter Registration Number:").pack()
reg_number = tk.Entry(app)
reg_number.pack()

tk.Label(app, text="Enter Full Name:").pack()
entry_name = tk.Entry(app)
entry_name.pack()

tk.Label(app, text="Enter Branch:").pack()
entry_branch = tk.Entry(app)
entry_branch.pack()

tk.Label(app, text="Enter Age:").pack()
entry_age = tk.Entry(app)
entry_age.pack()

tk.Label(app, text="Enter Date of Birth:").pack()
entry_dob = tk.Entry(app)
entry_dob.pack()

tk.Label(app, text="Enter Blood Group:").pack()
entry_blood_group = tk.Entry(app)
entry_blood_group.pack()

tk.Label(app, text="Enter Mobile Number:").pack()
entry_mobile_number = tk.Entry(app)
entry_mobile_number.pack()

tk.Label(app, text="Enter Address:").pack()
entry_address = tk.Entry(app)
entry_address.pack()

tk.Button(app, text="Generate ID Card", command=generate_id_card).pack()

app.mainloop()
