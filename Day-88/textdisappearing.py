import tkinter as tk




window = tk.Tk()
window.title("Text Disappearing Writing App")
window.config(padx=10,pady=10)

timer = None

def game_start():
    global exit_button
    global typing_window
    text.destroy()
    start_button.destroy()
    typing_window = tk.Text(window)
    typing_window.pack()
    exit_button = tk.Button(window,text="Exit",command=window.destroy)
    exit_button.config(padx=10,pady=10,bg="red")
    exit_button.pack()
    typing_window.bind("<Key>",reset_timer)

def reset_timer(event = None):
    global timer
    if timer:
        window.after_cancel(timer)
    timer = window.after(5000,del_text)

def del_text():
    typing_window.delete("1.0",tk.END)




def display():
    global text
    global start_button
    text = tk.Label(
            window,
            text="Welcome to the Text Disappeaing App.\n" \
            "You need to type something continously but if you stop for 5 sec the text you typed will disappear.\n" \
            "The motive of this game is to increase the typing speed",
            font=("Courier", 30, "bold"),
            fg="blue",
            wraplength=1000
        )
    text.pack()
    start_button = tk.Button(window,text="Start",command=game_start)
    start_button.config(padx=10,pady=10,bg="green")
    start_button.pack()

display()

window.mainloop()