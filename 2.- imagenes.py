import tkinter as tk
import mysql.connector
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from fpdf import FPDF
import os

# Variable global para guardar la ruta de la imagen seleccionada
ruta_imagen = None

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
        imagen.thumbnail((200, 200))
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk
        ruta_imagen = archivo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
        ruta_imagen = None

def almacenar_imagen():
    if not ruta_imagen:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna imagen")
        return
    conect = mysql.connector.connect(host="localhost", user="root", password="", database="alumnos")
    cursor = conect.cursor()
    try:
        with open(ruta_imagen, "rb") as file:
            image_bytes = file.read()
        cursor.execute("INSERT INTO imagen (imagen) VALUES (%s)", (image_bytes,))
        conect.commit()
        messagebox.showinfo("Éxito", "Imagen guardada correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo guardar la imagen {err}")
    finally:
        cursor.close()
        conect.close()

def convertir_a_pdf_visual():
    if not ruta_imagen:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna imagen")
        return
    try:
        # Crear PDF temporal
        pdf = FPDF()
        pdf.add_page()
        img = Image.open(ruta_imagen)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            temp_path = ruta_imagen + "_temp.jpg"
            img.save(temp_path)
            img_path = temp_path
        else:
            img_path = ruta_imagen
        pdf.image(img_path, x=10, y=10, w=pdf.w - 20)
        temp_pdf = "temp_vista_previa.pdf"
        pdf.output(temp_pdf)

        # Ventana de vista previa
        vista = Toplevel(imagenes)
        vista.title("Vista previa PDF")
        vista.geometry("600x800")
        vista.config(bg="white")

        # Mostrar la imagen en la vista previa (no PDF directo, pero sí la imagen que irá al PDF)
        img_preview = Image.open(img_path)
        img_preview.thumbnail((500, 700))
        img_preview_tk = ImageTk.PhotoImage(img_preview)
        lbl_img = tk.Label(vista, image=img_preview_tk, bg="white")
        lbl_img.image = img_preview_tk
        lbl_img.pack(pady=20)

        def guardar_pdf():
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Guardar como PDF")
            if save_path:
                pdf.output(save_path)
                messagebox.showinfo("Éxito", f"Imagen convertida a PDF correctamente:\n{save_path}")
                vista.destroy()
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

        btn_guardar = tk.Button(vista, text="Guardar PDF", font=("arial", 14, "bold"), bg="green", fg="white", command=guardar_pdf)
        btn_guardar.pack(pady=10)

        def cerrar_vista():
            vista.destroy()
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

        btn_cerrar = tk.Button(vista, text="Cancelar", font=("arial", 14, "bold"), bg="red", fg="white", command=cerrar_vista)
        btn_cerrar.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo convertir la imagen a PDF:\n{e}")

# Ventana principal
imagenes = tk.Tk()
imagenes.title("Imágenes en Base de Datos")
imagenes.geometry("900x600")
imagenes.config(bg="red")
imagenes.resizable(0, 0)

im1 = tk.Label(imagenes, text="Imágenes", font=("arial", 20, "bold"), bg="red", fg="black")
im1.place(x=370, y=20)

etiqueta_imagen = tk.Label(imagenes, bg="white")
etiqueta_imagen.place(x=350, y=100, width=200, height=200)

buscar = tk.Button(imagenes, text="Buscar Imágen", font=("arial", 15, "bold"), bg="white", fg="black", command=seleccionar_imagen)
buscar.place(x=350, y=400)

guardar = tk.Button(imagenes, text="Guardar Imágen", font=("arial", 15, "bold"), bg="blue", fg="white", command=almacenar_imagen)
guardar.place(x=345, y=460)

pdf_btn = tk.Button(imagenes, text="PDF", font=("arial", 15, "bold"), bg="green", fg="white", command=convertir_a_pdf_visual)
pdf_btn.place(x=570, y=460)

salir = tk.Button(imagenes, text="Salir", font=("arial", 15, "bold"), bg="red", fg="white", command=imagenes.destroy)
salir.place(x=700, y=520)

imagenes.mainloop()