import re
import os
import psycopg2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from image_icon_paths import icon_path, dbnames, users, passwords, hosts, ports, image_path

db_password = 'Nolcubs0#'

def final_add_part_number(entry_fields, password_entry, logged_in_user, popup):
    db_connection = None
    db_cursor = None
    try:
        # Check if the entered password matches the predefined password
        entered_password = password_entry.get().strip()
        if entered_password != "Nolcubs03":
            popup.grab_set()
            messagebox.showerror("Password Incorrect", "Incorrect password. Please try again.")
            return

        # Database connection and data insertion
        db_connection = psycopg2.connect(
            dbname=dbnames,
            user=users,
            password=passwords,
            host=hosts,
            port=ports
        )
        db_cursor = db_connection.cursor()

        data = [entry.get().strip().upper() for entry in entry_fields]  # Strip and convert to uppercase
        part_number = data[0]

        first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

        # Input validation
        if not all(data):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("All fields must be filled out.")

        if not part_number.isalnum():
            popup.grab_set()
            raise ValueError("Part number must contain only letters and numbers.")

        # INSERT into raw_iqc_storage without 'good_parts'
        query_iqc_storage = '''
            INSERT INTO finish_goods_dropdown (finish_goods, "logged_in_users")
            VALUES (%s, %s)
        '''
        db_cursor.execute(query_iqc_storage, (part_number, f"{first_name} {last_name}"))

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


def add_final_seletion_dropdown(root, logged_in_user):
    # Set up the Tkinter window
    popup = tk.Toplevel(root)
    popup.title("MFP Dropdown Selection")

    popup.iconbitmap(icon_path)

    def validate_entry(text):
        # Check if the input text length is less than or equal to 5
        return len(text) <= 4

    # Create a validation function for the entry
    vcmd = (popup.register(validate_entry), '%P')

    add_path = "admin_area.png"
    full_path = image_path + add_path
    image = Image.open(full_path)  # Replace with your image path
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(popup, image=photo)
    image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)  # Add padx and pady for spacing

    # Entry fields
    entry_labels = ["Part Number:"]
    entry_fields = []

    for i, label in enumerate(entry_labels):
        tk.Label(popup, text=label, font="bold").grid(row=i+1, column=0, sticky='e', padx=2, pady=5)  # Add padx and pady for spacing
        entry = tk.Entry(popup, validate='key', validatecommand=vcmd)
        entry.grid(row=i+1, column=1, sticky='w', padx=2, pady=5)  # Add padx and pady for spacing
        entry_fields.append(entry)

    # Password entry field
    tk.Label(popup, text="Password:", font="bold").grid(row=len(entry_labels)+1, column=0, sticky='e', padx=2, pady=5)
    password_entry = tk.Entry(popup, show="*")  # Show asterisks for password input
    password_entry.grid(row=len(entry_labels)+1, column=1, sticky='w', padx=2, pady=5)
    
    # Bind the <Return> key to the submit_button when focus is on password entry
    password_entry.bind('<Return>', lambda event=None: submit_button.invoke())

    submit_button = ttk.Button(popup, text="Submit", command=lambda: final_add_part_number(entry_fields, password_entry, logged_in_user, popup))
    submit_button.grid(row=len(entry_labels) + 2, column=0, padx=10, pady=(0, 8), sticky="ew")  # Add padx and pady for spacing

    def cancel():
        popup.destroy()

    # Button to cancel and
    cancel_button = ttk.Button(popup, text="Cancel", width=12, command=cancel)
    cancel_button.grid(row=len(entry_labels) + 2, column=1, padx=10, pady=(0, 8))  # Add padx and pady for spacing

    popup.mainloop()
