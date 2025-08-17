import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
import datetime
import os
from tkinter import filedialog
from PIL import Image, ImageTk
from fpdf import FPDF
from fpdf.enums import XPos, YPos


ventana = tk.Tk()
ventana.title("Registro de Alumno")
#ventana.geometry("1300x800")
ventana.state("zoomed")
ventana.configure(bg="#0ef8f8")

fondo = tk.PhotoImage(file=r"c:\Users\Alexa\Desktop\EXAMEN PYTHON\POO(UNIDAD 1)\rog2.png")
fondo_label = tk.Label(ventana, image=fondo)
fondo_label.place(relwidth=1, relheight=1)

tiempo=datetime.datetime.now()
tiempo=tiempo.strftime("%d/%m/%Y")

fecha=tk.Label(ventana, text="fecha:"+tiempo, font=("ROG Fonts", 14, "bold"), fg="black", bg="lightblue")
fecha.place(x=1000, y=20)

etiqueta1 = tk.Label(ventana, text="Registro de alumno", font=("ROG Fonts", 18), bg="#0ef8f8")
etiqueta1.pack(pady=10, anchor="center")

def agregar_alumno():
    cn=mysql.connector.connect( host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
    cursor = cn.cursor()
    sql = "INSERT INTO alumnos_registrados (Matricula, Nombre, Apellido_Paterno, Apellido_Materno, Fecha_Nacimiento, Sexo, Carrera, Direccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # Guardar la fecha como string en formato DD/MM/YYYY
    fecha_nacimiento = fecha_nac.get()
    # Opcional: Validar formato
    try:
        datetime.datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use DD/MM/YYYY", parent=ventana)
        return
    datos = (matricula.get(), nombre.get(), apellido1.get(), apellido2.get(), fecha_nacimiento, opcion_genero.get(), carrera.get(), direccion.get())
    cursor.execute(sql, datos)
    cursor.close()
    cn.commit()
    cn.close()
    # También guardar en la tabla visual
    datos_tabla = [matricula.get(), nombre.get(), apellido1.get(), apellido2.get(), direccion.get(), opcion_genero.get(), carrera.get()]
    tabla.insert("", "end", values=datos_tabla)
     
       
    # Crear PDF
    alto=120
    ancho=210
    # Solicitar las calificaciones al usuario y obtener los valores
    base, calificaciones = asignar_calificaciones()
    if not base or not calificaciones:
        messagebox.showerror("Error", "Debe ingresar las calificaciones")
        return
    
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.image(r"C:\Users\Alexa\Desktop\EXAMEN PYTHON\POO(UNIDAD 1)\imagen.jpg", x=0, y=0, w=pdf.w, h=pdf.h)

    pdf.image(r"C:\Users\Alexa\Desktop\EXAMEN PYTHON\POO(UNIDAD 1)\Imagen45.jpg", x=10, y=8, w=185, h=30)
            
    pdf.ln(30)
    
    # Intentar configurar el locale en español, compatible con Windows y Linux
    import locale
    for loc in ['es_ES.UTF-8', 'es_ES', 'Spanish_Spain', 'Spanish']:
        try:
            locale.setlocale(locale.LC_TIME, loc)
            break
        except locale.Error:
            continue

            fecha_actual = datetime.datetime.now()
            dia = fecha_actual.strftime("%d")
            mes = fecha_actual.strftime("%B")
            anio = fecha_actual.strftime("%Y")
            
            # Construir la cadena de texto completa
            texto_ubicacion = "Zacualtipán de Ángeles Hgo., a "
            texto_fecha_bold_underline = f"{dia} de {mes}"
            texto_anio = f" del {anio}"
            
            # Establecer fuente normal para la ubicación
            pdf.set_font("Arial", size=12)
            
            # Mover el cursor a la posición adecuada para la alineación a la derecha
            x_pos = pdf.w - pdf.r_margin - pdf.get_string_width(texto_ubicacion + texto_fecha_bold_underline + texto_anio)
            pdf.set_x(x_pos)
            
            # Escribir la parte de la ubicación
            pdf.cell(pdf.get_string_width(texto_ubicacion), 10, txt=texto_ubicacion, ln=0)
            
            # Escribir la parte de la fecha en negritas y subrayado
            pdf.set_font("Arial", "BU", 12)
            pdf.cell(pdf.get_string_width(texto_fecha_bold_underline), 10, txt=texto_fecha_bold_underline, ln=0)
            
            # Escribir el año con fuente normal
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=texto_anio, ln=1)

            pdf.ln(8)

    pdf.set_font("helvetica", size=16, style="B")
    pdf.cell(200, 10, text="Datos del estudiante", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(1)
    pdf.set_font("helvetica", size=10)
        # Mover las líneas de datos personales un poco más a la derecha
    x_offset = 60  # Puedes ajustar este valor para mover más o menos
    pdf.set_x(x_offset)
    pdf.set_font("helvetica", size=14)
    pdf.cell(30, 10, text="Nombre:")
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(0, 10, text=f" {datos[1]} {datos[2]} {datos[3]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(x_offset)
    pdf.set_font("helvetica", size=14)
    pdf.cell(30, 10, text="Maricula:")
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(50, 10, text=f" {datos[0]}")
    pdf.set_font("helvetica", size=14)
    pdf.set_x(x_offset + 70)
    pdf.cell(20, 10, text="Sexo:")
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(40, 10, text=f" {datos[5]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(x_offset)
    pdf.set_font("helvetica", size=14)
    pdf.cell(40, 10, text="Fecha de Nacimiento:")
    pdf.set_x(x_offset + 60)
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(0, 10, text=f" {datos[4]}")
    # pdf.set_font("helvetica", size=14, style="B")
    # pdf.set_x(x_offset + 70)
    # pdf.cell(40, 10, text="Apellido Materno:")
    # pdf.set_x(x_offset +115)
    # pdf.set_font("helvetica", size=12)
    # pdf.cell(40, 10, text=f" {datos[3]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(x_offset)
    pdf.set_font("helvetica", size=14)
    pdf.cell(45, 10, text="Fecha de Nacimiento:")
    pdf.set_x(x_offset + 60)  # Mueve el valor más a la derecha
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(0, 10, text=f" {datos[4]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(x_offset)
    pdf.set_font("helvetica", size=14)
    pdf.cell(25, 10, text="Carrera:")
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(0, 10, text=f" {datos[6]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(x_offset)
    pdf.set_font("helvetica", size=14)
    pdf.cell(25, 10, text="Dirección:")
    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(0, 10, text=f" {datos[7]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(0, 10, txt="Calificaciones", ln=1, align='C')
    pdf.ln(3)
    pdf.set_font("Arial", size=12, style="B")
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
        pdf.cell(130, 8, align="L", text=materia)
        pdf.cell(40, 8, align="R", text=str(calificacion), new_x=XPos.LMARGIN, new_y=YPos.NEXT, border="L")
    pdf.ln(5)
    
    califs_validas=[float (c) for c in calificaciones if str (c).replace(".","",1).isdigit()]
    if califs_validas:
                promedio=round(sum(califs_validas)/len(califs_validas),2)
    else:
                promedio="N/A"
    pdf.set_font("helvetica", size=13, style="B")
    pdf.cell(0, 10, align="R", text=f"Promedio General: {promedio}", ln=1)

        # Agregar imagen (opcional)
    if ruta:
        try:
            pdf.image(ruta, x=10, y=68, w=40, h=40)  # Ajustar la imagen al PDF
        except Exception as e:
                messagebox.showwarning("Advertencia", f"No se pudo agregar la imagen: {e}", parent=ventana)

        # Guardar PDF
        nombre_pdf = f"{datos[0]}_registro.pdf"
        pdf.output(nombre_pdf)

        messagebox.showinfo("Éxito", f"Alumno registrado y PDF guardado como {nombre_pdf}", parent=ventana)
    else:
        messagebox.showerror("Error", f"Ocurrió un error: {e}", parent=ventana)

    messagebox.showinfo("Éxito", "Alumno registrado correctamente... =)", parent=ventana)
            
    # Limpiar campos
    matricula.delete(0, tk.END)
    nombre.delete(0, tk.END)
    apellido1.delete(0, tk.END)
    apellido2.delete(0, tk.END)
    fecha_nac.delete(0, tk.END)
    direccion.delete(0, tk.END)
    opcion_genero.set("")
    carrera.delete(0, tk.END)

#     PDF = fpdf.FPDF(orientation="p", unit="mm", format="A4")
#     PDF.add_page()
#     PDF.set_font("Arial", size=12)
#     PDF.cell(0, 10, txt=f"Matricula: {matricula}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Nombre: {nombre}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Apellido Paterno: {apellido1.get()}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Apellido Materno: {apellido2.get()}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Fecha de Nacimiento: {fecha_nac.get()}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Direccion: {direccion.get()}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Sexo: {opcion_genero.get()}", ln=True, align='C')
#     PDF.cell(0, 10, txt=f"Carrera: {carrera.get()}", ln=True, align='C')
#     pdf_file = f"{matricula.get()}_registro.pdf"
#     PDF.output(pdf_file)
#     messagebox.showinfo("Éxito", f"Datos guardados en PDF: {pdf_file}", parent=ventana)
    
#  # agregar imagen al pdf
#     if ruta:
#         try:
#             PDF.add_page()
#             PDF.image(seleccionar, x=10, y=30, w=180)  # Ajustar la imagen al PDF
#             pdf_file=f"{matricula.get()}_registro_con_imagen.pdf"
#             PDF.output(pdf_file)
#             messagebox.showinfo("Éxito", f"Imagen guardada en PDF: {pdf_file}", parent=ventana)
#         except Exception as e:
#             messagebox.showerror("Error", f"No se pudo agregar la imagen al PDF: {e}", parent=ventana)

    
tk.Label(ventana, text="Matricula:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=20, y=70)
matricula = tk.Entry(ventana, font=("Arial", 12), width=30, bg="#97c5d6", fg="black", bd=2, relief="flat", highlightthickness=3, highlightbackground="#2ac6ec", highlightcolor="#1c6ccb")
matricula.place(x=110, y=70)

tk.Label(ventana, text="Nombre:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=20, y=120)
nombre=tk.Entry(ventana, font=("Arial", 12), width=30, bg="#97c5d6", fg="black", bd=2, relief="flat", highlightthickness=3, highlightbackground="#2ac6ec", highlightcolor="#1c6ccb")
nombre.place(x=110, y=120)

tk.Label(ventana, text="Fecha nacimiento:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=20, y=170)
fecha_nac=tk.Entry(ventana, font=("Arial", 12), width=23, bg="#97c5d6", fg="black", bd=2, relief="flat", highlightthickness=3, highlightbackground="#2ac6ec", highlightcolor="#1c6ccb")
fecha_nac.place(x=174, y=170)

tk.Label(ventana, text="Direccion:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=20, y=210)

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

direccion_var = tk.StringVar()
direccion = ttk.Combobox(ventana, textvariable=direccion_var, values=direcciones, state="readonly", width=47)
direccion.place(x=110, y=210)
direccion.set("Selecciona una dirección")

tk.Label(ventana, text="Apellido Paterno:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=500, y=70)
apellido1=tk.Entry(ventana, font=("Arial", 12), width=20, bg="#97c5d6", fg="black", bd=2, relief="flat", highlightthickness=3, highlightbackground="#2ac6ec", highlightcolor="#1c6ccb")
apellido1.place(x=644, y=70)

tk.Label(ventana, text="Apellido Materno:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=500, y=120)
apellido2=tk.Entry(ventana, font=("Arial", 12), width=20, bg="#97c5d6", fg="black", bd=2, relief="flat", highlightthickness=3, highlightbackground="#2ac6ec", highlightcolor="#1c6ccb")
apellido2.place(x=644, y=120)

opcion_genero = tk.StringVar(value="") 

tk.Label(ventana, text="Genero:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=500, y=170)
genero=tk.Radiobutton(ventana, text="Hombre", variable=opcion_genero, value="Hombre").place(x=574, y=170)
genero1=tk.Radiobutton(ventana, text="Mujer", variable=opcion_genero, value="Mujer").place(x=650, y=170)
no_bin=tk.Radiobutton(ventana, text="No binario", variable=opcion_genero, value="No binario").place(x=715, y=170)

def actualizar_carreras(event):
    seleccion = direccion_var.get()
    carreras = carreras_dict.get(seleccion, [])
    carrera['values'] = carreras
    carrera.set("Selecciona una carrera")

direccion.bind('<<ComboboxSelected>>', actualizar_carreras)

tk.Label(ventana, text="Carrera:", font=("Arial", 12, "bold"), bg="#d357e7").place(x=500, y=210)
carrera_var = tk.StringVar()
carrera = ttk.Combobox(ventana, textvariable=carrera_var, state="readonly", width=47)
carrera.place(x=570, y=210)
carrera.set("Selecciona una carrera")


# Tabla para mostrar los datos
columnas = ("Matricula", "Nombre", "Apellido paterno", "Apellido Materno", "Direccion", "Sexo", "Carrera")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
tabla.place(x=50, y=350, width=1400)  # Más ancho
tabla.heading("#0", text="")
# Ajustar el ancho de cada columna para mejor visualización
ancho_columnas = [130, 180, 160, 160, 250, 120, 250]
for col, ancho in zip(columnas, ancho_columnas):
    tabla.heading(col, text=col)
    tabla.column(col, width=ancho, anchor="center")
tabla.place(x=50, y=350, width=1400)

# Función para cargar los alumnos registrados al iniciar
def cargar_alumnos_registrados():
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
        cursor = cn.cursor()
        cursor.execute("SELECT Matricula, Nombre, Apellido_Paterno, Apellido_Materno, Direccion, Sexo, Carrera FROM alumnos_registrados")
        alumnos = cursor.fetchall()
        for alumno in alumnos:
            tabla.insert("", "end", values=alumno)
        cursor.close()
        cn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la lista de alumnos al iniciar: {e}", parent=ventana)


# Llamar la función al iniciar
cargar_alumnos_registrados()

# --- Botones de editar y borrar para la tabla principal ---
def editar_seleccionado_tabla():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Sin selección", "Selecciona un alumno de la tabla para editar.", parent=ventana)
        return
    item = seleccionado[0]
    valores = tabla.item(item, "values")
    matricula.delete(0, tk.END)
    matricula.insert(0, valores[0])
    nombre.delete(0, tk.END)
    nombre.insert(0, valores[1])
    apellido1.delete(0, tk.END)
    apellido1.insert(0, valores[2])
    apellido2.delete(0, tk.END)
    apellido2.insert(0, valores[3])
    direccion.set(valores[4])
    opcion_genero.set(valores[5])
    carrera.set(valores[6])

def borrar_seleccionado_tabla():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Sin selección", "Selecciona un alumno de la tabla para eliminar.", parent=ventana)
        return
    item = seleccionado[0]
    valores = tabla.item(item, "values")
    matricula_eliminar = valores[0]
    confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar al alumno con matrícula {matricula_eliminar}?", parent=ventana)
    if not confirmar:
        return
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
        cursor = cn.cursor()
        cursor.execute("DELETE FROM alumnos_registrados WHERE Matricula=%s", (matricula_eliminar,))
        cn.commit()
        cursor.close()
        cn.close()
        tabla.delete(item)
        messagebox.showinfo("Éxito", "Alumno eliminado correctamente.", parent=ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el alumno: {e}", parent=ventana)

# Botones debajo de la tabla principal
btn_editar_tabla = tk.Button(ventana, text="Editar seleccionado", font=("Arial", 14), command=editar_seleccionado_tabla, bg="#1c6ccb", fg="white")
btn_editar_tabla.place(x=50, y=300)
btn_borrar_tabla = tk.Button(ventana, text="Eliminar seleccionado", font=("Arial", 14), command=borrar_seleccionado_tabla, bg="#e74c3c", fg="white")
btn_borrar_tabla.place(x=250, y=300)


def guardar_usuario():
    datos = [matricula.get(), nombre.get(), apellido1.get(), apellido2.get(), direccion.get(), opcion_genero.get(), carrera.get()]
    tabla.insert("", "end", values=datos)
    
    # try:
    #     agregar_alumno()
    #     from fpdf import FPDF
        
    #     matricula = matricula.get().strip()
    #     nombre = nombre.get().strip()
    #     apellido1 = apellido1.get().strip()
    #     apellido2 = apellido2.get().strip()
    #     fecha_nac = fecha_nac.get().strip()
    #     direccion = direccion.get().strip()
    #     genero = opcion_genero.get().strip()
    #     carrera = carrera.get().strip()
        
    #     PDF = FPDF(orientation="p", unit="mm", format="A4")
    #     PDF.add_page()
    #     PDF.set_font("Arial", size=12)
    #     PDF.cell(0, 10, txt=f"Matricula: {matricula}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Nombre: {nombre}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Apellido Paterno: {apellido1}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Apellido Materno: {apellido2}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Fecha de Nacimiento: {fecha_nac}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Direccion: {direccion}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Sexo: {genero}", ln=True, align='C')
    #     PDF.cell(0, 10, txt=f"Carrera: {carrera}", ln=True, align='C')
    #     PDF.ln(5)
        
    #     # Guardar la imagen si se seleccionó
    #     if ruta:
    #         try:
    #             PDF.image(seleccionar, x=10, y=30, w=180)
    #         except Exception as e:
    #             messagebox.showerror("Error", f"No se pudo agregar la imagen al PDF: {e}", parent=ventana)
    #             return
    #     pdf_file = f"{matricula}_registro.pdf"
    #     PDF.output(pdf_file)
        
    #     messagebox.showinfo("Éxito", f"Datos guardados en PDF: {pdf_file}", parent=ventana)
    # except Exception as e:
    #     messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}", parent=ventana)
        
    
    # Limpiar campos
    matricula.delete(0, tk.END)
    nombre.delete(0, tk.END)
    apellido1.delete(0, tk.END)
    apellido2.delete(0, tk.END)
    fecha_nac.delete(0, tk.END)
    direccion.delete(0, tk.END)
    opcion_genero.set("")
    carrera.delete(0, tk.END)
    
def editar_alumno():
    # Crear ventana para mostrar todos los usuarios
    ventana_usuarios = tk.Toplevel(ventana)
    ventana_usuarios.title("Selecciona un alumno para editar")
    ventana_usuarios.geometry("900x400")
    ventana_usuarios.configure(bg="#eaf6fb")

    columnas_usuarios = ("Matricula", "Nombre", "Apellido Paterno", "Apellido Materno", "Direccion", "Sexo", "Carrera")
    tabla_usuarios = ttk.Treeview(ventana_usuarios, columns=columnas_usuarios, show="headings", height=15)
    tabla_usuarios.pack(fill="both", expand=True)
    for col in columnas_usuarios:
        tabla_usuarios.heading(col, text=col)
        tabla_usuarios.column(col, width=120, anchor="center")

    # Consultar todos los alumnos en la base de datos
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
        cursor = cn.cursor()
        cursor.execute("SELECT Matricula, Nombre, Apellido_Paterno, Apellido_Materno, Direccion, Sexo, Carrera FROM alumnos_registrados")
        alumnos = cursor.fetchall()
        for alumno in alumnos:
            tabla_usuarios.insert("", "end", values=alumno)
        cursor.close()
        cn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de alumnos: {e}", parent=ventana_usuarios)
        ventana_usuarios.destroy()
        return

    def seleccionar_usuario():
        seleccionado = tabla_usuarios.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un alumno para editar.", parent=ventana_usuarios)
            return
        item = seleccionado[0]
        valores = tabla_usuarios.item(item, "values")
        matricula.delete(0, tk.END)
        matricula.insert(0, valores[0])
        nombre.delete(0, tk.END)
        nombre.insert(0, valores[1])
        apellido1.delete(0, tk.END)
        apellido1.insert(0, valores[2])
        apellido2.delete(0, tk.END)
        apellido2.insert(0, valores[3])
        direccion.delete(0, tk.END)
        direccion.insert(0, valores[4])
        opcion_genero.set(valores[5])
        carrera.delete(0, tk.END)
        carrera.insert(0, valores[6])
        ventana_usuarios.destroy()

    btn_seleccionar = tk.Button(ventana_usuarios, text="Seleccionar", font=("Arial", 12), command=seleccionar_usuario, bg="#1c6ccb", fg="white")
    btn_seleccionar.pack(pady=10)
        


def eliminar_alumno():
    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Selecciona un alumno para eliminar")
    ventana_eliminar.geometry("900x400")
    ventana_eliminar.configure(bg="#ffe5e5")

    columnas_usuarios = ("Matricula", "Nombre", "Apellido Paterno", "Apellido Materno", "Direccion", "Sexo", "Carrera")
    tabla_usuarios = ttk.Treeview(ventana_eliminar, columns=columnas_usuarios, show="headings", height=15)
    tabla_usuarios.pack(fill="both", expand=True)
    for col in columnas_usuarios:
        tabla_usuarios.heading(col, text=col)
        tabla_usuarios.column(col, width=120, anchor="center")

    # Consultar todos los alumnos en la base de datos
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
        cursor = cn.cursor()
        cursor.execute("SELECT Matricula, Nombre, Apellido_Paterno, Apellido_Materno, Direccion, Sexo, Carrera FROM alumnos_registrados")
        alumnos = cursor.fetchall()
        for alumno in alumnos:
            tabla_usuarios.insert("", "end", values=alumno)
        cursor.close()
        cn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de alumnos: {e}", parent=ventana_eliminar)
        ventana_eliminar.destroy()
        return

    def eliminar_usuario():
        seleccionado = tabla_usuarios.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un alumno para eliminar.", parent=ventana_eliminar)
            return
        item = seleccionado[0]
        valores = tabla_usuarios.item(item, "values")
        matricula_eliminar = valores[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar al alumno con matrícula {matricula_eliminar}?", parent=ventana_eliminar)
        if not confirmar:
            return
        try:
            cn = mysql.connector.connect(host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
            cursor = cn.cursor()
            cursor.execute("DELETE FROM alumnos_registrados WHERE Matricula=%s", (matricula_eliminar,))
            cn.commit()
            cursor.close()
            cn.close()
            # Eliminar de la tabla visual principal
            for item_tabla in tabla.get_children():
                valores_tabla = tabla.item(item_tabla, "values")
                if valores_tabla and valores_tabla[0] == matricula_eliminar:
                    tabla.delete(item_tabla)
                    break
            # Eliminar de la tabla de la ventana
            tabla_usuarios.delete(item)
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente.", parent=ventana_eliminar)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el alumno: {e}", parent=ventana_eliminar)

    btn_eliminar = tk.Button(ventana_eliminar, text="Eliminar", font=("Arial", 12), command=eliminar_usuario, bg="#e74c3c", fg="white")
    btn_eliminar.pack(pady=10)

#boton_editar = tk.Button(ventana, text="Seleccionar alumno..", font=("Arial", 14), command=editar_alumno, bg="#1c6ccb", fg="white")
#boton_editar.place(x=50, y=300)

#boton_eliminar = tk.Button(ventana, text="Eliminar alumno...", font=("Arial", 14), command=eliminar_alumno, bg="#e74c3c", fg="white")
#boton_eliminar.place(x=250, y=300)

    

# Botón para guardar usuario nuevo
btn_guardar = tk.Button(ventana, text="Guardar Datos...", font=("Arial", 14), command=agregar_alumno, bg="green", fg="white")
btn_guardar.place(x=520, y=300)

# Botón para guardar cambios de edición
def guardar_cambios():
    # Validar que la matrícula no esté vacía
    if not matricula.get():
        messagebox.showwarning("Advertencia", "No hay alumno seleccionado para editar.", parent=ventana)
        return
    # Confirmar edición
    confirmar = messagebox.askyesno("Confirmar", "¿Deseas guardar los cambios realizados?", parent=ventana)
    if not confirmar:
        return
    try:
        cn = mysql.connector.connect(host="localhost", user="root", password="", port="3306", database="registro_de_alumno")
        cursor = cn.cursor()
        sql = "UPDATE alumnos_registrados SET Nombre=%s, Apellido_Paterno=%s, Apellido_Materno=%s, Direccion=%s, Sexo=%s, Carrera=%s WHERE Matricula=%s"
        datos = (nombre.get(), apellido1.get(), apellido2.get(), direccion.get(), opcion_genero.get(), carrera.get(), matricula.get())
        cursor.execute(sql, datos)
        cn.commit()
        cursor.close()
        cn.close()
        # Actualizar en la tabla visual
        actualizado = False
        for item in tabla.get_children():
            valores = tabla.item(item, "values")
            if valores and valores[0] == matricula.get():
                tabla.item(item, values=[matricula.get(), nombre.get(), apellido1.get(), apellido2.get(), direccion.get(), opcion_genero.get(), carrera.get()])
                actualizado = True
                break
        if not actualizado:
            # Si no existe, lo agregamos
            tabla.insert("", "end", values=[matricula.get(), nombre.get(), apellido1.get(), apellido2.get(), direccion.get(), opcion_genero.get(), carrera.get()])
        messagebox.showinfo("Éxito", "Cambios guardados correctamente y mostrados en la tabla.", parent=ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}", parent=ventana)
        
def seleccionar():
    global ruta
    ruta = None
    archivo = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
    if not archivo:
        return
    try:
        from PIL import Image, ImageTk
        imagen = Image.open(archivo)
        imagen.thumbnail((150, 150))  # Redimensionar la imagen
        image_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen.config(image=image_tk)
        etiqueta_imagen.image = image_tk  # Mantener una referencia a la imagen
        ruta = archivo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
        ruta = None
        
def asignar_calificaciones():
    calif = tk.Toplevel(ventana)
    calif.title("Asignar Calificaciones")
    calif.geometry("1200x800")
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
        
etiqueta_imagen = tk.Label(ventana, bg="white")
etiqueta_imagen.place(x=900, y=60, width=200, height=200)

btn_guardar_cambios = tk.Button(ventana, text="Guardar Cambios", font=("Arial", 14), command=guardar_cambios, bg="#f7b731", fg="black")
btn_guardar_cambios.place(x=700, y=300)


boton_imagen = tk.Button(etiqueta_imagen, text="Seleccionar Imagen", font=("Arial", 12), command=seleccionar, bg="white", fg="black")
boton_imagen.place(x=25, y=100)

# Botón para salir
btn_salir = tk.Button(ventana, text="Salir del Registro", font=("Arial", 14, "bold"), command=ventana.destroy, bg="red", fg="black")
btn_salir.place(x=500, y=680)

ventana.mainloop()