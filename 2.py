import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

ventana = tk.Tk()
ventana.geometry("1050x700")
ventana.title("Registro de Alumnos")
ventana.resizable(False, False)
ventana.configure(bg="#1d65a1")

tk.Label(ventana, text="Registro de Alumnos", font=("Arial", 15, "bold")).place(x=400, y=10)

def actualizar_fecha():
    hoy = datetime.now().strftime("%d/%m/%Y")
    fecha_label.config(text=hoy)
    ventana.after(60000, actualizar_fecha)

def obtener_direcciones():
    try:
        cn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="alumnos")
        cursor = cn.cursor()
        cursor.execute("SELECT id_direccion, Nombre_direccion FROM direccion")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()
        return {nombre: id_ for id_, nombre in resultado}
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las direcciones:\n{e}")
        return {}

def obtener_carreras_por_direccion(Nombre_direccion):
    try:
        id_direccion = direccion_map.get(Nombre_direccion)
        if id_direccion is None:
            return []
        cn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="alumnos")
        cursor = cn.cursor()
        cursor.execute("SELECT Nombre_carrera FROM carreras WHERE id_direccion = %s", (id_direccion,))
        carreras = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        cn.close()
        return carreras
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las carreras:\n{e}")
        return []

def limpiar_formulario():
    Matricula.delete(0, tk.END)
    Nombre.delete(0, tk.END)
    Apellidos.delete(0, tk.END)
    Fecha_Nacimiento.delete(0, tk.END)
    id_direccion.set("")
    Carrera.set("")
    sexo_var.set("Masculino")

def cargar_alumnos():
    try:
        cn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="alumnos")
        cursor = cn.cursor()
        cursor.execute("""
            SELECT a.Matricula, a.Nombre, a.Apellidos, a.Sexo, d.Nombre_direccion, a.Carrera
            FROM alumnosregistrados a
            JOIN direccion d ON a.id_direccion = d.id_direccion
        """)
        registros = cursor.fetchall()
        cursor.close()
        cn.close()

        tabla.delete(*tabla.get_children())

        for matricula, nombre, apellidos, sexo, direccion, carrera in registros:
            nombre_completo = f"{nombre} {apellidos}"
            tabla.insert("", "end", values=(matricula, nombre_completo, sexo, direccion, carrera))

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los alumnos:\n{e}")

sexo_var = tk.StringVar()
sexo_var.set("Masculino")

def seleccionar_alumno(event):
    item = tabla.focus()
    if item:
        datos = tabla.item(item)["values"]
        Matricula.delete(0, tk.END)
        Matricula.insert(0, datos[0])
        Nombre.delete(0, tk.END)
        nombre_parts = datos[1].split()
        Nombre.insert(0, nombre_parts[0])
        Apellidos.delete(0, tk.END)
        Apellidos.insert(0, " ".join(nombre_parts[1:]))
        sexo_var.set(datos[2])
        id_direccion.set(datos[3])
        Carrera.set(datos[4])

def editar_alumno():
    try:
        cn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="alumnos")
        cursor = cn.cursor()
        direccion_id = direccion_map.get(id_direccion.get())
        sql = """UPDATE alumnosregistrados SET Nombre=%s, Apellidos=%s, Fecha_Nacimiento=%s,
                 id_direccion=%s, Carrera=%s, Sexo=%s WHERE Matricula=%s"""
        datos = (Nombre.get(), Apellidos.get(), Fecha_Nacimiento.get(), direccion_id, Carrera.get(), sexo_var.get(), Matricula.get())
        cursor.execute(sql, datos)
        cn.commit()
        cursor.close()
        cn.close()
        messagebox.showinfo("Éxito", "Alumno actualizado correctamente.")
        limpiar_formulario()
        cargar_alumnos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo editar el alumno:\n{e}")

def eliminar_alumno():
    seleccion = tabla.focus()
    if seleccion:
        matricula = tabla.item(seleccion)["values"][0]
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar al alumno con matrícula {matricula}?")
        if confirmacion:
            try:
                cn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="alumnos")
                cursor = cn.cursor()
                cursor.execute("DELETE FROM alumnosregistrados WHERE Matricula = %s", (matricula,))
                cn.commit()
                cursor.close()
                cn.close()
                messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
                cargar_alumnos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el alumno:\n{e}")

