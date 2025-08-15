import tkinter as tk
import mysql.connector
from tkinter import messagebox
import datetime
from tkinter import ttk

def singuardar():
    if not entry_matricula.get() or not entry_nombre.get() or not direccion_var.get() or not carrera_var.get() or not sexo_var.get():
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    else:
        try:
            agregaralumno()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error de base de datos", str(e))

def agregaralumno():
    cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
    cursor = cn.cursor()
    sql = "INSERT INTO Alumnos_Registrados (Matricula, Nombre_Completo, Sexo, Direccion, Carrera) VALUES (%s, %s, %s, %s, %s)"
    datos = (int(entry_matricula.get()), entry_nombre.get(), sexo_var.get(), direccion_var.get(), carrera_var.get())
    cursor.execute(sql, datos)
    cn.commit()
    cn.close()
    messagebox.showinfo("Éxito", "Alumno registrado correctamente")
    mostrar_datos()

def limpiar_campos():
    entry_matricula.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_fechanac.delete(0, tk.END)
    direccion_combo.set("Selecciona una dirección")
    carrera_combo.set("Selecciona una carrera")
    sexo_var.set("")

def mostrar_datos():
    for row in tree.get_children():
        tree.delete(row)
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
        cursor.execute("SELECT Matricula, Nombre_Completo, Sexo, Direccion, Carrera FROM Alumnos_Registrados")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cn.close()
    except Exception as e:
        messagebox.showerror("Error al cargar datos", str(e))

ventana = tk.Tk()
ventana.title("Alumnos")
ventana.geometry("1200x800")
ventana.config(bg="lightblue")

titulo = tk.Label(ventana, text="Registro de Alumnos", font=("arial", 25, "bold"), fg="black", bg="lightblue")
titulo.place(x=350, y=10)

# Fecha actual
tiempo = datetime.datetime.now().strftime("%d/%m/%Y")
fecha = tk.Label(ventana, text="Fecha:" + tiempo, font=("arial", 15, "bold"), fg="black", bg="lightblue")
fecha.place(x=1000, y=15)

# Frame para agregar datos
frame_registros = tk.Frame(ventana, bg="#DBDBDB", bd=2, relief="groove")
frame_registros.place(x=50, y=60, width=1100, height=250)

tk.Label(frame_registros, text="Matricula", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=20)
entry_matricula = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="grey")
entry_matricula.place(x=150, y=20, height=30, width=130)

tk.Label(frame_registros, text="Nombre Completo", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=70)
entry_nombre = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="grey", width=40)
entry_nombre.place(x=180, y=70, height=30)

tk.Label(frame_registros, text="Fecha de Nacimiento", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=10, y=120)
entry_fechanac = tk.Entry(frame_registros, font=("arial", 15, "italic"), bg="grey")
entry_fechanac.place(x=210, y=120, height=30, width=130)

tk.Label(frame_registros, text="Sexo", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=400, y=20)
sexo_var = tk.StringVar(value="")
radio_Mujer = tk.Radiobutton(frame_registros, text="Mujer", value="Mujer", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="#DBDBDB")
radio_Mujer.place(x=470, y=20)
radio_Hombre = tk.Radiobutton(frame_registros, text="Hombre", value="Hombre", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="#DBDBDB")
radio_Hombre.place(x=570, y=20)

direcciones = ["Ciencias Económico-Administrativas", "Ciencias Naturales e Ingeniería", "Tecnologías de la Información", "Ciencias Exactas", "Ciencias de la Salud"]
carreraseco = ["Maestría en Innovación y Negocios", "Licenciatura en Administración", "Licenciatura en Contaduría", "Licenciatura en Negocios y Mercadotecnia"]
carrerasnat = ["Maestría en Sistemas de Gestión Ambiental", "Licenciatura en Ingeniería en Mantenimiento Industrial", "Licenciatura en Ingeniería Civil", "Licenciatura en Ingeniería en Manejo de Recursos Naturales"]
carrerasti = ["Desarrollo de Software Multiplataforma", "Infraestructura de Redes Digitales", "Automatización"]
carrerasexac = ["Licenciatura en Ingeniería Mecánica", "Licenciatura en Ingeniería Industrial", "Licenciatura en Ingeniería en Diseño Textil y Moda"]
carrerassalud = ["Licenciatura en Terapia Física", "Licenciatura en Enfermería", "Licenciatura en Médico Cirujano y Partero"]

carreras_dict = {
    "Ciencias Económico-Administrativas": carreraseco,
    "Ciencias Naturales e Ingeniería": carrerasnat,
    "Tecnologías de la Información": carrerasti,
    "Ciencias Exactas": carrerasexac,
    "Ciencias de la Salud": carrerassalud
}

tk.Label(frame_registros, text="Dirección", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=400, y=70)
direccion_var = tk.StringVar()
direccion_combo = ttk.Combobox(frame_registros, textvariable=direccion_var, values=direcciones, state="readonly", width=40)
direccion_combo.place(x=500, y=75)
direccion_combo.set("Selecciona una dirección")

tk.Label(frame_registros, text="Carrera", font=("arial", 15, "italic"), bg="#DBDBDB", fg="black").place(x=400, y=120)
carrera_var = tk.StringVar()
carrera_combo = ttk.Combobox(frame_registros, textvariable=carrera_var, state="readonly", width=40)
carrera_combo.place(x=500, y=125)
carrera_combo.set("Selecciona una carrera")

def actualizar_carreras(event):
    seleccion = direccion_var.get()
    carreras = carreras_dict.get(seleccion, [])
    carrera_combo['values'] = carreras
    carrera_combo.set("Selecciona una carrera")

direccion_combo.bind('<<ComboboxSelected>>', actualizar_carreras)

btnGuardar = tk.Button(frame_registros, text="Guardar", font=("arial", 15, "bold"), fg="white", bg="blue", command=singuardar, width=10, height=2)
btnGuardar.place(x=900, y=180)

# Frame para mostrar datos
tree_frame = tk.Frame(ventana)
tree_frame.place(x=50, y=350)
columns = ("Matricula", "Nombre_Completo", "Sexo", "Direccion", "Carrera")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=180)
tree.pack(fill="both", expand=True)

mostrar_datos()
ventana.mainloop()