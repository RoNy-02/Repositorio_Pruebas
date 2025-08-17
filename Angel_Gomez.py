import tkinter as tk

angel_gomez = tk.Tk()
angel_gomez.title("Angel Gomez's Window")
angel_gomez.geometry("400x300")

label = tk.Label(angel_gomez, text="Hello, Angel Gomez!", font=("Arial", 16))
label.pack(pady=20)
button = tk.Button(angel_gomez, text="Click Me", command=lambda: print("Button clicked!"))
button.pack(pady=10)

angel_gomez.mainloop()