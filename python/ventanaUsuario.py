from tkinter import *
import pathlib
import os
import tkinter
from ventanas.fieldFrame import FieldFrame
from tkinter import ttk

from excepciones.errorAplicacion import ErrorAplicacion
from excepciones.excepcionExistente import ExcepcionExistente
from excepciones.excepcionLongitud import ExcepcionLongitud
from excepciones.excepcionNumerica import ExcepcionNumerica
from excepciones.excepcionVacio import ExcepcionVacio
from excepciones.excepcionNoMetas import ExcepcionNoMeta
from excepciones.excepcionNoAhorros import ExcepcionNoAhorros
from baseDatos.serializador import Serializador
from ventanas.popUp import PopUp
import ventanaInicio

from gestorAplicacion.interfaz.Usuario import Usuario
from gestorAplicacion.interfaz.Meta import Meta
from gestorAplicacion.interfaz.Categoria import Categoria
from gestorAplicacion.interfaz.Ahorro import Ahorro



class VentanaUsuario(Tk):

    framesEnPantalla=[]

    def __init__(self, usuario):
        super().__init__()
        self._usuario = usuario

        # Parámetros de la ventana de usuario

        self.title('Finanzas Personales')
        self.option_add("*tearOff",  False)
        self.geometry("1366x768")
        self.resizable(False,False)

        # Barra de menú
        self._barraMenu = Menu(self)
        archivo = Menu(self._barraMenu)
        archivo.add_command(label="Aplicacion", command=lambda: infoApp())
        archivo.add_command(label="Salir y guardar", command=lambda: cerrarGuardar())
        self._barraMenu.add_cascade(label="Archivo", menu=archivo)
        self.config(menu= self._barraMenu)

        def infoApp():
            ventanaDevs = Tk()
            ventanaDevs.geometry("800x300")
            ventanaDevs.resizable(False,False)
            ventanaDevs.title("Aplicacion-Sistemas Gestor de Dinero")

            textoInfo = f"Finanzas Personales es una aplicación que permite al usuario realizar multiples tareas como:\n" \
                           f"1. Ver Estadisticas de la cuenta.\n" \
                           f"2. Ingresar dinero a su cuenta.\n" \
                           f"3. Mover dinero en su cuenta.\n" \
                           f"4. Sacar dinero de su cuenta.\n" \
                           f"5. Agregar Ahorro a su cuenta.\n" \
                           f"6. Agregar meta a su cuenta.\n" \
                           f"7. Modificar Ahorro\Bolsillo\Meta.\n" \
                           f"8. Solicitar Prestamo.\n" \
                           f"9. Abonar a un prestamo o meta.\n" \

            devs = Label(ventanaDevs, text = textoInfo, justify = "left", font=("Verdana", 12))
            devs.pack(fill=tkinter.Y, expand=True)

        procesosYConsultas = Menu(self._barraMenu)

        verSaldosDispo = Menu(self._barraMenu)
        verSaldosDispo.add_command(label="Ver bolsillos", command=lambda: cambiarVista(frameVerBolsillos))
        verSaldosDispo.add_command(label="Ver ahorros", command=lambda: cambiarVista(frameVerAhorros))
        verSaldosDispo.add_command(label="Ver metas", command=lambda: cambiarVista(frameVerMetas))
        verSaldosDispo.add_command(label="Ver dinero total", command=lambda: cambiarVista(frameVerDineroTotal))
        procesosYConsultas.add_cascade(label="Ver estadísticas de la cuenta", menu=verSaldosDispo)

        ingresarDinero = Menu(self._barraMenu)
        ingresarDinero.add_command(label="Bolsillos", command=lambda: cambiarVista(frameIngresarBolsillos))
        ingresarDinero.add_command(label="Ahorros", command=lambda: cambiarVista(frameIngresarAhorros))
        procesosYConsultas.add_cascade(label="Ingresar dinero a su cuenta", menu=ingresarDinero)

        moverDinero = Menu(self._barraMenu)
        moverDinero.add_command(label="Bolsillos", command=lambda: cambiarVista(frameMoverBolsillos))
        moverDinero.add_command(label="Ahorros", command=lambda: cambiarVista(frameMoverAhorros))
        procesosYConsultas.add_cascade(label="Mover dinero en su cuenta", menu=moverDinero)

        sacarDinero = Menu(self._barraMenu)
        sacarDinero.add_command(label="Retiro", command=lambda: cambiarVista(frameRetiro))
        procesosYConsultas.add_cascade(label="Sacar dinero de su cuenta", menu=sacarDinero)

        procesosYConsultas.add_separator()
        
        procesosYConsultas.add_command(label="Agregar ahorro a su cuenta", command=lambda: cambiarVista(frameAgregarAhorro))
        
        procesosYConsultas.add_command(label="Agregar meta a su cuenta", command=lambda: cambiarVista(frameAgregarMeta))

        procesosYConsultas.add_separator()

        modificarColBolMet = Menu(self._barraMenu)
        modificarColBolMet.add_command(label="Bolsillo", command=lambda: cambiarVista(frameModificarBolsillo))
        modificarColBolMet.add_command(label="Ahorro", command=lambda: cambiarVista(frameModificarAhorro))
        modificarColBolMet.add_command(label="Meta", command=lambda: cambiarVista(frameModificarMeta))
        procesosYConsultas.add_cascade(label="Modificar Colchon/Bolsillo/Meta", menu=modificarColBolMet)
         
        procesosYConsultas.add_separator()
       
        procesosYConsultas.add_command(label="SolicitarPrestamo", command=lambda: cambiarVista(frameSolicitarLargo))

        procesosYConsultas.add_separator()


        abonarPrestamoMeta = Menu(self._barraMenu)
        abonarPrestamoMeta.add_command(label="Prestamos", command=lambda: cambiarVista(frameAbonarPrestamo))
        abonarPrestamoMeta.add_command(label="Metas", command=lambda: cambiarVista(frameAbonarMetas))
        procesosYConsultas.add_cascade(label="Abonar a un prestamo o meta", menu=abonarPrestamoMeta)

        self._barraMenu.add_cascade(label="Procesos y consultas", menu= procesosYConsultas)

        ayuda = Menu(self._barraMenu)
        ayuda.add_command(label="Acerca de", command = lambda: infoDevs())
        self._barraMenu.add_cascade(label="Ayuda", menu = ayuda)

        self.config(menu = self._barraMenu)

        # Funciones utiles en la manipulacion de Frames
        
        # Cambiar vista del frame
        def cambiarVista(frameUtilizado):
            for frame in VentanaUsuario.framesEnPantalla:
                frame.pack_forget()
            frameUtilizado.pack(fill=BOTH,expand=True, pady = (10,10))

        # Mostrar un output
        def mostrarOutput(string, text):
            text.delete("1.0", "end")
            text.insert(INSERT, string)
            text.pack(fill=X, expand=True, padx=(10,10))

        # Verificar input vacio

        def verificarVacio(fieldFrame):
            for criterio in fieldFrame._criterios:
                if fieldFrame.getValue(criterio) == "":
                    raise ExcepcionVacio(criterio)

        # Verificar longitud de input

        def verificarLongitud(texto, requerido, nombreCampo):
            if len(texto) < requerido:
                raise ExcepcionLongitud([nombreCampo, requerido])

        # Verificar input numerico
        def verificarNumero(valor):
            if not valor.isnumeric():
                raise ExcepcionNumerica(valor)

        # Ayuda
        def infoDevs():
            ventanaDevs = Tk()
            ventanaDevs.geometry("640x360")
            ventanaDevs.resizable(False,False)
            ventanaDevs.title("Finanzas Personales - Acerca de")

            textoInfo = f"Desarrolladores:\n" \
                        f"• Julián Álvarez\n" \
                        f"• Isabela Hernández\n" \
                        f"• Ana María Guarín\n" \
                        f"• Cristian Imbacuan\n" \

            devs = Label(ventanaDevs, text = textoInfo, justify = "left", font=("Verdana", 12))
            devs.pack(fill=tkinter.Y, expand=True)

        #serializar el usuario
        def cerrarGuardar():
            serializar = Serializador(self._usuario)
            serializar.serializar()
            self.destroy()
            ventanaInicio.VentanaInicio(self._usuario)
            

        #Pantalla de inicio
        framePantallaInicio = Frame(self)
        nombrePantallaInicio = Label(framePantallaInicio, text="Bienvenidee", font=("Verdana", 16), fg="#8EAC50")
        outputPantallaInicio = Text(framePantallaInicio, height=100, font=("Verdana",10))

        nombrePantallaInicio.pack()
        outputPantallaInicio.pack(fill=X, expand=True, padx=(10, 10))

        VentanaUsuario.framesEnPantalla.append(framePantallaInicio)
        cambiarVista(framePantallaInicio)

        #Boton para ver el saldo disponible en Bolsillos
        def botonVerBolsillos():
            try:
                
                # Obtener los bolsillos del usuario
                categorias = [(nombre, categoria.value[0], categoria.value[1]) for nombre, categoria in Categoria.__members__.items()]
                categorias.pop()
                
                # Actualizar los valores en el FieldFrame
                FFVerBolsillos.setValue("Viajes", f"Saldo {categorias[0][1]}\tPresupuesto {categorias[0][2]}")
                FFVerBolsillos.setValue("Salud", f"Saldo {categorias[1][1]}\tPresupuesto {categorias[1][2]}")
                FFVerBolsillos.setValue("Alimentacion", f"Saldo {categorias[2][1]}\tPresupuesto {categorias[2][2]}")
                FFVerBolsillos.setValue("Transporte", f"Saldo {categorias[3][1]}\tPresupuesto {categorias[3][2]}")
                FFVerBolsillos.setValue("Educacion", f"Saldo {categorias[4][1]}\tPresupuesto {categorias[4][2]}")
                FFVerBolsillos.setValue("Hogar", f"Saldo {categorias[5][1]}\tPresupuesto {categorias[5][2]}")
                FFVerBolsillos.setValue("Entretenimiento", f"Saldo {categorias[6][1]}\tPresupuesto {categorias[6][2]}")
                FFVerBolsillos.setValue("Imprevistos", f"Saldo {categorias[7][1]}\tPresupuesto {categorias[7][2]}")
                
            except ErrorAplicacion as e:
                PopUp(str(e))
        
        #Se crea el frame
        frameVerBolsillos = Frame(self)
        nombreVerBolsillos = Label(frameVerBolsillos, text="Saldo en Bolsillos", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descVerBolsillos = Label(frameVerBolsillos, text="Su saldo disponible en su bolsillo es de:", font=("Arial Rounded MT Bold", 14))
        FFVerBolsillos = FieldFrame(frameVerBolsillos,None, ["Viajes", "Salud", "Alimentacion", "Transporte", "Educacion", "Hogar", "Entretenimiento", "Imprevistos"], None,None)
        FFVerBolsillos.crearBotones(botonVerBolsillos)

        outputVerBolsillos = Text(frameVerBolsillos, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputVerBolsillos)

        nombreVerBolsillos.pack()
        descVerBolsillos.pack()
        FFVerBolsillos.pack()

        VentanaUsuario.framesEnPantalla.append(frameVerBolsillos)

        #Boton para ver el saldo disponible en Ahorros
        def botonVerAhorros():
            
            try:
                # Obtener los ahorros del usuario
                ahorros_usuario = Usuario.getAhorros(self._usuario)
                
                # Verificar si hay metas disponibles
                if not ahorros_usuario:
                    raise ExcepcionNoAhorros
                else:
                    for ahorro in ahorros_usuario:
                        # Actualizar los valores en el FieldFrame
                        FFVerAhorros.setValue("Nombre del ahorro", ahorro.getNombre())
                        FFVerAhorros.setValue("Disponible", ahorro.getDisponible())
                        FFVerAhorros.setValue("Fecha de retiro", ahorro.getFechaRetiro())
                        
            except ErrorAplicacion as e:
                PopUp(str(e))
        
        
        #Se crea el frame
        frameVerAhorros = Frame(self)
        nombreVerAhorros = Label(frameVerAhorros, text="Saldo en Ahorros", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descVerAhorros = Label(frameVerAhorros, text="Su saldo disponible en su ahorro es de:", font=("Arial Rounded MT Bold", 14))
        FFVerAhorros = FieldFrame(frameVerAhorros, None, ["Nombre del ahorro", "Disponible","Fecha de retiro"], None, None, None)
        FFVerAhorros.crearBotones(botonVerAhorros)

        outputVerAhorros = Text(frameVerAhorros, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputVerAhorros)
        
        nombreVerAhorros.pack()
        descVerAhorros.pack()
        FFVerAhorros.pack()
        VentanaUsuario.framesEnPantalla.append(frameVerAhorros)
        
        
        #Boton para ver el saldo disponible en Metas
        def botonVerMetas():
            try:
                # Obtener las metas del usuario
                metas_usuario = Usuario.getMetas(self._usuario)
                
                # Verificar si hay metas disponibles
                if not metas_usuario:
                    raise ExcepcionNoMeta
                else:
                    for meta in metas_usuario:
                        # Actualizar los valores en el FieldFrame
                        metacum = meta.getCumplida()
                        FFVerMetas.setValue("Nombre de la meta", meta.getNombre())
                        if metacum is False:
                            FFVerMetas.setValue("Cumplido", "No")
                        else:
                            FFVerMetas.setValue("Cumplido", "Si")
                        FFVerMetas.setValue("Disponible", meta.getSaldo())
                        FFVerMetas.setValue("Cantidad objetivo", meta.getObjetivo())
                        
            except ErrorAplicacion as e:
                PopUp(str(e))
        
        frameVerMetas = Frame(self)
        nombreVerMetas = Label(frameVerMetas, text="Saldo en Metas", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descVerMetas = Label(frameVerMetas, text="Su saldo disponible en su meta es de:", font=("Arial Rounded MT Bold", 14))
        FFVerMetas = FieldFrame(frameVerMetas, None, ["Nombre de la meta", "Cumplido", "Disponible", "Cantidad objetivo"], None, None)
        FFVerMetas.crearBotones(botonVerMetas)
        
        outputVerMetas = Text(frameVerMetas, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputVerMetas)
        
        nombreVerMetas.pack()
        descVerMetas.pack()
        FFVerMetas.pack()
        
        VentanaUsuario.framesEnPantalla.append(frameVerMetas)
        
        
        #Boton para ver el saldo disponible en el Dinero Total
        def botonVerDineroTotal():
            
            try:
                dinerototal = usuario.getDineroCuenta()
                FFVerDineroTotal.setValue("Disponible", dinerototal)
                
            except ErrorAplicacion as e:
                PopUp(str(e))
        
        frameVerDineroTotal = Frame(self)
        nombreVerDineroTotal = Label(frameVerDineroTotal, text="Saldo Dinero Total", font=("Arial Rounded MT Bold", 18), fg ="#8EAC50")
        descVerDineroTotal = Label(frameVerDineroTotal, text="Su dinero total es de:", font=("Arial Rounded MT Bold", 14))
        FFVerDineroTotal = FieldFrame(frameVerDineroTotal, None, ["Disponible"], None, None)
        FFVerDineroTotal.crearBotones(botonVerDineroTotal)
        
        outputVerDineroTotal = Text(frameVerDineroTotal, height=10, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputVerDineroTotal)
        
        nombreVerDineroTotal.pack()
        descVerDineroTotal.pack()
        FFVerDineroTotal.pack()
        
        VentanaUsuario.framesEnPantalla.append(frameVerDineroTotal)
        
        #Boton para Ingresar dinero a bolsillos
        def botonIngresarBolsillos():
            try:
                verificarVacio(FFIngresarBolsillos)
                escogerBolsillo = FFIngresarBolsillos.getValue("Escoger Bolsillo")
                cantidad = FFIngresarBolsillos.getValue("Ingresar cantidad")
   
                verificarLongitud(escogerBolsillo, 3, "Escoger Bolsillo")
                verificarNumero(cantidad)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameIngresarBolsillos = Frame(self)
        nombreIngresarBolsillos = Label(frameIngresarBolsillos, text="Ingresar dinero a un bolsillo", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descIngresarBolsillos = Label(frameIngresarBolsillos, text="Seleccionar el bolsillo al que desea ingresar el dinero", font=("Arial Rounded MT Bold", 14))
        FFIngresarBolsillos = FieldFrame(frameIngresarBolsillos, None, ["Escoger Bolsillo",  "Ingresar cantidad"], None, None)
        FFIngresarBolsillos.crearBotones(botonIngresarBolsillos)

        outputIngresarBolsillos = Text(frameIngresarBolsillos, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputIngresarBolsillos)

        nombreIngresarBolsillos.pack()
        descIngresarBolsillos.pack()
        FFIngresarBolsillos.pack()

        VentanaUsuario.framesEnPantalla.append(frameIngresarBolsillos)

        #Boton para Ingresar dinero a sus Ahorros
        def botonIngresarAhorros():

            try:
                verificarVacio(FFIngresarAhorros)
                escogerAhorros = FFIngresarAhorros.getValue("Escoger ahorro")
                cantidad = FFIngresarAhorros.getValue("Ingresar cantidad")

                verificarLongitud(escogerAhorros, 3, "Escoger Bolsillo")
                verificarNumero(cantidad)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameIngresarAhorros = Frame(self)
        nombreIngresarAhorros = Label(frameIngresarAhorros, text="Ingresar dinero a un ahorro", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descIngresarAhorros = Label(frameIngresarAhorros, text="Seleccionar el ahorro al que desea ingresar el dinero", font=("Arial Rounded MT Bold", 14))
        FFIngresarAhorros = FieldFrame(frameIngresarAhorros, None, ["Escoger ahorro", "Ingresar cantidad"], None, None)
        FFIngresarAhorros.crearBotones(botonIngresarAhorros)

        outputIngresarAhorros = Text(frameIngresarAhorros, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputIngresarAhorros)

        nombreIngresarAhorros.pack()
        descIngresarAhorros.pack()
        FFIngresarAhorros.pack()

        VentanaUsuario.framesEnPantalla.append(frameIngresarAhorros)

        #Boton para Mover dinero a Bolsillos
        def botonMoverBolsillos():

            try:
                verificarVacio(FFMoverBolsillos)
                cantidad = FFMoverBolsillos.getValue("Cantidad a transferir")
   
                verificarNumero(cantidad)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameMoverBolsillos = Frame(self)
        nombreMoverBolsillos = Label(frameMoverBolsillos, text="Mover dinero a un Bolsillo", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descMoverBolsillos = Label(frameMoverBolsillos, text="Seleccionar el Bolsillo al que desea ingresar el dinero", font=("Arial Rounded MT Bold", 14))
        FFMoverBolsillos = FieldFrame(frameMoverBolsillos, None, ["Elegir a que bolsillo desea mover su dinero", "De donde sale el dinero", "Escoger uno de los disponibles", "Cantidad a transferir"], None, None)
        FFMoverBolsillos.crearBotones(botonMoverBolsillos)

        outputMoverBolsillos = Text(frameMoverBolsillos, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputMoverBolsillos)

        nombreMoverBolsillos.pack()
        descMoverBolsillos.pack()
        FFMoverBolsillos.pack()

        VentanaUsuario.framesEnPantalla.append(frameMoverBolsillos)

        #Boton para Mover dinero a Ahorros
        def botonMoverAhorros():

            try:
                verificarVacio(FFMoverAhorros)
                cantidad = FFMoverAhorros.getValue("Cantidad a transferir")
   
                verificarNumero(cantidad)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameMoverAhorros = Frame(self)
        nombreMoverAhorros = Label(frameMoverAhorros, text="Mover dinero a un Ahorro", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descMoverAhorros = Label(frameMoverAhorros, text="Seleccionar el Shorro al que desea ingresar el dinero", font=("Arial Rounded MT Bold", 14))
        FFMoverAhorros = FieldFrame(frameMoverAhorros, None, ["Elegir a que ahorro desea mover su dinero", "De donde sale el dinero", "Escoger uno de los disponibles", "Cantidad a transferir"], None, None)
        FFMoverAhorros.crearBotones(botonMoverAhorros)

        outputMoverAhorros = Text(frameMoverAhorros, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputMoverAhorros)

        nombreMoverAhorros.pack()
        descMoverAhorros.pack()
        FFMoverAhorros.pack()

        VentanaUsuario.framesEnPantalla.append(frameMoverAhorros)

        #Boton para Mover dinero a Ahorros
        def botonRetiro():
            try:
                verificarVacio(FFRetiro)
                cantidad = FFRetiro.getValue("Cantidad a transferir")
   
                verificarNumero(cantidad)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameRetiro = Frame(self)
        nombreRetiro = Label(frameRetiro, text="Retirar dinero", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descRetiro = Label(frameRetiro, text="Ingrese los siguientes datos para proceder al retiro de su dinero: ", font=("Arial Rounded MT Bold", 14))
        FFRetiro = FieldFrame(frameRetiro, None, ["De donde sale el dinero", "Escoger uno de los disponibles", "Cantidad a transferir"], None, None)
        FFRetiro.crearBotones(botonRetiro)

        outputRetiro = Text(frameRetiro, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputRetiro)

        nombreRetiro.pack()
        descRetiro.pack()
        FFRetiro.pack()

        VentanaUsuario.framesEnPantalla.append(frameRetiro)

        #Boton Agregar Ahorros
        def botonAgregarAhorro():

            try:
                verificarVacio(FFAgregarAhorro)
                nombreAhorro = FFAgregarAhorro.getValue("Nombre del nuevo ahorro")
                fechaLiberar = FFAgregarAhorro.getValue("Fecha de liberacion del ahorro")
                ahorro = Ahorro(self._usuario, nombreAhorro, fechaLiberar)
                self._usuario.nuevoAhorro(ahorro)

                
                resultadoAgregarAhorro = "Ahorro "+ nombreAhorro +" agregado con exito"
                mostrarOutput(resultadoAgregarAhorro, outputAgregarAhorro)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameAgregarAhorro = Frame(self)
        nombreAgregarAhorro = Label(frameAgregarAhorro, text="Agregar Ahorro", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descAgregarAhorro = Label(frameAgregarAhorro, text="Rellene los siguientes datos para agregar un ahorro a su cuenta: ", font=("Arial Rounded MT Bold", 14))
        FFAgregarAhorro = FieldFrame(frameAgregarAhorro, None, ["Nombre del nuevo ahorro", "Fecha de liberacion del ahorro"], None, None)
        FFAgregarAhorro.crearBotones(botonAgregarAhorro)

        outputAgregarAhorro = Text(frameAgregarAhorro, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputAgregarAhorro)

        nombreAgregarAhorro.pack()
        descAgregarAhorro.pack()
        FFAgregarAhorro.pack()

        VentanaUsuario.framesEnPantalla.append(frameAgregarAhorro)

        #Boton Agregar Meta
        def botonAgregarMeta():

            try:
                verificarVacio(FFAgregarMeta)
                nombreMeta = FFAgregarMeta.getValue("Nombre de la nueva Meta")
                objetivo = FFAgregarMeta.getValue("Valor Objetivo de la meta")

                meta = Meta(self._usuario, nombreMeta, objetivo)
                self._usuario.nuevaMeta(meta)
                resultadoAgregarMeta = "Meta "+ nombreMeta  +" agregado con exito"
                mostrarOutput(resultadoAgregarMeta, outputAgregarMeta)


            except ErrorAplicacion as e:
                PopUp(str(e))

        frameAgregarMeta = Frame(self)
        nombreAgregarMeta = Label(frameAgregarMeta, text="Agregar Meta", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descAgregarMeta = Label(frameAgregarMeta, text="Rellene los siguientes datos para agregar una nueva meta a su cuenta: ", font=("Arial Rounded MT Bold", 14))
        FFAgregarMeta = FieldFrame(frameAgregarMeta, None, ["Nombre de la nueva Meta", "Valor Objetivo de la meta"], None, None)
        FFAgregarMeta.crearBotones(botonAgregarMeta)

        outputAgregarMeta = Text(frameAgregarMeta, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputAgregarMeta)

        nombreAgregarMeta.pack()
        descAgregarMeta.pack()
        FFAgregarMeta.pack()

        VentanaUsuario.framesEnPantalla.append(frameAgregarMeta)

        #Boton para Modificar Bolsillo
        def botonModificarBolsillo():

            try:
                verificarVacio(FFModificarBolsillo)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameModificarBolsillo = Frame(self)
        nombreModificarBolsillo = Label(frameModificarBolsillo, text="Modificar Bolsillo", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descModificarBolsillo = Label(frameModificarBolsillo, text="Rellene los siguientes datos para modificar un bolsillo en su cuenta: ", font=("Arial Rounded MT Bold", 14))
        FFModificarBolsillo = FieldFrame(frameModificarBolsillo, None, ["Seleccionar Bolsillo a modificar","¿Qué desea modificar?", "Nueva edición"], None, None)
        FFModificarBolsillo.crearBotones(botonModificarBolsillo)

        outputModificarBolsillo = Text(frameModificarBolsillo, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputModificarBolsillo)

        nombreModificarBolsillo.pack()
        descModificarBolsillo.pack()
        FFModificarBolsillo.pack()

        VentanaUsuario.framesEnPantalla.append(frameModificarBolsillo)

        #Boton para Modificar Ahorro
        def botonModificarAhorro():

            try:
                verificarVacio(FFModificarAhorro)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameModificarAhorro = Frame(self)
        nombreModificarAhorro = Label(frameModificarAhorro, text="Modificar Ahorro", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descModificarAhorro = Label(frameModificarAhorro, text="Rellene los siguientes datos para modificar un ahorro en su cuenta: ", font=("Arial Rounded MT Bold", 14))
        FFModificarAhorro = FieldFrame(frameModificarAhorro, None, ["Seleccionar ahorro a modificar","¿Qué desea modificar?", "Nueva edición"], None, None) #Condicional para las opciones de eleccion
        FFModificarAhorro.crearBotones(botonModificarAhorro)

        outputModificarAhorro = Text(frameModificarAhorro, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputModificarAhorro)

        nombreModificarAhorro.pack()
        descModificarAhorro.pack()
        FFModificarAhorro.pack()

        VentanaUsuario.framesEnPantalla.append(frameModificarAhorro)

        #Boton para Modificar Meta
        def botonModificarMeta():

            try:
                verificarVacio(FFModificarMeta)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameModificarMeta = Frame(self)
        nombreModificarMeta = Label(frameModificarMeta, text="Modificar Meta", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descModificarMeta = Label(frameModificarMeta, text="Rellene los siguientes datos para modificar un colchon en su cuenta: ", font=("Arial Rounded MT Bold", 14))
        FFModificarMeta = FieldFrame(frameModificarMeta, None, ["Seleccionar Meta a modificar","¿Qué desea modificar?", "Nueva edición"], None, None) 
        FFModificarMeta.crearBotones(botonModificarMeta)

        outputModificarMeta = Text(frameModificarMeta, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputModificarMeta)

        nombreModificarMeta.pack()
        descModificarMeta.pack()
        FFModificarMeta.pack()

        VentanaUsuario.framesEnPantalla.append(frameModificarMeta)


        #Boton solicitar un Prestamo Largo
        def botonSolicitarLargo():

            try:
                verificarVacio(FFSolicitarLargo)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameSolicitarLargo = Frame(self)
        nombreSolicitarLargo = Label(frameSolicitarLargo, text="Solicitar un Prestamo", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descSolicitarLargo = Label(frameSolicitarLargo, text="Rellene los siguientes datos para solicitar un prestamo: ", font=("Arial Rounded MT Bold", 14))
        FFSolicitarLargo = FieldFrame(frameSolicitarLargo, None, ["¿Cuantos hijos tiene?","¿Cuántos Años tiene usted?","Digite su ingreso mensual","Escriba el nombre de una referencia","Escriba el numero telefonico de la referencia","¿Desea dar alguna garantia para reducir la tasa de interes?","Escoja el elemento que dejara como garantia","Escoja el bolsillo al que se le envia el dinero"], None, None) 
        FFSolicitarLargo.crearBotones(botonSolicitarLargo)

        outputSolicitarLargo = Text(frameSolicitarLargo, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputSolicitarLargo)

        nombreSolicitarLargo.pack()
        descSolicitarLargo.pack()
        FFSolicitarLargo.pack()

        VentanaUsuario.framesEnPantalla.append(frameSolicitarLargo)

        #Boton abonar a un prestamo
        def botonAbonarPrestamo():

            try:
                verificarVacio(FFAbonarPrestamo)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameAbonarPrestamo = Frame(self)
        nombreAbonarPrestamo = Label(frameAbonarPrestamo, text="Abonar a un Prestamo", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descAbonarPrestamo = Label(frameAbonarPrestamo, text="Rellene los siguientes datos para abonar a un prestamo: ", font=("Arial Rounded MT Bold", 14))
        FFAbonarPrestamo = FieldFrame(frameAbonarPrestamo, None, ["Seleccione el bolsillo desde el que va a abonar","Ingrese la cantidad que va a abonar"], None, None) 
        FFAbonarPrestamo.crearBotones(botonAbonarPrestamo)

        outputAbonarPrestamo = Text(frameAbonarPrestamo, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputAbonarPrestamo)

        nombreAbonarPrestamo.pack()
        descAbonarPrestamo.pack()
        FFAbonarPrestamo.pack()

        VentanaUsuario.framesEnPantalla.append(frameAbonarPrestamo)

        #Boton abonar a una meta
        def botonAbonarMetas():

            try:
                verificarVacio(FFAbonarMetas)

            except ErrorAplicacion as e:
                PopUp(str(e))

        frameAbonarMetas = Frame(self)
        nombreAbonarMetas = Label(frameAbonarMetas, text="Abonar a una Meta", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descAbonarMetas = Label(frameAbonarMetas, text="Rellene los siguientes datos para abonar a una meta: ", font=("Arial Rounded MT Bold", 14))
        FFAbonarMetas = FieldFrame(frameAbonarMetas, None, ["Seleccione una meta","Seleccione el bolsillo desde el que va a abonar", "Ingrese la cantidad que va a abonar"], None, None) 
        FFAbonarMetas.crearBotones(botonAbonarMetas)

        outputAbonarMetas = Text(frameAbonarMetas, height=100, font=("Arial Rounded MT Bold", 10))
        VentanaUsuario.framesEnPantalla.append(outputAbonarMetas)

        nombreAbonarMetas.pack()
        descAbonarMetas.pack()
        FFAbonarMetas.pack()

        VentanaUsuario.framesEnPantalla.append(frameAbonarMetas)