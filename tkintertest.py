import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        choiceVar = tk.StringVar()
        choices = ("choice 1", "choice 2", "choice 3", "choice 4")
        choiceVar.set(choices[0])

        om = tk.OptionMenu(self, choiceVar, *choices)
       
        om.pack()

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
