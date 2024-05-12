import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from ttkbootstrap import Style

def create_users_table():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create the users table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

def login():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Retrieve the password associated with the entered username
    c.execute("SELECT password FROM users WHERE username=?", (username_entry.get(),))
    stored_password = c.fetchone()

    # Close connection
    conn.close()

    # Check if the username exists and the entered password matches the stored password
    if stored_password and password_entry.get() == stored_password[0]:
        logged_in_user = f"Logged in as: {stored_password[1]} {stored_password[2]}"  # Assuming first name is stored at index 1 and last name at index 2
        root.destroy()  # Close the login window
        open_main_application()
    else:
        login_status_label.config(text="Invalid username or password", fg="red")

def open_main_application():
    # Put the code for opening your main application window here
    exec(open("database_ttk.py").read())
    print("Main application opened")

def signup():
    # Create a new window for signup
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    # First name label and entry
    first_name_label = tk.Label(signup_window, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = tk.Entry(signup_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # Last name label and entry
    last_name_label = tk.Label(signup_window, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = tk.Entry(signup_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    # Username label and entry
    username_label = tk.Label(signup_window, text="Username:")
    username_label.grid(row=2, column=0, padx=10, pady=5)
    username_entry_signup = tk.Entry(signup_window)
    username_entry_signup.grid(row=2, column=1, padx=10, pady=5)

    # Password label and entry
    password_label = tk.Label(signup_window, text="Password:")
    password_label.grid(row=3, column=0, padx=10, pady=5)
    password_entry_signup = tk.Entry(signup_window, show="*")
    password_entry_signup.grid(row=3, column=1, padx=10, pady=5)

    # Sign up button
    signup_button = ttk.Button(signup_window, text="Sign Up", command=lambda: signup_process(first_name_entry.get(), last_name_entry.get(), username_entry_signup.get(), password_entry_signup.get(), signup_window))
    signup_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

def signup_process(first_name, last_name, username, password, signup_window):
    # Check if any field is empty
    if not all([first_name, last_name, username, password]):
        messagebox.showerror("Sign Up", "All fields are required. Please fill in all the fields.")
        return

    # Check if password is at least 8 characters long
    if len(password) < 8:
        messagebox.showerror("Sign Up", "Password must be at least 8 characters long.")
        return

    # Capitalize the first letter of first name and last name
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()

    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the username already exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        messagebox.showerror("Sign Up", "Username already taken. Please choose another username.")
    else:
        # Insert new user
        c.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)", (first_name, last_name, username, password))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Sign Up", "Sign up successful!")
        signup_window.destroy()  # Close the signup window after successful signup

# Create the main Tkinter window for login

def print_database_contents():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Retrieve data from the users table
    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    # Print the contents of the users table
    print("Contents of the users table:")
    for row in rows:
        print(row)

    # Close connection
    conn.close()

# Call this function to create the users table if it doesn't exist
create_users_table()

root = tk.Tk()
root.title("Login")

# Create a style object with 'litera' theme
style = Style(theme='litera')
# Configure the style for TButton
style.configure('TButton', font=('Segoe UI', 10, 'bold'))

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Login button
login_button = ttk.Button(root, text="Login", command=login, style="TButton.Outline")
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

# Sign up button
signup_button = ttk.Button(root, text="Sign Up", command=signup, style="TButton.Outline")
signup_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

# Label to show login status
login_status_label = tk.Label(root, text="", fg="red")
login_status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
