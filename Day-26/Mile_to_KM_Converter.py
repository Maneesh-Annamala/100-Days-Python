from tkinter import *

def converter():
    """Convert miles into kilometers and update the result label."""

    mile = mile_input.get()

    km_convert.config(text=f"{float(mile) * 1.60934:.2f}")


# Create main window
window = Tk()

window.title("Mile to Km Converter")

window.minsize(width=300, height=100)

# Add padding around the window
window.config(padx=20, pady=20)


# Input field for miles
mile_input = Entry(width=10)
mile_input.grid(row=1, column=2)


# Miles label
label = Label(text="Miles")
label.grid(row=1, column=3)


# Static text label
label1 = Label(text="is equal to")
label1.grid(row=2, column=1)


# Result label
km_convert = Label(text="0")
km_convert.grid(row=2, column=2)


# KM label
km = Label(text="KM")
km.grid(row=2, column=3)


# Calculate button
button = Button(text="Calculate",command=converter)
button.grid(row=3, column=2)


# Run application
window.mainloop()