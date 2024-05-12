import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

def button1_clicked():
    label_text.set("An increasing trend in today's world is the emergence of the argument that topic. This will discuss the advantages")

def button2_clicked():
    label_text.set("Button 2 clicked")

def button3_clicked():
    label_text.set("Button 3 clicked")

def button4_clicked():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the inventory table already exists
    c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='inventory' ''')
    table_exists = c.fetchone()

    if not table_exists:
        # Create the inventory table if it doesn't exist
        c.execute('''CREATE TABLE inventory (
                        id INTEGER PRIMARY KEY,
                        item_name TEXT,
                        quantity INTEGER,
                        price REAL
                    )''')

        # Commit changes and close connection
        conn.commit()
        conn.close()

        # Update label text
        label_text.set("Table created successfully.")
    else:
        conn.close()
        # Update label text
        label_text.set("Table already exists.")



def button5_clicked():
    label_text.set("Button 5 clicked")

def button6_clicked():
    root.destroy()


def open_main_window(logged_in_user):
    global label_text, root
    
    root = tk.Tk()
    root.title("Excel Summary")

    # Set the initial size of the window
    root.geometry("810x600")

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
    style.configure('TButton', font=('Segoe UI', 10, 'bold'))

    button1 = ttk.Button(button_frame, text="Add User", width=13, command=button1_clicked, style="TButton")
    button2 = ttk.Button(button_frame, text="Remove User", width=13, command=button2_clicked, style="TButton")
    button3 = ttk.Button(button_frame, text="Access Control", width=13, command=button3_clicked, style="TButton")
    button4 = ttk.Button(button_frame, text="Add table", width=13, command=button4_clicked, style="TButton")
    button5 = ttk.Button(button_frame, text="View Map", width=13, command=button5_clicked, style="TButton")
    button6 = ttk.Button(button_frame, text="Exit", width=13, command=button6_clicked, style="TButton")

    # Pack buttons in the button frame
    button1.pack(side=tk.LEFT, padx=10, pady=15)
    button2.pack(side=tk.LEFT, padx=10, pady=15)
    button3.pack(side=tk.LEFT, padx=10, pady=15)
    button4.pack(side=tk.LEFT, padx=10, pady=15)
    button5.pack(side=tk.LEFT, padx=10, pady=15)
    button6.pack(side=tk.LEFT, padx=10, pady=15)

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

# Test the code
open_main_window("John Doe")
