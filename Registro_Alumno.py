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
    try:
        imagen = Image.open(archivo)
        imagen.thumbnail((120, 120))
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")
        etiqueta_imagen.config(image='')
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

def asignar_calificaciones():
    calif = tk.Toplevel(ventana)
    calif.title("Asignar Calificaciones")
    calif.geometry("600x350")
    calif.config(bg="lightblue")

    materias = [
        "Base de Datos",
        "Desarrollo de Pensamiento y Toma de Decisiones",
        "Inglés 3",
        "Programación Orientada a Objetos",
        "Tópicos de Calidad para el Diseño de Software"
    ]
    entradas = []

    tk.Label(calif, text="Asignar Calificaciones", font=("arial", 18, "bold"), bg="lightblue").pack(pady=10)
    for i, materia in enumerate(materias):
        tk.Label(calif, text=materia + ":", font=("arial", 13), bg="lightblue").place(x=30, y=60 + i*40)
        entrada = tk.Entry(calif)
        entrada.place(x=350, y=60 + i*40)
        entradas.append(entrada)

    resultado = {'calificaciones': None}

    def guardar_calificaciones():
        calificaciones = [e.get() for e in entradas]
        if not all(calificaciones):
            messagebox.showerror("Error", "Todas las calificaciones son obligatorias")
            return
        resultado['calificaciones'] = calificaciones
        calif.destroy()

    btn_guardar = tk.Button(calif, text="Guardar Calificaciones", font=("arial", 13), bg="green", fg="white", command=guardar_calificaciones)
    btn_guardar.place(x=200, y=280)

    calif.grab_set()
    calif.wait_window()
    return resultado['calificaciones']

def guardar_calificaciones_bd(matricula, calificaciones):
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
        sql = "INSERT INTO calificaciones (matricula, bd, dptd, ingles, poo, topicos) VALUES (%s, %s, %s, %s, %s, %s)"
        datos = (int(matricula), float(calificaciones[0]), float(calificaciones[1]), float(calificaciones[2]), float(calificaciones[3]), float(calificaciones[4]))
        cursor.execute(sql, datos)
        cn.commit()
        cursor.close()
        cn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar las calificaciones.\n{e}")

def exportar_pdf_alumno_seleccionado(matricula, calificaciones=None):
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

        # Recuperar calificaciones si no se pasan
        if calificaciones is None:
            cursor.execute("SELECT bd, dptd, ingles, poo, topicos FROM calificaciones WHERE matricula=%s", (matricula,))
            calif_row = cursor.fetchone()
            if calif_row:
                calificaciones = [str(c) for c in calif_row]
            else:
                calificaciones = None

        cursor.close()
        cn.close()

        if not row:
            return

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        # Imagen de fondo
        try:
            pdf.image("Venao.jpg", x=0, y=0, w=pdf.w, h=pdf.h)
        except Exception:
            pass

        # Logo superior
        try:
            pdf.image("Logo2.jpg", x=10, y=8, w=185, h=30)
        except Exception:
            pass

        pdf.ln(30)

        #pdf, elementos y ubicacion de datos y registros
        import locale
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        fecha_actual = datetime.datetime.now()
        dia = fecha_actual.strftime("%d")
        mes = fecha_actual.strftime("%B")
        anio = fecha_actual.strftime("%Y")
        ubicacion = "Zacualtipán de Ángeles Hgo., a "

        pdf.set_font("Arial", size=12)
        texto_ubic = ubicacion
        w_ubic = pdf.get_string_width(texto_ubic)
        w_dia = pdf.get_string_width(dia)
        w_de = pdf.get_string_width(" de ")
        w_mes = pdf.get_string_width(mes)
        w_del = pdf.get_string_width(" del " + anio + ".")
        w_total = w_ubic + w_dia + w_de + w_mes + w_del

        # Calcula la posición para alinear a la derecha
        x_pos = pdf.w - pdf.r_margin - w_total
        pdf.set_xy(x_pos, pdf.get_y())

        pdf.set_font("Arial", size=12)
        pdf.cell(w_ubic, 10, texto_ubic, ln=0)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(w_dia, 10, dia, ln=0)
        pdf.set_font("Arial", size=12)
        pdf.cell(w_de, 10, " de ", ln=0)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(w_mes, 10, mes, ln=0)
        pdf.set_font("Arial", size=12)
        pdf.cell(w_del, 10, f" del {anio}.", ln=1)
        pdf.ln(3)

        # Título
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(0, 10, txt="Datos del Estudiante", ln=1, align='C')
        pdf.ln(2)
        
        # Datos del alumno: campo normal, dato en negritas
        pdf.set_x(70)
        pdf.set_font("Arial", "", 13)
        pdf.cell(60, 10, "Nombre Completo:", ln=0)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, f"{row[1]} {row[2]}", ln=1)

        pdf.set_x(70)
        pdf.set_font("Arial", "", 13)
        pdf.cell(30, 10, "Matrícula:", ln=0)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(40, 10, f"{row[0]}", ln=0)
        pdf.set_font("Arial", "", 13)
        pdf.cell(15, 10, "Sexo:", ln=0)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, f"{row[3]}", ln=1)

        pdf.set_x(70)
        pdf.set_font("Arial", "", 13)
        pdf.cell(30, 10, "Dirección:", ln=0)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, f"{row[4]}", ln=1)

        pdf.set_x(70)
        pdf.set_font("Arial", "", 13)
        pdf.cell(25, 10, "Carrera:", ln=0)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, f"{row[5]}", ln=1)

        pdf.set_x(70)
        pdf.set_font("Arial", "", 13)
        pdf.cell(60, 10, "Fecha de Nacimiento:", ln=0)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, f"{row[6]}", ln=1)
        pdf.ln(10)

        # Tabla de calificaciones y promedio
        if calificaciones:
            materias = [
                "Base de Datos",
                "Desarrollo y Pensamientos y Toma de Decisiones",
                "Inglés 3",
                "Programación Orientada a Objetos",
                "Proyecto Integrador I",
                "Tópicos de Calidad para el Diseño de Software"
            ]
            # Si tienes solo 5 materias, elimina "Proyecto Integrador I" de la lista y ajusta el resto
            if len(calificaciones) == 5:
                materias = materias[:2] + materias[3:]

            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt="Calificaciones", ln=1, align='C')
            pdf.ln(2)

            # Encabezados en negritas, con líneas arriba y abajo
            pdf.set_font("Arial", "B", 12)
            x_inicio = pdf.get_x()
            y_inicio = pdf.get_y()
            pdf.cell(100, 8, "Materia", border="LTR", align="L")
            pdf.cell(40, 8, "Calificación", border="TR", align="C", ln=1)
            pdf.set_font("Arial", size=12)

            suma = 0
            for materia, calificacion in zip(materias, calificaciones):
                try:
                    calif_num = float(calificacion)
                except:
                    calif_num = 0
                suma += calif_num
                pdf.cell(100, 8, materia, border="L", align="L")
                pdf.set_font("Arial", "B", 12)  # Calificación en negritas
                pdf.cell(40, 8, str(calificacion), border="R", align="C", ln=1)
                pdf.set_font("Arial", "", 12)   # Regresa a normal para la siguiente fila

            promedio = suma / len(calificaciones)
            pdf.ln(2)
            # Promedio en negritas y subrayado
            pdf.set_font("Arial", "B", 12)
            pdf.cell(100, 8, "", border=0)
            pdf.cell(40, 8, "", border=0, ln=1)
            pdf.cell(100, 8, "Promedio General:", border=0, align="R")
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 0)
            # Guarda la posición antes de imprimir el número
            x_num = pdf.get_x()
            y_num = pdf.get_y()
            promedio_str = f"{promedio:.2f}"
            pdf.cell(0, 8, promedio_str, border=0, align="L")
            # Calcula el ancho del número y subraya solo el número
            num_width = pdf.get_string_width(promedio_str)
            pdf.line(x_num, y_num + 8, x_num + num_width, y_num + 8)
            pdf.ln(10)
            pdf.set_text_color(0, 0, 0)

        # Foto del alumno
        if row[7]:
            temp_img = f"temp_{row[0]}.jpg"
            with open(temp_img, "wb") as img_file:
                img_file.write(row[7])
            try:
                pdf.image(temp_img, x=15, y=60, w=50, h=50)
            except Exception:
                pass
            os.remove(temp_img)

        # Guardar automáticamente en la carpeta BASE DE DATOS-PYTHON
        carpeta = os.path.dirname(os.path.abspath(__file__))
        nombre_pdf = os.path.join(carpeta, f"Alumno_{row[0]}.pdf")
        pdf.output(nombre_pdf)
    except Exception as e:
        messagebox.showerror("Error PDF", str(e))

