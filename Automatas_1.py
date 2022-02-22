import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as FileDialog
from io import open
from tkinter import PhotoImage
import re
from PIL import Image,ImageTk
import MySQLdb

path=""
codigo=""
errorTarjeta=True
errorIdentidad=True
errorNacimiento=True
errorHora=True
errorAños=True
errorFecha=True
errorTelefono=True
errorCorreo=True
errorSitio=True
errorMonto=True

def ArchivoNuevo():
    global path
    print(path)
    global codigo
    x=0
    print(x)
    if  (x==0) and (path != "") and (texto.get(1.0, "end-1c")!=codigo):
        x=PreguntaGuardar()
        if x==0:
            textoAux=texto.get(1.0, "end-1c")
            mensaje.set("Nuevo Archivo")
            path=""
            texto.delete(1.0, "end")
            root.title("Editor")
        elif x==1:
            mensaje.set("Guardar archivo")
            if path !="":
                file =open(path,"w+")
                contenido = texto.get(1.0,'end-1c')
                file.write(contenido)
                file.close()
                mensaje.set("Archivo Guardado")
                mensaje.set("Nuevo Archivo")
                path=""
                texto.delete(1.0, "end")
                root.title("Editor")

    else:
        
        mensaje.set("Nuevo Archivo")
        path=""
        texto.delete(1.0, "end")
        root.title("Editor")


def PreguntaGuardar():
    respuesta= messagebox.askquestion("Advertencia", "¿Desea Guardar Cambios?")
    if respuesta=="yes":
        return 1
    elif respuesta=="no":
        return 0

def AbrirArchivo():
    global path
    global codigo
    pathaux=path
    mensaje.set("Abrir archivo")
    path = FileDialog.askopenfilename(initialdir='_',filetypes=(("Ficheros de texto", "*.php"),),title="Abrir archivo")
    if path!= "":
        file = open(path,'r')
        contenido=file.readlines()
        texto.delete(1.0, "end")
        x=0
        for line in contenido:
            texto.insert('insert',line)
        file.close()
        codigo=texto.get(1.0, "end-1c")
        root.title(path)
    else:
        path= pathaux

def GuardarArchivo():
    global path
    x=1
    mensaje.set("Guardar archivo")
    if len(texto.get(1.0,"end-1c"))==0:
        messagebox.showwarning("Advertencia","El texto esta vacio")
        x=0
    if x==1:
        if path !="":
            file =open(path,"w+")
            contenido = texto.get(1.0,'end-1c')
            file.write(contenido)
            file.close()
            mensaje.set("Archivo Guardado")
        else:
            mensaje.set("Guardar Como")
            file = FileDialog.asksaveasfile(title="Guardar archivo",filetypes=(("Ficheros de texto", "*.php"),), mode ="w")
            if file is not None:
                path = file.name
                contenido = texto.get(1.0, "end-1c")
                file.write(contenido)
                file.close()
                mensaje.set("Archivo Guardado")
            else:
                mensaje.set("No se Guardo")
                path=""

def GuardarComo():
    global path
    global codigo
    mensaje.set("Guardar Como")
    x=1
    mensaje.set("Guardar archivo")
    if len(texto.get(1.0,"end-1c"))==0:
        messagebox.showwarning("Advertencia","El texto esta vacio")
        x=0
    if x==1:
        file = FileDialog.asksaveasfile(title="Guardar archivo",filetypes=(("Ficheros de texto", "*.php"),), mode ="w")
        if file is not None:
            path = file.name
            contenido = texto.get(1.0, "end-1c")
            file.write(contenido)
            file.close()
            mensaje.set("Archivo Guardado")
        else:
            mensaje.set("No se Guardo")
            path=""

