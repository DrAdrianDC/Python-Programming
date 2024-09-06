import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        # Creating input
        self.display = tk.Entry(master, width=30, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        # Creating Buttons
        self.create_button('7', 1, 0)
        self.create_button('8', 1, 1)
        self.create_button('9', 1, 2)
        self.create_button('/', 1, 3)

        self.create_button('4', 2, 0)
        self.create_button('5', 2, 1)
        self.create_button('6', 2, 2)
        self.create_button('*', 2, 3)

        self.create_button('1', 3, 0)
        self.create_button('2', 3, 1)
        self.create_button('3', 3, 2)
        self.create_button('-', 3, 3)

        self.create_button('0', 4, 0)
        self.create_button('C', 4, 1)
        self.create_button('=', 4, 2)
        self.create_button('+', 4, 3)

        # Store current equation
        self.current_equation = ""

    def create_button(self, value, row, col):
        button = tk.Button(self.master, text=value, width=5, height=2, command=lambda: self.on_button_click(value))
        button.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, value):
        if value == "C":
            self.clear_display()
        elif value == "=":
            self.calculate_result()
        else:
            self.append_to_display(value)

    def clear_display(self):
        self.display.delete(0, tk.END)
        self.current_equation = ""

    def append_to_display(self, value):
        self.current_equation += str(value)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.current_equation)

    def calculate_result(self):
        try:
            result = eval(self.current_equation)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.current_equation = str(result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            self.clear_display()

# Main program
root = tk.Tk()
calculator = Calculator(root)
root.mainloop()


