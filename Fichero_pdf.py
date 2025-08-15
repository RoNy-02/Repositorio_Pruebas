from fpdf import FPDF
pdf = FPDF()

class FPDF(Orientation = "P", unit="mm",format="A4"):  #mm son los milimitros o escala
    pdf.add_page()
    pdf.set_font("arial",size=15)
    pdf.cell(0,8,align="C",txt="saludos soy panchito", border = "LB", ln=100)
    pdf.cell(0,8,align="C",txt="\nsaludos soy panchito", border = "LB") #definir celdas dentro del documento, borde = 1 seria borde completo, borde B,T,L,R,BL=IZQUIERDO
    pdf.image("panda.jpg",60,60,100)

    pdf.output("Prueba_1.pdf") #salida del pdf



#align= "C" es centrar el texto
#el txt solo aceptara texto
#ln = 0 es un salto de linea pero como es 0 no lo hara, si es 1 si