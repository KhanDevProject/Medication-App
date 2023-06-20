import subprocess
import customtkinter as ctk 
import tkinter.messagebox as mbox

app = ctk.CTk()
app.geometry("400x400")
app.title("Login")
mbox.showinfo("Welcome to Login System", "Below is the key to access\nUsername: 1\nPassword: a")

# Create the login frame
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20,padx=40, fill='both',expand=True)

# Set the label inside the frame
label = ctk.CTkLabel(master=frame, text='Medication Reminder')
label.pack(pady=12,padx=10)

# Create the text box for taking username input from user
user_entry= ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12,padx=10)

# Create a text box for taking password input from user
user_pass= ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12,padx=10)

# Define the login function
def login():
    # Get the entered username and password
    entered_username = user_entry.get()
    entered_password = user_pass.get()
    
    # Check if the entered username and password are correct
    if entered_username == "1" and entered_password == "a":
        # Launch the new app
        subprocess.Popen(["python", "Medication_Reminder.py"])
        # Destroy the login frame
        app.destroy()
        
    else:
        # Show an error message
        mbox.showerror("Invalid Login", "Please enter valid username and password.")


# Create a login button to login
button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12,padx=10)

# Create a remember me checkbox
checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12,padx=10)

app.mainloop()