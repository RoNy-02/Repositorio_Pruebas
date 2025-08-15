import tkinter as tk
import mysql.connector
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
from fpdf import FPDF
import os
import datetime

ventana = tk.Tk()
ventana.title("Registro De Alumnos")
ventana.geometry("1300x700")
ventana.configure(bg="white")

# Variable global para la ruta de la imagen seleccionada
ruta_imagen = None

def seleccionar_imagen():
    global ruta_imagen
    archivo = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de Imagen", "*.jpg;*.jpeg;*.png")])
    if not archivo:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna imagen.")
        ruta_imagen = None
        etiqueta_imagen.config(image='')
        etiqueta_imagen.image = None
        return
    ruta_imagen = archivo
    # Mostrar vista previa en la interfaz
    try:
        imagen = Image.open(archivo)
        imagen.thumbnail((120, 120))
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk  # Mantener referencia
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")
        etiqueta_imagen.config(imagen='')
        etiqueta_imagen.image = None
    messagebox.showinfo("Imagen seleccionada", f"Imagen seleccionada correctamente:\n{archivo}")

def guardar_imagen_bd(matricula):
    if not ruta_imagen:
        return
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
        with open(ruta_imagen, "rb") as file:
            image_bytes = file.read()
        # Intenta actualizar si ya existe, si no, inserta
        cursor.execute("SELECT COUNT(*) FROM imagen WHERE matricula=%s", (matricula,))
        existe = cursor.fetchone()[0]
        if existe:
            cursor.execute("UPDATE imagen SET imagen=%s WHERE matricula=%s", (image_bytes, matricula))
        else:
            cursor.execute("INSERT INTO imagen (matricula, imagen) VALUES (%s, %s)", (matricula, image_bytes))
        cn.commit()
        cursor.close()
        cn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la imagen en la base de datos:\n{e}")

# ...existing code...

def exportar_pdf_alumno_seleccionado(matricula):
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
        cursor.execute("""
            SELECT a.Matricula, a.Nombre, a.Apellidos, a.Sexo, a.Direccion, a.Carrera, a.Fecha_Nacimiento, i.imagen
            FROM alumnosregistrados a
            LEFT JOIN imagen i ON a.Matricula = i.matricula
            WHERE a.Matricula = %s
        """, (matricula,))
        row = cursor.fetchone()
        cursor.close()
        cn.close()

        if not row:
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Datos del Alumno", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Matricula: {row[0]}", ln=True)
        pdf.cell(0, 10, f"Nombre: {row[1]}", ln=True)
        pdf.cell(0, 10, f"Apellidos: {row[2]}", ln=True)
        pdf.cell(0, 10, f"Sexo: {row[3]}", ln=True)
        pdf.cell(0, 10, f"Direccion: {row[4]}", ln=True)
        pdf.cell(0, 10, f"Carrera: {row[5]}", ln=True)
        pdf.cell(0, 10, f"Fecha de Nacimiento: {row[6]}", ln=True)
        if row[7]:
            temp_img = f"temp_{row[0]}.jpg"
            with open(temp_img, "wb") as img_file:
                img_file.write(row[7])
            pdf.image(temp_img, x=150, y=60, w=50,h=50)
            os.remove(temp_img)
        # Guardar automáticamente en la carpeta BASE DE DATOS-PYTHON
        carpeta = os.path.dirname(os.path.abspath(__file__))
        nombre_pdf = os.path.join(carpeta, f"Alumno_{row[0]}.pdf")
        pdf.output(nombre_pdf)
        # Si quieres mostrar un mensaje, descomenta la siguiente línea:
        # messagebox.showinfo("PDF", f"PDF guardado automáticamente en:\n{nombre_pdf}")
    except Exception:
        pass

# ...existing code...

def singuardar():
    if not entry_matricula.get() or not entry_nombre.get() or not entry_apellidos.get() or not direccion_var.get() or not carrera_var.get() or not sexo_var.get() or not entry_fecha.get():
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    else:
        try:
            agregaralumno()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error de base de datos", str(e))

def conectar():
    try:
        conec = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        bases = conec.cursor()
        bases.execute("show databases")
        for base in bases:
            print(base)
        conec.close()
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))

def agregaralumno():
    global ruta_imagen
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
        # Verificar si la matrícula ya existe
        cursor.execute("SELECT COUNT(*) FROM alumnosregistrados WHERE Matricula = %s", (int(entry_matricula.get()),))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "La matrícula ya existe. Usa otra matrícula.")
            cursor.close()
            cn.close()
            return
        sql = "INSERT INTO alumnosregistrados (Matricula, Nombre, Apellidos, Sexo, Direccion, Carrera, Fecha_Nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        datos = (
            int(entry_matricula.get()),
            entry_nombre.get(),
            entry_apellidos.get(),
            sexo_var.get(),
            direccion_var.get(),
            carrera_var.get(),
            entry_fecha.get()
        )
        cursor.execute(sql, datos)
        cn.commit()
        cursor.close()
        cn.close()
        guardar_imagen_bd(datos[0])
        messagebox.showinfo("Éxito", "Alumno registrado correctamente.")
        mostrar_datos()
        exportar_pdf_alumno_seleccionado(datos[0])
        ruta_imagen = None
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el alumno.\n{e}")

