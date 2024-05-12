import re
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from ttkbootstrap import Style
from tkinter import ttk, messagebox

def button1_clicked():
    global label_text
    label_text.set("An increasing trend in today's world is the emergence of the argument that topic. This will discuss the advantages")

def button2_clicked():
    global label_text
    label_text.set("Button 2 clicked")

def button3_clicked():
    global label_text
    label_text.set("Button 3 clicked")

def button4_clicked():
    global label_text
    label_text.set("Button 4 clicked")

def button5_clicked():
    global label_text
    label_text.set("Button 5 clicked")

def button6_clicked():
    root.destroy()

def open_main_window(logged_in_user):
    global label_text, root
    
    root = tk.Tk()
    root.title("Excel Summary")

    # Set the initial size of the window
    root.geometry("780x600")

    # Load images
    logo_image = Image.open("logo.png")
    logo_photo = ImageTk.PhotoImage(logo_image)

    other_image = Image.open("logo2.png")
    other_photo = ImageTk.PhotoImage(other_image)

    # Create a frame for the logo
    logo_frame = tk.Frame(root)
    logo_frame.pack()

    # Create a label to display the logo
    logo_label = tk.Label(logo_frame, image=logo_photo)
    logo_label.pack(side=tk.LEFT)

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.pack()

    # Create buttons with ttkbootstrap style
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Segoe UI', 11, 'bold'))

    button1 = ttk.Button(button_frame, text="View Qty", width=12, command=button1_clicked, style="TButton")
    button2 = ttk.Button(button_frame, text="Withdraw", width=12, command=button2_clicked, style="TButton")
    button3 = ttk.Button(button_frame, text="Barrow/Return", width=12, command=button3_clicked, style="TButton")
    button4 = ttk.Button(button_frame, text="Add Inventory", width=12, command=button4_clicked, style="TButton")
    button5 = ttk.Button(button_frame, text="View Map", width=12, command=button5_clicked, style="TButton")
    button6 = ttk.Button(button_frame, text="Exit", width=12, command=button6_clicked, style="TButton")

    # Pack buttons in the button frame
    button1.pack(side=tk.LEFT, padx=4, pady=15)
    button2.pack(side=tk.LEFT, padx=4, pady=15)
    button3.pack(side=tk.LEFT, padx=4, pady=15)
    button4.pack(side=tk.LEFT, padx=4, pady=15)
    button5.pack(side=tk.LEFT, padx=4, pady=15)
    button6.pack(side=tk.LEFT, padx=4, pady=15)

    # Create a frame for the other image
    other_frame = tk.Frame(root)
    other_frame.pack()

    # Create a label to display the other image
    other_label = tk.Label(other_frame, image=other_photo)
    other_label.pack(pady=10)

    # Create a label for displaying text with a gray background
    label_text = tk.StringVar()
    label_text.set(logged_in_user)  # Set the value of the label_text variable
    text_label = tk.Label(root, textvariable=label_text, bg="white", width=139, height=3)
    text_label.pack(side="bottom", pady=(0, 10))

    root.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Set the initial size of the window
login_window.geometry("210x220")

# Load and display the logo
logo_image = Image.open("C:/Users/joanm/Desktop/Noly/database tinker/login.png")
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
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Retrieve the password associated with the entered username
    c.execute("SELECT * FROM users WHERE username=?", (username_entry.get(),))
    user_data = c.fetchone()

    # Close connection
    conn.close()

    # Check if the username exists and the entered password matches the stored password
    if user_data and password_entry.get() == user_data[4]:  # Assuming password is stored at index 4
        logged_in_user = f"Logged in as: {user_data[1]} {user_data[2]}"  # Assuming first name is stored at index 1 and last name at index 2
        login_window.destroy()  # Close the login window
        open_main_window(logged_in_user)  # Pass logged_in_user to the main window
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")

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
    signup_button = ttk.Button(signup_window, text="Sign Up", command=lambda: signup_process(first_name_entry.get(), last_name_entry.get(), username_entry_signup.get(), password_entry_signup.get(), signup_window), style="TButton.Outline")
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

    # Check if password contains letters, numbers, and special characters
    if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=~`[\]{}|\\:;"\'<>,.?/]).{8,}$', password):
        messagebox.showerror("Sign Up", "Password must contain letters, numbers, and special characters.")
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
        # Insert new user with default 'admin' value of 'no'
        c.execute("INSERT INTO users (first_name, last_name, username, password, admin) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, username, password, 'no'))
        
        # Commit changes
        conn.commit()

        # Print the contents of the users table
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        print("Contents of the users table:")
        for row in rows:
            print(row)

        conn.close()

        messagebox.showinfo("Sign Up", "Sign up successful!")
        signup_window.destroy()  # Close the signup window after successful signup

signup_button = ttk.Button(login_window, text="Sign Up", width=13, command=signup, style="TButton.Outline")
signup_button.grid(row=4, column=0, columnspan=2, padx=(20, 10), pady=5, sticky="ew")

login_window.mainloop()
