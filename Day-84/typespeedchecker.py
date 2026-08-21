import tkinter as tk
import random
import time


sentences = [
    "Learning to program is not about memorizing every piece of code, but about understanding how to break a difficult problem into smaller and manageable pieces.",
    "The more you practice solving programming problems without immediately looking at the solution, the better your logical thinking and problem solving skills will become over time.",
    "Python is a powerful programming language that can be used for web development, automation, data analysis, artificial intelligence, machine learning, and many other interesting applications.",
    "When you build a project from scratch, you will probably make many mistakes, encounter confusing errors, and sometimes feel stuck, but every error teaches you something valuable.",
    "A good programmer does not necessarily know every function or library by memory, but knows how to understand a problem, search for useful information, test different approaches, and build a working solution.",
    "Consistency is more important than studying for many hours on a single day because spending a reasonable amount of time practicing every day helps you remember concepts and gradually improves your programming skills.",
    "The fastest way to improve your typing speed is to focus on accuracy first and gradually increase your speed instead of trying to type extremely fast and making a large number of mistakes.",
    "Technology continues to change rapidly, so developers need to keep learning new tools, frameworks, programming languages, and concepts throughout their careers in order to remain effective and adaptable.",
    "Sometimes a programming problem may look extremely complicated at first, but after carefully understanding the input, output, constraints, and required operations, the solution can become surprisingly simple.",
    "Building small projects is one of the best ways to transform theoretical programming knowledge into practical experience because projects force you to connect different concepts and solve problems that tutorials may not cover."
]


window = tk.Tk()

window.title("Type Speed Check")
window.config(padx=10, pady=10, bg="skyblue")
window.grid_columnconfigure(0, weight=1)

original_text = random.choice(sentences)
typed_text = ""


def display():
    global start
    global typed_text
    global text
    global text_enter

    start = time.time()
    start_button.destroy()

    text = tk.Label(
        window,
        text=original_text,
        font=("Courier", 30, "bold"),
        wraplength=1000
    )
    text.grid(row=1, column=0)

    text_enter = tk.Text(window)
    text_enter.grid(row=2, column=0)

    tk.Button(
        window,
        text="SUBMIT",
        command=calculations
    ).grid(row=3, column=0)


def calculations():
    end = time.time()
    result = end - start

    typed_text = text_enter.get("1.0", tk.END)

    text.destroy()
    text_enter.destroy()

    count = 0

    org = original_text.split()
    typed = typed_text.split()

    for i in range(min(len(typed), len(org))):
        if org[i] == typed[i]:
            count += 1

    typing_speed = int(count * 60 / result)

    tk.Label(
        window,
        text=f"Words: {count}",
        font=("Courier", 30, "bold"),
        wraplength=1000
    ).grid(row=0, column=0)

    tk.Label(
        window,
        text=f"WPM: {typing_speed}",
        font=("Courier", 30, "bold")
    ).grid(row=1, column=0)


start_button = tk.Button(
    window,
    text="START",
    command=display
)

start_button.pack()

window.mainloop()