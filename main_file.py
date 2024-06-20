import os
import psycopg2
import tkinter as tk
from PIL import Image, ImageTk
from ttkbootstrap import Style
from tkinter import messagebox
from withdrawal import withdraw
from borrow_goods import borrow
from view_all import view_all_data
from tkinter import ttk, messagebox
import tkinter.messagebox as messagebox
from raw_add_parts import raw_iqc_entry
from raw_quarantine import quarantine_raw
from signup_processes import signup_process
from final_shipped import final_shipped_goods
from raw_withdrawal_parts import raw_withdrawal
from raw_view_inventory import button01_clicked
from raw_move_to_storage import move_to_storage
from return_good_stocks import return_good_stock
from finish_goods_button import final_goods_entry
from final_shipped_view import final_view_shipped
from raw_create_table_final import create_popup_table
from raw_add_newpartnumber import raw_add_partnumber_data
from raw_delete_partnumbers import raw_delete_part_numbers
from final_dropdown_selection import add_final_seletion_dropdown
from final_del_dropdown_selection import final_delete_part_numbers
from image_icon_paths import icon_path, dbnames, users, passwords, hosts, ports, image_path

# Meow! Here's a little drawing of a cat to lighten up your code. 
#  /\_/\  
# ( o.o ) 
#  > ^ <

db_password = passwords
db_connection = None
db_cursor = None

def button1_tab0_clicked(root, logged_in_user):
    raw_add_partnumber_data(root, logged_in_user)

def button2_tab0_clicked(root):
    raw_delete_part_numbers(root)

def button3_tab0_clicked(root, logged_in_user):
    add_final_seletion_dropdown(root, logged_in_user)

def button4_tab0_clicked(root):
    final_delete_part_numbers(root)

def button5_tab0_clicked(root):
    if __name__ == "__main__":
        create_popup_table(root)

def button6_tab0_clicked(root):
     final_view_shipped(root)

def button1_tab1_clicked(root):
    button01_clicked(root)

def button2_tab1_clicked(root, logged_in_user):
    raw_iqc_entry(root, logged_in_user)

def button3_tab1_clicked(root, logged_in_user):
    move_to_storage(root, logged_in_user, db_cursor, db_connection)

def button4_tab1_clicked(root, logged_in_user):
    raw_withdrawal(root, logged_in_user, db_cursor, db_connection)

def button5_tab1_clicked(root, logged_in_user):
    quarantine_raw(root, logged_in_user, db_cursor, db_connection)


def button2_clicked(root, logged_in_user):
    view_all_data(root, logged_in_user, db_cursor, db_connection)

def button3_clicked(root, logged_in_user, is_admin):
    withdraw(root, logged_in_user, db_cursor, db_connection, is_admin)

def button4_clicked(root, logged_in_user):
    borrow(root, logged_in_user, db_cursor, db_connection)

def button5_clicked(root, logged_in_user):
    final_goods_entry(root, logged_in_user)

def button6_clicked(root, logged_in_user):
    return_good_stock(root, logged_in_user, db_cursor, db_connection)

def button7_clicked(root, logged_in_user):
    final_shipped_goods(root, logged_in_user)

def button_clicked(root):
    root.destroy()

