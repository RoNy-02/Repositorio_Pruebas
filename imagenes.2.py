import tkinter as tk
import mysql.connector
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Variable global para guardar la ruta de la imagen seleccionada
ruta_imagen = None

#Importar imagenes

def seleccionar_imagen():
    global ruta_imagen
    archivo = filedialog.askopenfilename(title="Seleccionar Imágen", filetypes=[("Archivos de Imagen", "*.jpg;*.jpeg;*.png")])
    if not archivo:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna imagen.")
        ruta_imagen = None
        etiqueta_imagen.config(image='')
        return
    try:
        imagen = Image.open(archivo)
        imagen.thumbnail((200, 200))  # Redimensionar la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk  # Mantener una referencia a la imagen
        ruta_imagen = archivo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
        ruta_imagen = None

def almacenar_imagen():
    if not ruta_imagen:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguns imsgen")
        return
    conect=mysql.connector.connect(host="localhost", user="root", password="", database="actividad2")
    cursor=conect.cursor()
    try:
        with open(ruta_imagen, "rb") as file:
            image_bytes=file.read()
        cursor.execute("INSERT INTO act2 (imagen) VALUES (%s)", (image_bytes,))
        conect.commit()
        messagebox.showinfo("Éxito", "Imagen guardada correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo guardar la imagen {err}")
    finally:
        cursor.close()
        conect.close()

def crear_pdf():
    from fpdf import FPDF

    pdf=FPDF(orientation="P", unit="mm", format="A4")

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, align="C", txt="Saludos soy un PeDeeFee", border="B", ln=100)
    pdf.image(ruta_imagen, 5, 30, 100, 100)
    pdf.output("TAREA.pdf")

#Ventana
imagenes=tk.Tk()
imagenes.title("Imágenes en Base de Datos")
imagenes.geometry("900x600")
imagenes.config(bg="lightblue")
imagenes.resizable(0, 0)

#Etiqueta de título
im1=tk.Label(imagenes, text="Imágenes", font=("arial", 20, "bold"), bg="lightblue", fg="black")
im1.place(x=370, y=20)

etiqueta_imagen=tk.Label(imagenes, bg="lightblue")
etiqueta_imagen.place(x=350, y=100, width=200, height=200)

#Botón para buscar
buscar=tk.Button(imagenes, text="Buscar Imágen", font=("arial", 15, "bold"), bg="yellow", fg="black", command=seleccionar_imagen)
buscar.place(x=350, y=400)

#Botón para guardar
guardar=tk.Button(imagenes, text="Guardar Imágen", font=("arial", 15, "bold"), bg="blue", fg="white", command=almacenar_imagen)
guardar.place(x=345, y=460)

crear_pdf1=tk.Button(imagenes, text="Crear PDF",  command=crear_pdf)
crear_pdf1.place(x=345, y=520)

#Botón para salir
salir=tk.Button(imagenes, text="Salir", font=("arial", 15, "bold"), bg="red", fg="white", command=imagenes.destroy)
salir.place(x=700, y=520)

imagenes.mainloop()