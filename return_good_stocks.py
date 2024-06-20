import os
import psycopg2
import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import tkinter.messagebox as messagebox
from tkinter import ttk, messagebox, filedialog
from image_icon_paths import icon_path

db_password = 'Nolcubs0#'

def return_good_stock(root, logged_in_user, db_cursor, db_connection):
    try:
        # Create a new Toplevel window
        data_popup = tk.Toplevel(root)
        data_popup.title("The table contains all of the borrowed goods data.")
        data_popup.iconbitmap(icon_path)
        
        # Create a Treeview widget with the new "Work Order" column
        tree = ttk.Treeview(data_popup, columns=("User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Set up column headings with centered text
        for col in ("User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Function to fetch data and populate the table
        def populate_table():
            try:
                # Clear old data from the Treeview
                tree.delete(*tree.get_children())
                
                # Execute the SQL query using the selected table name
                db_cursor.execute('SELECT "logged_in_users", "unit", "location_area", "qty", to_char("timestamp", \'DD-MM-YYYY    -    HH24:MI:SS\'), "work_order" FROM public.borrow_goods;')
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
                    messagebox.showerror("Return Error", "Return amount cannot be negative.")
                    return  # Exit the function if withdrawal amount is negative

                # Get the current quantity for the selected work order
                db_cursor.execute("SELECT qty FROM borrow_goods WHERE work_order = %s", (selected_work_order,))
                current_qty = db_cursor.fetchone()[0]

                # Check if withdrawal amount exceeds available quantity
                if withdrawal_amount > current_qty:
                    messagebox.showerror("Return Error", "Return amount exceeds available quantity.")
                    return  # Exit the function if withdrawal amount exceeds available quantity

                # Grab the focus to the popup window
                data_popup.grab_set()

                # Confirmation dialog before proceeding with withdrawal
                confirm = messagebox.askokcancel("Confirm Return", f"Are you sure you want to Return {withdrawal_amount} item(s) for Work Order {selected_work_order}?")

                if confirm:
                    # Proceed with the withdrawal
                    # Deduct the specified amount from the quantity for the selected work order in the database
                    db_cursor.execute("UPDATE borrow_goods SET qty = qty - %s WHERE work_order = %s RETURNING logged_in_users, unit, location_area, %s, %s", (withdrawal_amount, selected_work_order, withdrawal_amount, selected_work_order))
                    updated_rows = db_cursor.fetchall()  # Get the updated rows

                    if updated_rows:
                        for updated_row in updated_rows:
                            logged_in_users, unit, location_area, withdrawal_amount, work_order = updated_row

                            # Extract the first word from the work_order
                            work_order_first_word = work_order.split()[0]
                            new_work_order = f"{work_order_first_word} Returned {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

                            first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

                            # Insert the information into finish_goods
                            db_cursor.execute("INSERT INTO finish_goods (logged_in_users, unit, location_area, qty, work_order) VALUES (%s, %s, %s, %s, %s)",
                                            (f"{first_name} {last_name}", unit, location_area, withdrawal_amount, new_work_order))

                        db_connection.commit()  # Commit the transaction

                        # Show success message
                        messagebox.showinfo("Return Successful", f"{withdrawal_amount} item(s) deducted successfully.")

                        # Check for items with qty = 0 and delete them
                        db_cursor.execute("DELETE FROM borrow_goods WHERE qty = 0")
                        db_connection.commit()  # Commit the delete operation

                    else:
                        messagebox.showerror("Return Error", "No records were updated. Please check your selection.")

                    # Refresh the table after withdrawal
                    populate_table()

            except ValueError:
                messagebox.showerror("Return Error", "Please enter a valid Return amount.")
            except Exception as e:
                messagebox.showerror("Return Error", f"An error occurred during return: {e}")
            finally:
                # Release the grab after completing the withdrawal or if an error occurs
                data_popup.grab_release()

        def perform_scrap():
            try:
                # Get the selected work order from the dropdown menu
                selected_work_order = selected_option.get()
                # Get the withdrawal amount
                withdrawal_amount = int(withdrawal_amount_entry.get())

                # Check if withdrawal amount is negative
                if withdrawal_amount < 0:
                    messagebox.showerror("Return Error", "Return amount cannot be negative.")
                    return  # Exit the function if withdrawal amount is negative

                # Get the current quantity for the selected work order
                db_cursor.execute("SELECT qty FROM borrow_goods WHERE work_order = %s", (selected_work_order,))
                current_qty = db_cursor.fetchone()[0]

                # Check if withdrawal amount exceeds available quantity
                if withdrawal_amount > current_qty:
                    messagebox.showerror("Return Error", "Return amount exceeds available quantity.")
                    return  # Exit the function if withdrawal amount exceeds available quantity

                # Grab the focus to the popup window
                data_popup.grab_set()

                # Confirmation dialog before proceeding with withdrawal
                confirm = messagebox.askokcancel("Confirm Return", f"Are you sure you want to Scrap {withdrawal_amount} item(s) for Work Order {selected_work_order}?")

                if confirm:
                    # Proceed with the withdrawal
                    # Deduct the specified amount from the quantity for the selected work order in the database
                    db_cursor.execute("UPDATE borrow_goods SET qty = qty - %s WHERE work_order = %s RETURNING logged_in_users, unit, location_area, %s, %s", (withdrawal_amount, selected_work_order, withdrawal_amount, selected_work_order))
                    updated_rows = db_cursor.fetchall()  # Get the updated rows

                    if updated_rows:
                        for updated_row in updated_rows:
                            logged_in_users, unit, location_area, withdrawal_amount, work_order = updated_row

                            # Extract the first word from the work_order
                            work_order_first_word = work_order.split()[0]
                            new_work_order = f"{work_order_first_word} Scrap {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

                            first_name, last_name = logged_in_user.split(":")[1].strip().split(" ")

                            # Insert the information into finish_goods
                            db_cursor.execute("INSERT INTO final_scrap (logged_in_users, unit, location_area, qty, work_order) VALUES (%s, %s, %s, %s, %s)",
                                            (f"{first_name} {last_name}", unit, location_area, withdrawal_amount, new_work_order))

                            db_cursor.execute("INSERT INTO history_gparts (logged_in_users, unit, location_area, qty, work_order) VALUES (%s, %s, %s, %s, %s)",
                                            (f"{first_name} {last_name}", unit, location_area, withdrawal_amount,  " Borrowed " + new_work_order))

                        db_connection.commit()  # Commit the transaction

                        # Show success message
                        messagebox.showinfo("Return Successful", f"{withdrawal_amount} item(s) deducted successfully.")

                        # Check for items with qty = 0 and delete them
                        db_cursor.execute("DELETE FROM borrow_goods WHERE qty = 0")
                        db_connection.commit()  # Commit the delete operation

                    else:
                        messagebox.showerror("Return Error", "No records were updated. Please check your selection.")

                    # Refresh the table after withdrawal
                    populate_table()

            except ValueError:
                messagebox.showerror("Return Error", "Please enter a valid Return amount.")
            except Exception as e:
                messagebox.showerror("Return Error", f"An error occurred during return: {e}")
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

        def validate_entry(text):
            # Check if the input text length is less than or equal to 5
            return len(text) <= 3

        # Create a validation function for the entry
        vcmd = (data_popup.register(validate_entry), '%P')

        # Create an entry for withdrawal amount with validation
        withdrawal_amount_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)        
        withdrawal_amount_entry.grid(row=0, column=3, padx=4, pady=1, sticky="nsew")

        # Create a button for withdrawal
        withdrawal_button = ttk.Button(frame, text="Return", command=perform_withdrawal)
        withdrawal_button.grid(row=0, column=5, padx=4, pady=1, sticky="nsew")

        # Create a button for the new action
        new_action_button = ttk.Button(frame, text="Scrap", command=perform_scrap)
        new_action_button.grid(row=0, column=6, padx=4, pady=1, sticky="nsew")


        # Fetch available options dynamically from borrow_goods table
        db_cursor.execute("SELECT DISTINCT work_order FROM borrow_goods;")
        available_work_orders = db_cursor.fetchall()
        options = [work_order[0] for work_order in available_work_orders]

        # Create a dropdown menu
        selected_option = tk.StringVar()
        selected_option.set(options[0])  # Set default option
        dropdown_menu = tk.OptionMenu(frame, selected_option, *options)
        dropdown_menu.config(width=10, bg='black')
        dropdown_menu.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")

        # Bind treeview click event to maximize_tree function
        tree.bind("<Button-1>", maximize_tree)

    except Exception as e:
        messagebox.showerror("Info", f"Currently without any borrowed parts.")
        data_popup.destroy()
