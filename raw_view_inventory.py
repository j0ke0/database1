import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
import os
import pandas as pd
from datetime import datetime
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
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

def get_part_numbers():
    try:
        db_cursor.execute("SELECT partnumber FROM raw_partnumbers;")
        partnumbers = db_cursor.fetchall()
        return [part[0] for part in partnumbers]
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Error fetching part numbers: {e}")
        return []

def button01_clicked(root):
    try:
        # Create a new Toplevel window
        data_popup = tk.Toplevel(root)
        data_popup.title("Choose the raw materials you wish to see.")

        data_popup.iconbitmap(icon_path)
        
        # Create a Treeview widget
        tree = ttk.Treeview(data_popup, columns=("Part Number", "Purchase Number", "Quantity", "Storage", "User", "Date and Time"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Set up column headings with centered text
        for col in ("Part Number", "Purchase Number", "Quantity", "Storage", "User", "Date and Time"):
            tree.heading(col, text=col, anchor="center")

        # Function to fetch data and populate the table
        def populate_table(selected_table):
            try:
                # Clear old data from the Treeview
                tree.delete(*tree.get_children())
                
                # Set up style for centered text
                tree.tag_configure('center', anchor='center')

                # Execute the SQL query using the selected table name
                db_cursor.execute(f'SELECT part_number, purchase_number, qty, storage, "logged_in_users", time_stamp FROM public.{selected_table};')
                results = db_cursor.fetchall()

                # Insert data into the table
                for row in results:
                    # Format the timestamp to exclude milliseconds
                    formatted_row = list(row)
                    formatted_row[-1] = row[-1].strftime('%d-%m-%Y - %H:%M:%S')
                    tree.insert("", "end", values=formatted_row, tags='center')  # Apply centering tag

                # Center align the data inside the treeview
                for col in ("Part Number", "Purchase Number", "Quantity", "Storage", "User", "Date and Time"):
                    tree.heading(col, anchor="center")
                    tree.column(col, anchor="center")

            except psycopg2.Error as e:
                messagebox.showerror("Database Error", f"Error executing the query: {e}")


        # Function to export data to Excel
        def export_to_excel():
            try:
                data = []
                for item in tree.get_children():
                    item_data = [tree.item(item, 'values')[i] for i in range(len(tree["columns"]))]
                    data.append(item_data)

                df = pd.DataFrame(data, columns=["Part Number", "Purchase Number", "Quantity", "Storage", "User", "Date and Time"])

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
                                cell.alignment = Alignment(horizontal='left')

                    messagebox.showinfo("Export Successful", "Data exported to Excel successfully.")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

        def maximize_tree(event):
            # Check if the click event occurred outside the treeview
            if event.widget == tree:
                return
            data_popup.attributes('-fullscreen', True)

        # Create a frame to hold the label, dropdown, and buttons
        frame = ttk.Frame(data_popup)
        frame.pack()

        # Get part numbers from the database
        partnumbers = get_part_numbers()

        # Create a button to display raw_history table
        button_raw_history = ttk.Button(frame, text="Raw History", command=lambda: populate_table("raw_history"))
        button_raw_history.grid(row=0, column=0, padx=7, pady=1, sticky="nsew")

        # Create and grid label
        label = ttk.Label(frame, text="View Options:", font=("TkDefaultFont", 10, "bold"))
        label.grid(row=0, column=1, padx=5, pady=1) 

        # Create a dropdown menu
        selected_option = tk.StringVar()
        selected_option.set(partnumbers[0] if partnumbers else "")  # Set default option if available
        dropdown_menu = tk.OptionMenu(frame, selected_option, *partnumbers)
        dropdown_menu.config(width=10, bg='black')
        dropdown_menu.grid(row=0, column=2, padx=7, pady=1, sticky="nsew")

        # Create a button to trigger data population
        button_above_table = ttk.Button(frame, text="View Data", command=lambda: populate_table(selected_option.get().lower()))
        button_above_table.grid(row=0, column=3, padx=7, pady=1, sticky="nsew")

        # Create a button to export data to Excel
        export_button = ttk.Button(frame, text="Export to Excel", command=export_to_excel)
        export_button.grid(row=0, column=4, padx=7, pady=1, sticky="nsew")

        # Bind treeview click event to maximize_tree function
        tree.bind("<Button-1>", maximize_tree)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
