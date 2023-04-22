import tkinter as tk
from tkinter import PhotoImage

Large_font_style = ("Arial", 24, "bold")
Small_Font_style = ("Arial", 12)
Digit_font_style = ("Arial", 16, "bold")
Default_font = ("Arial", 14)

OFF_white = "#F8FAFF"
White = "#FFFFFF"
Light_gray = "#F5F5F5"
Label_color = "#25265E"
Light_blue = "#CCEDFF"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        # self.window.geometry("375x667")
        self.window.geometry("250x400")
        self.window.resizable(False, False)
        self.window.title("Calc")
        img = PhotoImage(file='resources/icon.png')
        self.window.iconphoto(False, img)
        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_op_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<Delete>", lambda event: self.clear())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def minus(self):
        self.current_expression *= -1

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=Light_gray,
                               fg=Label_color, padx=24, font=Small_Font_style)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=Light_gray,
                         fg=Label_color, padx=24, font=Large_font_style)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=Light_gray)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=White, fg=Label_color, font=Digit_font_style,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_op_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_white, fg=Label_color, font=Default_font,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_white, fg=Label_color, font=Default_font,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        for _, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_white, fg=Label_color, font=Default_font,
                               borderwidth=0, command=self.square)
            button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_white, fg=Label_color, font=Default_font,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:

            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"

        finally:
            self.update_label()

    def create_equals_button(self):
        for _, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text="=", bg=Light_blue, fg=Label_color, font=Default_font,
                               borderwidth=0, command=self.evaluate)
            button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f"{symbol}")
            self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:9])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
