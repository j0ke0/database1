import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
import re
from image_icon_paths import icon_path, dbnames, users, passwords, hosts, ports, image_path

#signup_process 

def signup_process(first_name, last_name, username, password, signup_window, db_password):
    try:
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

        # Capitalize 2 words the first letter of first name and last name
        first_name = ' '.join(word.capitalize() for word in first_name.split())
        last_name = ' '.join(word.capitalize() for word in last_name.split())

        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=dbnames,
            user=users,
            password=passwords,
            host=hosts,
            port=ports
        )
        c = conn.cursor()

        # Check if the username already exists
        c.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = c.fetchone()

        if existing_user:
            messagebox.showerror("Sign Up", "Username already taken. Please choose another username.")
        else:
            # Insert new user with default 'admin' value of 'no'
            c.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, username, password))
            
            # Commit changes
            conn.commit()

            conn.close()

            messagebox.showinfo("Sign Up", "Sign up successful!")
            signup_window.destroy()  # Close the signup window after successful signup
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")