def singuardar():
    if not entry_matricula.get() or not entry_nombre.get() or not entry_apellidos.get() or not direccion_var.get() or not carrera_var.get() or not sexo_var.get() or not entry_fecha.get():
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    else:
        calificaciones = asignar_calificaciones()
        if not calificaciones:
            return
        try:
            agregaralumno()
            guardar_calificaciones_bd(entry_matricula.get(), calificaciones)
            limpiar_campos()
            exportar_pdf_alumno_seleccionado(entry_matricula.get(), calificaciones)
        except Exception as e:
            messagebox.showerror("Error de base de datos", str(e))

def agregaralumno():
    global ruta_imagen
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
        cursor = cn.cursor()
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
                # Elimina primero de las tablas relacionadas
                cursor.execute("DELETE FROM calificaciones WHERE matricula = %s", (matricula,))
                cursor.execute("DELETE FROM imagen WHERE matricula = %s", (matricula,))
                # Ahora elimina el alumno
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

etiqueta_imagen = tk.Label(frame_registros, bg="white", relief="groove")
etiqueta_imagen.place(x=1050, y=100, width=120, height=120)

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

btnEditar = tk.Button(frame_registros, text="Editar", font=("arial", 15, "bold"), fg="white", bg="#FF8800", command=editar_alumno)
btnEditar.place(x=800, y=40)

btnGuardar = tk.Button(frame_registros, text="Guardar", font=("arial", 15, "bold"), fg="white", bg="#228B22", command=singuardar)
btnGuardar.place(x=890, y=40)

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

def cargar_datos_en_campos(event):
    seleccion = tree.focus()
    if seleccion:
        datos = tree.item(seleccion)["values"]
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
        exportar_pdf_alumno_seleccionado(datos[0])
        try:
            cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos")
            cursor = cn.cursor()
            cursor.execute("SELECT imagen FROM imagen WHERE matricula=%s", (datos[0],))
            result = cursor.fetchone()
            if result and result[0]:
                from io import BytesIO
                img = Image.open(BytesIO(result[0]))
                img.thumbnail((120, 120))
                img_tk = ImageTk.PhotoImage(img)
                etiqueta_imagen.config(image=img_tk)
                etiqueta_imagen.image = img_tk
            else:
                etiqueta_imagen.config(image='')
                etiqueta_imagen.image = None
            cursor.close()
            cn.close()
        except Exception:
            etiqueta_imagen.config(image='')
            etiqueta_imagen.image = None

tree.bind("<<TreeviewSelect>>", cargar_datos_en_campos)

mostrar_datos()
ventana.mainloop()