def create_notebook(root, logged_in_user, is_admin):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both', padx=7, pady=(7, 0))  # Add pady=(10, 0) for top padding

    # Create tabs
    tab0 = ttk.Frame(notebook)
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)

    # Center the labels within the available space
    label_width = 22  # Adjust this value according to your preference
    tab_label0 = 'Admin Tab'.center(label_width)
    tab_label1 = 'Raw Materials & Parts'.center(label_width)
    tab_label2 = 'SRCK & MFP Inventory'.center(label_width)

    # Add tabs to the notebook with centered labels
    notebook.add(tab0, text=tab_label0)
    notebook.add(tab1, text=tab_label1)
    notebook.add(tab2, text=tab_label2)

    style = ttk.Style()
    style.map("TNotebook.Tab", foreground=[('selected', 'blue')])

    if is_admin:
        button1_tab0 = ttk.Button(tab0, text="Add Raw Parts", command=lambda: button1_tab0_clicked(root, logged_in_user))
        button1_tab0.pack(side=tk.LEFT, padx=2, pady=15)

    if is_admin:
        button2_tab0 = ttk.Button(tab0, text="Del Raw Parts", command=lambda: button2_tab0_clicked(root))
        button2_tab0.pack(side=tk.LEFT, padx=2, pady=15)

    if is_admin:
        button3_tab0 = ttk.Button(tab0, text="Add Final MFP", command=lambda: button3_tab0_clicked(root, logged_in_user))
        button3_tab0.pack(side=tk.LEFT, padx=2, pady=15)

    if is_admin:
        button4_tab0 = ttk.Button(tab0, text="Del Final MFP", command=lambda: button4_tab0_clicked(root))
        button4_tab0.pack(side=tk.LEFT, padx=2, pady=15)

    if is_admin:
        button5_tab0 = ttk.Button(tab0, text="Make Raw Table", command=lambda: button5_tab0_clicked(root))
        button5_tab0.pack(side=tk.LEFT, padx=2, pady=15)

    button6_tab0 = ttk.Button(tab0, text="Shipped History", command=lambda: final_view_shipped(root))
    button6_tab0.pack(side=tk.LEFT, padx=2, pady=15)


    # Add buttons to tab1
    button1_tab1 = ttk.Button(tab1, text="View Inventory", command=lambda: button1_tab1_clicked(root))
    button1_tab1.pack(side=tk.LEFT, padx=4, pady=15)

    button2_tab1 = ttk.Button(tab1, text="IQC Entries", command=lambda: button2_tab1_clicked(root, logged_in_user))
    button2_tab1.pack(side=tk.LEFT, padx=4, pady=15)

    # Add your new button to tab1
    button3_tab1 = ttk.Button(tab1, text="IQC to Storage", command=lambda: button3_tab1_clicked(root, logged_in_user))
    button3_tab1.pack(side=tk.LEFT, padx=4, pady=15)

    # Add your new button to tab1
    button4_tab1 = ttk.Button(tab1, text="Parts Withdrawal", command=lambda: button4_tab1_clicked(root, logged_in_user))
    button4_tab1.pack(side=tk.LEFT, padx=4, pady=15)

    # Add your new button to tab1
    button5_tab1 = ttk.Button(tab1, text="Quarantine Parts", command=lambda: button5_tab1_clicked(root, logged_in_user))
    button5_tab1.pack(side=tk.LEFT, padx=4, pady=15)


    # Add buttons to tab2 (for admin)
    button2 = ttk.Button(tab2, text="View MFP", command=lambda: button2_clicked(root, logged_in_user))
    button2.pack(side=tk.LEFT, padx=4, pady=15)

    button3 = ttk.Button(tab2, text="Withdrawal", command=lambda: button3_clicked(root, logged_in_user, is_admin))
    button3.pack(side=tk.LEFT, padx=4, pady=15)

    button4 = ttk.Button(tab2, text="Borrow", command=lambda: button4_clicked(root, logged_in_user))
    button4.pack(side=tk.LEFT, padx=4, pady=15)

    button5 = ttk.Button(tab2, text="AQL Entries", command=lambda: button5_clicked(root, logged_in_user))
    button5.pack(side=tk.LEFT, padx=4, pady=15)

    button6 = ttk.Button(tab2, text="Return", command=lambda: button6_clicked(root, logged_in_user))
    button6.pack(side=tk.LEFT, padx=4, pady=15)

    button7 = ttk.Button(tab2, text="Ship MFP", command=lambda: button7_clicked(root, logged_in_user))
    button7.pack(side=tk.LEFT, padx=4, pady=15)

def open_main_window(logged_in_user, is_admin):
    root = tk.Tk()
    root.title("Production Parts Monitoring")
    root.geometry("740x300")

    root.iconbitmap(icon_path)

        # Adjusting style for the tabs
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[0, 4])  # Adjust padx and pady values as needed
    style.configure('TButton', font=('Segoe UI', 12))

    add_path = "logo.png"
    full_path = image_path + add_path
    image = Image.open(full_path)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo)
    image_label.pack()

    create_notebook(root, logged_in_user, is_admin)

    # Create a label for displaying text with a gray background
    label_text = tk.StringVar()
    label_text.set(logged_in_user)
    text_label = tk.Label(root, textvariable=label_text, bg="white", width=30, height=3)
    text_label.pack(side=tk.LEFT, pady=(0, 10))

    # Create a button
    logout_button = ttk.Button(root, text="Logout", command=lambda: button_clicked(root))
    logout_button.pack(side=tk.LEFT, pady=(0, 10))

    small_image = "lower image.png"
    full_small = image_path + small_image
    small_image = Image.open(full_small)  # Replace "path_to_small_image.png" with the actual path
    small_photo = ImageTk.PhotoImage(small_image)
    small_image_label = tk.Label(root, image=small_photo)
    small_image_label.pack(side=tk.LEFT, padx=25, pady=(0, 10))

    root.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Set the initial size of the window
