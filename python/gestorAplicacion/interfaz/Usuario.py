import pickle

from gestorAplicacion.interfaz import Categoria


class Usuario:
    def __init__(self, cedula, nombre, correo):
        self._cedula = cedula
        self._nombre = nombre
        self._correo = correo
        self._bolsillos=list(Categoria)
        self._ahorros = []
        self._ingresos = []
        self._retiros = []
        self._prestamos = []
        self._metas = []

    def getNombre(self):
        return self._nombre

    def getCorreo(self):
        return self._correo

    def getCedula(self):
        return self._cedula

    def getAhorros(self):
        return self._ahorros

    def getIngresos(self):
        return self._ingresos

    def getRetiros(self):
        return self._retiros

    def getPrestamos(self):
        return self._prestamos

    def getMetas(self):
        return self._metas
    
    def getBolsillos(self):
        return self._bolsillos

    def setNombre(self, nombre):
        self._nombre = nombre

    def setCorreo(self, correo):
        self._correo = correo

    def setCedula(self, cedula):
        self._cedula = cedula

    def setAhorros(self, ahorros):
        self._ahorros = ahorros

    def setIngresos(self, ingresos):
        self._ingresos = ingresos

    def setRetiros(self, retiros):
        self._retiros = retiros

    def setPrestamos(self, prestamos):
        self._prestamos = prestamos

    def setMetas(self, metas):
        self._metas = metas

    def nuevoIngreso(self, ingreso):
        if ingreso.getCuentaDestino() is not None:
            ingreso.getCuentaDestino().depositar(ingreso.getMonto())
            self._ingresos.append(ingreso)

    def nuevoRetiro(self, retiro):
        if retiro.getCuentaOrigen() is not None:
            salida = retiro.getCuentaOrigen().retirar(retiro.getMonto())

            if salida:
                self._retiros.append(retiro)

            return salida
        else:
            if retiro.getCategoria().getSaldo() <= retiro.getMonto():
                return True
            else:
                return False

    def nuevoAhorro(self, ahorro):
        self._ahorros.append(ahorro)

    def nuevaMeta(self, meta):
        self._metas.append(meta)

    def getDineroCuenta(self):
        total = 0

        for ahorro in self._ahorros:
            total += ahorro.getSaldo()

        for categoria in Categoria:
            total += categoria.getSaldo()

        for meta in self._metas:
            total += meta.getSaldo()

        return total

    def nuevoPrestamo(self, prestamo, bolsillo):
        self._prestamos.append(prestamo)
        bolsillo.setSaldo(bolsillo.getSaldo() + prestamo.getMontoPrestado())

    def guardar_en_archivo(self, nombre_archivo):
        with open(nombre_archivo, "wb") as archivo:
            pickle.dump(self, archivo)

    @staticmethod
    def cargar_desde_archivo(nombre_archivo):
        with open(nombre_archivo, "rb") as archivo:
            usuario = pickle.load(archivo)
        return usuario
