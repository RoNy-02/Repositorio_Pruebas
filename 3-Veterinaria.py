import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector

# Colores en tonos grises elegantes
BG_COLOR = "#d9d9d9"         # Fondo general
FRAME_COLOR = "#FFFFFF"      # Marco del formulario
TEXT_COLOR = "#333333"       # Texto oscuro
ENTRY_BG = "#f2f2f2"         # Fondo de entradas

# ventana principal
vetery = tk.Tk()
vetery.title("Veterinaria ")
vetery.geometry("500x400")
vetery.configure(bg=BG_COLOR)

def seleccionar_imagen():
    global ruta_imagen
    archivo = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png")])
    if not archivo:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna imagen.")
        ruta_imagen = None
        foto_label.config(image='', text="Foto")
        foto_label.image = None
        return
    ruta_imagen = archivo
    try:
        imagen = Image.open(archivo)
        imagen.thumbnail((100, 100))
        imagen_tk = ImageTk.PhotoImage(imagen)
        foto_label.config(image=imagen_tk, text="")
        foto_label.image = imagen_tk
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")
        foto_label.config(image='', text="Foto")
        foto_label.image = None

def agregar_registro():
    global ruta_imagen
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="veterinaria")
        cursor = cn.cursor()
        sql = "INSERT INTO registro (Nombre, Raza, Edad, Dueno, Med_Veterinario, Imagen) VALUES (%s, %s, %s, %s, %s, %s)"
        # Leer imagen como bytes si existe
        imagen_bytes = None
        if ruta_imagen:
            with open(ruta_imagen, "rb") as f:
                imagen_bytes = f.read()
        datos = (
            nombre_entry.get(),
            raza_entry.get(),
            edad_entry.get(),
            dueno_entry.get(),
            vet_entry.get(),
            imagen_bytes
        )
        cursor.execute(sql, datos)
        cn.commit()
        cursor.close()
        cn.close()
        messagebox.showinfo("Éxito", "Registro agregado correctamente.")
        ruta_imagen = None
        foto_label.config(image='', text="Foto")
        foto_label.image = None
        nombre_entry.delete(0, tk.END)
        raza_entry.delete(0, tk.END)
        edad_entry.delete(0, tk.END)
        dueno_entry.delete(0, tk.END)
        vet_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el animal.\n{e}")

# Título
titulo = tk.Label(vetery, text="Veterinaria \"HERNÁNDEZ\"", 
                  font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
titulo.pack(pady=10)

# Marco del formulario
frame = tk.Frame(vetery, bg=FRAME_COLOR, bd=2, relief="groove", padx=15, pady=15)
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Campo de "foto" como espacio visual
foto_label = tk.Label(frame, text="Foto", bg=ENTRY_BG, width=15, height=7, relief="ridge")
foto_label.grid(row=0, column=0, rowspan=3, padx=10, pady=5)

# Nombre
tk.Label(frame, text="Nombre:", bg=FRAME_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w")
nombre_entry = tk.Entry(frame, bg=ENTRY_BG)
nombre_entry.grid(row=0, column=2, padx=5, pady=5)

# Raza
tk.Label(frame, text="Raza:", bg=FRAME_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="w")
raza_entry = tk.Entry(frame, bg=ENTRY_BG)
raza_entry.grid(row=1, column=2, padx=5, pady=5)

# Edad
tk.Label(frame, text="Edad:", bg=FRAME_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold")).grid(row=2, column=1, sticky="w")
edad_entry = tk.Entry(frame, bg=ENTRY_BG)
edad_entry.grid(row=2, column=2, padx=5, pady=5)

# Dueño
tk.Label(frame, text="Dueño:", bg=FRAME_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=(10, 0))
dueno_entry = tk.Entry(frame, bg=ENTRY_BG, width=40)
dueno_entry.grid(row=3, column=1, columnspan=2, pady=(10, 0), padx=5)

# Médico Veterinario
tk.Label(frame, text="Méd. Veterinario:", bg=FRAME_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", pady=5)
vet_entry = tk.Entry(frame, bg=ENTRY_BG, width=40)
vet_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

# Ejecutar la aplicación
vetery.mainloop()