login_window.geometry("230x230")

login_window.iconbitmap(icon_path)

add_path = "login.png"
full_path_login = image_path + add_path
logo_image = Image.open(full_path_login)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(login_window, image=logo_photo)

# Place the logo label in the login window using grid
logo_label.grid(row=0, column=0, columnspan=2, pady=5)

# Add column and row weights to center the logo
login_window.columnconfigure(0, weight=1)
login_window.columnconfigure(1, weight=1)
login_window.rowconfigure(0, weight=1)

# Username and password entry fields
username_label = tk.Label(login_window, text="Username:", font=('Segoe UI', 10, 'bold'))
username_label.grid(row=1, column=0, padx=1, pady=5, sticky="e")

username_entry = tk.Entry(login_window)
username_entry.grid(row=1, column=1, padx=1, pady=5)

# Password label and entry fields
password_label = tk.Label(login_window, text="Password:", font=('Segoe UI', 10, 'bold'))
password_label.grid(row=2, column=0, padx=1, pady=5, sticky="e")

password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=2, column=1, padx=1, pady=5)

style = Style(theme='litera')
style.configure('TButton', font=('Segoe UI', 10, 'bold'))

def login(event=None):
    global db_connection, db_cursor
    try:
        # Connect to PostgreSQL database
        db_connection = psycopg2.connect(
            dbname=dbnames,
            user=users,
            password=passwords,
            host=hosts,
            port=ports
        )
        db_cursor = db_connection.cursor()

        # Retrieve the password, admin status, and other user data associated with the entered username
        db_cursor.execute("SELECT * FROM users WHERE username=%s", (username_entry.get(),))
        user_data = db_cursor.fetchone()

        if user_data:
            password_correct = password_entry.get() == user_data[4]  # Assuming password is stored at index 4
            is_admin = user_data[5]  # Assuming admin status is stored at index 5
            if is_admin is None:
                messagebox.showerror("Login Failed", "Account not approved. Please contact the administrator.")
            elif password_correct and is_admin in (True, False):
                # Capitalize the first letter of first and last names
                first_name = user_data[1].capitalize()
                last_name = user_data[2].capitalize()
                logged_in_user = f"How are you: {first_name} {last_name}"
                log_user = f"{first_name} {last_name}"
                login_window.destroy()  # Close the login window
                open_main_window(logged_in_user, is_admin)  # Pass is_admin to the main window function
            else:
                messagebox.showerror("Login Failed", "Incorrect password. Please try again.")
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")

# Login button
login_button = ttk.Button(login_window, text="Login", command=login, style="TButton.Outline")
login_button.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=5, sticky="ew")

# Bind the <Return> or <KP_Enter> key to the login function
login_window.bind('<Return>', login)

# Alternatively, you can also bind it to the password entry field
password_entry.bind('<Return>', login)

def signup():
    # Create a new window for signup
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")

    # Set the initial size of the window
    signup_window.geometry("240x180")

    signup_window.iconbitmap(icon_path)

    # First name label and entry
    first_name_label = tk.Label(signup_window, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
    first_name_entry = tk.Entry(signup_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="WE")

    # Last name label and entry
    last_name_label = tk.Label(signup_window, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
    last_name_entry = tk.Entry(signup_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="WE")

    # Username label and entry
    username_label = tk.Label(signup_window, text="Username:")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
    username_entry_signup = tk.Entry(signup_window)
    username_entry_signup.grid(row=2, column=1, padx=10, pady=5, sticky="WE")

    # Password label and entry
    password_label = tk.Label(signup_window, text="Password:")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="E")
    password_entry_signup = tk.Entry(signup_window, show="*")
    password_entry_signup.grid(row=3, column=1, padx=10, pady=5, sticky="WE")

    # Sign up button
    signup_button = ttk.Button(signup_window, text="Sign Up", command=lambda: signup_process(first_name_entry.get(), last_name_entry.get(), username_entry_signup.get(), password_entry_signup.get(), signup_window, db_password), style="TButton.Outline")
    signup_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

signup_button = ttk.Button(login_window, text="Sign Up", width=13, command=signup, style="TButton.Outline")
signup_button.grid(row=4, column=0, columnspan=2, padx=(20, 10), pady=(5, 10), sticky="ew")

login_window.mainloop()
