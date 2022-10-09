from tkinter import *


def click():
    a = eval(txt.get())
    lbl.configure(text=f"{a}")


window = Tk()
window.title("калькулятор")
window.geometry("800x600+300+100")
txt = Entry(window, width=20)
txt.grid(column=0)
btn = Button(window, text="calculate", command=click)
btn.grid(column=2, row=0)
lbl = Label(window)
lbl.grid(column=0, row=1)
window.mainloop()