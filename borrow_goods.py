import os
import psycopg2
import pandas as pd
import tkinter as tk
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import messagebox
from tkinter import ttk, messagebox, filedialog
from image_icon_paths import icon_path

db_password = 'Nolcubs0#'

def borrow(root, logged_in_user, db_cursor, db_connection):
    try:
        # Create a new Toplevel window
        data_popup = tk.Toplevel(root)
        data_popup.title("You are allowed to borrow the pieces shown in the table.")

        data_popup.iconbitmap(icon_path)
        
        # Create a Treeview widget with the new "Work Order" column
        tree = ttk.Treeview(data_popup, columns=("User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Set up column headings
        for col in ("User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")  # Center align column headings

        # Function to fetch data and populate the table
        def populate_table():
            try:
                tree.delete(*tree.get_children())  # Clear old data from the Treeview
                                
                db_cursor.execute('SELECT "logged_in_users", "unit", "location_area", "qty", to_char("timestamp", \'DD-MM-YYYY    -    HH24:MI:SS\'), "work_order" FROM public.finish_goods;')
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

                df = pd.DataFrame(data, columns=["User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"])

                # Get selected table name
                selected_table = selected_option.get()

                # Generate filename with table name and current date
                file_name = f"{selected_table}_{datetime.now().strftime('%d-%m-%Y')}.xlsx"
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=file_name)
                
                if file_path:
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Export Successful", "Data exported to Excel successfully.")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

        # Function to maximize the window upon treeview click
        def maximize_tree(event):
            # Check if the click event occurred outside the treeview
            if event.widget == tree:
                return
            data_popup.attributes('-fullscreen', True)

        def perform_withdrawal():
            try:
                # Get the selected work order from the dropdown menu
                selected_work_order = selected_option.get()
                # Get the withdrawal amount
                withdrawal_amount = int(withdrawal_amount_entry.get())

                # Check if withdrawal amount is negative
                if withdrawal_amount < 0:
                    messagebox.showerror("Withdrawal Error", "Borrow amount cannot be negative.")
                    return  # Exit the function if withdrawal amount is negative

                # Get the current quantity for the selected work order
                db_cursor.execute("SELECT qty FROM finish_goods WHERE work_order = %s", (selected_work_order,))
                current_qty = db_cursor.fetchone()[0]

                # Check if withdrawal amount exceeds available quantity
                if withdrawal_amount > current_qty:
                    messagebox.showerror("Borrow Error", "The amount borrowed is more than what is available.")
                    return  # Exit the function if withdrawal amount exceeds available quantity

                # Grab the focus to the popup window
                data_popup.grab_set()

                # Confirmation dialog before proceeding with withdrawal
                confirm = messagebox.askokcancel("Confirm Borrow", f"Are you sure you want to borrow {withdrawal_amount} item(s) for Work Order {selected_work_order}?")
                
                if confirm:
                    # Proceed with the withdrawal
                    # Deduct the specified amount from the quantity for the selected work order in the database
                    db_cursor.execute("UPDATE finish_goods SET qty = qty - %s WHERE work_order = %s RETURNING logged_in_users, unit, location_area, %s, %s", (withdrawal_amount, selected_work_order, withdrawal_amount, selected_work_order))
                    updated_rows = db_cursor.fetchall()  # Get the updated rows

                    if updated_rows:
                        for updated_row in updated_rows:
                            logged_in_users, unit, location_area, withdrawal_amount, work_order = updated_row

                            # Extract the first word from the work_order
                            work_order_first_word = work_order.split()[0]
                            new_work_order = f"{work_order_first_word} Borrowed {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

                            first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

                            # Insert the information into borrow_goods
                            db_cursor.execute("INSERT INTO borrow_goods (logged_in_users, unit, location_area, qty, work_order) VALUES (%s, %s, %s, %s, %s)",
                                            (f"{first_name} {last_name}", unit, location_area, withdrawal_amount, new_work_order))

                            # Insert into history_gparts
                            query_history_gparts = '''
                                INSERT INTO history_gparts ("logged_in_users", location_area, qty, work_order, unit, timestamp)
                                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                            '''
                            db_cursor.execute(query_history_gparts, (f"{first_name} {last_name}", location_area, withdrawal_amount, new_work_order, unit))

                        db_connection.commit()  # Commit the transaction


                        # Show success message
                        messagebox.showinfo("Return Successful", f"{withdrawal_amount} item(s) deducted successfully.")

                        # Check for items with qty = 0 and delete them
                        db_cursor.execute("DELETE FROM finish_goods WHERE qty = 0")
                        db_connection.commit()  # Commit the delete operation

                    else:
                        messagebox.showerror("Return Error", "No records were updated. Please check your selection.")

                    # Refresh the table after withdrawal
                    populate_table()

            except ValueError:
                messagebox.showerror("Borrow Error", "Please enter a valid Borrow amount.")
            except Exception as e:
                messagebox.showerror("Borrow Error", f"An error occurred during Borrow: {e}")
            finally:
                # Release the grab after completing the withdrawal or if an error occurs
                data_popup.grab_release()

        # Create a frame to hold the label, dropdown, and buttons
        frame = ttk.Frame(data_popup)
        frame.pack()

        # Create a button to trigger data population
        button_above_table = ttk.Button(frame, text="View All", command=populate_table)
        button_above_table.grid(row=0, column=1, padx=4, pady=1, sticky="nsew")

        # Create a button to export data to Excel
        export_button = ttk.Button(frame, text="Export to Excel", command=export_to_excel)
        export_button.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")

        withdrawal_amount_entry = ttk.Entry(frame)
        withdrawal_amount_entry.grid(row=0, column=3, padx=4, pady=1, sticky="nsew")

        # Function to validate the input
        def validate_withdrawal_amount(value):
            if value == "" or (value.isdigit() and int(value) <= 5):
                return True
            return False

        # Register the validation function with the entry widget
        vcmd = frame.register(validate_withdrawal_amount)
        withdrawal_amount_entry.config(validate="key", validatecommand=(vcmd, "%P"))


        # Create a button for withdrawal
        withdrawal_button = ttk.Button(frame, text="Borrow", command=perform_withdrawal)
        withdrawal_button.grid(row=0, column=5, padx=4, pady=1, sticky="nsew")

        # Fetch available options dynamically from finish_goods table
        db_cursor.execute("SELECT DISTINCT work_order FROM finish_goods;")
        available_work_orders = db_cursor.fetchall()

        # Filter out work orders longer than 25 characters
        options = [work_order[0] for work_order in available_work_orders if len(work_order[0]) <= 25]

        # Create a dropdown menu
        selected_option = tk.StringVar()
        selected_option.set(options[0])  # Set default option
        dropdown_menu = tk.OptionMenu(frame, selected_option, *options)
        dropdown_menu.config(width=10, bg='black')
        dropdown_menu.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")


        # Bind treeview click event to maximize_tree function
        tree.bind("<Button-1>", maximize_tree)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
