import re
import os
import psycopg2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from tkinter import messagebox, OptionMenu
from image_icon_paths import icon_path, dbnames, users, passwords, hosts, ports, image_path

db_password = 'Nolcubs0#'
db_connection = psycopg2.connect(
    dbname=dbnames,
    user=users,
    password=passwords,
    host=hosts,
    port=ports
)
db_cursor = db_connection.cursor()

def submit_and_display_data(entry_fields, logged_in_user, popup, table_name_var, pass_checkbox_var, fail_checkbox_var):
    try:
        db_connection = psycopg2.connect(
            dbname=dbnames,
            user=users,
            password=passwords,
            host=hosts,
            port=ports
        )
        db_cursor = db_connection.cursor()

        data = [entry.get().strip().upper() for entry in entry_fields]  # Strip and convert to uppercase
        part_number, purchase_number, qty, storage = data

        first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

        # Input validation
        if not all(data):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("All fields must be filled out.")

        if len(part_number) > 15:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Part number must be maximum 15 characters.")

        if len(purchase_number) > 8:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Purchase number must be maximum 8 characters.")

        if len(qty) > 4:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Qty must be maximum 4 characters.")

        if len(storage) > 12:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Storage must be maximum 12 characters.")

        selected_table_name = table_name_var.get().upper()  # Convert table name to uppercase
        if not part_number.startswith(selected_table_name):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError(f"Part number must start with '{selected_table_name}'.")

        if not re.match(r'^[A-Z]+\d+$', part_number):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError(f"Part number must start with '{selected_table_name}' followed by numbers.")

        if not re.match(r'^PO\d+$', purchase_number):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Purchase number must start with 'PO' and end with number.")

        if not qty.isdigit():
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Qty must contain only numbers.")

        if not re.match(r'^IQC.*\d$', storage):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Storage must start with 'IQC' and end with a number.")

        selected_table_name = table_name_var.get().upper()  # Convert table name to uppercase

        pass_checked = pass_checkbox_var.get()
        fail_checked = fail_checkbox_var.get()
        
        if not (pass_checked or fail_checked):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Please select either Pass or Fail.")

        if pass_checked and fail_checked:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Please select either Pass or Fail, not both.")

        good_part = pass_checked
        # INSERT into raw_iqc_storage
        query_iqc_storage = '''
            INSERT INTO raw_iqc_storage (part_number, purchase_number, qty, storage, good_parts, "logged_in_users", type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        db_cursor.execute(query_iqc_storage, (part_number, purchase_number, qty, storage, good_part, f"{first_name} {last_name}", selected_table_name.lower()))

        # INSERT into raw_history
        query_raw_history = '''
            INSERT INTO raw_history (part_number, purchase_number, qty, storage, "logged_in_users")
            VALUES (%s, %s, %s, %s, %s)
        '''
        purchase_number_iqc = f"{purchase_number}-Done-IQC"  # Append "IQC" before the purchase number
        db_cursor.execute(query_raw_history, (part_number, purchase_number_iqc, qty, storage, f"{first_name} {last_name}"))


        db_connection.commit()
        popup.grab_set()  # Ensure the popup remains on top before showing the message box
        messagebox.showinfo("Success", "Data inserted successfully")
        popup.destroy()  # Close the popup window after successful database write
    except psycopg2.Error as e:
        if db_connection:
            db_connection.rollback()  # Rollback the transaction in case of error
        messagebox.showerror("Database Error", f"Error inserting data: {e}")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    finally:
        if db_cursor:
            db_cursor.close()  # Close cursor
        if db_connection:
            db_connection.close()  # Close connection

def get_part_numbers():
    try:
        db_cursor.execute("SELECT partnumber FROM raw_partnumbers;")
        part_numbers = db_cursor.fetchall()
        return [part[0] for part in part_numbers]
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Error fetching part numbers: {e}")
        return []


def raw_iqc_entry(root, logged_in_user):
    # Set up the Tkinter window
    popup = tk.Toplevel(root)
    popup.title("IQC Entries Here")

    popup.iconbitmap(icon_path)

    table_names = get_part_numbers()

    add_path = "raw_iqc.png"
    full_path = image_path + add_path
    image = Image.open(full_path)  # Replace with your image path
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(popup, image=photo)
    image_label.grid(row=0, column=0, columnspan=2)  # Adjust row and column as needed

    # Dropdown for selecting table name
    table_name_var = tk.StringVar()
    table_name_label = tk.Label(popup, text="Component Type:")
    table_name_label.grid(row=1, column=0, sticky='e')

    table_names = get_part_numbers()  # Fetch part numbers from the raw_partnumbers table
    table_name_var.set(table_names[0])  # Set default value
    table_name_option_menu = OptionMenu(popup, table_name_var, *table_names)
    table_name_option_menu.config(width=12, bg='black', font=('Arial', 10, 'bold'))  # Adjust width and color as needed
    table_name_option_menu.grid(row=1, column=1, sticky='w')

    # Entry fields
    entry_labels = ["Part Number:", "Purchase Number:", "Quantity:", "Location:"]
    entry_fields = []

    for i, label in enumerate(entry_labels):
        tk.Label(popup, text=label).grid(row=i+2, column=0, sticky='e')  # Adjust row and column as needed
        if label == "Location:" or label == "Purchase Number:":
            default_value = "IQC Area 1" if label == "Location:" else "PO"
            entry = tk.Entry(popup, justify="center")  # Center align text
            entry.insert(0, default_value)  # Set default value
            entry.configure(state='readonly' if label == "Location:" else 'normal')  # Make the entry readonly after setting the default value
            entry.grid(row=i+2, column=1, sticky='w')  # Adjust row and column as needed
        else:
            entry = tk.Entry(popup, justify="center")  # Center align text
            entry.grid(row=i+2, column=1, sticky='w')  # Adjust row and column as needed
        entry_fields.append(entry)

    # Checkboxes for Pass and Fail
    pass_checkbox_var = tk.BooleanVar()
    pass_checkbox = tk.Checkbutton(popup, text="Pass", variable=pass_checkbox_var, command=lambda: fail_checkbox_var.set(False))
    pass_checkbox.grid(row=len(entry_labels) + 2, column=0, padx=(0, 0), pady=5, sticky='e')


    fail_checkbox_var = tk.BooleanVar()
    fail_checkbox = tk.Checkbutton(popup, text="Fail", variable=fail_checkbox_var, command=lambda: pass_checkbox_var.set(False))
    fail_checkbox.grid(row=len(entry_labels) + 2, column=1, padx=(0, 0), pady=5, sticky='w')

    submit_button = ttk.Button(popup, text="Submit", command=lambda: submit_and_display_data(entry_fields, logged_in_user, popup, table_name_var, pass_checkbox_var, fail_checkbox_var))
    submit_button.grid(row=len(entry_labels) + 4, column=0, padx=7, pady=8, sticky="ew")  # Adjust row and column as needed

    def cancel():
        popup.destroy()

    # Button to cancel and close the popup window
    cancel_button = ttk.Button(popup, text="Cancel", width=12, command=cancel)
    cancel_button.grid(row=len(entry_labels) + 4, column=1, padx=7, pady=8)

    popup.mainloop()
