import tkinter as tk
import mysql.connector
import datetime
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

#Función para validar campos
def guardar():
    if not entrada_matriculanew.get() or not entrada_nombre.get()  or not direccion_var.get() or not carrera_var.get() or not sexo_var.get() or not entrada_fechanac.get() or not entrada_apellidos.get() or not etiqueta_imagen.image:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    else:
        try:
            agregaralumno()
            from fpdf import FPDF
            import locale

            matricula=entrada_matriculanew.get().strip()
            nombre=entrada_nombre.get().strip()
            apellidos=entrada_apellidos.get().strip()
            sexo=sexo_var.get()
            direccion=direccion_var.get()
            carrera=carrera_var.get()
            # Solicitar las calificaciones al usuario y obtener los valores
            base, calificaciones = asignar_calificaciones()
            if not base or not calificaciones:
                messagebox.showerror("Error", "Debe ingresar las calificaciones")
                return
            


            pdf=FPDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()

            pdf.image("Venao.jpg", x=0, y=0, w=pdf.w, h=pdf.h)

            pdf.image("Logo2.png", x=10, y=8, w=185, h=30)
            
            pdf.ln(30)
    
            try:
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
            except locale.Error:
                locale.setlocale(locale.LC_TIME, 'es_ES')

            fecha_actual = datetime.datetime.now()

            fecha_formateada = fecha_actual.strftime("%d de %B del %Y")

            ubicacion = "Zacualtipán de Ángeles Hgo., a"
            fecha_final = f"{ubicacion} {fecha_formateada}"
            pdf.set_font("Arial", size=12)   

            pdf.cell(0, 10, txt=fecha_final, ln=True, align='R')

            pdf.ln(3)

            pdf.set_font("Arial", size=14, style="B")
            pdf.cell(0, 10, txt="Datos del Estudiante", ln=1, align='C')
            pdf.ln(2)

            pdf.set_font("Arial", size=13)
            pdf.set_x(70)
            pdf.cell(0, 10, txt=f"Nombre Completo: {nombre +" "+ apellidos}", ln=0.5)
            pdf.set_x(70)
            pdf.cell(0, 10, txt=f"Matrícula: {matricula}         Sexo: {sexo}", ln=0.5)
            pdf.set_x(70)
            pdf.cell(0, 10, txt=f"Dirección: {direccion}", ln=0.5)
            pdf.set_x(70)
            pdf.cell(0, 10, txt=f"Carrera: {carrera}", ln=0.5)
            pdf.ln(30)

            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt="Calificaciones", ln=1, align='C')
            pdf.ln(3)
            pdf.set_font("Arial", size=12)
            pdf.cell(130, 8, align="L", txt="Materia", border="B")
            pdf.cell(40, 8, align="C", txt="Calificación", border="LB", ln=1)
            pdf.ln(5)

            # Materias y calificaciones del usuario
            materias = [
                "Base de Datos",
                "Desarrollo de Pensamiento y Toma de Decisiones",
                "Inglés 3",
                "Programación Orientada a Objetos",
                "Tópicos de Calidad para el Diseño de Software"
            ]
            for materia, calificacion in zip(materias, calificaciones):
                pdf.cell(130, 8, align="L", txt=materia)
                pdf.cell(40, 8, align="R", txt=str(calificacion), ln=1, border="L")
            pdf.ln(5)
            #Insertar imagen si existe ruta
            if ruta:
                try:
                    pdf.image(ruta, x=15, y=60, w=50, h=50, )
                except Exception as e:
                    pass  # Si la imagen falla, el PDF se genera igual
            nombre_pdf=f"Registro_{matricula}.pdf"
            pdf.output(nombre_pdf)
            messagebox.showinfo("Éxito", f"PDF creado exitosamente como: '{nombre_pdf}'")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error de base de datos", str(e))

#Función para conectar a la base de datos
def conectar():
    try:
        conec=mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
        bases=conec.cursor()
        bases.execute("show databases")
        for base in bases:
            print(base)
        conec.close()
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))

