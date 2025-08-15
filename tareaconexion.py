import tkinter as tk
import mysql.connector
from tkinter import messagebox
import datetime
from tkinter import ttk

def conectar():
    conec=mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
    bases=conec.cursor()
    bases.execute("show databases")
    for base in bases:
        print(base)
    conec.close()

def agregaralumno():
    cn=mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
    cursor=cn.cursor()
    sql="INSERT INTO Alumnos_Regiatrados (Matricula, Nombre, Apellidos, Sexo, Direccion, Carrera) VALUES (%s, %s, %s, %s, %s, %s)"
    datos=(int(entrada_matricula.get()), entrada_nombre.get(), entrada_apellidos.get(), sexo_var.get(), entrada_direccion.get(), carrera_var.get())
    cursor.execute(sql, datos)
    cn.commit()
    cn.close()

ventana=tk.Tk()
ventana.title("Alumnos")
ventana.geometry("1200x800")
ventana.config(bg="lightblue")

titulo=tk.Label(ventana, text="Registro de Alumnos", font=("arial", 25, "bold"), fg="black", bg="lightblue")
titulo.place(x=350, y=10)

tiempo=datetime.datetime.now()
tiempo=tiempo.strftime("%d/%m/%Y")

fecha=tk.Label(ventana, text="Fecha:"+tiempo, font=("arial", 15, "bold"), fg="black", bg="lightblue")
fecha.place(x=1000, y=15)

matricula=tk.Label(ventana, text="Matricula:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
matricula.place(x=50, y=100)

entrada_matricula=tk.Entry(ventana)
entrada_matricula.place(x=150, y=105)

nombre=tk.Label(ventana, text="Nombre(s):", font=("arial", 15, "bold"), fg="black", bg="lightblue")
nombre.place(x=50, y=140)

entrada_nombre=tk.Entry(ventana)
entrada_nombre.place(x=160, y=145)

apellidos=tk.Label(ventana, text="Apellidos: ", font=("arial", 15, "bold"), fg="black", bg="lightblue")
apellidos.place(x=340, y=140)

entrada_apellidos=tk.Entry(ventana)
entrada_apellidos.place(x=438, y=145)

fechanac=tk.Label(ventana, text="Fecha de Nacimiento:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
fechanac.place(x=50, y=180)

entrada_fechanac=tk.Entry(ventana)
entrada_fechanac.place(x=260, y=185)

sexo=tk.Label(ventana, text="Sexo:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
sexo.place(x=430, y=180)

sexo_var = tk.StringVar(value="")  # Ningún valor seleccionado

radio_Mujer=tk.Radiobutton(ventana, text="Mujer", value="Mujer", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="lightblue")
radio_Mujer.place(x=500, y=180)

radio_Hombre=tk.Radiobutton(ventana, text="Hombre", value="Hombre", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="lightblue")
radio_Hombre.place(x=600, y=180)

direcciones=["Ciencias Económico-Administrativas", "Ciencias Naturales e Ingeniería", "Tecnologías de la Información", "Ciencias Exactas", "Ciencias de la Salud"]

direccion=tk.Label(ventana, text="Dirección:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
direccion.place(x=50, y=220)

entrada_direccion=tk.Entry(ventana, width=50)
entrada_direccion.place(x=150, y=225)

carreraseco=["Maestría en Innovación y Negocios", "Licenciatura en Administración", "Licenciatura en Contaduría", "Licenciatura en Negocios y Mercadoctenia"]

carrerasnat=["Maestría en Sistemas de Gestión Ambiental", "Licenciatura en Ingeniería en Mantenimiento Industrial", "Licenciatura en Ingenieía Civil", "Licenciatura en Ingeniería en Manejo de Recursos Naturales"]

carrerasti=["Desarrollo de Software Multiplataforma", "Infraestructura de Redes Digitales", "Automatización"]

carrerasexac=["Licenciatura en Ingeniería Mecánica", "Licenciatura en Ingeniería Industrial", "Licenciatura en Ingeniería en Diseño Textil y Moda"]

carrerassalud=["Licenciatura en Terapia Física", "Licenciatura en Enfermería", "Licenciatura en Médico Cirujano y Partero"]

carrera=tk.Label(ventana, text="Carrera:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
carrera.place(x=480, y=220)

entrada_carrera=tk.Entry(ventana, width=50)
entrada_carrera.place(x=570, y=225)

# Lista desplegable para Dirección
direccion_var=tk.StringVar()
direccion_combo=ttk.Combobox(ventana, textvariable=direccion_var, values=direcciones, state="readonly", width=47)
direccion_combo.place(x=150, y=225)
direccion_combo.set("Selecciona una dirección")

# Diccionario para carreras por dirección
carreras_dict = {
    "Ciencias Económico-Administrativas": carreraseco,
    "Ciencias Naturales e Ingeniería": carrerasnat,
    "Tecnologías de la Información": carrerasti,
    "Ciencias Exactas": carrerasexac,
    "Ciencias de la Salud": carrerassalud
}

# Lista desplegable para Carrera
carrera_var=tk.StringVar()
carrera_combo=ttk.Combobox(ventana, textvariable=carrera_var, state="readonly", width=47)
carrera_combo.place(x=570, y=225)
carrera_combo.set("Selecciona una carrera")

def actualizar_carreras(event):
    seleccion=direccion_var.get()
    carreras=carreras_dict.get(seleccion, [])
    carrera_combo['values']=carreras
    carrera_combo.set("Selecciona una carrera")

direccion_combo.bind('<<ComboboxSelected>>', actualizar_carreras)

btnGuardar=tk.Button(ventana, text="Guardar", font=("arial", 20, "bold"), fg="white", bg="blue", command=agregaralumno)
btnGuardar.place(x=500, y=300)

ventana.mainloop()