import os
import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import ttk, messagebox
from image_icon_paths import icon_path, dbnames, users, passwords, hosts, ports, image_path

db_password = 'Nolcubs0#'

def create_popup_table(root):
    def list_unmatched_partnumbers():
        unmatched_partnumbers = []
        try:
            # Connect to the database
            db_connection = psycopg2.connect(
                dbname=dbnames,
                user=users,
                password=passwords,
                host=hosts,
                port=ports
            )
            
            # Create a cursor object using the connection
            cursor = db_connection.cursor()
            
            # Retrieve table names
            query = sql.SQL("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            cursor.execute(query)
            tables = [table[0].lower() for table in cursor.fetchall()]
            
            # Retrieve part numbers from raw_partnumbers table
            cursor.execute("SELECT partnumber FROM raw_partnumbers")
            partnumbers = [partnumber[0].lower() for partnumber in cursor.fetchall()]
            
            # Find part numbers that have no match in tables
            unmatched_partnumbers = [partnumber for partnumber in partnumbers if partnumber not in tables]
            
            # Close cursor and connection
            cursor.close()
            db_connection.close()
            
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error connecting to PostgreSQL: {e}")
        
        return unmatched_partnumbers

    def create_button_action():
        selected_part_number = selected_partnumber.get().lower()

        # Check if a part number is selected
        if selected_part_number == "select part number":
            popuptable.destroy()
            messagebox.showwarning("No Part Number Selected", "Please select a part number from the dropdown.")
            return

        try:
            # Connect to the database
            db_connection = psycopg2.connect(
                dbname=dbnames,
                user=users,
                password=passwords,
                host=hosts,
                port=ports
            )

            # Create a cursor object using the connection
            cursor = db_connection.cursor()

            # SQL statement to create the table
            create_table_sql = f"""
            CREATE TABLE {selected_part_number} (
                pk SERIAL PRIMARY KEY,
                part_number VARCHAR(50),
                purchase_number VARCHAR(50),
                qty INTEGER,
                storage VARCHAR(100),
                logged_in_users VARCHAR(50),
                time_stamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """

            # Execute the SQL statement to create the table
            cursor.execute(create_table_sql)

            # Commit the transaction
            db_connection.commit()

            # Close cursor and connection
            cursor.close()
            db_connection.close()

            messagebox.showinfo("Success", f"Table '{selected_part_number}' created successfully.")

        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error creating table: {e}")
        finally:
            popuptable.destroy()

    def cancel_button_action():
        popuptable.destroy()

    unmatched_partnumbers = list_unmatched_partnumbers()
    if not unmatched_partnumbers:
        messagebox.showwarning("No Actions Required", "Each part number has received a table")
        return

    popuptable = tk.Tk()
    popuptable.title("Raw Parts")

    popuptable.iconbitmap(icon_path)

    selected_partnumber = tk.StringVar(value="Select Part Number")
    partnumber_option_menu = tk.OptionMenu(popuptable, selected_partnumber, *unmatched_partnumbers)
    partnumber_option_menu.config(width=20, bg='black')
    partnumber_option_menu.pack(padx=5, pady=10)

    create_button = ttk.Button(popuptable, text="Create", command=create_button_action)
    create_button.pack(side=tk.LEFT, padx=5, pady=10)

    cancel_button = ttk.Button(popuptable, text="Cancel", command=cancel_button_action)
    cancel_button.pack(side=tk.RIGHT, padx=5, pady=10)

    popuptable.mainloop()
