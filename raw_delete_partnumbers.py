import re
import os
import psycopg2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from image_icon_paths import icon_path, dbnames, users, passwords, hosts, ports, image_path

db_password = 'Nolcubs0#'

def delete_confirmation(partnumber, db_cursor, popup):
    confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete part number {partnumber}?")
    if confirmation:
        delete_row(partnumber, db_cursor, popup)

def delete_row(partnumber, db_cursor, popup):
    try:
        with db_cursor:
            db_cursor.execute("DELETE FROM raw_partnumbers WHERE partnumber = %s", (partnumber,))
            db_cursor.connection.commit()
            messagebox.showinfo("Success", f"Part number {partnumber} deleted successfully.")
            popup.destroy()  # Close the popup window first
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error deleting part number {partnumber}: {e}")
        print("SQL error:", e)
            
def fetch_partnumbers(db_cursor):
    try:
        db_cursor.execute("SELECT partnumber FROM raw_partnumbers")
        partnumbers = db_cursor.fetchall()
        return [row[0] for row in partnumbers]
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error fetching part numbers: {e}")
        return []
    finally:
        db_cursor.close()

def raw_delete_part_numbers(root):
    popup = tk.Toplevel(root)
    popup.title("Delete Raw List")

    popup.iconbitmap(icon_path)

    try:
        db_connection = psycopg2.connect(
            dbname=dbnames,
            user=users,
            password=passwords,
            host=hosts,
            port=ports
        )
        db_cursor = db_connection.cursor()

        add_path = "raw_remove_table.png"
        full_path = image_path + add_path
        image = Image.open(full_path)  # Replace with your image path
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(popup, image=photo)
        image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)  # Add padx and pady for spacing

        # Entry box for entering part number
        tk.Label(popup, text="Enter Part Number:", font="bold").grid(row=1, column=0, sticky='e', padx=1, pady=5)
        partnumber_entry = tk.Entry(popup)
        partnumber_entry.grid(row=1, column=1, padx=1, pady=5)

        # Entry box for entering password
        tk.Label(popup, text="Enter Password:", font="bold").grid(row=2, column=0, sticky='e', padx=1, pady=5)
        password_entry = tk.Entry(popup, show="*")  # Show * instead of actual characters
        password_entry.grid(row=2, column=1, padx=1, pady=5)

        # Submit button to display confirmation popup
        def submit_delete():
            entered_password = password_entry.get().strip()
            if entered_password != "Nolcubs03":  # Change the password here
                popup.grab_set()
                messagebox.showerror("Password Incorrect", "Incorrect password. Please try again.")
                return
            delete_confirmation(partnumber_entry.get().upper(), db_cursor, popup)  # Convert to uppercase

        submit_button = ttk.Button(popup, text="Delete", command=submit_delete)
        submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Cancel button to close the popup
        cancel_button = ttk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        popup.mainloop()
    finally:
        if db_connection is not None:
            db_connection.close()