def AutomataReales(Palabra):
    largo= len(Palabra)
    i=0
    estado=1
    while (i<largo):
        caracter=Palabra[i]
        if estado==1:
            if caracter.isdigit():
                estado=2
            else: 
                estado=-1
        elif estado==2:
            if caracter.isdigit():
                estado=2
            elif (caracter=='E' or caracter=='e'):
                estado=5
            elif caracter=='.':
                estado=3
            else: 
                estado=-1
        elif estado==3:
            if caracter.isdigit():
                estado=4
            else:
                estado=-1
        elif estado==4:
            if caracter.isdigit():
                estado=4
            elif (caracter=='e' or caracter=='E'):
                estado=5
        elif estado==5:
            if caracter.isdigit():
                estado=7
            elif (caracter=='+' or caracter=='-'):
                estado=6
            else:
                estado=-1
        elif estado==6:
            if caracter.isdigit():
                estado=7
            else:
                estado=-1
        elif estado==7: 
            if caracter.isdigit():
                estado=7
            else:
                estado=-1
        elif estado==-1:
            
            break           
        i+=1
    if estado==4 or estado!=7:
        print(Palabra)
        x=0
        aux=""
        for x in range(i-1):
            aux=aux+" "
        aux=aux+"^"
        print(aux)
        print("Error en esta pocision")
        messagebox.showwarning("Advertencia",Palabra+" Error en este numero real.")
        estado=-1
        return estado
         

def AutomataDeIdentificadores(palabra):
    cadena=palabra
    largo=len(cadena)
    i=0
    estado=0
    while i<largo:
        caracter=cadena[i]
    
        if estado==0:
            if caracter=="$":
                estado=1
            elif caracter.isalpha() and caracter!=" ":
                estado=2
            elif caracter=="_":
                estado=-1
            elif caracter.isdecimal():
                estado=-1
            elif (caracter.isalpha() == False) and (caracter.isdecimal() == False):
                estado=-1
                
        elif estado==1:
            if caracter.isalpha() and caracter!=" ":
                estado=2
            elif caracter.isdecimal():
                estado=-1
            elif caracter=="_":
                estado=-2
            elif (caracter.isalpha() == False) and (caracter.isdecimal() == False):
                estado=-2

        elif estado==2:
            if caracter.isalpha() and caracter!=" ":
                estado=2
            elif caracter.isdecimal():
                estado=4
            elif caracter=="_":
                estado=3
            elif (caracter.isalpha() == False) and (caracter.isdecimal() == False):
                estado=-2

        elif estado==3:
            if caracter.isalpha() and caracter!=" ":
                estado=2
            elif caracter.isdecimal():
                estado=4
            elif caracter=="_":
                estado=3
            elif (caracter.isalpha() == False) and (caracter.isdecimal() == False):
                estado=-2

        elif estado==4:
            if caracter.isalpha() and caracter!=" ":
                estado=2
            elif caracter.isdecimal():
                estado=4
            elif caracter=="_":
                estado=3
            elif (caracter.isalpha() == False) and (caracter.isdecimal() == False):
                estado=-2
    
        elif estado==-1:
            break
    
        elif estado==-2:
            break
       
        i+=1
    
    if cadena=="$":
        estado=-1
    if estado!=-2 and estado !=-1:
        pass
    else:
        print(cadena)
        x=0
        palabra=""
        for x in range(i-1):
            palabra=palabra+" "
        palabra=palabra+"^"
        print(palabra)
        print("Error en esta pocision")
        messagebox.showwarning("Advertencia",cadena+" Error en este identificador")
    return estado

def AutomataTipoNumeros(Palabra):
    #Palabra="55x0fe"
    largo = len(Palabra)
    i=0
    estado=0
    lista=['a','b','c','d','e','f']

    while (i<largo):
        caracter=Palabra[i]
        if estado==0:
            if caracter.isalpha():
                estado=0
            elif int(caracter)>0:
                estado=5
            elif estado==0:
                estado=1
            elif caracter=='.':
                estado=6
        elif estado==1:
            if caracter=='x' or caracter=='X':
                estado=8
            elif caracter=='.':
                estado=6
            elif int(caracter)>=0 and int(caracter)<=7:
                estado=2
        elif estado==2:
            if caracter.lower() in lista:
                estado=3
            elif int(caracter)<=9 and int(caracter)>=0:
                estado=3
        elif estado==3:
            if caracter.lower() in lista:
                estado=4
            elif int(caracter)<=9 and int(caracter)>=0:
                estado=4
        elif estado==3:
            if caracter.lower() in lista:
                estado=3
            elif int(caracter)<=9 and int(caracter)>=0:
                estado=3
        elif estado==5:
            try:
                if int(caracter)<=9 and int(caracter)>=0:
                    estado=5
                elif caracter=='.':
                    estado=6
            except:
                pass
        elif estado==6:
            if int(caracter)<=9 and int(caracter)>=0:
                estado=7
        elif estado==7:
            estado=7
        i+=1
   

    if estado==8 or estado==5 or estado==7 or estado==4:
        pass
    else:
        print(Palabra)
        x=0
        palabra=""
        for x in range(i-1):
            palabra=palabra+" "
        palabra=palabra+"^"
        print(palabra)
        print("Error en esta pocision")
        messagebox.showwarning("Advertencia",Palabra+" Error en este identificador")
    return estado
        
        