ruta=None

def seleccionar_imagen():
    global ruta
    archivo = filedialog.askopenfilename(title="Seleccionar Imágen", filetypes=[("Archivos de Imagen", "*.jpg;*.jpeg;*.png")])
    if not archivo:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna imagen.")
        ruta = None
        etiqueta_imagen.config(image='')
        return
    try:
        imagen = Image.open(archivo)
        imagen.thumbnail((150, 150))  # Redimensionar la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk  # Mantener una referencia a la imagen
        ruta=archivo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
        ruta=None

#Función para agregar datos a la base de datos
def agregaralumno():
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
        cursor = cn.cursor()

        # Obtener fecha
        try:
            fecha_nacimiento=datetime.datetime.strptime(entrada_fechanac.get(), "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Error de formato", "La fecha debe tener formato DD/MM/YYYY")
            cn.close()
            return

        # Leer imagen
        with open(ruta, "rb") as file:
            imagen_bytes = file.read()

        nombre_completo = " ".join([entrada_nombre.get().strip(), entrada_apellidos.get().strip()])
        if not nombre_completo:
            messagebox.showerror("Error", "El nombre completo no puede estar vacío")
            cn.close()
            return

        datos = (int(entrada_matriculanew.get()), nombre_completo, sexo_var.get(), direccion_var.get(), carrera_var.get(), fecha_nacimiento, imagen_bytes)

        sql = """INSERT INTO Alumnos_Registrados (Matricula, Nombre_Completo, Sexo, Dirección, Carrera, Fecha_Nacimiento, Imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, datos)
        cn.commit()
        cn.close()
        messagebox.showinfo("Éxito", "Alumno registrado correctamente")
        mostrar_datos()
    except Exception as e:
        messagebox.showerror("Error de base de datos", str(e))


# Limpiar campos luego de guardar
def limpiar_campos():
    entrada_matriculanew.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_fechanac.delete(0, tk.END)
    entrada_apellidos.delete(0, tk.END)
    direccion_combo.set("Selecciona una dirección")
    carrera_combo.set("Selecciona una carrera")
    sexo_var.set("")
    etiqueta_imagen.config(image='')  # Limpiar la imagen
    etiqueta_imagen.image = None      # Eliminar referencia a la imagen

# Funcionar para mostrar datos en el frame
def mostrar_datos():
    for row in tree.get_children():
        tree.delete(row)
    try:
        cn=mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
        cursor=cn.cursor()
        cursor.execute("SELECT Matricula, Nombre_Completo, Sexo, Dirección, Carrera FROM Alumnos_Registrados")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cn.close()
    except Exception as e:
        messagebox.showerror("Error al cargar datos", str(e))

def eliminar_alumno():
    selec_item=tree.selection()
    if not selec_item:
        messagebox.showerror("Error", "Selecciona un alumno para eliminar")
        return
    matricula=tree.item(selec_item, "values")[0]
    cn=mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
    cursor=cn.cursor()
    cursor.execute("DELETE FROM Alumnos_Registrados WHERE Matricula = %s", (matricula,))
    cn.commit()
    cn.close()
    messagebox.showinfo("Éxito", "Alumno eliminado correctamente")

def editar_alumno():
    select_item = tree.selection()
    if not select_item:
        messagebox.showerror("Error", "Seleccione un alumno para editar")
        return
    valores = tree.item(select_item, "values")
    matricula_original = valores[0]

    # Obtener datos actuales del alumno
    cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
    cursor = cn.cursor()
    cursor.execute("SELECT * FROM Alumnos_Registrados WHERE Matricula = %s", (matricula_original,))
    alumno = cursor.fetchone()
    cn.close()
    if not alumno:
        messagebox.showerror("Error", "Alumno no encontrado")
        return

    # Limpiar ruta para evitar confusiones al editar
    global ruta
    ruta = None
    # Cargar datos en los campos para edición
    entrada_matriculanew.delete(0, tk.END)
    entrada_matriculanew.insert(0, alumno[0])
    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(0, alumno[1].split()[0])
    entrada_apellidos.delete(0, tk.END)
    entrada_apellidos.insert(0, " ".join(alumno[1].split()[1:]))
    entrada_fechanac.delete(0, tk.END)
    entrada_fechanac.insert(0, alumno[5].strftime("%d/%m/%Y"))
    sexo_var.set(alumno[2])
    direccion_var.set(alumno[3])
    carrera_var.set(alumno[4])

    # Mostrar imagen guardada
    if alumno[6]:
        try:
            from io import BytesIO
            imagen_bytes = alumno[6]
            imagen = Image.open(BytesIO(imagen_bytes))
            imagen.thumbnail((150, 150))
            imagen_tk = ImageTk.PhotoImage(imagen)
            etiqueta_imagen.config(image=imagen_tk)
            etiqueta_imagen.image = imagen_tk
        except Exception as e:
            etiqueta_imagen.config(image='')
            etiqueta_imagen.image = None

    # Crear ventana de edición o botón para guardar cambios
    def guardar_edicion():
        global ruta
        nueva_matricula=entrada_matriculanew.get()
        nombre_completo=" ".join([entrada_nombre.get().strip(), entrada_apellidos.get().strip()])
        sexo=sexo_var.get()
        direccion=direccion_var.get()
        carrera=carrera_var.get()
        try:
            fecha_nacimiento=datetime.datetime.strptime(entrada_fechanac.get(), "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Error de formato", "La fecha debe tener formato DD/MM/YYYY")
            return
        # Obtener imagen: si ruta tiene valor, es nueva imagen; si no, usar la actual
        if ruta:
            try:
                with open(ruta, "rb") as file:
                    imagen_bytes = file.read()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
                return
        else:
            imagen_bytes = alumno[6]
        cn = mysql.connector.connect(host="localhost", user="root", password="", port=3306, database="alumnos_utsh")
        cursor = cn.cursor()
        cursor.execute("UPDATE Alumnos_Registrados SET Matricula=%s, Nombre_Completo=%s, Sexo=%s, Dirección=%s, Carrera=%s, Fecha_Nacimiento=%s, Imagen=%s WHERE Matricula=%s", (nueva_matricula, nombre_completo, sexo, direccion, carrera, fecha_nacimiento, imagen_bytes, matricula_original))
        cn.commit()
        cn.close()
        messagebox.showinfo("Éxito", "Alumno actualizado correctamente")
        mostrar_datos()
        limpiar_campos()
        ruta = None  # Limpiar ruta después de guardar

    # Crear botón para guardar cambios si no existe
    if not hasattr(ventana, 'btnGuardarEdicion'):
        ventana.btnGuardarEdicion = tk.Button(ventana, text="Guardar Edición", font=("arial", 15, "bold"), fg="white", bg="orange", command=guardar_edicion, width=15, height=2)
        ventana.btnGuardarEdicion.place(x=900, y=270)

def asignar_calificaciones():
    calif = tk.Toplevel(ventana)
    calif.title("Asignar Calificaciones")
    calif.geometry("900x300")
    calif.config(bg="lightblue")

    titulo_calif = tk.Label(calif, text="Asignar Calificaciones", font=("arial", 20, "bold"), fg="black", bg="lightblue")
    titulo_calif.pack(pady=20)

    base_calif = tk.Label(calif, text="Base de Datos:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
    base_calif.place(x=50, y=80)
    base_etiqueta_calif = tk.Entry(calif)
    base_etiqueta_calif.place(x=200, y=85)

    desa_calif = tk.Label(calif, text="Desarrollo de Pensamiento y Toma de Decisiones:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
    desa_calif.place(x=50, y=120)
    desa_etiqueta_calif = tk.Entry(calif)
    desa_etiqueta_calif.place(x=535, y=125)

    ingles_calif = tk.Label(calif, text="Inglés 3:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
    ingles_calif.place(x=50, y=160)
    ingles_etiqueta_calif = tk.Entry(calif)
    ingles_etiqueta_calif.place(x=150, y=165)

    programacion_calif = tk.Label(calif, text="Programación Orientada a Objetos:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
    programacion_calif.place(x=50, y=200)
    programacion_etiqueta_calif = tk.Entry(calif)
    programacion_etiqueta_calif.place(x=395, y=205)

    top_calif = tk.Label(calif, text="Tópicos de Calidad para el Diseño de Software:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
    top_calif.place(x=50, y=240)
    top_etiqueta_calif = tk.Entry(calif)
    top_etiqueta_calif.place(x=505, y=245)

    resultado = {'base': None, 'calificaciones': None}

    def guardar_calificaciones():
        materias = ["Base de Datos", "Desarrollo de Pensamiento y Toma de Decisiones", "Inglés 3", "Programación Orientada a Objetos", "Tópicos de Calidad para el Diseño de Software"]
        calificaciones = [base_etiqueta_calif.get(), desa_etiqueta_calif.get(), ingles_etiqueta_calif.get(), programacion_etiqueta_calif.get(), top_etiqueta_calif.get()]
        resultado['base'] = base_etiqueta_calif.get().strip()
        resultado['calificaciones'] = calificaciones
        calif.destroy()

    btnguaradarcalif = tk.Button(calif, text="Guardar Calificaciones", font=("arial", 15, "bold"), fg="white", bg="green", command=guardar_calificaciones, width=20, height=2)
    btnguaradarcalif.place(x=300, y=280)

    calif.grab_set()
    calif.wait_window()
    return resultado['base'], resultado['calificaciones']

#crear ventana
ventana=tk.Tk()
ventana.title("Alumnos")
ventana.geometry("1472x832")
ventana.config(bg="lightblue")

#insertar titulo
titulo=tk.Label(ventana, text="Registro de Alumnos", font=("arial", 25, "bold"), fg="black", bg="lightblue")
titulo.place(x=350, y=10)

# Fecha actual
tiempo=datetime.datetime.now()
tiempo=tiempo.strftime("%d/%m/%Y")

# Etiquetas y entradas
fecha=tk.Label(ventana, text="Fecha:" + tiempo, font=("arial", 15, "bold"), fg="black", bg="lightblue")
fecha.place(x=1000, y=15)

matriculanew=tk.Label(ventana, text="Matricula:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
matriculanew.place(x=50, y=100)

entrada_matriculanew=tk.Entry(ventana)
entrada_matriculanew.place(x=150, y=105)

nombre=tk.Label(ventana, text="Nombre:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
nombre.place(x=50, y=140)
entrada_nombre=tk.Entry(ventana, width=30)
entrada_nombre.place(x=135, y=145)

apellidos=tk.Label(ventana, text="Apellidos:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
apellidos.place(x=350, y=140)
entrada_apellidos=tk.Entry(ventana, width=30)
entrada_apellidos.place(x=450, y=145)

fechanac=tk.Label(ventana, text="Fecha de Nacimiento:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
fechanac.place(x=50, y=180)
entrada_fechanac=tk.Entry(ventana, fg="black")
entrada_fechanac.place(x=250, y=185)

# Ayuda de formato para el usuario
ayuda_fecha = tk.Label(ventana,text="(DD/MM/AAAA)",font=("arial", 7),fg="gray",bg="white")
ayuda_fecha.place(x=270, y=205)

sexo=tk.Label(ventana, text="Sexo:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
sexo.place(x=430, y=180)
sexo_var=tk.StringVar(value="")
radio_Mujer=tk.Radiobutton(ventana, text="Mujer", value="Mujer", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="lightblue")
radio_Mujer.place(x=500, y=180)
radio_Hombre=tk.Radiobutton(ventana, text="Hombre", value="Hombre", variable=sexo_var, font=("arial", 15, "bold"), fg="black", bg="lightblue")
radio_Hombre.place(x=600, y=180)

etiqueta_imagen=tk.Label(ventana, bg="white")
etiqueta_imagen.place(x=800, y=60, width=150, height=150)

selec=tk.Button(etiqueta_imagen, text="Seleccionar Imagen", bg="grey", command=seleccionar_imagen, fg="Black", width=15)
selec.place(x=15, y=60)

# Lista de direcciones y carreras
direcciones=["Ciencias Económico-Administrativas", "Ciencias Naturales e Ingeniería", "Tecnologías de la Información", "Ciencias Exactas", "Ciencias de la Salud"]
carreraseco=["Maestría en Innovación y Negocios", "Licenciatura en Administración", "Licenciatura en Contaduría", "Licenciatura en Negocios y Mercadotecnia"]
carrerasnat=["Maestría en Sistemas de Gestión Ambiental", "Licenciatura en Ingeniería en Mantenimiento Industrial", "Licenciatura en Ingeniería Civil", "Licenciatura en Ingeniería en Manejo de Recursos Naturales"]
carrerasti=["Desarrollo de Software Multiplataforma", "Infraestructura de Redes Digitales", "Automatización"]
carrerasexac=["Licenciatura en Ingeniería Mecánica", "Licenciatura en Ingeniería Industrial", "Licenciatura en Ingeniería en Diseño Textil y Moda"]
carrerassalud=["Licenciatura en Terapia Física", "Licenciatura en Enfermería", "Licenciatura en Médico Cirujano y Partero"]

carreras_dict={"Ciencias Económico-Administrativas": carreraseco, "Ciencias Naturales e Ingeniería": carrerasnat, "Tecnologías de la Información": carrerasti, "Ciencias Exactas": carrerasexac, "Ciencias de la Salud": carrerassalud}

# Dirección
direccion=tk.Label(ventana, text="Dirección:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
direccion.place(x=50, y=220)
direccion_var=tk.StringVar()
direccion_combo=ttk.Combobox(ventana, textvariable=direccion_var, values=direcciones, state="readonly", width=47)
direccion_combo.place(x=150, y=225)
direccion_combo.set("Selecciona una dirección")

# Carrera
carrera=tk.Label(ventana, text="Carrera:", font=("arial", 15, "bold"), fg="black", bg="lightblue")
carrera.place(x=480, y=220)
carrera_var=tk.StringVar()
carrera_combo=ttk.Combobox(ventana, textvariable=carrera_var, state="readonly", width=47)
carrera_combo.place(x=570, y=225)
carrera_combo.set("Selecciona una carrera")

#Funcion para
def actualizar_carreras(event):
    seleccion=direccion_var.get()
    carreras=carreras_dict.get(seleccion, [])
    carrera_combo['values']=carreras
    carrera_combo.set("Selecciona una carrera")

direccion_combo.bind('<<ComboboxSelected>>', actualizar_carreras)

# Botón Guardar
btnGuardar=tk.Button(ventana, text="Guardar", font=("arial", 15, "bold"), fg="white", bg="green", command=guardar, width=10, height=2)
btnGuardar.place(x=180, y=270)

btnSalir=tk.Button(ventana, text="Salir", font=("arial", 15, "bold"), fg="white", bg="red", command=ventana.destroy, width=10, height=2)
btnSalir.place(x=1000, y=600)

btneliminar=tk.Button(ventana, text="Eliminar Alumno", font=("arial", 15, "bold"), fg="white", bg="red", command=eliminar_alumno, width=15, height=2)
btneliminar.place(x=430, y=270)

btneditar=tk.Button(ventana, text="Editar Alumno", font=("Arial", 15, "bold"), fg="white", bg="blue", command=editar_alumno, width=15, height=2)
btneditar.place(x=680, y=270)

# Frame para mostrar datos
tree_frame=tk.Frame(ventana)
tree_frame.place(x=50, y=350)
columns=("Matricula", "Nombre_Completo", "Sexo", "Direccion", "Carrera")
tree=ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=180)
tree.pack(fill="both", expand=True)

mostrar_datos()

ventana.mainloop()