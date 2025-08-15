import tkinter as tk
from tkinter import messagebox
def clic():
    messagebox.showinfo("dale click")
root = tk.Tk()
root.title("prueba")
root.geometry("200x200")
btn1 = tk.Button(root, text="dar click", command=clic)
btn1.pack()

root.mainloop()