def CorrerAutomataTipoNumero():
    global path
    global codigo
    if path=="":
        codigo=texto.get(1.0, "end-1c")
        print(codigo)
        
        aux=AutomataTipoNumeros(codigo)
        if aux!=-1:
           GuardarComo()
        
    elif path!="":
        codigo=texto.get(1.0, "end-1c")
        
        aux=AutomataTipoNumeros(codigo)   
        if aux!=-1:
           GuardarArchivo()

def correrAutomataReales():
    global path
    global codigo
    if path=="":
        codigo=texto.get(1.0, "end-1c")
        print(codigo)
        
        aux=AutomataReales(codigo)
        if aux!=-1:
           GuardarComo()
        
    elif path!="":
        codigo=texto.get(1.0, "end-1c")
        
        aux=AutomataReales(codigo)   
        if aux!=-1:
           GuardarArchivo()

def correrAutomataVariables():
    global path
    global codigo
    if path=="":
        codigo=texto.get(1.0, "end-1c")
        print(codigo)
        
        AutomataDeIdentificadores(codigo)
        GuardarComo()
    elif path!="":
        codigo=texto.get(1.0, "end-1c")
        
        aux=AutomataDeIdentificadores(codigo)   
        if aux!=-1 and aux!=-2:
           GuardarArchivo()


def CrearNuevaVentana():
     Win2.deiconify() 
         
     

     
def ValorBoton():
    if errorTarjeta == False and errorIdentidad == False and errorNacimiento == False and errorHora == False and errorAños == False and errorFecha == False and errorTelefono== False and errorCorreo == False and errorCorreo == False and errorSitio == False and errorMonto== False:
        botonAceptar['state'] = NORMAL 
    else:
        botonAceptar['state'] = DISABLED 
       
    
def cambiotargeta(*args):
    global errorTarjeta
    if len(TextboxTarjeta.get())==0:
        labelTarjetaError['text']="Esperando..."
        errorTarjeta = True
        return
    valor = None
    valor=re.fullmatch(r'^\d{4}-\d{4}-\d{4}-\d{4}', TextboxTarjeta.get())
    valor=str(valor)
    if valor=="None":
        labelTarjetaError['text']="No es un numero de tarjeta de credito"
        errorTarjeta = True
    elif valor!="None":
        labelTarjetaError['text']="Valor Correcto!!!"
        errorTarjeta = False
    ValorBoton()

def cambioidentidad(*args):
    global errorIdentidad
    if len(TextBoxIdentidad.get())==0:
        labelIdentidadError['text']="Esperando..."
        errorIdentidad = True
        return
    valor = None
    valor = re.fullmatch(r'^\d{13}',TextBoxIdentidad.get())
    valor = str(valor)
    if valor == "None":
        labelIdentidadError['text']="No es un numero de Cui valido"
        errorIdentidad = True
    elif valor!="None":
        labelIdentidadError['text']="Valor Correcto!!!"
        errorIdentidad = False
    ValorBoton() 

def cambioNacimiento(*args):
    global errorNacimiento
    if len(TextBoxFechaNac.get())==0:
        labelFechaNacError['text']="Esperando..."
        errorNacimiento=True
        return
    valor = None
    valor = re.fullmatch(r'(\d{2}/\d{2}/[0-2][0][0-2][0-9])',TextBoxFechaNac.get())
    valor = str(valor)
    if valor=="None":
        labelFechaNacError['text']="No es una fecha de nacimiento valida"
        errorNacimiento=True
    elif valor!="None":
        labelFechaNacError['text']="Valor Correcto!!!"
        errorNacimiento= False
    ValorBoton() 

