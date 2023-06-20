from tkinter import *
import pathlib
import os
import tkinter
from gestorAplicacion.interfaz.Ahorro import Ahorro
from ventanas.fieldFrame import FieldFrame
from tkinter import ttk
from gestorAplicacion.interfaz.Categoria import Categoria
from excepciones.errorAplicacion import ErrorAplicacion
from excepciones.excepcionExistente import ExcepcionExistente
from excepciones.excepcionLongitud import ExcepcionLongitud
from excepciones.excepcionNumerica import ExcepcionNumerica
from excepciones.excepcionVacio import ExcepcionVacio
from baseDatos.serializador import Serializador
from ventanas.popUp import PopUp

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
            ventanaDevs.title("Sistemas Gestor de Dinero - Acerca de")

            textoInfo = f"Desarrolladores:\n" \
                        f"• Julián Álvarez\n" \
                        f"• Isabela Hernández\n" \
                        f"• Ana María Guarín\n" \

            devs = Label(ventanaDevs, text = textoInfo, justify = "left", font=("Verdana", 12))
            devs.pack(fill=tkinter.Y, expand=True)

        #serializar el usuario
        def cerrarGuardar():
            serializar = Serializador(self._usuario)
            serializar.serializar()
            self.destroy()
            

        #Pantalla de inicio

        framePantallaInicio = Frame(self)
        nombrePantallaInicio = Label(framePantallaInicio, text="Bienvenide", font=("Verdana", 16), fg="#8EAC50")
        outputPantallaInicio = Text(framePantallaInicio, height=100, font=("Verdana",10))

        nombrePantallaInicio.pack
        outputPantallaInicio.pack(fill=X, expand=True, padx=(10,10))

        VentanaUsuario.framesEnPantalla.append(framePantallaInicio)
        cambiarVista(framePantallaInicio)

        #Boton para ver el saldo disponible en Bolsillos
        def botonVerBolsillos():

            try:
                verificarVacio(FFVerBolsillos)
                nombre = FFVerBolsillos.getValue("Nombre del bolsillo")
                disponible = FFVerBolsillos.getValue("Saldo")
                presupuesto= FFVerBolsillos.getValue("Presupuesto")
                
   
                verificarNumero(disponible)
                verificarNumero(presupuesto)
                verificarLongitud(nombre, 3, "Nombre del bolsillo")
                

            except ErrorAplicacion as e:
                PopUp(str(e))

        #Hacer get para obtener el nombre del usuario como sus bolsillo, casillas que no sean editables, solo para observar
        frameVerBolsillos = Frame(self)
        nombreVerBolsillos = Label(frameVerBolsillos, text="Saldo en Bolsillos", font=("Arial Rounded MT Bold", 18), fg = "#8EAC50")
        descVerBolsillos = Label(frameVerBolsillos, text="Su saldo disponible en su bolsillo es de:", font=("Arial Rounded MT Bold", 14))
        FFVerBolsillos = FieldFrame(frameVerBolsillos, None, ["Nombre del bolsillo", "Saldo","Presupuesto"], None, None, None)
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
                verificarVacio(FFVerAhorros)
                nombre = FFVerAhorros.getValue("Nombre del ahorro")
                disponible = FFVerAhorros.getValue("Disponible")
                fechaRetiro = FFVerAhorros.getValue("Fecha de retiro")
   
                verificarNumero(disponible)
                verificarLongitud(nombre, 3, "Nombre del bolsillo")

            except ErrorAplicacion as e:
                PopUp(str(e))