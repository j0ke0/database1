import os
import psycopg2
import openpyxl
import tkinter as tk
import pandas as pd
from datetime import datetime
from tkinter import filedialog
from tkinter import ttk, messagebox
from openpyxl.styles import Alignment
from image_icon_paths import icon_path

db_password = 'Nolcubs0#'

def export_to_excel(tree):
    try:
        data = []
        for item in tree.get_children():
            item_data = [tree.item(item, 'values')[i] for i in range(len(tree["columns"]))]
            data.append(item_data)

        df = pd.DataFrame(data, columns=["User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"])

        # Generate filename with current date
        file_name = f"data_export_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=file_name)
        
        if file_path:
            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']

                # Auto-size columns
                for col in worksheet.columns:
                    max_length = 0
                    column = col[0].column_letter  # Get the column name
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                            cell.alignment = Alignment(horizontal='center', vertical='center')
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 1.2
                    worksheet.column_dimensions[column].width = adjusted_width

            messagebox.showinfo("Export Successful", "Data exported to Excel successfully.")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

def view_all_data(root, logged_in_user, db_cursor, db_connection):
    def populate_table(table_name):
        try:
            # Clear old data from the Treeview
            tree.delete(*tree.get_children())
            
            # Execute the SQL query using the selected table name
            db_cursor.execute(f'SELECT "logged_in_users", "unit", "location_area", "qty", to_char("timestamp", \'DD-MM-YYYY    -    HH24:MI:SS\'), "work_order" FROM public.{table_name};')
            results = db_cursor.fetchall()

            # Insert data into the table
            for row in results:
                tree.insert("", "end", values=row)

        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"Error executing the query: {e}")

    try:
        # Create a new Toplevel window
        data_popup = tk.Toplevel(root)
        data_popup.title("Choose the information you wish to view.")

        data_popup.iconbitmap(icon_path)

        # Create a Treeview widget with the new "Work Order" column
        tree = ttk.Treeview(data_popup, columns=("User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        # Set up column headings with centered text
        for col in ("User Name", "Part Number", "Location", "Quantity", "Date and Time", "Work Order"):
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center")  # Center align the data inside the treeview


        # Create a frame to hold the label and buttons
        frame = ttk.Frame(data_popup)
        frame.pack()

        # Create a button to trigger data population for finish_goods
        button_finish_goods = ttk.Button(frame, text="View Finish Goods", command=lambda: populate_table("finish_goods"))
        button_finish_goods.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")

        # Create a button to trigger data population for borrow_goods
        button_borrow_goods = ttk.Button(frame, text="View Borrow Goods", command=lambda: populate_table("borrow_goods"))
        button_borrow_goods.grid(row=0, column=1, padx=4, pady=1, sticky="nsew")

        # Create a button to trigger data population for history_gparts
        button_history_gparts = ttk.Button(frame, text="View History Goods", command=lambda: populate_table("history_gparts"))
        button_history_gparts.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")

        # Create a button to export data to Excel
        button_export_excel = ttk.Button(frame, text="Export to Excel File", command=lambda: export_to_excel(tree))
        button_export_excel.grid(row=0, column=3, padx=4, pady=1, sticky="nsew")

        # Function to maximize the window upon treeview click
        def maximize_tree(event):
            # Check if the click event occurred outside the treeview
            if event.widget == tree:
                return
            data_popup.attributes('-fullscreen', True)

        # Bind treeview click event to maximize_tree function
        tree.bind("<Button-1>", maximize_tree)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
