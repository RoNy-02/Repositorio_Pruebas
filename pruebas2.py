import tkinter as tk
import mysql.connector
from tkinter import messagebox
import datetime
from tkinter import ttk

#Función para validar campos
def singuardar():
    if not entrada_matricula.get() or not entrada_nombre.get()  or not direccion_var.get() or not carrera_var.get() or not sexo_var.get():
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    else:
        try:
            agregaralumno()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error de base de datos", str(e))

#Función para conectar a la base de datos
def conectar():
    try:
        conec = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
        bases = conec.cursor()
        bases.execute("show databases")
        for base in bases:
            print(base)
        conec.close()
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))

#Función para agregar datos a la base de datos
def agregaralumno():
    cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
    cursor = cn.cursor()
    sql = "INSERT INTO Alumnos_Registrados (Matricula, Nombre_Completo, Sexo, Direccion, Carrera) VALUES (%s, %s, %s, %s, %s)"
    datos = (int(entrada_matricula.get()), entrada_nombre.get(), sexo_var.get(), direccion_var.get(), carrera_var.get())
    cursor.execute(sql, datos)
    cn.commit()
    cn.close()
    messagebox.showinfo("Éxito", "Alumno registrado correctamente")
    mostrar_datos()

# Limpiar campos luego de guardar
def limpiar_campos():
    entrada_matricula.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_fechanac.delete(0, tk.END)
    direccion_combo.set("Selecciona una dirección")
    carrera_combo.set("Selecciona una carrera")
    sexo_var.set("")

# Funcionar para mostrar datos en el frame
def mostrar_datos():
    for row in tree.get_children():
        tree.delete(row)
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
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
tiempo = datetime.datetime.now()
tiempo = tiempo.strftime("%d/%m/%Y")

# Etiquetas y entradas
fecha = tk.Label(ventana, text="Fecha:" + tiempo, font=("arial", 15, "bold"), fg="black", bg="lightblue")
fecha.place(x=1000, y=15)

matricula = tk.Label(ventana, text="Matricula:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
matricula.place(x=50, y=100)
entrada_matricula = tk.Entry(ventana)
entrada_matricula.place(x=150, y=105)

nombre = tk.Label(ventana, text="Nombre Completo:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
nombre.place(x=50, y=140)
entrada_nombre = tk.Entry(ventana, width=50)
entrada_nombre.place(x=250, y=145)

fechanac = tk.Label(ventana, text="Fecha de Nacimiento:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
fechanac.place(x=50, y=180)
entrada_fechanac = tk.Entry(ventana)
entrada_fechanac.place(x=260, y=185)

sexo = tk.Label(ventana, text="Sexo:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
sexo.place(x=430, y=180)
sexo_var = tk.StringVar(value="")
radio_Mujer = tk.Radiobutton(ventana, text="Mujer", value="Mujer", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="lightblue")
radio_Mujer.place(x=500, y=180)
radio_Hombre = tk.Radiobutton(ventana, text="Hombre", value="Hombre", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="lightblue")
radio_Hombre.place(x=600, y=180)

# Lista de direcciones y carreras
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

# Dirección
direccion = tk.Label(ventana, text="Dirección:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
direccion.place(x=50, y=220)
direccion_var = tk.StringVar()
direccion_combo = ttk.Combobox(ventana, textvariable=direccion_var, values=direcciones, state="readonly", width=47)
direccion_combo.place(x=150, y=225)
direccion_combo.set("Selecciona una dirección")

# Carrera
carrera = tk.Label(ventana, text="Carrera:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
carrera.place(x=480, y=220)
carrera_var = tk.StringVar()
carrera_combo = ttk.Combobox(ventana, textvariable=carrera_var, state="readonly", width=47)
carrera_combo.place(x=570, y=225)
carrera_combo.set("Selecciona una carrera")

def actualizar_carreras(event):
    seleccion = direccion_var.get()
    carreras = carreras_dict.get(seleccion, [])
    carrera_combo['values'] = carreras
    carrera_combo.set("Selecciona una carrera")

direccion_combo.bind('<<ComboboxSelected>>', actualizar_carreras)

# Botón Guardar
btnGuardar = tk.Button(ventana, text="Guardar", font=("arial", 20, "bold"), fg="white", bg="blue", command=singuardar, width=10, height=2)
btnGuardar.place(x=500, y=270)

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