def agregar_alumno():
    try:
        cn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="alumnos")
        cursor = cn.cursor()

        cursor.execute("SELECT COUNT(*) FROM alumnosregistrados WHERE Matricula=%s", (Matricula.get(),))
        existe = cursor.fetchone()[0]
        if existe > 0:
            messagebox.showerror("Error", f"La matrícula {Matricula.get()} ya está registrada, pruebe otro")
            cursor.close()
            cn.close()
            return

        nombre_dir = id_direccion.get()
        direccion_id = direccion_map.get(nombre_dir)

        if direccion_id is None:
            messagebox.showerror("Error", "Debes seleccionar una dirección válida")
            cursor.close()
            cn.close()
            return

        if not Carrera.get():
            messagebox.showerror("Error", "Debes seleccionar una carrera")
            cursor.close()
            cn.close()
            return

        sql = "INSERT INTO alumnosregistrados (Matricula, Nombre, Apellidos, Fecha_Nacimiento, id_direccion, Carrera, Sexo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        datos = (Matricula.get(), Nombre.get(), Apellidos.get(), Fecha_Nacimiento.get(), direccion_id, Carrera.get(), sexo_var.get())
        cursor.execute(sql, datos)
        cn.commit()
        cursor.close()
        cn.close()
        messagebox.showinfo("Éxito", "Alumno agregado correctamente.")
        limpiar_formulario()
        cargar_alumnos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el alumno:\n{e}")

tk.Label(ventana, text="Matrícula:").place(x=80, y=80)
Matricula = tk.Entry(ventana)
Matricula.place(x=160, y=80)

tk.Label(ventana, text="Nombre:").place(x=80, y=120)
Nombre = tk.Entry(ventana)
Nombre.place(x=170, y=120)

tk.Label(ventana, text="Fecha de Nacimiento:").place(x=80, y=160)
Fecha_Nacimiento = tk.Entry(ventana)
Fecha_Nacimiento.place(x=230, y=160)

tk.Label(ventana, text="Apellidos:").place(x=500, y=120)
Apellidos = tk.Entry(ventana)
Apellidos.place(x=600, y=120)

tk.Label(ventana, text="Dirección de carrera:").place(x=80, y=200)
direccion_map = obtener_direcciones()
id_direccion = ttk.Combobox(ventana, values=list(direccion_map.keys()), state="readonly")
id_direccion.place(x=220, y=200)
fecha_label = tk.Label(ventana, font=("Arial", 12), bg="#ffffff", fg="#333333")
fecha_label.place(x=750, y=10)
actualizar_fecha()

tk.Label(ventana, text="Carrera:").place(x=500, y=200)
Carrera = ttk.Combobox(ventana, state="readonly")
Carrera.place(x=600, y=200)

def actualizar_carreras(event):
    seleccion = id_direccion.get()
    opciones = obtener_carreras_por_direccion(seleccion)
    Carrera["values"] = opciones
    Carrera.set("")

id_direccion.bind("<<ComboboxSelected>>", actualizar_carreras)

tk.Label(ventana, text="Sexo:").place(x=500, y=160)
marco_sexo = tk.Frame(ventana)
marco_sexo.place(x=600, y=160)

tk.Radiobutton(marco_sexo, text="Masculino", variable=sexo_var, value="Masculino").pack(side="left", padx=10)
tk.Radiobutton(marco_sexo, text="Femenino", variable=sexo_var, value="Femenino").pack(side="left", padx=10)

tk.Button(ventana, text="Agregar Alumno", font=("Arial", 12), command=agregar_alumno, bg="#B345B3", fg="black").place(x=300, y=280)
tk.Button(ventana, text="Editar Alumno", font=("Arial", 12), command=editar_alumno, bg="#37c51e", fg="black").place(x=450, y=280)
tk.Button(ventana, text="Eliminar Alumno", font=("Arial", 12), command=eliminar_alumno, bg="#f8d7da", fg="black").place(x=600, y=280)

tabla_frame = tk.Frame(ventana)
tabla_frame.place(x=20, y=400)

tabla = ttk.Treeview(tabla_frame, columns=("Matricula", "NombreCompleto", "Sexo", "Direccion", "Carrera"), show="headings")

for col, texto in zip(("Matricula", "NombreCompleto", "Sexo", "Direccion", "Carrera"),
                      ("Matrícula", "Nombre Completo", "Sexo", "Dirección", "Carrera")):
    tabla.heading(col, text=texto)
    tabla.column(col, width=200)

tabla.pack()
tabla.bind("<Double-1>", seleccionar_alumno)

cargar_alumnos()
ventana.mainloop()