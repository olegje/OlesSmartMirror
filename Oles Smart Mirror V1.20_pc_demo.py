#!/usr/bin/python3

try:
    import Tkinter as tk
    from Tkinter import *
except ImportError:
    # for Python3
    import tkinter as tk
    from tkinter import *
import time
print("Verison 99.99.99")
class Master_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self) # creation of frame
            self.frames[F] = frame # puts frame in dictionary
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="black")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont] # local variable
        frame.tkraise() # raises frame from self.frames

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        button1 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
class Switch(Master_GUI):
    def __init__(self):
        #Here i want to run a command to change to PageOne:
        #Master_GUI.show_frame(tk.Frame, PageOne)
        #app.show_frame(PageOne)
        x = 2

if __name__ == "__main__":
    app = Master_GUI()
    switch = Switch()
    app.mainloop()