def limpiar_campos():
    entry_matricula.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellidos.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    direccion_combo.set("Selecciona una dirección")
    carrera_combo.set("Selecciona una carrera")
    sexo_var.set("")

def mostrar_datos():
    for row in tree.get_children():
        tree.delete(row)
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
        cursor.execute("SELECT Matricula, Nombre, Apellidos, Sexo, Direccion, Carrera, Fecha_Nacimiento FROM alumnosregistrados")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cn.close()
    except Exception as e:
        messagebox.showerror("Error al cargar datos", str(e))

def editar_alumno():
    seleccion = tree.focus()
    if seleccion:
        datos = tree.item(seleccion)["values"]
        matricula = datos[0]
        try:
            cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
            cursor = cn.cursor()
            sql = """UPDATE alumnosregistrados SET 
                        Nombre=%s, Apellidos=%s, Sexo=%s, Direccion=%s, Carrera=%s, Fecha_Nacimiento=%s 
                     WHERE Matricula=%s"""
            valores = (
                entry_nombre.get(),
                entry_apellidos.get(),
                sexo_var.get(),
                direccion_var.get(),
                carrera_var.get(),
                entry_fecha.get(),
                matricula
            )
            cursor.execute(sql, valores)
            cn.commit()
            cursor.close()
            cn.close()
            messagebox.showinfo("Éxito", "Alumno editado correctamente.")
            mostrar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar el alumno:\n{e}")

def eliminar_alumno():
    seleccion = tree.focus()
    if seleccion:
        datos = tree.item(seleccion)["values"]
        matricula = datos[0]
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar al alumno con matrícula {matricula}?")
        if confirmacion:
            try:
                cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
                cursor = cn.cursor()
                cursor.execute("DELETE FROM alumnosregistrados WHERE Matricula = %s", (matricula,))
                cn.commit()
                cursor.close()
                cn.close()
                messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
                mostrar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el alumno:\n{e}")

def Salir():
    exit()

tiempo = datetime.datetime.now().strftime("%d/%m/%Y")
fecha = tk.Label(ventana, text="Fecha: " + tiempo, font=("arial", 15, "bold"), fg="black", bg="white")
fecha.place(x=800, y=15)

frame_registros = tk.Frame(ventana, bg="#DBDBDB", bd=2, relief="groove")
frame_registros.place(x=20, y=60, width=1250, height=500)

tk.Label(frame_registros, text="REGISTRO DE ALUMNOS", font=("arial", 20, "bold"), bg="#DBDBDB", fg="black").place(x=10, y=10)

tk.Label(frame_registros, text="Matricula", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=60)
entry_matricula = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="white")
entry_matricula.place(x=150, y=60, height=30, width=130)

tk.Label(frame_registros, text="Nombre", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=110)
entry_nombre = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="white")
entry_nombre.place(x=150, y=110, height=30, width=130)

tk.Label(frame_registros, text="Apellidos", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=300, y=110)
entry_apellidos = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="white", fg="black")
entry_apellidos.place(x=400, y=110, height=30, width=230)

tk.Label(frame_registros, text="Fecha de Nacimiento", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=160)
entry_fecha = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="white")
entry_fecha.insert(0, "DD/MM/AAAA")
entry_fecha.place(x=210, y=160, height=30, width=130)

tk.Label(frame_registros, text="Sexo", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=210)
sexo_var = tk.StringVar(value="")
radio_masculino = tk.Radiobutton(frame_registros, text="Masculino", value="Masculino", variable=sexo_var, font=("arial", 13), bg="#DBDBDB")
radio_femenino = tk.Radiobutton(frame_registros, text="Femenino", value="Femenino", variable=sexo_var, font=("arial", 13), bg="#DBDBDB")
radio_masculino.place(x=150, y=210)
radio_femenino.place(x=250, y=210)

tk.Label(frame_registros, text="Dirección", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=260)
direcciones = [
    "Ciencias Económico-Administrativas",
    "Ciencias Naturales e Ingeniería",
    "Tecnologías de la Información",
    "Ciencias Exactas",
    "Ciencias de la Salud"
]
direccion_var = tk.StringVar()
direccion_combo = ttk.Combobox(frame_registros, textvariable=direccion_var, values=direcciones, state="readonly", width=30)
direccion_combo.place(x=150, y=265)
direccion_combo.set("Selecciona una dirección")

