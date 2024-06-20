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

work_order_pattern = r'^WO\d+$'
quantity_pattern = r'^\d+$'
location_pattern = r'^[a-zA-Z0-9]+[a-zA-Z]+\d+$'
def submit_and_display_data(entry_fields, logged_in_user, popup, table_name_var):
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
        location, qty, work_order, unit_type = data

        first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

        # Input validation
        if not all(data):
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("All fields must be filled out.")
        
        if len(location) > 6:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Location must not exceed 6 characters.")
        
        if not re.match(location_pattern, location):
            popup.grab_set()
            raise ValueError("Location must start with letters or numbers and end with number.") 
        
        if len(qty) > 4:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Qty must not exceed 4 characters.")

        if not re.match(quantity_pattern, qty):
            popup.grab_set()
            raise ValueError("Quantity must be a positive number.") 

        if len(work_order) > 9:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Work order must not exceed 9 characters.")        
              
        if not re.match(work_order_pattern, work_order):
            popup.grab_set()
            raise ValueError("Work Order must start with 'WO' followed by numbers.")
       
        if len(unit_type) > 12:
            popup.grab_set()  # Ensure the popup remains on top before showing the message box
            raise ValueError("Unit Type must not exceed 12 characters.")
        
        # Check unit_type format
        selected_part_number = table_name_var.get()
        if not unit_type.startswith(selected_part_number):
            popup.grab_set()
            raise ValueError(f"Unit Type must start with '{selected_part_number}'.")

        unit_type_suffix = unit_type[len(selected_part_number):]
        if not re.match(r'^[A-Za-z0-9]*\d+$', unit_type_suffix):
            popup.grab_set()
            raise ValueError(f"Unit Type must end with a number after '{selected_part_number}' and can contain letters or numbers in between.")
        
        query_iqc_storage = '''
            INSERT INTO finish_goods ("logged_in_users", location_area, qty, work_order, unit, timestamp)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        '''
        db_cursor.execute(query_iqc_storage, (f"{first_name} {last_name}", location, qty, work_order, unit_type))

        # Append "Done-AQL" to the work_order
        work_order_done_aql = f"{work_order} Done-AQL"

        # Execute the query
        query_history_gparts = '''
            INSERT INTO history_gparts ("logged_in_users", location_area, qty, work_order, unit, timestamp)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        '''
        db_cursor.execute(query_history_gparts, (f"{first_name} {last_name}", location, qty, work_order_done_aql, unit_type))

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
        db_cursor.execute("SELECT finish_goods FROM finish_goods_dropdown;")
        part_numbers = db_cursor.fetchall()
        return [part[0] for part in part_numbers]
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Error fetching part numbers: {e}")
        return []

def final_goods_entry(root, logged_in_user):
    # Set up the Tkinter window
    popup = tk.Toplevel(root)
    popup.title("IQC Entries Here")

    popup.iconbitmap(icon_path)

    table_names = get_part_numbers()

    add_path = "finish_goods logo.png"
    full_path = image_path + add_path
    image = Image.open(full_path)  # Replace with your image path
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(popup, image=photo)
    image_label.grid(row=0, column=0, columnspan=2)  # Adjust row and column as needed

    # Entry fields
    entry_labels = ["Location:", "Quantity:", "Work Order:", "Unit Type:"]
    entry_fields = []

    for i, label in enumerate(entry_labels):
        tk.Label(popup, text=label).grid(row=i+1, column=0, sticky='e')  # Adjust row and column as needed
        entry = tk.Entry(popup)
        entry.grid(row=i+1, column=1, sticky='w')  # Adjust row and column as needed
        entry_fields.append(entry)

    # Dropdown for selecting table name
    table_name_var = tk.StringVar()
    table_name_label = tk.Label(popup, text="Component Type:")
    table_name_label.grid(row=len(entry_labels) + 1, column=0, sticky='e')

    table_names = get_part_numbers()  # Fetch part numbers from the raw_partnumbers table
    table_name_var.set(table_names[0])  # Set default value
    table_name_option_menu = OptionMenu(popup, table_name_var, *table_names)
    table_name_option_menu.config(width=12, bg='black', font=('Arial', 10, 'bold'))  # Adjust width and color as needed
    table_name_option_menu.grid(row=len(entry_labels) + 1, column=1, sticky='w')

    submit_button = ttk.Button(popup, text="Submit", command=lambda: submit_and_display_data(entry_fields, logged_in_user, popup, table_name_var))
    submit_button.grid(row=len(entry_labels) + 3, column=0, padx=7, pady=8, sticky="ew")  # Adjust row and column as needed

    def cancel():
        popup.destroy()

    # Button to cancel and close the popup window
    cancel_button = ttk.Button(popup, text="Cancel", width=12, command=cancel)
    cancel_button.grid(row=len(entry_labels) + 3, column=1, padx=7, pady=8)

    popup.mainloop()