def cambioHora(*args):
    global errorHora
    if len(TextBoxHora.get())==0:
        labelHoraError['text']="Esperando..."
        errorHora=True
        return
    valor = None
    valor = re.fullmatch(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',TextBoxHora.get())
    valor = str(valor)
    if valor=="None":
        labelHoraError['text']="No es una hora valida"
        errorHora=True
    elif valor!="None":
        labelHoraError['text']="Valor Correcto!!!"
        errorHora=False
    ValorBoton() 

def cambioAños(*args):
    global errorAños
    if len(TextBoxAños.get())==0:
        labelAñosError['text']="Esperando..."
        errorAños=True
        return
    valor = None
    valor = re.fullmatch(r'^[2][0-9][0-9][0-9]',TextBoxAños.get())
    valor = str(valor)
    if valor=="None":
        labelAñosError['text']="No es año valido"
        errorAños=True
    elif valor!="None":
        labelAñosError['text']="Valor Correcto!!!"
        errorAños=False
    ValorBoton() 

def cambioFecha(*args):
    global errorFecha
    if len(TextBoxFecha.get())==0:
        labelFechaError['text']="Esperando..."
        errorFecha=True
        return
    valor = None
    valor = re.fullmatch(r'^[1-3][0-9][/][0-1?][0-9][/][1-2][0-9][0-9][0-9]',TextBoxFecha.get())
    valor = str(valor)
    if valor=="None":
        
        labelFechaError['text']="No es una hora valida"
        errorFecha=True
    elif valor!="None":
        labelFechaError['text']="Valor Correcto!!!"
        errorFecha=False
    ValorBoton() 

def cambioTelefono(*args):
    global errorTelefono
    if len(TextBoxTelefono.get())==0:
        labelTelefonoError['text']="Esperando..."
        errorTelefono=True
        return
    valor = None
    valor = re.fullmatch(r'^[0-9]{8}',TextBoxTelefono.get())
    valor = str(valor)
    if valor=="None":
        labelTelefonoError['text']="No es un número de telefono valido"
        errorTelefono = True
    elif valor !="None":
        labelTelefonoError['text']="Valor Correcto!!!"
        errorTelefono = False
    ValorBoton() 
    
def cambioCorreo(*args):
    global errorCorreo
    if len(TextBoxCorreo.get())==0:
        labelCorreoError['text']="Esperando..."
        errorCorreo=True
        return
    valor = None
    valor = re.fullmatch(r'^([a-zA-z]{1,})[@]([a-zA-z+]{1,})[.]([a-zA-z]{1,})', TextBoxCorreo.get())
    valor = str(valor)
    if valor=="None":
        labelCorreoError['text']="No es un correo valido"
        errorCorreo=True
    elif valor!="None":
        labelCorreoError['text']="Valor Correcto!!!"
        errorCorreo = False
    ValorBoton() 


def cambioSitio(*args):
    global errorSitio
    if len(TextBoxWeb.get())==0:
        labelWebError['text']="Esperando..."
        errorSitio=True
        return
    valor = None
    valor = re.fullmatch(r'^([w]{3})[.]([a-zA-z+]{1,})[.]([a-zA-z]{1,})', TextBoxWeb.get())
    valor = str(valor)
    if valor == "None":
        labelWebError['text'] = "No es un sitio web valido"
        errorSitio=True
    elif valor !="None":
        labelWebError['text'] = "Valor Correcto!!!"
        errorSitio=False
    ValorBoton() 


def cambioMonto(*args):
    global errorMonto
    if len(TextBoxMonto.get())==0:
        labelMontoError['text']="Esperando..."
        errorMonto=True
        return
    valor = None
    valor = re.fullmatch(r'^([0-9]{1,})',TextBoxMonto.get())
    if valor== None:
        valor = re.fullmatch(r'^([0-9]{1,}.[0-9]{1,})',TextBoxMonto.get())
    valor = str(valor)
    if valor =="None":
        labelMontoError['text']="No es un montovalido"
        errorMonto=True
       
    elif valor !="None":
        labelMontoError['text']="Valor Correcto!!!"
        errorMonto=False
    ValorBoton()    
    
def GuardarEnDB():
    conexion = MySQLdb.Connect(host="127.0.0.1",port=3310,user="root",passwd="ferluan123",database="automatas")
    cur = conexion.cursor()
    cur.execute("INSERT INTO `automatas`.`new_table` (`tarjetaCredito`,`identidad`,`fechaNacimiento`,`hora`,`años`,`fecha`,`telefono`,`correo`,`sitioweb`,`monto`)"+
    "VALUES"+
    "('"+ TextboxTarjeta.get() +"','"+TextBoxIdentidad.get()+"','"+TextBoxFechaNac.get()+"','"+TextBoxHora.get()+"','"+TextBoxAños.get()+"','"+TextBoxFecha.get()+"','"+TextBoxTelefono.get()+"','"+TextBoxCorreo.get()+"','"+TextBoxWeb.get()+"','"+TextBoxMonto.get()+"');")
    conexion.commit()
    conexion.close()

    labelSave = tkinter.Label(Win2, text = "Esperando...")
    labelSave.place(x=400, y=265)


root = Tk()
#root = tkinter.Tk()  
root.config()
root.title("Editor")

imagen_compilar = Image.open('play.png')
imagen_compilar = imagen_compilar.resize((15, 15)) # Redimension (Alto, Ancho)
imagen_compilar = ImageTk.PhotoImage(imagen_compilar)


#Variables de Cambio
#1
tarjeta = tkinter.StringVar()
tarjeta.trace_add("write",cambiotargeta)
#2
Identidad = tkinter.StringVar()
Identidad.trace_add("write",cambioidentidad)
#3
Nacimiento = tkinter.StringVar()
Nacimiento.trace_add("write",cambioNacimiento)
#4
Hora = tkinter.StringVar()
Hora.trace_add("write",cambioHora)
#5
Años = tkinter.StringVar()
Años.trace_add("write",cambioAños)
#6
Fecha = tkinter.StringVar()
Fecha.trace_add("write",cambioFecha)
#7
Telefono = tkinter.StringVar()
Telefono.trace_add("write",cambioTelefono)
#8
Correo = tkinter.StringVar()
Correo.trace_add("write",cambioCorreo)
#9
Sitio = tkinter.StringVar()
Sitio.trace_add("write",cambioSitio)
#10
Monto = tkinter.StringVar()
Monto.trace_add("write",cambioMonto)



menubar=Menu(root)
menubar.add_command(label="Nuevo",command=ArchivoNuevo)
menubar.add_command(label="Abrir", command=AbrirArchivo)
menubar.add_command(label="Guardar", command=GuardarArchivo)
menubar.add_command(label="Guardar Como", command=GuardarComo)

botonCompilar1 = tkinter.Button(root, image=imagen_compilar, compound="top", command=correrAutomataVariables)
botonCompilar1.place(x=5, y=1)
botonCompilar2 = tkinter.Button(root, image=imagen_compilar, compound="top", command=correrAutomataReales)
botonCompilar2.place(x=30, y=1)
botonCompilar3 = tkinter.Button(root, image=imagen_compilar, compound="top", command=CorrerAutomataTipoNumero)
botonCompilar3.place(x=55, y=1)

Win2 = tkinter.Toplevel(root)
Win2.geometry("650x300")
Win2.withdraw()
#Tarjeta de credito
labelTarjeta = tkinter.Label(Win2, text = "Tarjeta de Credito")
labelTarjeta.place(x=5,y=5)
TextboxTarjeta = tkinter.Entry(Win2,textvariable=tarjeta)
TextboxTarjeta.place(x=250, y=5)
labelTarjetaError = tkinter.Label(Win2, text = "Esperando...")
labelTarjetaError.place(x=400, y=5)


#Identiad
labelIdentidad = tkinter.Label(Win2 ,text = "Identidad")
labelIdentidad.place(x=5,y=30)
TextBoxIdentidad = tkinter.Entry(Win2,textvariable=Identidad)
TextBoxIdentidad.place(x=250,y=30)
labelIdentidadError = tkinter.Label(Win2, text = "Esperando...")
labelIdentidadError.place(x=400, y=30)
#Fecha de Nacimiento
labelFechaNac = tkinter.Label(Win2,text = "Fecha de Nacimiento")
labelFechaNac.place(x=5,y=55)
TextBoxFechaNac = tkinter.Entry(Win2,textvariable=Nacimiento)
TextBoxFechaNac.place(x=250,y=55)
labelFechaNacError = tkinter.Label(Win2, text = "Esperando...")
labelFechaNacError.place(x=400, y=55)
#Hora
labelHora = tkinter.Label(Win2,text = "Hora")
labelHora.place(x=5,y=80)
TextBoxHora = tkinter.Entry(Win2,textvariable=Hora)
TextBoxHora.place(x=250,y=80)
labelHoraError = tkinter.Label(Win2, text = "Esperando...")
labelHoraError.place(x=400, y=80)
#Años
labelAños = tkinter.Label(Win2,text = "Años")
labelAños.place(x=5,y=105)
TextBoxAños = tkinter.Entry(Win2,textvariable=Años)
TextBoxAños.place(x=250,y=105)
labelAñosError= tkinter.Label(Win2, text = "Esperando...")
labelAñosError.place(x=400, y=105)
#Fecha
labelFecha = tkinter.Label(Win2,text = "Fecha")
labelFecha.place(x=5,y=130)
TextBoxFecha = tkinter.Entry(Win2,textvariable=Fecha)
TextBoxFecha.place(x=250,y=130)
labelFechaError= tkinter.Label(Win2, text = "Esperando...")
labelFechaError.place(x=400, y=130)
#Telefono
labelTelefono = tkinter.Label(Win2,text = "Telefono")
labelTelefono.place(x=5,y=155)
TextBoxTelefono= tkinter.Entry(Win2,textvariable=Telefono)
TextBoxTelefono.place(x=250,y=155)
labelTelefonoError = tkinter.Label(Win2, text = "Esperando...")
labelTelefonoError.place(x=400, y=155)
#Correo Electronico
labelCorreo = tkinter.Label(Win2,text = "Correo Electronico")
labelCorreo.place(x=5,y=180)
TextBoxCorreo= tkinter.Entry(Win2,textvariable=Correo)
TextBoxCorreo.place(x=250,y=180)
labelCorreoError = tkinter.Label(Win2, text = "Esperando...")
labelCorreoError.place(x=400, y=180)
#Sitio web
labelWeb = tkinter.Label(Win2,text = "Sitio Web")
labelWeb.place(x=5,y=205)
TextBoxWeb= tkinter.Entry(Win2,textvariable=Sitio)
TextBoxWeb.place(x=250,y=205)
labelWebError = tkinter.Label(Win2, text = "Esperando...")
labelWebError.place(x=400, y=205)
#Monto
labelMonto = tkinter.Label(Win2,text = "Monto")
labelMonto.place(x=5,y=230)
TextBoxMonto= tkinter.Entry(Win2,textvariable=Monto)
TextBoxMonto.place(x=250,y=230)
labelMontoError = tkinter.Label(Win2, text = "Esperando...")
labelMontoError.place(x=400, y=230)
botonAceptar = tkinter.Button(Win2,text="Guardar Datos",state=DISABLED, command = GuardarEnDB)
botonAceptar.place(x=250, y=265)


botonExpreciones = tkinter.Button(root, compound="top",text="Expreciones Regulares", command=CrearNuevaVentana)
botonExpreciones.place(x=80,y=1)

texto = Text(root)
texto.place(x=5,y=25,relwidth=0.99,relheight=0.99)
#texto.pack(fill="both", expand=1,pady=25,padx=20,)
texto.config(bd=0,padx=5, pady=4, font=("Consolas",12),bg="white")

monitor1= Label(root,textvar="0")
monitor1.pack(side="left",fill="both")

mensaje = StringVar()
mensaje.set("Bienvenido")
monitor = Label(root, textvar=mensaje, justify='left')
monitor.pack(side="bottom", fill="both",expand=0)
monitor.config(bg="gray85")

root.config(menu=menubar)
root.geometry("500x500")
root.mainloop()