carreraseco = [
    "Maestría en Innovación y Negocios",
    "Licenciatura en Administración",
    "Licenciatura en Contaduría",
    "Licenciatura en Negocios y Mercadoctenia"
]
carrerasnat = [
    "Maestría en Sistemas de Gestión Ambiental",
    "Licenciatura en Ingeniería en Mantenimiento Industrial",
    "Licenciatura en Ingenieía Civil",
    "Licenciatura en Ingeniería en Manejo de Recursos Naturales"
]
carrerasti = [
    "Desarrollo de Software Multiplataforma",
    "Infraestructura de Redes Digitales",
    "Automatización"
]
carrerasexac = [
    "Licenciatura en Ingeniería Mecánica",
    "Licenciatura en Ingeniería Industrial",
    "Licenciatura en Ingeniería en Diseño Textil y Moda"
]
carrerassalud = [
    "Licenciatura en Terapia Física",
    "Licenciatura en Enfermería",
    "Licenciatura en Médico Cirujano y Partero"
]

carreras_dict = {
    "Ciencias Económico-Administrativas": carreraseco,
    "Ciencias Naturales e Ingeniería": carrerasnat,
    "Tecnologías de la Información": carrerasti,
    "Ciencias Exactas": carrerasexac,
    "Ciencias de la Salud": carrerassalud
}

tk.Label(frame_registros, text="Carrera", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=400, y=260)
carrera_var = tk.StringVar()
carrera_combo = ttk.Combobox(frame_registros, textvariable=carrera_var, state="readonly", width=30)
carrera_combo.place(x=500, y=265)
carrera_combo.set("Selecciona una carrera")

def actualizar_carreras(event):
    seleccion = direccion_var.get()
    carreras = carreras_dict.get(seleccion, [])
    carrera_combo['values'] = carreras
    carrera_combo.set("Selecciona una carrera")

direccion_combo.bind('<<ComboboxSelected>>', actualizar_carreras)

btnEliminar = tk.Button(frame_registros, text="Eliminar", font=("arial", 15, "italic"), fg="white", bg="#FF0000", command=eliminar_alumno)
btnEliminar.place(x=680, y=40)

# Etiqueta para vista previa de imagen
etiqueta_imagen = tk.Label(frame_registros, bg="white", relief="groove")
etiqueta_imagen.place(x=1050, y=100, width=120, height=120)

# Frame para la imagen y el botón juntos
frame_imagen = tk.Frame(frame_registros, bg="white", relief="flat")
frame_imagen.place(x=1050, y=220, width=120, height=50)

btn_agregar_imagen = tk.Button(
    frame_imagen,
    text="Agregar imagen",
    font=("arial", 10),
    bg="#e0e0e0",
    fg="black",
    command=seleccionar_imagen,
    relief="ridge"
)
btn_agregar_imagen.pack(fill="both", expand=True, padx=5, pady=5)

# Botones separados
btnEditar = tk.Button(frame_registros, text="Editar", font=("arial", 15, "bold"), fg="white", bg="#FF8800", command=editar_alumno)
btnEditar.place(x=800, y=40)

btnGuardar = tk.Button(frame_registros, text="Guardar", font=("arial", 15, "bold"), fg="white", bg="#228B22", command=singuardar)
btnGuardar.place(x=890, y=40)

# Tabla de alumnos
tree_frame = tk.Frame(ventana)
tree_frame.place(x=10, y=370, width=1260, height=300)
columns = ("Matricula", "Nombre", "Apellidos", "Sexo", "Direccion", "Carrera", "Fecha de Nacimiento")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.S, width=180)
tree.pack(fill="both", expand=True)

btn_Salir = tk.Button(ventana, text="Salir", font=("arial", 15, "italic"), bg="#FF0000", fg="black", command=Salir)
btn_Salir.place(x=1020, y=610)

# --- Cargar datos al seleccionar un registro ---
def cargar_datos_en_campos(event):
    seleccion = tree.focus()
    if seleccion:
        datos = tree.item(seleccion)["values"]
        # Asume el orden: Matricula, Nombre, Apellidos, Sexo, Direccion, Carrera, Fecha de Nacimiento
        entry_matricula.delete(0, tk.END)
        entry_matricula.insert(0, datos[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])
        entry_apellidos.delete(0, tk.END)
        entry_apellidos.insert(0, datos[2])
        sexo_var.set(datos[3])
        direccion_combo.set(datos[4])
        carrera_combo.set(datos[5])
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datos[6])
        etiqueta_imagen.config(image='')
        etiqueta_imagen.image = None

tree.bind("<<TreeviewSelect>>", cargar_datos_en_campos)

mostrar_datos()
ventana.mainloop()