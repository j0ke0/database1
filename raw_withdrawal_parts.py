import os
import psycopg2
import pandas as pd
import tkinter as tk
from datetime import datetime
import tkinter.messagebox as messagebox
from openpyxl.styles import Alignment
from tkinter import messagebox
from openpyxl.utils import get_column_letter
from tkinter import ttk, messagebox, filedialog
from image_icon_paths import icon_path

db_password = 'Nolcubs0#'

def get_part_numbers(db_cursor):
    try:
        db_cursor.execute("SELECT partnumber FROM raw_partnumbers;")
        partnumbers = db_cursor.fetchall()
        return [part[0] for part in partnumbers]
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Error fetching part numbers: {e}")
        return []

def raw_withdrawal(root, logged_in_user, db_cursor, db_connection):
    try:
        # Create a new Toplevel window
        data_popup = tk.Toplevel(root)
        data_popup.title("Withdraw or update parts location.")

        data_popup.iconbitmap(icon_path)

        # Create a Treeview widget with the new "Work Order" column
        tree = ttk.Treeview(data_popup, columns=("Part Number", "Purchase Number", "Quantity", "Location", "Date and Time", "User Account"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        # Set up column headings with centered text
        for col in ("Part Number", "Purchase Number", "Quantity", "Location", "Date and Time", "User Account"):
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center")

        # Function to fetch data and populate the table
        def populate_table():
            try:
                # Clear old data from the Treeview
                tree.delete(*tree.get_children())

                selected_table = selected_option.get()
                db_cursor.execute('SELECT "part_number", "purchase_number", "qty", "storage", to_char("time_stamp", \'DD-MM-YYYY    -    HH24:MI:SS\'), "logged_in_users" FROM public.' + selected_table + ';')
                results = db_cursor.fetchall()

                # Insert data into the table
                for row in results:
                    tree.insert("", "end", values=row)

            except psycopg2.Error as e:
                messagebox.showerror("Database Error", f"Error executing the query: {e}")

        # Function to export data to Excel
        def export_to_excel():
            try:
                data = []
                for item in tree.get_children():
                    item_data = [tree.item(item, 'values')[i] for i in range(len(tree["columns"]))]
                    data.append(item_data)

                df = pd.DataFrame(data, columns=["Part Number", "Purchase Number", "Quantity", "Storage", "User Account", "Date and Time"])

                # Get selected table name
                selected_table = selected_option.get()

                # Generate filename with table name and current date
                file_name = f"{selected_table}_{datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.xlsx"
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=file_name)
                
                if file_path:
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)

                        # Autofit column width and set alignment
                        sheet = writer.sheets['Sheet1']
                        for column in sheet.columns:
                            max_length = 0
                            column = [cell for cell in column if cell.value is not None]
                            if column:
                                max_length = max(len(str(cell.value)) for cell in column)
                            adjusted_width = (max_length + 2) * 1.2
                            sheet.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width
                            
                            # Set horizontal alignment
                            for cell in column:
                                cell.alignment = Alignment(horizontal='center', vertical='center')

                    messagebox.showinfo("Export Successful", "Data exported to Excel successfully.")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

        # Function to maximize the window upon treeview click
        def maximize_tree(event):
            # Check if the click event occurred outside the treeview
            if event.widget == tree:
                return
            data_popup.attributes('-fullscreen', True)

        def withdrawal_process():
            try:
                # Get selected item
                selected_item = tree.selection()[0]

                # Get data associated with selected item
                selected_data = tree.item(selected_item, 'values')

                # Display data for editing (you can use Entry widgets or any other suitable widgets)
                # For example:
                edit_window = tk.Toplevel(root)
                edit_window.title("Edit Data")

                edit_window.iconbitmap(icon_path)

                edit_window.grab_set()

                # Display selected data for reference
                for idx, col_name in enumerate(("Part Number", "Purchase Number", "Withdrawal Qty:", "Location")):
                    label = ttk.Label(edit_window, text=col_name)
                    if col_name == "Withdrawal Qty:":
                        label.config(font=("TkDefaultFont", 10, "bold"))  # Set the label to bold
                    label.grid(row=idx, column=0, padx=5, pady=5, sticky="e")

                    entry = ttk.Entry(edit_window)
                    entry.insert(0, selected_data[idx])
                    entry.config(state="disabled")  # Disable editing for other columns
                    entry.grid(row=idx, column=1, padx=5, pady=5)

                # Enable editing only for the "Quantity" column with validation
                quantity_entry = ttk.Entry(edit_window, validate="key", validatecommand=(edit_window.register(validate_entry), '%P'))
                quantity_entry.insert(0, selected_data[2])  # Index 2 corresponds to the "Quantity" column
                quantity_entry.grid(row=2, column=1, padx=5, pady=5)

                # Update function to update data in the tree and database
                def update_data():
                    try:
                        # Get the edited quantity from the entry widget
                        edited_quantity = quantity_entry.get().strip()

                        # Check if the input is not empty and is a positive integer
                        if edited_quantity == "" or not edited_quantity.isdigit() or int(edited_quantity) <= 0:
                            messagebox.showerror("Invalid Input", "Please enter a positive number for quantity.")
                            return

                        edited_quantity = int(edited_quantity)  # Convert to integer
                        original_quantity = int(selected_data[2])
                        new_quantity = original_quantity - edited_quantity
                        selected_table = selected_option.get()
                        first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")
                        
                        # Check if edited quantity is greater than original quantity
                        if edited_quantity > original_quantity:
                            messagebox.showerror("Update Error", "The amount specified exceeds what is currently in stock.")
                            return  # Exit the function without proceeding further

                        # Update quantity in the treeview
                        tree.item(selected_item, values=(selected_data[0], selected_data[1], new_quantity, selected_data[3], selected_data[4], selected_data[5]))

                        # Update data in the database
                        db_cursor.execute('UPDATE public.' + selected_table + ' SET qty = %s WHERE part_number = %s', (new_quantity, selected_data[0]))

                        # If new_quantity is zero, delete the row from the table
                        if new_quantity == 0:
                            db_cursor.execute('DELETE FROM public.' + selected_table + ' WHERE part_number = %s', (selected_data[0],))

                        # Modify purchase number for withdrawals
                        if edited_quantity > 0:
                            note = "Withdrawal"  # Add a note for withdrawal
                        else:
                            note = ""  # No note for other transactions

                        # Insert data into the history table
                        db_cursor.execute('INSERT INTO public.raw_history (part_number, purchase_number, qty, storage, logged_in_users, time_stamp) VALUES (%s, %s, %s, %s, %s, %s)',
                                        (selected_data[0], f"{selected_data[1]} - {note}", edited_quantity, selected_data[3], f"{first_name} {last_name}", datetime.now()))

                        db_connection.commit()

                        # Close edit window
                        edit_window.destroy()

                        messagebox.showinfo("Update Successful", "Quantity updated successfully.")

                    except Exception as e:
                        messagebox.showerror("Update Error", f"An error occurred while updating quantity: {e}")


                # Button to update data
                update_button = ttk.Button(edit_window, text="Update", command=update_data)
                update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

            except IndexError:
                messagebox.showwarning("No Selection", "Please select an item to edit.")

        def update_location():
            try:
                # Get selected item
                selected_item = tree.selection()[0]

                # Get data associated with selected item
                selected_data = tree.item(selected_item, 'values')

                # Display data for editing
                edit_window = tk.Toplevel(root)
                edit_window.title("Update Location")

                edit_window.iconbitmap(icon_path)

                edit_window.grab_set()

                # Function to validate the entry length
                def validate_entry(text):
                    # Check if the input text length is less than or equal to 15
                    return len(text) <= 15

                # Create a validation function for the entry
                vcmd = (edit_window.register(validate_entry), '%P')

                # Display selected data for reference
                for idx, col_name in enumerate(("Part Number", "Purchase Number", "Quantity", "Current Location")):
                    label = ttk.Label(edit_window, text=col_name)
                    if col_name == "Current Location":
                        label.config(font=("TkDefaultFont", 10, "bold"))  # Set the label to bold for specific fields
                    label.grid(row=idx, column=0, padx=5, pady=5, sticky="e")

                    if col_name == "Current Location":
                        entry = ttk.Entry(edit_window, validate="key", validatecommand=vcmd)
                        entry.insert(0, selected_data[3])  # Index 3 corresponds to the "Location" column
                    else:
                        entry = ttk.Entry(edit_window)
                        entry.insert(0, selected_data[idx])
                        entry.config(state="disabled")
                    entry.grid(row=idx, column=1, padx=5, pady=5)

                # Function to update location
                def update_location_in_db():
                    try:
                        new_location = entry.get().strip()
                        if not new_location:
                            messagebox.showerror("Invalid Input", "Please enter a new location.")
                            return

                        # Check if the length of the new location exceeds 15 characters
                        if len(new_location) > 15:
                            messagebox.showerror("Invalid Input", "Location must not exceed 15 characters.")
                            return

                        # Update location in the database
                        db_cursor.execute('UPDATE public.' + selected_option.get() + ' SET storage = %s WHERE part_number = %s', (new_location, selected_data[0]))
                        db_connection.commit()

                        # Update location in the Treeview
                        tree.set(selected_item, column="Location", value=new_location)

                        # Close edit window
                        edit_window.destroy()

                        messagebox.showinfo("Location Update", "Location updated successfully.")

                    except Exception as e:
                        messagebox.showerror("Update Error", f"An error occurred while updating location: {e}")

                # Create a button to update location
                update_button = ttk.Button(edit_window, text="Update", command=update_location_in_db)
                update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

            except IndexError:
                messagebox.showwarning("No Selection", "Please select an item to update location.")

        # Create a frame to hold the label, dropdown, and buttons
        frame = ttk.Frame(data_popup)
        frame.pack()

        # Create a button to trigger data population
        button_above_table = ttk.Button(frame, text="View Stocks", command=populate_table)
        button_above_table.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")

        # Create a button on the right side of button_above_table in the same row
        update_locations = ttk.Button(frame, text="Update Location", command=update_location)
        update_locations.grid(row=0, column=4, padx=4, pady=1, sticky="nsew")

        # Create a button to export data to Excel
        export_button = ttk.Button(frame, text="Export to Excel", command=export_to_excel)
        export_button.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")

        def validate_entry(text):
            # Check if the input text length is less than or equal to 5
            return len(text) <= 4

        # Create a validation function for the entry
        vcmd = (data_popup.register(validate_entry), '%P')

        # Create a button for withdrawal
        withdrawal_button = ttk.Button(frame, text="Withdraw", command=withdrawal_process)
        withdrawal_button.grid(row=0, column=3, padx=4, pady=1, sticky="nsew")

        # Create a dropdown menu
        selected_option = tk.StringVar()
        options = get_part_numbers(db_cursor)  # Pass the database cursor
        selected_option.set(options[0])  # Set default option
        dropdown_menu = tk.OptionMenu(frame, selected_option, *options)
        dropdown_menu.config(width=10, bg='black')
        dropdown_menu.grid(row=0, column=1, padx=7, pady=1, sticky="nsew")

        # Bind treeview click event to maximize_tree function
        tree.bind("<Button-1>", maximize_tree)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
