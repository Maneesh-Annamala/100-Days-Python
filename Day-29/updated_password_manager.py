from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    """Generate a secure random password and copy it to the clipboard."""

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Generate random letters
    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    # Generate random symbols
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    # Generate random numbers
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    # Combine all characters
    password_list = password_letters + password_symbols + password_numbers

    # Shuffle password characters
    shuffle(password_list)

    # Convert list into string
    password = "".join(password_list)

    # Clear old password if present
    password_entry.delete(0, END)

    # Insert generated password
    password_entry.insert(0, password)

    # Copy password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    """Save website credentials into a JSON file."""

    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()

    # Structure for new website data
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Validate input fields
    if website and email and password:

        asking = messagebox.askyesno(
            title="Validating",
            message="Do you want to save your details?"
        )

        if asking:

            try:
                with open("data.json", "r") as data_file:

                    # Read existing JSON data
                    data = json.load(data_file)

            except (FileNotFoundError, json.JSONDecodeError):

                # Create file if it doesn't exist
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:

                # Add new data to existing data
                data.update(new_data)

                # Save updated data
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:

                # Clear input fields after saving
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)

                # Focus cursor back to website entry
                website_entry.focus()

    else:
        messagebox.showwarning(
            title="Warning",
            message="Please fill every box"
        )


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    """Search and display credentials for a website."""

    web_entry = website_entry.get().title()

    # Prevent searching with empty website field
    if not web_entry:
        messagebox.showwarning(
            title="Warning",
            message="Please enter website name"
        )
        return

    try:
        with open("data.json") as data_file:

            # Load stored credentials
            data = json.load(data_file)

    except (FileNotFoundError, json.JSONDecodeError):

        messagebox.showerror(
            title="Error",
            message="Data file doesn't exist"
        )

    else:

        # Check if website exists
        if web_entry in data:

            email = data[web_entry]["email"]
            password = data[web_entry]["password"]

            # Display credentials
            messagebox.showinfo(
                title=web_entry,
                message=f"Email: {email}\nPassword: {password}"
            )

        else:

            messagebox.showerror(
                title="Error",
                message=f"{web_entry} doesn't exist in file"
            )


# ---------------------------- UI SETUP ------------------------------- #

# Main application window
window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo image
photo = PhotoImage(file="logo.png")

canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=1)

# Website label
website_input = Label(text="Website:")
website_input.grid(row=1, column=0)

# Email/Username label
email_input = Label(text="Email/Username:")
email_input.grid(row=2, column=0)

# Password label
password_input = Label(text="Password:")
password_input.grid(row=3, column=0)

# Website entry box
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

# Email entry box
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)

# Optional default email
# email_entry.insert(0, "your_email@gmail.com")

# Password entry box
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Search button
search_button = Button(
    text="Search",
    command=find_password,
    width=13
)
search_button.grid(row=1, column=2)

# Generate password button
gen_pass = Button(
    text="Generate Password",
    command=password_generator
)
gen_pass.grid(row=3, column=2)

# Add credentials button
add_button = Button(
    text="Add",
    width=36,
    command=save
)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()