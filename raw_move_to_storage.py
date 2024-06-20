import os
import re
import psycopg2
import openpyxl
import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import tkinter.messagebox as messagebox
from tkinter import ttk, filedialog
from image_icon_paths import icon_path

db_password = 'Nolcubs0#'

def move_to_storage(root, logged_in_user, db_cursor, db_connection):
    try:
        # Create a new Toplevel window
        data_popup = tk.Toplevel(root)
        data_popup.title("All completed IQCs are listed in the table, which has to be moved to storage.")

        data_popup.iconbitmap(icon_path)
        
        # Create a Treeview widget with the updated columns
        tree = ttk.Treeview(data_popup, columns=("Part Number", "Purchase Number", "Quantity", "Location", "User Account", "Part Type", "Passed IQC Evaluation", "Date and Time"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        # Set up column headings with centered text
        for col in ("Part Number", "Purchase Number", "Quantity", "Location", "User Account", "Part Type", "Passed IQC Evaluation", "Date and Time"):
            tree.heading(col, text=col, anchor="center")

        # Center align the data inside the treeview
        for col in ("Part Number", "Purchase Number", "Quantity", "Location", "User Account", "Part Type", "Passed IQC Evaluation", "Date and Time"):
            tree.column(col, anchor="center")

        # Function to fetch data and populate the table
        def populate_table():
            try:
                # Clear old data from the Treeview
                tree.delete(*tree.get_children())
                
                # Execute the SQL query using the selected table name
                db_cursor.execute('SELECT "part_number", "purchase_number", "qty", "storage", "logged_in_users", "type", "good_parts", to_char("time_stamp", \'DD-MM-YYYY    -    HH24:MI:SS\') FROM raw_iqc_storage;')
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

                df = pd.DataFrame(data, columns=["Part Number", "Purchase Number", "Quantity", "Location", "User Account", "Part Type", "Passed IQC Evaluation", "Date and Time"])

                # Generate filename with table name and current date
                file_name = f"{datetime.now().strftime('%d-%m-%Y')}.xlsx"
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=file_name)
                
                if file_path:
                    # Save DataFrame to Excel
                    df.to_excel(file_path, index=False)
                    
                    # Open the Excel file with openpyxl
                    workbook = openpyxl.load_workbook(file_path)
                    sheet = workbook.active
                    
                    # Auto size all columns
                    for col in sheet.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(cell.value)
                            except:
                                pass
                        adjusted_width = (max_length + 2) * 1.2
                        sheet.column_dimensions[column].width = adjusted_width
                    
                    # Save the changes to the Excel file
                    workbook.save(file_path)
                    
                    messagebox.showinfo("Export Successful", "Data exported to Excel successfully.")
                    
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

        # Function to maximize the window upon treeview click
        def maximize_tree(event):
            # Check if the click event occurred outside the treeview
            if event.widget == tree:
                return
            data_popup.attributes('-fullscreen', True)

        def validate_entry(text):
            # Check if the input text length is less than or equal to 10
            return len(text) <= 11

        # Function to edit selected data
        def edit_selected_data():
            try:
                # Get selected item
                selected_item = tree.selection()[0]

                # Get data associated with selected item
                selected_data = tree.item(selected_item, 'values')

                table_select = selected_data[5]
                
                first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

                # Check if the selected table exists in the database
                db_cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_select,))
                table_exists = db_cursor.fetchone()[0]

                if not table_exists:
                    messagebox.showerror("Table Error", f"You should speak with an administrator to add the table {table_select.upper()} to the database.")
                    return

                # Display data for editing (you can use Entry widgets or any other suitable widgets)
                # For example:
                edit_window = tk.Toplevel(root) 
                edit_window.title("Edit Data")

                edit_window.iconbitmap(icon_path)
                
                # Grab focus and set the window to be on top
                edit_window.grab_set()

                # Display selected data for reference
                for idx, col_name in enumerate(("Part Number", "Purchase Number", "Quantity", "Location:")):
                    label = ttk.Label(edit_window, text=col_name)
                    if col_name == "Location:":
                        label.config(font=("TkDefaultFont", 10, "bold"))  # Set the label to bold for "Location"
                    label.grid(row=idx, column=0, padx=5, pady=5, sticky="e")

                    entry = ttk.Entry(edit_window)
                    entry.insert(0, selected_data[idx])
                    entry.config(state="disabled")  # Disable editing for other columns
                    entry.grid(row=idx, column=1, padx=5, pady=5)

                # Enable editing only for the "Location" column with validation
                location_entry = ttk.Entry(edit_window, validate="key", validatecommand=(edit_window.register(validate_entry), '%P'))
                location_entry.insert(0, selected_data[3])  # Index 3 corresponds to the "Location" column
                location_entry.grid(row=3, column=1, padx=5, pady=5)

                # Update function to update data in the database
                def update_data():
                    try:
                        # Get edited values from entry widgets and capitalize the location
                        edited_location = location_entry.get().strip().upper()

                        # Validate edited_location
                        if not edited_location or not (edited_location[0].isalnum() and edited_location[-1].isdigit()):
                            messagebox.showerror("Validation Error", "Location must start with text or a number and end with a number.")
                            return

                        # Continue saving data if validation passes
                        selected_item = tree.selection()[0]
                        selected_data = tree.item(selected_item, 'values')

                        # Extract time_stamp value
                        time_stamp = selected_data[-1]  # Assuming it's the last element in the selected_data tuple
                        true_or_false = selected_data[6]

                        if true_or_false == 'False':  # If passed IQC evaluation is False
                            # Save data to quarantine table
                            db_cursor.execute('''
                                INSERT INTO quarantine (part_number, purchase_number, qty, storage, logged_in_users) 
                                VALUES (%s, %s, %s, %s, %s)
                                ''', 
                                (selected_data[0], selected_data[1], selected_data[2], edited_location, f"{first_name} {last_name}"))
                            db_connection.commit()

                            # Concatenate 'fail-IQC' with the existing purchase_number
                            purchase_number_fail_iqc = f"{selected_data[1]} -Failed Quarantine"

                            # Execute the modified INSERT statement
                            db_cursor.execute('''
                                INSERT INTO raw_history (part_number, purchase_number, qty, storage, logged_in_users) 
                                VALUES (%s, %s, %s, %s, %s)
                                ''', 
                                (selected_data[0], purchase_number_fail_iqc, selected_data[2], edited_location, f"{first_name} {last_name}"))
                            db_connection.commit()

                            # Delete the selected row from raw_iqc_storage based on time_stamp
                            db_cursor.execute('DELETE FROM raw_iqc_storage WHERE to_char("time_stamp", \'DD-MM-YYYY    -    HH24:MI:SS\') = %s', (time_stamp,))
                            db_connection.commit()

                            # Delete the selected item from the Treeview widget
                            tree.delete(selected_item)

                            # Refresh table
                            populate_table()

                            messagebox.showinfo("Update Successful", "Data updated successfully. Saved in quarantine.")
                        else:  # If passed IQC evaluation is True
                            # Save data to the selected table
                            db_cursor.execute('''
                                INSERT INTO {} (part_number, purchase_number, qty, storage, logged_in_users) 
                                VALUES (%s, %s, %s, %s, %s)
                                '''.format(table_select), 
                                (selected_data[0], selected_data[1], selected_data[2], edited_location, f"{first_name} {last_name}"))
                            db_connection.commit()

                            # Concatenate 'fail-IQC' with the existing purchase_number
                            purchase_number_fail_iqc = f"{selected_data[1]} Passed - Storage"

                            # Execute the modified INSERT statement
                            db_cursor.execute('''
                                INSERT INTO raw_history (part_number, purchase_number, qty, storage, logged_in_users) 
                                VALUES (%s, %s, %s, %s, %s)
                                ''', 
                                (selected_data[0], purchase_number_fail_iqc, selected_data[2], edited_location, f"{first_name} {last_name}"))
                            db_connection.commit()

                            # Delete the selected row from raw_iqc_storage based on time_stamp
                            db_cursor.execute('DELETE FROM raw_iqc_storage WHERE to_char("time_stamp", \'DD-MM-YYYY    -    HH24:MI:SS\') = %s', (time_stamp,))
                            db_connection.commit()

                            # Delete the selected item from the Treeview widget
                            tree.delete(selected_item)

                            # Refresh table
                            populate_table()

                            messagebox.showinfo("Update Successful", "Data updated successfully.")
                            
                        # Close edit window
                        edit_window.destroy()

                    except Exception as e:
                        messagebox.showerror("Update Error", f"An error occurred while updating data: {e}")

                # Button to update data
                update_button = ttk.Button(edit_window, text="Update", command=update_data)
                update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

            except IndexError:
                messagebox.showwarning("No Selection", "Please select an item to edit.")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


        # Create a frame to hold the label, dropdown, and buttons
        frame = ttk.Frame(data_popup)
        frame.pack()

        # Create a button to trigger data population
        button_above_table = ttk.Button(frame, text="View All", command=populate_table)
        button_above_table.grid(row=0, column=1, padx=4, pady=1, sticky="nsew")

        # Create a button to export data to Excel
        export_button = ttk.Button(frame, text="Export to Excel", command=export_to_excel)
        export_button.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")

        # Create a button to edit selected data
        edit_button = ttk.Button(frame, text="Edit Location", command=edit_selected_data)
        edit_button.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")

        # Bind treeview click event to maximize_tree function
        tree.bind("<Button-1>", maximize_tree)

        # Function to handle double-click event on selected data
        def double_click(event):
            edit_selected_data()

        # Bind double-click event to treeview
        tree.bind("<Double-1>", double_click)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
