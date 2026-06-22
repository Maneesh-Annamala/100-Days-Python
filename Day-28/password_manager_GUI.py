from tkinter import *
from tkinter import messagebox
from random import randint,choice,shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    """Generate a random password and copy it to clipboard."""

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Generate random letters, symbols and numbers
    password_letters = [choice(letters) for ch in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for i in range(randint(2, 4))]

    # Combine all characters
    password_list = password_letters + password_symbols + password_numbers

    # Shuffle password characters
    shuffle(password_list)

    # Convert list into string
    password = "".join(password_list)

    # Insert password into entry field
    password_entry.delete(0,END)
    password_entry.insert(0,password)

    # Copy password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    """Save website, email and password into a text file."""

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if all fields are filled
    if website and email and password:

        asking = messagebox.askyesno(
            title="Validating",
            message="Do you want to save your details?"
        )

        if asking:

            with open("Day-29/password-manager-start/data.txt","a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")

            # Clear input fields after saving
            website_entry.delete(0,END)
            email_entry.delete(0,END)
            password_entry.delete(0,END)

    else:
        messagebox.showwarning(
            title="Warning",
            message="Please fill every box"
        )


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()

window.title("Password Manager")

window.config(padx=50,pady=50)


# Logo image
photo = PhotoImage(file="logo.png")

canvas = Canvas(height=200,width=200)

canvas.create_image(100,100,image=photo)

canvas.grid(row=0,column=1)


# Website label
website_input = Label(text="Website:")
website_input.grid(row=1,column=0)


# Email/Username label
email_input = Label(text="Email/Username:")
email_input.grid(row=2,column=0)


# Password label
passsword_input = Label(text="Password:")
passsword_input.grid(row=3,column=0)


# Entry boxes
website_entry = Entry(width=35)
website_entry.grid(row=1,column=1,columnspan=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2,column=1,columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(row=3,column=1)


# Generate password button
gen_pass = Button(
    text="Generate Password",
    command=password_generator
)
gen_pass.grid(row=3,column=2)


# Save details button
add_button = Button(
    text="Add",
    width=36,
    command=save
)
add_button.grid(row=4,column=1,columnspan=2)


window.mainloop()