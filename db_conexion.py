import tkinter as tk
import mysql.connector
from tkinter import messagebox
def conectar():
    cn=mysql.connector.connect(host="localhost",user="root",password="Cora3022",port=3306,database="Escuela")
    bases=cn.cursor()
    bases.execute("show databases")
    for base in bases:
        print(base)
def agregarDatos():
    cn=mysql.connector.connect(host="localhost",user="root",password="Cora3022",port=3306,database="Escuela")
    cursor=cn.cursor()
    sql="insert into Alumnos (Matricula, nombre,Apellidos) values(%s,%s,%s)"
    datos=(121222,"Bernardo","Sostenes Kabrera")
    cursor.execute(sql,datos)
    cursor.close
    cn.commit()
    
def agregarAlumno():
    cn=mysql.connector.connect(host="localhost",user="root",password="Cora3022",port=3306,database="Escuela")
    cursor=cn.cursor()
    sql="insert into Alumnos (Matricula, nombre,Apellidos) values(%s,%s,%s)"
    datos=(int(txtMatricula.get()),txtNombre.get(),txtApellidos.get())
    cursor.execute(sql,datos)
    cursor.close
    cn.commit()
    messagebox.showinfo("Sistema","El alumnos ha sido agregado....")
    

    
ventana=tk.Tk()
ventana.geometry("450x456")
frm_Titulo=tk.Frame(ventana,bg="#5DADE2")
lblTitulo=tk.Label(frm_Titulo,text="Conexiòn a Base de datos",
                   font=("Arial","20","bold"),fg="blue",pady=25,
                   bg="#5DADE2")
lblTitulo.pack()
frm_Titulo.pack(fill=tk.BOTH)
frm_Buttons=tk.Frame(ventana,bg="#9D36F1")
frm_Buttons.pack(fill=tk.BOTH)
btnConectar=tk.Button(frm_Buttons,text="Conectar BD",command=conectar)
btnConectar.pack()
btnAgregar=tk.Button(frm_Buttons,text="Agregar Datos",command=agregarDatos,)
btnAgregar.pack(pady=10)

lblMatricula=tk.Label(frm_Buttons,text="Matricula:")
txtMatricula=tk.Entry(frm_Buttons)
lblMatricula.pack()
txtMatricula.pack()
lblNombre=tk.Label(frm_Buttons,text="Nombre:")
txtNombre=tk.Entry(frm_Buttons)
lblNombre.pack()
txtNombre.pack()
lblApellidos=tk.Label(frm_Buttons,text="Apellidos:")
txtApellidos=tk.Entry(frm_Buttons)
lblApellidos.pack()
txtApellidos.pack()
btnAgregarAlu=tk.Button(frm_Buttons,text="Agregar Alumno",command=agregarAlumno)
btnAgregarAlu.pack(pady=10)
ventana.mainloop()