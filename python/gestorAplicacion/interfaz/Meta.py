from gestorAplicacion.interfaz import Cuenta
from gestorAplicacion.interfaz import Retiro
from gestorAplicacion.interfaz import Abonable
from gestorAplicacion.interfaz import Categoria
from gestorAplicacion.interfaz import Ingreso
from datetime import date

class Meta(Abonable):

    def __init__(self, usuario, nombre, fechaInicio, objetivo):
        
        self._nombre = nombre
        self._cumplida = False
        self._fechaCumplimiento = None
        self._fechaInicio = fechaInicio
        self._objetivo = objetivo
        self._usuario = usuario
        self._saldo = 0

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def isCumplida(self):
        return self._cumplida

    def setCumplida(self, cumplida):
        self._cumplida = cumplida


    def getObjetivo(self):
        return self._objetivo

    def setObjetivo(self, objetivo):
        bol = [False for _ in range(2)]
        if not self._cumplida:
            self._objetivo = objetivo
            bol[1] = self.metaCumplida()
            bol[0] = True
        else:
            bol[0] = False
            bol[1] = False
        return bol

    def metaCumplida(self):
        return self._saldo>= self._objetivo

    def getSaldo(self):
        return self._saldo

    def setSaldo(self, saldo):
        self._saldo = saldo

    def getUsuario(self):
        return self._usuario

    def setUsuario(self, usuario):
        self._usuario = usuario

    def getFechaCumplimiento(self):
        return self._fechaCumplimiento

    def setFechaCumplimiento(self, fechaCumplimiento):
        self._fechaCumplimiento = fechaCumplimiento

    def getFechaInicio(self):
        return self._fechaInicio

    def setFechaInicio(self, fechaInicio):
        self._fechaInicio = fechaInicio

    def abonar(self, monto, origen):
        if not self._cumplida:
            if isinstance(origen, Cuenta):
                retiro = Retiro(monto, date.today(), origen, None,Categoria.Nulo)
                retirado = self._usuario.nuevoRetiro(retiro)
                if not retirado:
                    return None
                self._saldo += monto
                return retiro
            if isinstance(origen, Categoria):
                if origen.getSaldo() >= monto:
                    retiro = Retiro(monto,date.today(),None,None, origen)
                    self._saldo += monto
                    return retiro
                else:
                    return None

        return None

    def terminar(self, cuenta):
        if isinstance(cuenta, Cuenta):
            nuevoSaldo = self._saldo
            self._saldo = 0
            self._cumplida = True
            self._fechaCumplimiento = date.today()
            ingreso = Ingreso(nuevoSaldo, date.today(), None, cuenta,Categoria.Nulo)
            self._usuario.nuevoIngreso(ingreso)
            return ingreso
        
        if isinstance(cuenta, Categoria):
            nuevoSaldo = self._saldo
            self._saldo = 0
            self._cumplida = True
            self._fechaCumplimiento = date.today()
            ingreso = Ingreso(nuevoSaldo, date.today(),None,None, cuenta)
            self._usuario.nuevoIngreso(ingreso)
            return ingreso
